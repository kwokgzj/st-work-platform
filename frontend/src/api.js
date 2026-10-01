// 後端 API 封裝（契約見架構設計 §3）+ 用戶鑑權
// 單檔模式：以 file:// 直接打開構建出的單 HTML 時，自動切換到瀏覽器 localStorage 存儲，
// 無需任何後端即可使用（AI 走瀏覽器直連；用戶數據按登入用戶隔離）。
const TOKEN_KEY = 'plas_token';

async function j(r){
  if(!r.ok){
    if(r.status===401){ localStorage.removeItem(TOKEN_KEY); }
    let msg='HTTP '+r.status;
    try{ msg=(await r.json()).detail || msg; }catch(e){}
    throw new Error(msg);
  }
  if(r.status===204) return null;
  return r.json();
}
const authHeaders = () => { const t=localStorage.getItem(TOKEN_KEY); return t?{Authorization:'Bearer '+t}:{}; };
const post = (url, body) => fetch(url, {method:'POST', headers:{'Content-Type':'application/json', ...authHeaders()}, body:JSON.stringify(body)}).then(j);
const put  = (url, body) => fetch(url, {method:'PUT',  headers:{'Content-Type':'application/json', ...authHeaders()}, body:JSON.stringify(body)}).then(j);
const get  = (url) => fetch(url, {headers:authHeaders()}).then(j);
const del  = (url) => fetch(url, {method:'DELETE', headers:authHeaders()}).then(j);

const remoteApi = {
  standalone: false,
  // 鑑權
  login   : body => post('/api/auth/login', body),
  register: body => post('/api/auth/register', body),
  me      : () => get('/api/auth/me'),
  logout  : () => { localStorage.removeItem(TOKEN_KEY); return Promise.resolve(); },
  listUsers: () => get('/api/users'),
  createUser: body => post('/api/users', body),
  updateUser: (uid, body) => put('/api/users/'+encodeURIComponent(uid), body),
  delUser : uid => del('/api/users/'+encodeURIComponent(uid)),
  // 業務
  listChildren : ()      => get('/api/records'),
  getChild     : id      => get('/api/records/'+encodeURIComponent(id)),
  addChild     : c       => post('/api/records', c),
  putChild     : (id, c) => put('/api/records/'+encodeURIComponent(id), c),
  delChild     : id      => del('/api/records/'+encodeURIComponent(id)),
  getSeeds     : ()      => get('/api/seeds'),
  putSeeds     : arr     => put('/api/seeds', arr),
  async getAi(){ const r=await fetch('/api/settings/ai', {headers:authHeaders()}); return r.status===404 ? null : j(r); },
  putAi        : cfg     => put('/api/settings/ai', cfg),
  aiChat       : (prompt, max_tokens) => post('/api/ai/chat', {prompt, max_tokens}),
};

// ── 單檔模式：localStorage 版後端（用戶分鍵隔離；鍵名沿用舊單檔版，舊數據自動歸入 admin）──
const STANDALONE = typeof location !== 'undefined' && location.protocol === 'file:';
const U='plas_users', SESS='plas_session', SEEDS='plas_seeds';
const kidsKey = uid => 'plas_children__'+uid;
const aiKey   = uid => 'plas_ai__'+uid;
function lsRead(k, fb){ try{ const v=JSON.parse(localStorage.getItem(k)); return v==null?fb:v; }catch(e){ return fb; } }
function lsWrite(k, v){ localStorage.setItem(k, JSON.stringify(v)); }
const clone = v => Promise.resolve(JSON.parse(JSON.stringify(v)));
async function sha(t){ const b=await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t));
  return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join(''); }
async function ensureUsers(){
  let u=lsRead(U, []);
  if(!u.length){   // 首次：內建管理員 admin / 123456
    const salt=Math.random().toString(16).slice(2);
    u=[{id:'u_admin', username:'admin', display_name:'管理員', role:'admin', salt, pw:await sha(salt+'123456'), disabled:0}];
    lsWrite(U, u);
  }
  return u;
}
function localUsersAll(){ return lsRead(U, []); }
const pub = u => ({id:u.id, username:u.username, display_name:u.display_name, role:u.role, disabled:u.disabled||0});
function curUid(){ const sess=lsRead(SESS, null); if(!sess||!sess.userId) throw new Error('未登入'); return sess.userId; }

