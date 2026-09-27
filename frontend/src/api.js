// 後端 API 封裝，替代原 localStorage db（契約見架構設計 §3）
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

export const api = {
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
