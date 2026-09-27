"""LLM 三协议代理，移植自原单文件 HTML 的 callLLM()（openai 兼容 / responses / anthropic）。

文案沿用前端现状（繁体），失败抛 ValueError，由路由转 502 返回浏览器。
"""
import re

import httpx

TIMEOUT = httpx.Timeout(180.0)  # 单次请求上限 3 分钟，与前端现状一致
_MODEL_HINT = re.compile(
    r"model_access_denied|invalid model|model.?not.?exist|does not exist", re.I
)


def _norm_base(u: str) -> str:
    s = (u or "").strip().rstrip("/")
    if s and not s.endswith("/chat/completions"):
        s += "/chat/completions"
    return s


def _norm_anthropic(u: str) -> str:
    s = (u or "").strip().rstrip("/")
    if not s:
        return s
    if s.endswith("/messages"):
        return s
    if s.endswith("/v1"):
        return s + "/messages"
    return s + "/v1/messages"


def _is_anthropic(cfg: dict) -> bool:
    return cfg.get("type") == "anthropic" or "anthropic.com" in (cfg.get("base") or "")


def _is_responses(cfg: dict) -> bool:
    base = (cfg.get("base") or "").strip().rstrip("/")
    return cfg.get("type") == "responses" or base.endswith("/responses")


def _http_err(status: int, body: str, extra: str = "") -> ValueError:
    msg = f"HTTP {status}：{body[:180]}"
    if extra:
        msg += extra
    return ValueError(msg)


_MODEL_EXTRA = (
    " —— 模型名稱可能錯誤或帳號未開通該模型，"
    "請更換模型名稱（如 glm-4-flash、deepseek-chat、gpt-4o-mini）"
)


def call_llm(cfg: dict, prompt: str, max_tokens: int = 4000) -> str:
    """调用 LLM 返回文本；网络/上游失败抛 ValueError。"""
    key = (cfg.get("key") or "").strip()
    base = (cfg.get("base") or "").strip().rstrip("/")
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            if _is_responses(cfg):
                url = base if base.endswith("/responses") else base + "/responses"
                r = client.post(
                    url,
                    headers={"Authorization": "Bearer " + key},
                    json={
                        "model": cfg.get("model"),
                        "input": prompt,
                        "max_output_tokens": max_tokens or 4000,
                    },
                )
                if r.status_code >= 400:
                    extra = (
                        " —— 若你是 Codex/Responses 協議接入，"
                        "請確認 AI 設定的協議已選「OpenAI Responses」"
                        if r.status_code == 403
                        else ""
                    )
                    raise _http_err(r.status_code, r.text, extra)
                data = r.json()
                txt = "".join(
                    "".join(c.get("text") or "" for c in (o.get("content") or []))
                    for o in (data.get("output") or [])
                )
                return txt or data.get("output_text") or ""

            if _is_anthropic(cfg):
                url = _norm_anthropic(base)
                headers = {
                    "content-type": "application/json",
                    "anthropic-version": "2023-06-01",
                    # 原浏览器直连的 CORS 规避头，服务端无实际作用，保留以与前端现状一致
                    "anthropic-dangerous-direct-browser-access": "true",
                }
                if key.startswith("sk-ant-oat"):
                    headers["authorization"] = "Bearer " + key  # Claude 訂閱 OAuth token
                else:
                    headers["x-api-key"] = key  # 一般 API key
                r = client.post(
                    url,
                    headers=headers,
                    json={
                        "model": cfg.get("model"),
                        "max_tokens": max_tokens or 4000,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                if r.status_code >= 400:
                    extra = (
                        _MODEL_EXTRA
                        if r.status_code == 403 or _MODEL_HINT.search(r.text)
                        else ""
                    )
                    raise _http_err(r.status_code, r.text, extra)
                data = r.json()
                return "".join(c.get("text") or "" for c in (data.get("content") or []))

            url = _norm_base(base)
            r = client.post(
                url,
                headers={"Authorization": "Bearer " + key},
                json={
                    "model": cfg.get("model"),
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.4,
                },
            )
            if r.status_code >= 400:
                extra = (
                    _MODEL_EXTRA
                    if r.status_code == 403 or _MODEL_HINT.search(r.text)
                    else ""
                )
                raise _http_err(r.status_code, r.text, extra)
            data = r.json()
            choices = data.get("choices") or [{}]
            return (choices[0].get("message") or {}).get("content") or ""
    except httpx.TimeoutException:
        raise ValueError("請求逾時（超過 3 分鐘未回應），請重試或更換較快的模型")
    except httpx.TransportError as e:
        # ponytail: 服务端无 CORS 概念，报错文案较前端精简；前端如需区分再补
        raise ValueError(f"無法連上 LLM 服務 — 網路問題或服務不可用（{type(e).__name__}）")