function localApi(){
  return {
    standalone: true,
    // 鑑權
    async login(body){
      const users=await ensureUsers();
      const u=users.find(x=>x.username===(body.username||'').trim());
      if(!u || u.pw!==await sha(u.salt+(body.password||''))) throw new Error('帳號或密碼錯誤');
      if(u.disabled) throw new Error('帳號已停用，請聯繫管理員');
      lsWrite(SESS, {userId:u.id});
      if(u.id==='u_admin' && localStorage.getItem('plas_children') && !localStorage.getItem(kidsKey(u.id))){
        localStorage.setItem(kidsKey(u.id), localStorage.getItem('plas_children'));   // 舊數據歸入 admin
      }
      return clone({token:'local', user:pub(u)});
    },
    async register(body){
      const users=await ensureUsers();
      const username=(body.username||'').trim();
      if(!username || (body.password||'').length<6) throw new Error('帳號必填，密碼至少 6 位');
      if(users.some(x=>x.username===username)) throw new Error('帳號已存在');
      const salt=Math.random().toString(16).slice(2);
      const u={id:'u'+Date.now().toString(16), username, display_name:(body.display_name||'').trim()||username,
               role:'therapist', salt, pw:await sha(salt+body.password), disabled:0};
      users.push(u); lsWrite(U, users); lsWrite(SESS, {userId:u.id});
      return clone({token:'local', user:pub(u)});
    },
    async me(){
      const uid=curUid();
      const u=(await ensureUsers()).find(x=>x.id===uid);
      return u && !u.disabled ? pub(u) : Promise.reject(new Error('未登入'));
    },
    logout: () => { localStorage.removeItem(SESS); return Promise.resolve(); },
    async listUsers(){ const me=lsRead(SESS,{}).userId; const meU=(await ensureUsers()).find(x=>x.id===me);
      if(!meU || meU.role!=='admin') throw new Error('僅管理員可管理用戶');
      return (await ensureUsers()).map(pub); },
    async createUser(body){
      const users=await ensureUsers(); const username=(body.username||'').trim();
      if(!username || (body.password||'').length<6) throw new Error('帳號必填，密碼至少 6 位');
      if(users.some(x=>x.username===username)) throw new Error('帳號已存在');
      const salt=Math.random().toString(16).slice(2);
      users.push({id:'u'+Date.now().toString(16), username, display_name:(body.display_name||'').trim()||username,
                  role:body.role==='admin'?'admin':'therapist', salt, pw:await sha(salt+body.password), disabled:0});
      lsWrite(U, users); return {ok:true};
    },
    async updateUser(uid, body){
      const users=await ensureUsers(); const u=users.find(x=>x.id===uid);
      if(!u) throw new Error('用戶不存在');
      if(uid===curUid() && body.disabled) throw new Error('不能停用自己的帳號');
      if(body.password!=null) u.pw=await sha(u.salt+body.password);
      if(body.display_name!=null) u.display_name=(body.display_name||'').trim()||u.display_name;
      if(body.disabled!=null) u.disabled=body.disabled?1:0;
      if(body.role==='admin'||body.role==='therapist') u.role=body.role;
      lsWrite(U, users); return {ok:true};
    },
    async delUser(uid){
      if(uid===curUid()) throw new Error('不能刪除自己的帳號');
      lsWrite(U, (await ensureUsers()).filter(x=>x.id!==uid));
      localStorage.removeItem(kidsKey(uid)); localStorage.removeItem(aiKey(uid));
      return {ok:true};
    },
    // 業務（當前用戶作用域）
    listChildren: () => clone(lsRead(kidsKey(curUid()), []).map(c=>({
      id:c.id, name:c.name, sex:c.sex||'', dob:c.dob||'', org:c.org||'',
      guardian:c.guardian||'', phone:c.phone||'', updated_at:c.updatedAt||c.savedAt||c.createdAt||''
    }))),
    getChild: id => { const c=lsRead(kidsKey(curUid()), []).find(x=>x.id===id);
      return c ? clone(c) : Promise.reject(new Error('記錄不存在')); },
    addChild: c => { const k=kidsKey(curUid()); const a=lsRead(k, []);
      c.updatedAt=new Date().toISOString(); a.unshift(c); lsWrite(k, a); return clone(c); },
    putChild: (id, c) => { const k=kidsKey(curUid()); const a=lsRead(k, []); const i=a.findIndex(x=>x.id===id);
      if(i<0) return Promise.reject(new Error('記錄不存在'));
      c.updatedAt=new Date().toISOString(); a[i]=JSON.parse(JSON.stringify(c)); lsWrite(k, a); return clone(a[i]); },
    delChild: id => { const k=kidsKey(curUid());
      lsWrite(k, lsRead(k, []).filter(x=>x.id!==id)); return clone(null); },
    getSeeds: () => clone(lsRead(SEEDS, [])),
    putSeeds: arr => { lsWrite(SEEDS, arr); return clone({count:(arr||[]).length}); },
    getAi: () => clone(lsRead(aiKey(curUid()), null)),
    putAi: cfg => { lsWrite(aiKey(curUid()), cfg); return clone(null); },
    aiChat: (prompt, max_tokens) => {
      const cfg=lsRead(aiKey(curUid()), null) || {};
      if(!cfg.base || !cfg.key) return Promise.reject(new Error('尚未設定 AI，請先到「設置」頁填寫並儲存'));
      return directLLM(cfg, prompt, max_tokens).then(r=>({text:r.text, reasoning:r.reasoning||''}));
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
  let text='', reasoning='';
  if(isResp){
    text=(data.output||[]).map(o=>(o.content||[]).map(c=>c.text||'').join('')).join('') || data.output_text || '';
  }else if(isAnth){
    text=(data.content||[]).map(c=>c.text||'').join('');
    reasoning=(data.content||[]).filter(c=>c.type==='thinking').map(c=>c.thinking||'').join('\n');
  }else{
    const msg=(data.choices||[{}])[0].message||{};
    text=msg.content || '';
    reasoning=msg.reasoning_content || msg.reasoning || '';
  }
  if(!text){
    const finish=(data.choices&&data.choices[0]&&data.choices[0].finish_reason)||data.stop_reason||'';
    const rsn=(data.choices||[{}])[0].message||{};
    const rsnTxt=rsn.reasoning_content || rsn.reasoning || '';
    if(finish==='length' && rsnTxt)
      throw new Error('模型把輸出全部用於思考（finish_reason=length，思考了 '+(data.usage&&data.usage.completion_tokens||'?')+' tokens 仍未寫正文）— 請在「AI 設定」將思考檔位設為「關閉思考」，或提高輸出上限。思考開頭：'+rsnTxt.slice(0,300));
    throw new Error('LLM 回應為空'+(finish?'（finish_reason='+finish+'）':'')+' — 常見原因：推理模型耗盡輸出上限、協議不匹配或內容被過濾；可重試或在 AI 設定換模型/關閉思考。原始回應：'+txt.slice(0,800));
  }
  return {text, reasoning};
}

export const api = STANDALONE ? localApi() : remoteApi;
