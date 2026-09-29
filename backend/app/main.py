"""FastAPI 路由 + StaticFiles 托管前端构建产物（前后端同源，无 CORS）。"""
import datetime
import json
from contextlib import closing
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles

from . import ai, db

app = FastAPI(title="st-work-platform")
db.init_db()


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _save_record(conn, rid: str, data: dict) -> dict:
    """整份替换写入（INSERT OR REPLACE），updated_at 由服务器写入。"""
    ts = _now()
    data["id"] = rid
    conn.execute(
        "INSERT OR REPLACE INTO children(id, name, data, updated_at) VALUES(?,?,?,?)",
        (rid, data.get("name") or "", json.dumps(data, ensure_ascii=False), ts),
    )
    conn.commit()
    return {**data, "updated_at": ts}


# ---------- 健康检查 ----------

@app.get("/api/health")
def health():
    return {"status": "ok"}


# ---------- 记录（儿童档案） ----------

@app.get("/api/records")
def list_records():
    """轻载荷列表（档案下拉只需 name/sex/dob/org）。"""
    with closing(db.get_conn()) as conn:
        rows = conn.execute(
            "SELECT id, name, data, updated_at FROM children ORDER BY updated_at DESC"
        ).fetchall()
    out = []
    for r in rows:
        d = json.loads(r["data"])
        out.append({
            "id": r["id"],
            "name": r["name"],
            "sex": d.get("sex", ""),
            "dob": d.get("dob", ""),
            "org": d.get("org", ""),
            "guardian": d.get("guardian", ""),
            "phone": d.get("phone", ""),
            "updated_at": r["updated_at"],
        })
    return out


@app.post("/api/records", status_code=201)
def create_record(body: dict = Body(...)):
    rid = body.get("id")
    if not rid:
        raise HTTPException(400, "缺少 id（id 由客户端生成，如 'c' + 时间戳）")
    with closing(db.get_conn()) as conn:
        return _save_record(conn, str(rid), body)


@app.get("/api/records/{rid}")
def get_record(rid: str):
    with closing(db.get_conn()) as conn:
        row = conn.execute(
            "SELECT data, updated_at FROM children WHERE id = ?", (rid,)
        ).fetchone()
    if row is None:
        raise HTTPException(404, "记录不存在")
    return {**json.loads(row["data"]), "updated_at": row["updated_at"]}


@app.put("/api/records/{rid}")
def replace_record(rid: str, body: dict = Body(...)):
    """整份替换：保存评估、存课程记录都是整份写。"""
    with closing(db.get_conn()) as conn:
        return _save_record(conn, rid, body)


@app.delete("/api/records/{rid}", status_code=204)
def delete_record(rid: str):
    with closing(db.get_conn()) as conn:
        cur = conn.execute("DELETE FROM children WHERE id = ?", (rid,))
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(404, "记录不存在")
    return Response(status_code=204)


# ---------- 种子库（整组读写，对应客户端 saveSeeds/importSeeds/resetSeeds） ----------

@app.get("/api/seeds")
def get_seeds():
    with closing(db.get_conn()) as conn:
        rows = conn.execute("SELECT data FROM seeds ORDER BY rowid").fetchall()
    return [json.loads(r["data"]) for r in rows]


@app.put("/api/seeds")
def replace_seeds(body: list = Body(...)):
    for i, seed in enumerate(body):
        if not isinstance(seed, dict) or not seed.get("id"):
            raise HTTPException(400, f"第 {i + 1} 条种子缺少 id")
    with closing(db.get_conn()) as conn:
        conn.execute("DELETE FROM seeds")
        conn.executemany(
            "INSERT INTO seeds(id, data) VALUES(?,?)",
            [(s["id"], json.dumps(s, ensure_ascii=False)) for s in body],
        )
        conn.commit()
    return {"count": len(body)}


# ---------- AI 设置与 LLM 代理 ----------

@app.get("/api/settings/ai")
def get_ai_settings():
    with closing(db.get_conn()) as conn:
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = 'ai'"
        ).fetchone()
    return json.loads(row["value"]) if row else {}


@app.put("/api/settings/ai")
def put_ai_settings(body: dict = Body(...)):
    with closing(db.get_conn()) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO app_settings(key, value) VALUES('ai', ?)",
            (json.dumps(body, ensure_ascii=False),),
        )
        conn.commit()
    return {"ok": True}


@app.post("/api/ai/chat")
def ai_chat(body: dict = Body(...)):
    prompt = body.get("prompt")
    if not prompt:
        raise HTTPException(400, "缺少 prompt")
    with closing(db.get_conn()) as conn:
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = 'ai'"
        ).fetchone()
    cfg = json.loads(row["value"]) if row else {}
    if not cfg.get("base") or not cfg.get("key"):
        raise HTTPException(400, "尚未設定 AI，請先在「AI 設定」中填寫並儲存")
    try:
        text = ai.call_llm(cfg, prompt, body.get("max_tokens") or 16384)
    except ValueError as e:
        raise HTTPException(502, str(e))
    if not text or not text.strip():
        raise HTTPException(502, "LLM 回應為空 — 常見於推理模型耗盡輸出上限或協議不匹配，請重試或在 AI 設定更換模型/關閉思考")
    return {"text": text}


# ---------- 静态托管（前端构建产物；须在 API 路由之后挂载） ----------

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
