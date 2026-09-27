"""SQLite 连接与迁移：WAL、busy_timeout、建表、user_version 迁移。

数据落位对应原 localStorage 三份数据：
- plas_children → children（儿童档案，整份 JSON）
- plas_seeds    → seeds（干预种子库，整组读写）
- plas_ai       → app_settings（key='ai'）
"""
import os
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


def init_db() -> None:
    """建表 + user_version 迁移。应用导入时调用一次。"""
    with closing(get_conn()) as conn:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        if version < 1:
            conn.executescript(SCHEMA_V1)
            conn.execute("PRAGMA user_version = 1")
            conn.commit()
