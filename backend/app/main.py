"""FastAPI 路由 + StaticFiles 托管前端构建产物（前后端同源，无 CORS）。"""
import datetime
import json
import secrets
from contextlib import closing
from pathlib import Path

from fastapi import Body, Depends, FastAPI, Header, HTTPException, Response
from fastapi.staticfiles import StaticFiles

from . import ai, db

app = FastAPI(title="st-work-platform")
db.init_db()


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _save_record(conn, rid: str, data: dict, owner: str) -> dict:
    """整份替换写入（INSERT OR REPLACE），updated_at 与 owner 由服务器写入。"""
    ts = _now()
    data["id"] = rid
    conn.execute(
        "INSERT OR REPLACE INTO children(id, name, data, updated_at, owner) VALUES(?,?,?,?,?)",
        (rid, data.get("name") or "", json.dumps(data, ensure_ascii=False), ts, owner),
    )
    conn.commit()
    return {**data, "updated_at": ts}


# ---------- 鉴权：用户、登录会话 ----------

SESSION_DAYS = 30

def _public_user(u: dict) -> dict:
    return {k: u[k] for k in ("id", "username", "display_name", "role", "disabled")}


def _new_token(uid: str) -> str:
    token = secrets.token_hex(32)
    exp = (datetime.datetime.now(datetime.timezone.utc)
           + datetime.timedelta(days=SESSION_DAYS)).isoformat(timespec="seconds")
    with closing(db.get_conn()) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO auth_sessions(token, user_id, expires_at) VALUES(?,?,?)",
            (token, uid, exp),
        )
        conn.commit()
    return token


