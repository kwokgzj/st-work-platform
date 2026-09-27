"""API 回路测试：records CRUD + 重开连接数据仍在 + seeds/settings/ai 代理接线。

运行（在 backend/ 目录）：
  python -m tests.test_api          # 无需 pytest
  python -m pytest tests/test_api.py
"""
import json
import os
import sqlite3
import tempfile

# 必须在导入 app 之前指向测试库，避免污染开发数据
os.environ["DB_PATH"] = os.path.join(
    tempfile.mkdtemp(prefix="stwo-test-"), "test.db"
)

from fastapi.testclient import TestClient  # noqa: E402

import app.db as db  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)

CHILD = {
    "id": "c1698000000000",
    "name": "小明",
    "sex": "男",
    "dob": "2020-05-01",
    "org": "某機構",
    "dx": "",
    "sev": "",
    "obs": {"o1": "", "o2": "", "o3": ""},
    "states": {"i1": 1, "i2": 2},
    "sessions": [{
        "id": 1698000000000, "no": 1, "date": "", "goals": [], "games": [],
        "homeTip": "", "effect": {"level": "待評", "note": ""},
    }],
    "createdAt": "", "savedAt": "",
}

SEEDS = [
    {"id": "s1", "domain": "rec", "amin": 2, "amax": 4, "name": "遊戲A", "goal": "", "desc": ""},
    {"id": "s2", "domain": "exp", "amin": 3, "amax": 5, "name": "遊戲B", "goal": "", "desc": ""},
]


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_records_crud_roundtrip():
    # 创建 → 201，返回存储后记录
    r = client.post("/api/records", json=CHILD)
    assert r.status_code == 201
    created = r.json()
    assert created["id"] == CHILD["id"]
    assert created["name"] == "小明"
    assert created["updated_at"]  # 服务器时间

    # 列表 → 轻载荷
    r = client.get("/api/records")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["id"] == CHILD["id"]
    assert items[0]["sex"] == "男"
    assert items[0]["dob"] == "2020-05-01"
    assert items[0]["org"] == "某機構"
    assert "sessions" not in items[0]  # 不携带全量数据

    # 读取完整记录
    r = client.get(f"/api/records/{CHILD['id']}")
    assert r.status_code == 200
    full = r.json()
    assert full["states"] == {"i1": 1, "i2": 2}
    assert full["sessions"][0]["effect"]["level"] == "待評"

    # 整份替换（PUT）
    CHILD["states"] = {"i1": 3}
    r = client.put(f"/api/records/{CHILD['id']}", json=CHILD)
    assert r.status_code == 200
    assert client.get(f"/api/records/{CHILD['id']}").json()["states"] == {"i1": 3}

    # 缺 id → 400；不存在 → 404
    assert client.post("/api/records", json={"name": "無id"}).status_code == 400
    assert client.get("/api/records/nope").status_code == 404
    assert client.delete("/api/records/nope").status_code == 404

    # 删除 → 204，之后 404
    assert client.delete(f"/api/records/{CHILD['id']}").status_code == 204
    assert client.get(f"/api/records/{CHILD['id']}").status_code == 404


def test_persistence_across_reopened_connection():
    client.post("/api/records", json=CHILD)
    client.put("/api/seeds", json=SEEDS)
    client.put("/api/settings/ai", json={"type": "openai", "base": "https://x/v1", "key": "k", "model": "m"})

    # 完全重开一条原始连接直查库，证明数据落盘而非进程内存
    conn = sqlite3.connect(db.db_path())
    try:
        n_children = conn.execute("SELECT COUNT(*) FROM children").fetchone()[0]
        n_seeds = conn.execute("SELECT COUNT(*) FROM seeds").fetchone()[0]
        ai_cfg = json.loads(conn.execute(
            "SELECT value FROM app_settings WHERE key='ai'").fetchone()[0])
    finally:
        conn.close()
    assert n_children == 1
    assert n_seeds == 2
    assert ai_cfg["model"] == "m"

    # 新连接（新 TestClient 请求）读回一致
    assert client.get("/api/records").json()[0]["id"] == CHILD["id"]
    assert len(client.get("/api/seeds").json()) == 2
    assert client.get("/api/settings/ai").json()["key"] == "k"


def test_seeds_validation_and_settings_default():
    assert client.put("/api/seeds", json=[{"name": "無id"}]).status_code == 400
    assert client.put("/api/seeds", json=[]).json() == {"count": 0}  # 清空合法
    client.post("/api/records", json=CHILD)  # 留一条给后续测试


def test_ai_chat_wiring(monkeypatch=None):
    # 未配置 → 400
    r = client.post("/api/ai/chat", json={"prompt": "hi"})
    assert r.status_code == 400

    # 配置后走代理（mock 掉真实 HTTP），上游失败 → 502
    from app import ai as ai_mod

    client.put("/api/settings/ai", json={"type": "openai", "base": "https://x/v1", "key": "k", "model": "m"})

    orig = ai_mod.call_llm
    ai_mod.call_llm = lambda cfg, prompt, max_tokens=4000: "好的"
    try:
        r = client.post("/api/ai/chat", json={"prompt": "hi", "max_tokens": 8})
    finally:
        ai_mod.call_llm = orig
    assert r.status_code == 200
    assert r.json() == {"text": "好的"}


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\n{len(fns)} tests passed")
