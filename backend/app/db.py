"""SQLite 连接与迁移：WAL、busy_timeout、建表、user_version 迁移。

数据落位对应原 localStorage 三份数据：
- plas_children → children（儿童档案，整份 JSON，按用户隔离）
- plas_seeds    → seeds（干预种子库，整组读写，平台共享）
- plas_ai       → app_settings（key='ai:<user_id>'，按用户隔离）
"""
import hashlib
import os
import secrets
import sqlite3
from contextlib import closing
from pathlib import Path

# 位置：环境变量 DB_PATH 优先；默认 <仓库根>/data/app.db（compose 卷挂载点）
_DB_PATH = os.environ.get(
    "DB_PATH",
    str(Path(__file__).resolve().parent.parent.parent / "data" / "app.db"),
)

SCHEMA_V1 = """
CREATE TABLE IF NOT EXISTS children (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL DEFAULT '',
  data        TEXT NOT NULL,
  updated_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_children_updated ON children(updated_at DESC);

CREATE TABLE IF NOT EXISTS seeds (
  id   TEXT PRIMARY KEY,
  data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS app_settings (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
"""


def get_conn() -> sqlite3.Connection:
    """每次调用打开新连接：线程安全（FastAPI 同步端点跑在线程池），WAL 下开销可忽略。"""
    Path(_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # 写入即落盘，容器被 kill 不丢
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def db_path() -> str:
    return _DB_PATH


def hash_pw(password: str, salt_hex: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt_hex), 100_000).hex()


def init_db() -> None:
    """建表 + user_version 迁移。应用导入时调用一次。"""
    with closing(get_conn()) as conn:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        if version < 1:
            conn.executescript(SCHEMA_V1)
            conn.execute("PRAGMA user_version = 1")
            conn.commit()
        if version < 2:
            # ── 用户体系：users + 登录会话 + 档案权属 ──
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                  id          TEXT PRIMARY KEY,
                  username    TEXT NOT NULL UNIQUE,
                  display_name TEXT NOT NULL DEFAULT '',
                  role        TEXT NOT NULL DEFAULT 'therapist',
                  pw_salt     TEXT NOT NULL,
                  pw_hash     TEXT NOT NULL,
                  disabled    INTEGER NOT NULL DEFAULT 0,
                  created_at  TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS auth_sessions (
                  token      TEXT PRIMARY KEY,
                  user_id    TEXT NOT NULL,
                  expires_at TEXT NOT NULL
                );
            """)
            conn.execute("ALTER TABLE children ADD COLUMN owner TEXT NOT NULL DEFAULT ''")
            conn.execute("PRAGMA user_version = 2")
            conn.commit()
        if version < 3:
            # 移除舊版自動預設的管理員種子帳號（若從未被使用），改由首次開機自行創建
            n = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
            if n == 1 and conn.execute("SELECT 1 FROM users WHERE id = 'u_admin'").fetchone():
                conn.execute("DELETE FROM auth_sessions WHERE user_id = 'u_admin'")
                conn.execute("DELETE FROM users WHERE id = 'u_admin'")
            conn.execute("PRAGMA user_version = 3")
            conn.commit()