def current_user(authorization: str = Header(default="")) -> dict:
    """Bearer token → 当前用户（过期/停用一律 401）。"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "未登錄")
    with closing(db.get_conn()) as conn:
        row = conn.execute(
            "SELECT u.* FROM auth_sessions s JOIN users u ON u.id = s.user_id"
            " WHERE s.token = ? AND s.expires_at > ?",
            (authorization[7:].strip(), _now()),
        ).fetchone()
    if row is None or row["disabled"]:
        raise HTTPException(401, "登入已過期或帳號停用，請重新登入")
    return dict(row)


def require_admin(user: dict = Depends(current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(403, "僅管理員可管理用戶")
    return user


def _auth_login_row(row) -> dict:
    return {"token": _new_token(row["id"]), "user": _public_user(dict(row))}


@app.get("/api/auth/has_users")
def auth_has_users():
    with closing(db.get_conn()) as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
    return {"hasUsers": n > 0}


@app.post("/api/auth/setup")
def auth_setup(body: dict = Body(...)):
    """首次初始化：僅在系統內沒有任何用戶時可調用，創建第一個管理員並接收存量檔案。"""
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""
    display = (body.get("display_name") or "").strip() or username
    if not username or len(password) < 6:
        raise HTTPException(400, "帳號必填，密碼至少 6 位")
    with closing(db.get_conn()) as conn:
        if conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"] > 0:
            raise HTTPException(403, "系統已初始化，請直接登入")
        # 孤兒檔案（含舊版預設管理員遺留）歸入首個管理員
        conn.execute(
            "UPDATE children SET owner = ? WHERE owner = ''"
            " OR owner NOT IN (SELECT id FROM users)",
            (uid_placeholder := "u" + secrets.token_hex(8),),
        )
        salt = secrets.token_hex(16)
        conn.execute(
            "INSERT INTO users(id, username, display_name, role, pw_salt, pw_hash, disabled, created_at)"
            " VALUES(?,?,?,'admin',?,?,0,?)",
            (uid_placeholder, username, display, salt, db.hash_pw(password, salt), _now()),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM users WHERE id = ?", (uid_placeholder,)).fetchone()
    return _auth_login_row(dict(row))


@app.post("/api/auth/login")
def auth_login(body: dict = Body(...)):
    username = (body.get("username") or "").strip()
    with closing(db.get_conn()) as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if row is None or db.hash_pw(body.get("password") or "", row["pw_salt"]) != row["pw_hash"]:
        raise HTTPException(401, "帳號或密碼錯誤")
    if row["disabled"]:
        raise HTTPException(403, "帳號已停用，請聯繫管理員")
    return _auth_login_row(row)


@app.post("/api/auth/register")
def auth_register(body: dict = Body(...)):
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""
    display = (body.get("display_name") or "").strip() or username
    if not username or not password:
        raise HTTPException(400, "帳號與密碼必填")
    if len(password) < 6:
        raise HTTPException(400, "密碼至少 6 位")
    with closing(db.get_conn()) as conn:
        if conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone():
            raise HTTPException(400, "帳號已存在")
        uid = "u" + secrets.token_hex(8)
        salt = secrets.token_hex(16)
        conn.execute(
            "INSERT INTO users(id, username, display_name, role, pw_salt, pw_hash, disabled, created_at)"
            " VALUES(?,?,?,'therapist',?,?,0,?)",
            (uid, username, display, salt, db.hash_pw(password, salt), _now()),
        )
        conn.commit()
    with closing(db.get_conn()) as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
    return _auth_login_row(dict(row))


@app.get("/api/auth/me")
def auth_me(user: dict = Depends(current_user)):
    return _public_user(user)


# ---------- 用户管理（僅管理員） ----------

@app.get("/api/users")
def list_users(admin: dict = Depends(require_admin)):
    with closing(db.get_conn()) as conn:
        rows = conn.execute(
            "SELECT id, username, display_name, role, disabled, created_at"
            " FROM users ORDER BY created_at"
        ).fetchall()
    return [dict(r) for r in rows]


@app.post("/api/users")
def create_user(body: dict = Body(...), admin: dict = Depends(require_admin)):
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""
    if not username or len(password) < 6:
        raise HTTPException(400, "帳號必填，密碼至少 6 位")
    role = body.get("role") if body.get("role") in ("admin", "therapist") else "therapist"
    with closing(db.get_conn()) as conn:
        if conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone():
            raise HTTPException(400, "帳號已存在")
        uid = "u" + secrets.token_hex(8)
        salt = secrets.token_hex(16)
        conn.execute(
            "INSERT INTO users(id, username, display_name, role, pw_salt, pw_hash, disabled, created_at)"
            " VALUES(?,?,?,?,?,?,0,?)",
            (uid, username, (body.get("display_name") or "").strip() or username,
             role, salt, db.hash_pw(password, salt), _now()),
        )
        conn.commit()
    return {"id": uid}


@app.put("/api/users/{uid}")
def update_user(uid: str, body: dict = Body(...), admin: dict = Depends(require_admin)):
    with closing(db.get_conn()) as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
        if row is None:
            raise HTTPException(404, "用戶不存在")
        if uid == admin["id"] and body.get("disabled"):
            raise HTTPException(400, "不能停用自己的帳號")
        if body.get("password") is not None:
            if len(body["password"]) < 6:
                raise HTTPException(400, "密碼至少 6 位")
            salt = secrets.token_hex(16)
            conn.execute("UPDATE users SET pw_salt = ?, pw_hash = ? WHERE id = ?",
                         (salt, db.hash_pw(body["password"], salt), uid))
        if body.get("display_name") is not None:
            conn.execute("UPDATE users SET display_name = ? WHERE id = ?",
                         ((body["display_name"] or "").strip() or row["display_name"], uid))
        if body.get("disabled") is not None:
            conn.execute("UPDATE users SET disabled = ? WHERE id = ?", (1 if body["disabled"] else 0, uid))
        if body.get("role") in ("admin", "therapist") and not (uid == admin["id"] and body["role"] != "admin"):
            conn.execute("UPDATE users SET role = ? WHERE id = ?", (body["role"], uid))
        conn.commit()
    return {"ok": True}


@app.delete("/api/users/{uid}")
def delete_user(uid: str, admin: dict = Depends(require_admin)):
    if uid == admin["id"]:
        raise HTTPException(400, "不能刪除自己的帳號")
    with closing(db.get_conn()) as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (uid,))
        conn.execute("DELETE FROM children WHERE owner = ?", (uid,))   # 連同其檔案一併清除
        conn.execute("DELETE FROM auth_sessions WHERE user_id = ?", (uid,))
        conn.commit()
    return {"ok": True}


# ---------- 健康检查 ----------

@app.get("/api/health")
def health():
    return {"status": "ok"}


# ---------- 记录（儿童档案） ----------

@app.get("/api/records")
def list_records(user: dict = Depends(current_user)):
    """轻载荷列表（档案下拉只需 name/sex/dob/org）。僅返回當前用戶的檔案。"""
    with closing(db.get_conn()) as conn:
        rows = conn.execute(
            "SELECT id, name, data, updated_at FROM children WHERE owner = ? ORDER BY updated_at DESC",
            (user["id"],),
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
def create_record(body: dict = Body(...), user: dict = Depends(current_user)):
    rid = body.get("id")
    if not rid:
        raise HTTPException(400, "缺少 id（id 由客户端生成，如 'c' + 时间戳）")
    with closing(db.get_conn()) as conn:
        return _save_record(conn, str(rid), body, owner=user["id"])


@app.get("/api/records/{rid}")
def get_record(rid: str, user: dict = Depends(current_user)):
    with closing(db.get_conn()) as conn:
        row = conn.execute(
            "SELECT data, updated_at FROM children WHERE id = ? AND owner = ?",
            (rid, user["id"]),
        ).fetchone()
    if row is None:
        raise HTTPException(404, "记录不存在")
    return {**json.loads(row["data"]), "updated_at": row["updated_at"]}


@app.put("/api/records/{rid}")
def replace_record(rid: str, body: dict = Body(...), user: dict = Depends(current_user)):
    """整份替换：保存评估、存课程记录都是整份写（僅限本人檔案）。"""
    with closing(db.get_conn()) as conn:
        row = conn.execute(
            "SELECT 1 FROM children WHERE id = ? AND owner = ?", (rid, user["id"])
        ).fetchone()
        if row is None:
            raise HTTPException(404, "记录不存在")
        return _save_record(conn, rid, body, owner=user["id"])


@app.delete("/api/records/{rid}", status_code=204)
def delete_record(rid: str, user: dict = Depends(current_user)):
    with closing(db.get_conn()) as conn:
        cur = conn.execute("DELETE FROM children WHERE id = ? AND owner = ?", (rid, user["id"]))
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(404, "记录不存在")
    return Response(status_code=204)


# ---------- 全量导出 / 導入（僅管理員，跨設備遷移） ----------

@app.get("/api/data/export")
def export_data(admin: dict = Depends(require_admin)):
    with closing(db.get_conn()) as conn:
        users = [dict(r) for r in conn.execute(
            "SELECT id, username, display_name, role, pw_salt, pw_hash, disabled, created_at FROM users").fetchall()]
        children = [dict(r) for r in conn.execute(
            "SELECT id, name, data, updated_at, owner FROM children").fetchall()]
        seeds = [json.loads(r["data"]) for r in conn.execute("SELECT data FROM seeds ORDER BY rowid").fetchall()]
        ai_settings = [dict(r) for r in conn.execute("SELECT key, value FROM app_settings").fetchall()]
        ver = conn.execute("PRAGMA user_version").fetchone()[0]
    return {
        "app": "st-work-platform", "mode": "server", "schema_version": ver,
        "exported_at": _now(), "users": users, "children": children,
        "seeds": seeds, "ai_settings": ai_settings,
    }


@app.post("/api/data/import")
def import_data(body: dict = Body(...), admin: dict = Depends(require_admin)):
    # 全量覆蓋導入：用戶（含密碼材料）/兒童檔案/種子庫/AI 設定；導入後需重新登入。
    if body.get("app") != "st-work-platform":
        raise HTTPException(400, "不是本平台的備份檔案")
    if body.get("mode") != "server":
        raise HTTPException(400, "此備份來自單檔版，請在單檔版中導入")
    users = body.get("users") or []
    children = body.get("children") or []
    seeds = body.get("seeds") or []
    ai_settings = body.get("ai_settings") or []
    if not isinstance(users, list) or not isinstance(children, list) or not users:
        raise HTTPException(400, "備份格式不正確（缺少用戶或兒童數據）")
    with closing(db.get_conn()) as conn:
        conn.execute("DELETE FROM auth_sessions")
        conn.execute("DELETE FROM children")
        conn.execute("DELETE FROM seeds")
        conn.execute("DELETE FROM app_settings")
        conn.execute("DELETE FROM users")
        conn.executemany(
            "INSERT INTO users(id, username, display_name, role, pw_salt, pw_hash, disabled, created_at)"
            " VALUES(:id, :username, :display_name, :role, :pw_salt, :pw_hash, :disabled, :created_at)", users)
        conn.executemany(
            "INSERT INTO children(id, name, data, updated_at, owner) VALUES(:id, :name, :data, :updated_at, :owner)",
            children)
        conn.executemany(
            "INSERT INTO seeds(id, data) VALUES(:id, :data)",
            [{"id": s["id"], "data": json.dumps(s, ensure_ascii=False)} for s in seeds])
        conn.executemany(
            "INSERT INTO app_settings(key, value) VALUES(:key, :value)", ai_settings)
        conn.commit()
    return {"ok": True, "users": len(users), "children": len(children), "seeds": len(seeds)}


# ---------- 种子库（整组读写，对应客户端 saveSeeds/importSeeds/resetSeeds） ----------

@app.get("/api/seeds")
def get_seeds(user: dict = Depends(current_user)):
    with closing(db.get_conn()) as conn:
        rows = conn.execute("SELECT data FROM seeds ORDER BY rowid").fetchall()
    return [json.loads(r["data"]) for r in rows]


@app.put("/api/seeds")
def replace_seeds(body: list = Body(...), user: dict = Depends(current_user)):
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
def get_ai_settings(user: dict = Depends(current_user)):
    with closing(db.get_conn()) as conn:
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = ?", (f"ai:{user['id']}",)
        ).fetchone()
    return json.loads(row["value"]) if row else {}


@app.put("/api/settings/ai")
def put_ai_settings(body: dict = Body(...), user: dict = Depends(current_user)):
    with closing(db.get_conn()) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO app_settings(key, value) VALUES(?, ?)",
            (f"ai:{user['id']}", json.dumps(body, ensure_ascii=False)),
        )
        conn.commit()
    return {"ok": True}


@app.post("/api/ai/chat")
def ai_chat(body: dict = Body(...), user: dict = Depends(current_user)):
    prompt = body.get("prompt")
    if not prompt:
        raise HTTPException(400, "缺少 prompt")
    with closing(db.get_conn()) as conn:
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = ?", (f"ai:{user['id']}",)
        ).fetchone()
    cfg = json.loads(row["value"]) if row else {}
    if not cfg.get("base") or not cfg.get("key"):
        raise HTTPException(400, "尚未設定 AI，請先在「AI 設定」中填寫並儲存")
    try:
        res = ai.call_llm(cfg, prompt, body.get("max_tokens") or 16384)
    except ValueError as e:
        raise HTTPException(502, str(e))
    if not res["text"] or not res["text"].strip():
        raise HTTPException(502, "LLM 回應為空 — 常見於推理模型耗盡輸出上限或協議不匹配，請重試或在 AI 設定更換模型/關閉思考")
    return {"text": res["text"], "reasoning": res.get("reasoning") or ""}


# ---------- 静态托管（前端构建产物；须在 API 路由之后挂载） ----------

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
