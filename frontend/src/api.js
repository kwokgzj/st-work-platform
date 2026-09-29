// 後端 API 封裝（契約見架構設計 §3）
// 單檔模式：以 file:// 直接打開構建出的單 HTML 時，自動切換到瀏覽器 localStorage 存儲，
// 無需任何後端即可使用（AI 生成不可用，自動回退「依種子庫生成」）。
async function j(r){
  if(!r.ok){
    let msg='HTTP '+r.status;
    try{ msg=(await r.json()).detail || msg; }catch(e){}
    throw new Error(msg);
  }
  if(r.status===204) return null;
  return r.json();
}
const post = (url, body) => fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)}).then(j);
const put  = (url, body) => fetch(url, {method:'PUT',  headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)}).then(j);

const remoteApi = {
  listChildren : ()      => fetch('/api/records').then(j),
  getChild     : id      => fetch('/api/records/'+encodeURIComponent(id)).then(j),
  addChild     : c       => post('/api/records', c),
  putChild     : (id, c) => put('/api/records/'+encodeURIComponent(id), c),
  delChild     : id      => fetch('/api/records/'+encodeURIComponent(id), {method:'DELETE'}).then(j),
  getSeeds     : ()      => fetch('/api/seeds').then(j),
  putSeeds     : arr     => put('/api/seeds', arr),
  async getAi(){ const r=await fetch('/api/settings/ai'); return r.status===404 ? null : j(r); },
  putAi        : cfg     => put('/api/settings/ai', cfg),
  aiChat       : (prompt, max_tokens) => post('/api/ai/chat', {prompt, max_tokens}),
};

// ── 單檔模式：localStorage 版後端（鍵名沿用舊單檔版，舊數據自動可見）──
const STANDALONE = typeof location !== 'undefined' && location.protocol === 'file:';
const KIDS='plas_children', SEEDS='plas_seeds', AI='plas_ai';
function lsRead(k, fb){ try{ const v=JSON.parse(localStorage.getItem(k)); return v==null?fb:v; }catch(e){ return fb; } }
function lsWrite(k, v){ localStorage.setItem(k, JSON.stringify(v)); }
const clone = v => Promise.resolve(JSON.parse(JSON.stringify(v)));

function localApi(){
  return {
    standalone: true,
    listChildren: () => clone(lsRead(KIDS, []).map(c=>({
      id:c.id, name:c.name, sex:c.sex||'', dob:c.dob||'', org:c.org||'',
      guardian:c.guardian||'', phone:c.phone||'', updated_at:c.updatedAt||c.savedAt||c.createdAt||''
    }))),
    getChild: id => { const c=lsRead(KIDS, []).find(x=>x.id===id);
      return c ? clone(c) : Promise.reject(new Error('記錄不存在')); },
    addChild: c => { const a=lsRead(KIDS, []); c.updatedAt=new Date().toISOString();
      a.unshift(c); lsWrite(KIDS, a); return clone(c); },
    putChild: (id, c) => { const a=lsRead(KIDS, []); const i=a.findIndex(x=>x.id===id);
      if(i<0) return Promise.reject(new Error('記錄不存在'));
      c.updatedAt=new Date().toISOString(); a[i]=JSON.parse(JSON.stringify(c)); lsWrite(KIDS, a); return clone(a[i]); },
    delChild: id => { lsWrite(KIDS, lsRead(KIDS, []).filter(x=>x.id!==id)); return clone(null); },
    getSeeds: () => clone(lsRead(SEEDS, [])),
    putSeeds: arr => { lsWrite(SEEDS, arr); return clone({count:(arr||[]).length}); },
    getAi: () => clone(lsRead(AI, null)),
    putAi: cfg => { lsWrite(AI, cfg); return clone(null); },
    aiChat: (prompt, max_tokens) => {
      const cfg = lsRead(AI, null) || {};
      if(!cfg.base || !cfg.key) return Promise.reject(new Error('尚未設定 AI，請先到「設置」頁填寫並儲存'));
      return directLLM(cfg, prompt, max_tokens).then(t=>({text:t}));
    },
  };
}

