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
    aiChat: () => Promise.reject(new Error('單檔模式無 AI 服務，請使用「依種子庫生成」')),
  };
}

export const api = STANDALONE ? localApi() : remoteApi;
