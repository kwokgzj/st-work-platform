// AI 助理工具層：把平台資料查詢封裝成可被 LLM 呼叫的工具（文字協議，跨服務商通用）
import { PAGES } from './data.js';

export const DOM_NAME = {rec:'理解', exp:'表達', nar:'敘事/高階', pra:'語用', oral:'口肌/發音'};

export function profileText(c){
  return `姓名 ${c.name}；性別 ${c.sex||'—'}；出生 ${c.dob||'—'}；機構 ${c.org||'—'}；學校/班級 ${c.school||'—'}；家庭語言 ${c.lang||'—'}；監護人 ${c.guardian||'—'}${c.relation?'（'+c.relation+'）':''} 電話 ${c.phone||'—'}；電郵 ${c.email||'—'}；轉介來源 ${c.referral||'—'}；備註 ${c.notes||'—'}；評估 ${(c.assessments||[]).length} 條；課程 ${(c.sessions||[]).length} 次`;
}

export function assessText(a){
  const st=a.states||{}; const weak={rec:[],exp:[],nar:[],pra:[],oral:[]}; let done=0,part=0,none=0;
  PAGES.forEach(p=>p.groups.forEach(g=>g.items.forEach(it=>{
    const v=st[it.id]||0;
    if(v===2)done++; else if(v===1){part++; if(weak[g.d])weak[g.d].push(it.t);} else if(v===3){none++; if(weak[g.d])weak[g.d].push(it.t);}
  })));
  const L=[`診斷 ${a.dx||'—'}${a.sev?'（'+a.sev+'）':''}；獨立完成 ${done} 項、需提示 ${part} 項、未掌握 ${none} 項`];
  Object.entries(weak).forEach(([d,items])=>{ if(items.length) L.push(`  ${DOM_NAME[d]}需加強：${items.slice(0,8).join('、')}${items.length>8?'等':''}`); });
  if(a.obs) L.push('臨床觀察：'+[a.obs.o1,a.obs.o2,a.obs.o3].filter(Boolean).join('／'));
  return L.join('\n');
}

export const TOOLS_SPEC=`可用工具（需要資料時，以 JSON 回覆呼叫，一次一個）：
{"tool":"list_children"} — 列出所有兒童概覽
{"tool":"get_child_profile","args":{"name":"姓名或id"}} — 某兒童完整檔案（不填 name = 當前兒童）
{"tool":"get_assessments","args":{"name":"..."}} — 某兒童全部評估記錄（各範疇掌握統計與需加強項）
{"tool":"get_sessions","args":{"name":"...","limit":10}} — 某兒童課程記錄
{"tool":"get_current_plan","args":{"name":"..."}} — 目前干預方案工作區（僅當前兒童）
{"tool":"search_games","args":{"keyword":"關鍵字","domain":"rec|exp|nar|pra|oral","age":4}} — 搜尋遊戲庫（條件可選）
查詢類問題請先用工具取得資料再回答；已有足夠資訊時，以 {"answer":"最終回答（繁體中文）"} 回覆。`;

// ctx: {children, curChild, curAssessId, plan, curVer, seeds, api, normalizeAssessments}
export function makeTools(ctx){
  const {children, curChild, plan, seeds, api, normalizeAssessments} = ctx;
  const find=q=>{ if(!q) return curChild.value?[curChild.value]:[]; const s=String(q).trim();
    return children.filter(c=>c.id===s||c.name===s||c.name.includes(s)); };
  async function loadFull(q){
    let base = q ? find(q)[0] : curChild.value;
    if(!base) return null;
    if(curChild.value && curChild.value.id===base.id) return curChild.value;
    const full=await api.getChild(base.id).catch(()=>null);
    if(full) normalizeAssessments(full);
    return full;
  }
  async function run(tool, args){
    args=args||{};
    const q=(args.name||args.id||'').toString().trim();
    switch(tool){
      case 'list_children':{
        const rows=children.map(c=>`${c.name}（${c.sex||'—'}・${c.dob||'—'}・${c.org||'—'}）最近更新 ${(c.updated_at||'').slice(0,10)}`);
        return `共 ${children.length} 名兒童：\n${rows.join('\n')||'（無）'}\n需要某個兒童的詳細資料請用 get_child_profile`;
      }
      case 'get_child_profile':{
        const c=await loadFull(q); if(!c) return '找不到兒童：'+(q||'(未指定)'); return profileText(c);
      }
      case 'get_assessments':{
        const c=await loadFull(q); if(!c) return '找不到兒童：'+q;
        const as=c.assessments||[]; if(!as.length) return `${c.name} 尚無評估記錄`;
        return `${c.name} 共 ${as.length} 條評估：\n`+as.map(a=>`【${a.adate||'未填日期'}${a.savedAt?'（存檔 '+a.savedAt+'）':''}】\n${assessText(a)}`).join('\n');
      }
      case 'get_sessions':{
        const c=await loadFull(q); if(!c) return '找不到兒童：'+q;
        const ss=c.sessions||[]; if(!ss.length) return `${c.name} 尚無課程記錄`;
        const lim=Math.min(Number(args.limit)||10, ss.length);
        return `${c.name} 共 ${ss.length} 次課程，最近 ${lim} 次：\n`+ss.slice(-lim).map(s=>`第${s.no}次(${s.date||'—'}) 目標：${(s.goals||[]).join('；')}｜遊戲：${(s.games||[]).map(g=>g.name).join('、')}｜效果：${s.effect?.level||'待評'}`).join('\n');
      }
      case 'get_current_plan':{
        const c=await loadFull(q); if(!c) return '找不到兒童：'+q;
        if(!plan.value||!curChild.value||c.id!==curChild.value.id||!ctx.curVer())
          return `${c.name} 目前沒有開啟中的方案工作區（工作區僅當前兒童有；歷史課程可用 get_sessions 查詢）`;
        return ctx.curVer().goals.map((g,i)=>`目標${i+1}：${g.text}\n`+(g.games.filter(x=>x.checked).map(x=>`  ▪ ${x.name}（${DOM_NAME[x.domain]||x.domain}）目標：${x.target}｜玩法：${x.desc}`).join('\n')||'  （無遊戲）')).join('\n');
      }
      case 'search_games':{
        const list=seeds.filter(s=>{
          if(args.domain && s.domain!==args.domain) return false;
          if(args.age!=null && args.age!=='' && !(s.amin<=Number(args.age)+1 && s.amax>=Number(args.age))) return false;
          if(args.keyword && !(String(s.name+s.goal+s.desc).includes(args.keyword))) return false;
          return true;
        });
        return `符合 ${list.length} 項：\n`+list.slice(0,15).map(s=>`${s.name}（${DOM_NAME[s.domain]||s.domain}，${s.amin}-${s.amax}歲）目標：${s.goal}｜玩法：${s.desc}`).join('\n');
      }
      default: return '未知工具：'+tool;
    }
  }
  return {spec:TOOLS_SPEC, run};
}