// ── 單檔模式：瀏覽器直連 LLM（移植自後端 ai.py 三協議；金鑰存在使用者本機瀏覽器）──
const _normBase = u => { let s=(u||'').trim().replace(/\/+$/,''); if(s && !s.endsWith('/chat/completions')) s+='/chat/completions'; return s; };
const _normAnth = u => { let s=(u||'').trim().replace(/\/+$/,''); if(!s) return s; if(s.endsWith('/messages')) return s; if(s.endsWith('/v1')) return s+'/messages'; return s+'/v1/messages'; };
const _MODEL_EXTRA = ' —— 模型名稱可能錯誤或帳號未開通該模型，請更換模型名稱（如 glm-4-flash、deepseek-chat、gpt-4o-mini）';

async function directLLM(cfg, prompt, maxTokens){
  const key=(cfg.key||'').trim(), base=(cfg.base||'').trim().replace(/\/+$/,'');
  const isAnth = cfg.type==='anthropic' || /anthropic\.com/.test(base);
  const isResp = cfg.type==='responses' || base.endsWith('/responses');
  let url, headers, body;
  if(isResp){
    url = base.endsWith('/responses') ? base : base + '/responses';
    headers = {'Content-Type':'application/json', Authorization:'Bearer '+key};
    body = {model:cfg.model, input:prompt, max_output_tokens:maxTokens||16384};
  }else if(isAnth){
    url = _normAnth(base);
    headers = {'content-type':'application/json','anthropic-version':'2023-06-01','anthropic-dangerous-direct-browser-access':'true'};
    if(key.startsWith('sk-ant-oat')) headers['authorization']='Bearer '+key;   // Claude 訂閱 OAuth token
    else headers['x-api-key']=key;
    body = {model:cfg.model, max_tokens:maxTokens||16384, messages:[{role:'user',content:prompt}]};
  }else{
    url = _normBase(base);
    headers = {'Content-Type':'application/json', Authorization:'Bearer '+key};
    body = {model:cfg.model, messages:[{role:'user',content:prompt}], temperature:0.4, max_tokens:maxTokens||16384};
  }
  if(cfg.thinking==='off'||cfg.thinking==='on'){
    if(isResp) body.reasoning={effort: cfg.thinking==='off'?'low':'high'};
    else if(isAnth) body.thinking = cfg.thinking==='off' ? {type:'disabled'} : {type:'enabled', budget_tokens:Math.min(4096,(maxTokens||16384)-1024)};
    else body.thinking={type: cfg.thinking==='off'?'disabled':'enabled'};
  }
  const ctl = new AbortController();
  const timer = setTimeout(()=>ctl.abort(), 180000);
  let r;
  try{
    r = await fetch(url, {method:'POST', headers, body:JSON.stringify(body), signal:ctl.signal});
  }catch(e){
    clearTimeout(timer);
    if(e.name==='AbortError') throw new Error('請求逾時（超過 3 分鐘未回應），請重試或更換較快的模型');
    throw new Error('無法連上 LLM 服務 — 網路問題、CORS 限制或服務不可用。部分服務商不允許瀏覽器直連，可更換服務商/接入點，或改用伺服器版');
  }
  clearTimeout(timer);
  const txt = await r.text();
  if(!r.ok){
    let extra = '';
    if(r.status===403 || /model_access_denied|invalid model|model.?not.?exist|does not exist/i.test(txt))
      extra = isResp ? ' —— 若你是 Codex/Responses 協議接入，請確認 AI 設定的協議已選「OpenAI Responses」' : _MODEL_EXTRA;
    throw new Error('HTTP '+r.status+'：'+txt.slice(0,180)+extra);
  }
  let data; try{ data=JSON.parse(txt); }catch(e){ throw new Error('回應非 JSON：'+txt.slice(0,120)); }
  let text='';
  if(isResp){
    text=(data.output||[]).map(o=>(o.content||[]).map(c=>c.text||'').join('')).join('') || data.output_text || '';
  }else if(isAnth){
    text=(data.content||[]).map(c=>c.text||'').join('');
  }else{
    text=((data.choices||[{}])[0].message||{}).content || '';
  }
  if(!text){
    const finish=(data.choices&&data.choices[0]&&data.choices[0].finish_reason)||data.stop_reason||'';
    throw new Error('LLM 回應為空'+(finish?'（finish_reason='+finish+'）':'')+' — 常見原因：推理模型耗盡輸出上限（max_tokens）、協議不匹配或內容被過濾；可重試或在 AI 設定換模型。原始回應：'+txt.slice(0,800));
  }
  return text;
}

export const api = STANDALONE ? localApi() : remoteApi;
