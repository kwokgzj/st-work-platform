<template>
  <el-container class="app-shell">

    <!-- ═══════ 左側菜單欄 ═══════ -->
    <aside class="sidebar no-print">
      <div class="brand">
        <div class="logo">ST</div>
        <div><b>言語治療工作平台</b><span>學前兒童口語評估量表（0–6 歲）</span></div>
      </div>
      <nav class="nav">
        <div class="grp-label">工作台</div>
        <a :class="{active:curPage==='children'}" @click="curPage='children'">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          兒童檔案
        </a>
        <a :class="{active:curPage==='assess'}" @click="curPage='assess'">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="m9 14 2 2 4-4"/></svg>
          評估
        </a>
        <a :class="{active:curPage==='interv'}" @click="curPage='interv'">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
          干預
        </a>
        <div class="grp-label">系統</div>
        <a :class="{active:curPage==='settings'}" @click="curPage='settings'">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
          設置
        </a>
      </nav>
      <div class="me" v-if="curChild">
        <div class="avatar">{{ (curChild.name||'·').slice(0,1) }}</div>
        <div><b>{{ curChild.name }}</b><span>目前兒童・{{ ageLabel }}</span></div>
      </div>
      <div class="me" v-else>
        <div class="avatar">—</div>
        <div><b>未選擇兒童</b><span>請先於「兒童檔案」選擇</span></div>
      </div>
    </aside>

    <el-container class="main-col">
      <!-- ═══════ 頂欄 ═══════ -->
      <el-header class="topbar no-print" height="auto">
        <span class="crumb">首頁 / <b>{{ pageTitles[curPage] }}</b></span>
        <span class="sp"></span>
        <span v-if="curChild" class="note" style="margin:0">{{ curChild.name }}・{{ curChild.sex||'—' }}・{{ curChild.dob||'—' }}｜已存 {{ curChild.sessions?.length||0 }} 次課程<span v-if="curChild.savedAt">｜評估存檔：{{ curChild.savedAt }}</span><span v-else>｜此檔案尚未存過評估</span></span>
      </el-header>

      <el-main class="content">

        <!-- ═══════ 1. 兒童檔案 ═══════ -->
        <section v-show="curPage==='children'">
          <el-card shadow="never" class="no-print">
            <template #header><b>兒童檔案</b><span class="sub-hint">點擊「載入」選擇兒童；選擇後自動載入已存檔的評估</span></template>
            <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:12px">
              <el-button type="primary" @click="ncDlg=true">＋ 新增兒童</el-button>
              <el-button type="primary" plain @click="saveAssessment" :disabled="!curChild">儲存目前評估到此檔案</el-button>
              <el-button @click="loadChild" :disabled="!curChild">載入此兒童評估</el-button>
              <el-popconfirm title="確定刪除此檔案及全部課程記錄？" @confirm="delChild">
                <template #reference><el-button type="danger" plain :disabled="!curChild">刪除檔案</el-button></template>
              </el-popconfirm>
            </div>
            <el-table :data="children" size="small" border highlight-current-row @row-click="c=>{curChildId=c.id}">
              <el-table-column label="姓名" min-width="150">
                <template #default="{row}"><b>{{ row.name }}</b><el-tag v-if="curChildId===row.id" size="small" effect="plain" style="margin-left:8px">目前</el-tag></template>
              </el-table-column>
              <el-table-column prop="sex" label="性別" width="70" align="center"></el-table-column>
              <el-table-column prop="dob" label="出生日期" width="120"></el-table-column>
              <el-table-column prop="org" label="機構" min-width="140"></el-table-column>
              <el-table-column prop="updated_at" label="最近更新" width="180"></el-table-column>
              <el-table-column label="" width="90" align="center">
                <template #default="{row}"><el-button link type="primary" size="small" @click.stop="curChildId=row.id">載入</el-button></template>
              </el-table-column>
            </el-table>
            <el-empty v-if="!children.length" description="尚無兒童檔案 — 按「＋ 新增兒童」建立第一份檔案" :image-size="80"></el-empty>
          </el-card>
        </section>

        <!-- ═══════ 2. 評估 ═══════ -->
        <section v-show="curPage==='assess'">
          <el-tabs v-model="assessTab">
            <el-tab-pane label="量表評估" name="scale">

    <!-- ═══════ 兒童資料（需先有兒童檔案）═══ -->
    <el-header class="metabar" height="auto" v-if="curChild">
      <el-form :inline="true" class="meta-form" size="default">
        <el-form-item label="機構"><el-input v-model="f.org" placeholder="機構名稱" style="width:170px"></el-input></el-form-item>
        <el-form-item label="姓名"><el-input v-model="f.name" placeholder="兒童姓名" style="width:120px"></el-input></el-form-item>
        <el-form-item label="出生日期"><el-date-picker v-model="f.dob" type="date" value-format="YYYY-MM-DD" placeholder="選擇日期" style="width:150px" @change="onDob"></el-date-picker></el-form-item>
        <el-form-item label="年齡"><el-tag :type="f.dob?'primary':'info'" :effect="f.dob?'dark':'plain'" size="large" style="font-weight:700">{{ ageLabel }}</el-tag></el-form-item>
        <el-form-item label="性別">
          <el-radio-group v-model="f.sex">
            <el-radio-button value="男">男</el-radio-button>
            <el-radio-button value="女">女</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="評估日期"><el-date-picker v-model="f.adate" type="date" value-format="YYYY-MM-DD" style="width:150px"></el-date-picker></el-form-item>
      </el-form>
    </el-header>

    <el-header class="toolbar no-print" height="auto">
      <div class="toolbar-row">
        <span style="font-weight:600;font-size:13px;color:var(--el-text-color-secondary)">按年齡篩選</span>
        <el-check-tag v-for="(lb,i) in ageLabels" :key="i" :checked="selMax!==null && i<=selMax" @change="pickAge(i)" size="small">{{ lb }}</el-check-tag>
        <el-check-tag :checked="selMax===null" @change="selMax=null" size="small">顯示全部</el-check-tag>
        <el-divider direction="vertical"></el-divider>
        <el-checkbox v-model="compact" size="small">智能縮減：列印時略去未記錄項</el-checkbox>
        <el-button type="primary" plain size="small" @click="printForm">列印評估表</el-button>
        <el-divider direction="vertical"></el-divider>
        <span style="font-size:12px;color:var(--el-text-color-secondary)">
          記錄狀態（點擊切換）：
          <el-tag type="info" effect="plain" size="small" style="margin:0 2px">○ 未測試</el-tag>
          <el-tag type="primary" effect="plain" size="small" style="margin:0 2px">✓ 獨立完成</el-tag>
          <el-tag type="danger" effect="plain" size="small" style="margin:0 2px">✗ 回答錯誤</el-tag>
          <el-tag type="warning" effect="plain" size="small" style="margin:0 2px">◐ 需提示／半完成</el-tag>
        </span>
      </div>
    </el-header>

    <el-empty v-if="!curChild" description="請先於「兒童檔案」新增或選擇兒童檔案，才可開始評估記錄" :image-size="90"></el-empty>

        <template v-if="curChild">
        <!-- ═══════ 臨床觀察 ═══════ -->
          <el-card shadow="never">
            <template #header><b>臨床觀察 (Clinical Observation)</b></template>
            <div class="grp-h">一般觀察 / 行為表現</div>
            <el-input v-model="f.obs1" type="textarea" :rows="3" placeholder="記錄兒童的一般行為、注意力、配合度、社交互動等臨床觀察…"></el-input>
            <div class="grp-h">言語特徵 / 發音情況</div>
            <el-input v-model="f.obs2" type="textarea" :rows="3" placeholder="記錄兒童的發音清晰度、音韻過程、語速、語調、聲音品質等特徵…"></el-input>
            <div class="grp-h">主要關注 / 建議</div>
            <el-input v-model="f.obs3" type="textarea" :rows="3" placeholder="記錄治療師的主要關注點、初步印象、後續建議或轉介意見…"></el-input>
          </el-card>


        <!-- ═══════ 理解 / 表達 / 敘事 / 語用口肌 ═══════ -->
        <template v-for="pg in pages" :key="pg.tab">
          <el-card shadow="never">
            <template #header><b>{{ pg.title }}</b><span v-if="pg.desc" style="color:var(--el-text-color-secondary);font-size:13px;margin-left:12px">{{ pg.desc }}</span></template>
            <template v-for="g in pg.groups" :key="g.h">
              <div class="grp-h">{{ g.h }} <el-tag v-if="g.tag" size="small" type="info" effect="plain">{{ g.tag }}</el-tag>
                <span class="selall">
                  <el-button link type="primary" size="small" @click="selectAll(g,2)" title="全部設為獨立完成">✓全選</el-button>
                  <el-button link type="danger" size="small" @click="selectAll(g,3)" title="全部設為回答錯誤">✗全選</el-button>
                  <el-button link type="warning" size="small" @click="selectAll(g,1)" title="全部設為需提示／半完成">◐全選</el-button>
                </span></div>
              <p v-if="g.note" class="note">{{ g.note }}</p>
              <div v-if="g.extra" style="margin:2px 0 6px" v-html="g.extra"></div>
              <div class="items">
                <el-tag v-for="it in g.items" :key="it.t" :class="['st','s'+it.s,{dim:isDim(it)}]"
                        size="large" effect="plain"
                        :type="it.s===2?'primary':it.s===1?'warning':it.s===3?'danger':'info'"
                        @click.capture="cycle(it)">{{ ['○','◐','✓','✗'][it.s] }} {{ it.t }}</el-tag>
              </div>
            </template>
            <!-- 口肌觀察表 -->
            <template v-if="pg.tab==='oral'">
              <div class="grp-h">口肌能力觀察 (Oral Motor)</div>
              <el-table :data="oralRows" size="small" border style="margin:6px 0 14px">
                <el-table-column prop="p" label="部位" width="150"></el-table-column>
                <el-table-column label="觀察項目（預設正常，有異常才點選）">
                  <template #default="{row}"><el-tag v-for="o in row.obs" :key="o.t" class="st" size="large" effect="plain" :type="o.s===1?'danger':'info'" @click.capture="toggleObs(o)">{{ o.s===1?'✗ 異常 — ':'✓ 正常 — ' }}{{ o.t }}</el-tag></template>
                </el-table-column>
              </el-table>
              <div class="items">
                <span class="note" style="margin-right:4px">日常表現（預設無，有才點選）：</span>
                <el-tag v-for="o in dailyObs" :key="o.t" class="st" size="large" effect="plain" :type="o.s===1?'danger':'info'" @click.capture="toggleObs(o)">{{ o.s===1?'✗ 有 ':'✓ 無 ' }}{{ o.t }}</el-tag>
                <el-input v-model="f.oralNote" placeholder="請補充…" style="width:230px" size="small"></el-input>
              </div>
              <div class="items" style="margin-top:8px">
                <span class="note" style="margin-right:4px">進食食物種類／質地（有攝取請點選）：</span>
                <el-tag v-for="o in foodObs" :key="o.t" class="st" size="large" effect="plain" :type="o.s===1?'primary':'info'" @click.capture="toggleObs(o)">{{ (o.s===1?'✓ ':'○ ') + o.t }}</el-tag>
                <el-input v-model="f.foodNote" placeholder="請補充…" style="width:230px" size="small"></el-input>
              </div>
              <el-divider></el-divider>
              <el-collapse>
                <el-collapse-item title="Speech Stimulability Test（HKCAT 後進行，只測未能正確發出的音）" name="stim">
                  <p class="note">跟住落嚟我哋會做一個測試，你重複我講嘅嘢……（Miccio, 2002）</p>
                  <el-table :data="stim" size="small" border>
                    <el-table-column prop="s" label="聲母" width="70" align="center"></el-table-column>
                    <el-table-column v-for="(v,i) in ['_a','_e','_i','_o','_u','隔離']" :key="v" :label="v" width="60" align="center">
                      <template #default="{row}"><el-checkbox v-model="row.c[i]"></el-checkbox></template>
                    </el-table-column>
                    <el-table-column prop="wi" label="詞首 WI"></el-table-column>
                    <el-table-column prop="wf" label="詞尾 WF"></el-table-column>
                    <el-table-column label="% correct" width="100"><template #default="{row}"><el-input v-model="row.pct" size="small"></el-input></template></el-table-column>
                  </el-table>
                </el-collapse-item>
              </el-collapse>
            </template>
          </el-card>
        </template>

        <!-- ═══════ 診斷 ═══════ -->
          <el-card shadow="never">
            <template #header><b>診斷 (Diagnosis)</b><span style="color:var(--el-text-color-secondary);font-size:13px;margin-left:12px">選擇診斷類別及嚴重程度</span></template>
            <el-select v-model="f.dx" placeholder="選擇診斷類別" style="width:100%;max-width:560px" size="large" clearable>
              <el-option v-for="d in dxs" :key="d.k" :label="d.k + ') ' + d.label" :value="d.label"></el-option>
            </el-select>
            <el-alert v-if="dxNote" :title="dxNote" type="info" :closable="false" style="margin:12px 0;line-height:1.8"></el-alert>
            <div style="display:flex;align-items:center;gap:12px;margin:14px 0">
              <span style="font-weight:600">嚴重程度：</span>
              <el-radio-group v-model="f.sev">
                <el-radio-button value="輕度">輕度 (Mild)</el-radio-button>
                <el-radio-button value="中度">中度 (Moderate)</el-radio-button>
                <el-radio-button value="嚴重">嚴重 (Severe)</el-radio-button>
              </el-radio-group>
            </div>
            <el-alert :title="'已選擇診斷：' + (f.dx || '—') + (f.sev ? '（' + f.sev + '）' : '')" type="info" :closable="false"></el-alert>
          </el-card>


        <!-- ═══════ 評估治療師 ═══════ -->
          <el-card shadow="never">
            <template #header><b>評估治療師 (Assessing Therapist)</b></template>
            <el-form label-width="140px" style="max-width:560px">
              <el-form-item label="治療師姓名"><el-input v-model="f.therapist"></el-input></el-form-item>
              <el-form-item label="專業資格 / 執照"><el-input v-model="f.license"></el-input></el-form-item>
              <el-form-item label="簽署日期"><el-date-picker v-model="f.signDate" type="date" value-format="YYYY-MM-DD" style="width:100%"></el-date-picker></el-form-item>
              <el-form-item label="簽名 / 簽署"><el-input v-model="f.signature"></el-input></el-form-item>
              <el-form-item label="手寫簽名">
                <el-upload :auto-upload="false" :show-file-list="false" accept="image/*" :on-change="onSignFile">
                  <el-button size="small">匯入手寫簽名圖片</el-button>
                </el-upload>
                <img v-if="f.signImg" :src="f.signImg" style="height:46px;margin-left:12px;border:1px dashed var(--el-border-color);border-radius:6px;padding:4px;background:#fff"/>
                <el-button v-if="f.signImg" link type="danger" size="small" @click="f.signImg=''">移除</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </template>

            </el-tab-pane>

            <el-tab-pane label="評估報告" name="report">
              <!-- ═══════ 家長報告 ═══════ -->
              <el-card shadow="never" class="no-print" style="margin-bottom:14px">
                <template #header><b>家長報告</b><span style="color:var(--el-text-color-secondary);font-size:13px;margin-left:12px">先完成評估記錄及頂欄資料，生成後報告內容可直接修改</span></template>
                <el-space wrap>
                  <el-button type="primary" @click="genReport">生成家長報告</el-button>
                  <el-button type="success" plain @click="downloadReport" :disabled="!repHtml">下載報告 PDF</el-button>
                  <el-button plain @click="printReport" :disabled="!repHtml">預覽 / 列印 PDF</el-button>
                </el-space>
                <el-alert v-if="repWarn" :title="repWarn" type="warning" :closable="false" style="margin-top:12px"></el-alert>
              </el-card>
              <el-card v-if="repHtml" shadow="never" style="padding:0">
                <div id="repDoc" v-html="repHtml"></div>
              </el-card>
              <el-empty v-else description="尚未生成報告 — 完成評估記錄後按「生成家長報告」"></el-empty>
            </el-tab-pane>
          </el-tabs>
        </section>

        <!-- ═══════ 3. 干預 ═══════ -->
        <section v-show="curPage==='interv'">
          <el-tabs v-model="intervTab">
            <el-tab-pane label="干預方案・課程記錄" name="plan">

<!-- ═══════ 干預方案・課程記錄 ═══════ -->
<el-card shadow="never">
  <template #header><b>干預方案・課程記錄</b>
    <span style="color:var(--el-text-color-secondary);font-size:13px;margin-left:12px">依評估結果生成干預方案 → 記錄每次課程與效果</span>
  </template>
  <el-divider content-position="left">本次干預方案（第 {{ nextSessionNo }} 次）</el-divider>
  <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:10px">
    <el-date-picker v-model="planDate" type="date" value-format="YYYY-MM-DD" style="width:150px"></el-date-picker>
    <el-button type="primary" @click="genPlan(true)" :loading="genLoading" :disabled="!curChild">{{ genLoading ? 'AI 生成中… ' + genSecs + ' 秒' : 'AI 生成方案' }}</el-button>
    <el-button @click="genPlan(false)" :disabled="!curChild">依種子庫生成</el-button>
    <el-button link type="primary" @click="aiDlg=true">AI 設定</el-button>
    <el-button type="success" @click="saveSession" :disabled="!plan">儲存為課程記錄</el-button>
  </div>
  <el-alert v-if="genLoading" title="AI 正在根據評估弱項與種子庫撰寫方案，長文生成可能需要 1–2 分鐘，請勿關閉頁面" type="info" :closable="false" style="margin-bottom:10px"/>
  <el-alert v-if="planErr" :title="planErr" type="error" :closable="false" style="margin-bottom:10px;line-height:1.8"/>
  <template v-if="plan">
    <div class="plan-ws">
      <!-- 左：版本 + 方案內容 -->
      <div class="plan-left">
        <div class="grp-h">方案版本</div>
        <div class="ver-list">
          <button v-for="(v,i) in plan.versions" :key="i" :class="['ver',{on:i===plan.curIdx}]" @click="plan.curIdx=i">{{ v.label }}</button>
        </div>
        <div class="grp-h">訓練目標與遊戲 <span class="note">（勾選 = 採用；每個目標可展開）</span></div>
        <el-collapse v-model="openGoals">
          <el-collapse-item v-for="(g,gi) in plan.versions[plan.curIdx].goals" :key="plan.curIdx+'-'+gi" :name="String(gi)">
            <template #title>
              <span class="goal-title">目標 {{ gi+1 }}</span>
              <el-tag size="small" :type="g.games.some(x=>x.checked)?'success':'info'" effect="plain">{{ g.games.filter(x=>x.checked).length }}/{{ g.games.length }} 遊戲採用</el-tag>
              <span style="flex:1"></span>
            </template>
            <el-input v-model="g.text" type="textarea" :autosize="{minRows:1,maxRows:4}" placeholder="訓練目標"></el-input>
            <div v-for="(gm,gmi) in g.games" :key="gmi" class="game-row">
              <el-checkbox v-model="gm.checked"></el-checkbox>
              <div class="game-fields">
                <el-input v-model="gm.name" size="small" placeholder="遊戲／活動名稱"></el-input>
                <div style="display:flex;gap:8px">
                  <el-tag size="small" :type="DOM_TAG[gm.domain]||'info'" effect="plain">{{ DOM_NAME[gm.domain]||gm.domain }}</el-tag>
                  <el-input v-model="gm.target" size="small" type="textarea" :autosize="{minRows:1,maxRows:3}" placeholder="要達到的目標"></el-input>
                </div>
                <el-input v-model="gm.desc" size="small" type="textarea" :autosize="{minRows:2,maxRows:6}" placeholder="玩法／措施"></el-input>
              </div>
              <el-button link type="danger" size="small" @click="g.games.splice(gmi,1)">刪</el-button>
            </div>
            <div style="display:flex;gap:8px;margin-top:8px">
              <el-button size="small" @click="addGame(gi)">＋ 加遊戲</el-button>
              <el-popconfirm title="刪除此目標？" @confirm="delGoal(gi)">
                <template #reference><el-button size="small" type="danger" plain>刪除此目標</el-button></template>
              </el-popconfirm>
            </div>
          </el-collapse-item>
        </el-collapse>
        <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap">
          <el-button size="small" @click="addGoal">＋ 加一個目標</el-button>
          <el-button size="small" type="success" @click="finalize">生成最終方案（採用勾選遊戲）</el-button>
        </div>
        <div v-if="finalPlan" class="final-box">
          <div class="grp-h">★ 最終方案（第 {{ finalPlan.no }} 次・{{ finalPlan.date }}）</div>
          <div v-for="(g,gi) in finalPlan.goals" :key="gi" style="margin-bottom:12px">
            <b>目標 {{ gi+1 }}：</b>{{ g.text }}
            <div v-for="(gm,gmi) in g.games" :key="gmi" style="margin:6px 0 0 18px;font-size:13px">
              ▪ <b>{{ gm.name }}</b>（{{ DOM_NAME[gm.domain]||gm.domain }}）─ 目標：{{ gm.target }}｜玩法：{{ gm.desc }}
            </div>
            <div v-if="!g.games.length" class="note" style="margin-left:18px">（此目標未採用遊戲）</div>
          </div>
        </div>
      </div>
      <!-- 右：對話 -->
      <div class="plan-right">
        <div class="grp-h" style="margin-top:2px">修改對話 <span class="note">（例：第二個目標太難，換簡單的遊戲／加入一個口肌遊戲）</span></div>
        <div class="chat-box" ref="chatBoxEl">
          <div v-for="(m,mi) in plan.chat" :key="mi" :class="['msg',m.role]">{{ m.text }}</div>
          <div v-if="chatLoading" class="msg assistant">⏳ AI 修改中…</div>
        </div>
        <div style="display:flex;gap:8px;margin-top:8px">
          <el-input v-model="chatInput" placeholder="輸入修改指示…" @keyup.enter="sendChat"></el-input>
          <el-button type="primary" @click="sendChat" :loading="chatLoading">送出</el-button>
        </div>
      </div>
    </div>
  </template>
  <el-empty v-else description="選擇兒童後，按「AI 生成方案」或「依種子庫生成」" :image-size="70"></el-empty>
  <el-divider content-position="left">課程記錄（{{ curChild?.sessions?.length||0 }} 次）</el-divider>
  <el-table :data="curChild?.sessions||[]" size="small" border v-if="curChild">
    <el-table-column prop="no" label="節數" width="64" align="center"></el-table-column>
    <el-table-column prop="date" label="日期" width="110"></el-table-column>
    <el-table-column label="訓練目標" min-width="220">
      <template #default="{row}"><span class="note">{{ row.goals.join('；') }}</span></template>
    </el-table-column>
    <el-table-column label="遊戲" width="170">
      <template #default="{row}"><span class="note">{{ row.games.map(g=>g.name).join('、') }}</span></template>
    </el-table-column>
    <el-table-column label="效果" width="150">
      <template #default="{row}">
        <el-select v-model="row.effect.level" size="small" @change="saveCurChild">
          <el-option v-for="e in EFFECTS" :key="e" :label="e" :value="e"></el-option>
        </el-select>
      </template>
    </el-table-column>
    <el-table-column label="" width="110" align="center">
      <template #default="{row}">
        <el-popconfirm title="刪除此記錄？" @confirm="delSession(row.id)">
          <template #reference><el-button link type="danger" size="small">刪除</el-button></template>
        </el-popconfirm>
      </template>
    </el-table-column>
  </el-table>
  <el-empty v-else description="尚未選擇兒童" :image-size="60"></el-empty>
</el-card>
            </el-tab-pane>

            <el-tab-pane label="干預種子庫" name="seeds">
<!-- ═══════ 干預種子庫 ═══════ -->
<el-card shadow="never">
  <template #header><b>干預種子庫</b>
    <span style="color:var(--el-text-color-secondary);font-size:13px;margin-left:12px">所有干預遊戲與措施的範本，可維護更新；生成方案時從此調用</span>
  </template>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px">
    <el-button type="primary" size="small" @click="openSeedDlg()">＋ 新增遊戲／措施</el-button>
    <el-button size="small" @click="resetSeeds">恢復預設範本</el-button>
    <el-upload :auto-upload="false" :show-file-list="false" accept=".json" :on-change="importSeeds"><el-button size="small">匯入 JSON</el-button></el-upload>
    <el-button size="small" @click="exportSeeds">匯出 JSON</el-button>
    <span class="note" style="align-self:center">共 {{ seeds.length }} 項（儲存於伺服器）</span>
  </div>
  <el-table :data="seeds" size="small" border>
    <el-table-column label="範疇" width="110">
      <template #default="{row}"><el-tag size="small" :type="DOM_TAG[row.domain]||'info'">{{ DOM_NAME[row.domain]||row.domain }}</el-tag></template>
    </el-table-column>
    <el-table-column prop="name" label="遊戲／措施" width="170"></el-table-column>
    <el-table-column label="適齡" width="100">
      <template #default="{row}">{{ row.amin }}–{{ row.amax }} 歲</template>
    </el-table-column>
    <el-table-column prop="goal" label="訓練目標" min-width="200"></el-table-column>
    <el-table-column prop="desc" label="玩法／措施" min-width="240"></el-table-column>
    <el-table-column label="" width="120" align="center">
      <template #default="{row}">
        <el-button link type="primary" size="small" @click="openSeedDlg(row)">編輯</el-button>
        <el-button link type="danger" size="small" @click="delSeed(row)">刪除</el-button>
      </template>
    </el-table-column>
  </el-table>
</el-card>
            </el-tab-pane>
          </el-tabs>
        </section>

        <!-- ═══════ 4. 設置 ═══════ -->
        <section v-show="curPage==='settings'">
          <el-card shadow="never">
            <template #header><b>AI 設定</b><span class="sub-hint">干預方案 AI 生成與對話修改所用的 LLM 連線</span></template>
            <p class="note" style="margin-top:0">API 金鑰儲存於後端伺服器，不存於瀏覽器；未設定時仍可用「依種子庫生成」方案。</p>
            <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
              <el-button type="primary" @click="aiDlg=true">開啟 AI 設定</el-button>
              <span class="note" style="margin:0" v-if="aiCfg.model">目前：{{ aiCfg.model }}｜協議：{{ aiCfg.type }}</span>
              <span class="note" style="margin:0" v-else>尚未設定模型</span>
            </div>
          </el-card>
          <el-card shadow="never">
            <template #header><b>關於本平台</b></template>
            <p class="note" style="margin-top:0">學前兒童口語評估量表（Preschool Language Assessment Scale，0–6 歲）｜言語治療評估與干預工作平台。</p>
            <p class="note" style="margin:0">本量表供註冊言語治療師作臨床評估之用；評估結果須結合臨床觀察及專業判斷綜合解讀。</p>
          </el-card>
        </section>

<!-- 新增兒童 -->
<el-dialog v-model="ncDlg" title="新增兒童檔案" width="420px">
  <el-form label-width="80px">
    <el-form-item label="姓名"><el-input v-model="nc.name"></el-input></el-form-item>
    <el-form-item label="性別">
      <el-radio-group v-model="nc.sex"><el-radio-button value="男">男</el-radio-button><el-radio-button value="女">女</el-radio-button></el-radio-group>
    </el-form-item>
    <el-form-item label="出生日期"><el-date-picker v-model="nc.dob" type="date" value-format="YYYY-MM-DD" style="width:100%"></el-date-picker></el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="ncDlg=false">取消</el-button>
    <el-button type="primary" @click="addChild">建立</el-button>
  </template>
</el-dialog>

<!-- 種子庫編輯 -->
<el-dialog v-model="seedDlg" :title="seedForm.id?'編輯遊戲／措施':'新增遊戲／措施'" width="520px">
  <el-form label-width="90px">
    <el-form-item label="名稱"><el-input v-model="seedForm.name"></el-input></el-form-item>
    <el-form-item label="範疇">
      <el-select v-model="seedForm.domain" style="width:100%">
        <el-option v-for="(v,k) in DOM_NAME" :key="k" :label="v" :value="k"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="適齡（歲）">
      <div style="display:flex;gap:8px;align-items:center">
        <el-input-number v-model="seedForm.amin" :min="0" :max="12"></el-input-number> 至
        <el-input-number v-model="seedForm.amax" :min="0" :max="12"></el-input-number>
      </div>
    </el-form-item>
    <el-form-item label="訓練目標"><el-input v-model="seedForm.goal" type="textarea" :rows="2"></el-input></el-form-item>
    <el-form-item label="玩法／措施"><el-input v-model="seedForm.desc" type="textarea" :rows="3"></el-input></el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="seedDlg=false">取消</el-button>
    <el-button type="primary" @click="saveSeed">儲存</el-button>
  </template>
</el-dialog>

<!-- AI 設定 -->
<el-dialog v-model="aiDlg" title="AI 設定" width="520px">
  <el-alert type="info" :closable="false" style="margin-bottom:14px;line-height:1.8"
    title="填入後端代連的 LLM API（OpenAI 相容 / Anthropic / Responses）。金鑰儲存於後端伺服器，不再存於瀏覽器；未填寫時仍可用「依種子庫生成」。"></el-alert>
  <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px">
    <span class="note">快速填入：</span>
    <el-button v-for="p in AI_PRESETS" :key="p.n" size="small" @click="applyPreset(p)">{{ p.n }}</el-button>
  </div>
  <el-form label-width="100px">
    <el-form-item label="協議">
      <el-select v-model="aiCfg.type" style="width:100%">
        <el-option label="OpenAI Chat Completions" value="openai"></el-option>
        <el-option label="OpenAI Responses（Codex 接入）" value="responses"></el-option>
        <el-option label="Anthropic Claude" value="anthropic"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="API 位址"><el-input v-model="aiCfg.base" placeholder="如 https://open.bigmodel.cn/api/v1"></el-input></el-form-item>
    <el-form-item label="API Key"><el-input v-model="aiCfg.key" type="password" show-password placeholder="sk-..."></el-input></el-form-item>
    <el-form-item label="模型"><el-input v-model="aiCfg.model" placeholder="glm-5.3 / deepseek-chat / claude-sonnet-4-5"></el-input></el-form-item>
  </el-form>
  <div style="display:flex;gap:10px;align-items:center">
    <el-button size="small" :loading="aiTesting" @click="testAi">測試連線</el-button>
    <span class="note" v-if="aiTest">{{ aiTest }}</span>
  </div>
  <template #footer>
    <el-button @click="aiDlg=false">關閉</el-button>
    <el-button type="primary" @click="saveAiCfg">儲存</el-button>
  </template>
</el-dialog>


                <el-backtop :right="24" :bottom="24"></el-backtop>
        <div class="footer no-print">本量表供註冊言語治療師作臨床評估之用；評估結果須結合臨床觀察及專業判斷綜合解讀。</div>

      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
// 學前兒童口語評估量表 — 自單檔 HTML 原樣遷移（Vite + Vue3 SFC），UI/交互保持不變
import { reactive, ref, computed, watch, nextTick } from 'vue';
import * as ElementPlus from 'element-plus';   // 業務邏輯大量使用 ElementPlus.ElMessage / ElMessageBox
import html2pdf from 'html2pdf.js';
import { PAGES, oralRows as oralRowsD, dailyObs as dailyObsD, foodObs as foodObsD, stim as stimD,
         dxs, TYP, DOMS, HOME_BASE, DEFAULT_SEEDS } from './data.js';
import { api } from './api.js';
import reportCss from './styles.css?inline';   // buildDoc() 列印預覽視窗的獨立樣式

const pages    = reactive(PAGES);
const oralRows = reactive(oralRowsD);
const dailyObs = reactive(dailyObsD);
const foodObs  = reactive(foodObsD);
const stim     = reactive(stimD);

    // ══ 頁面結構：左側菜單 4 大區 ══
    const curPage    = ref('children');
    const assessTab  = ref('scale');
    const intervTab  = ref('plan');
    const pageTitles = {children:'兒童檔案', assess:'評估', interv:'干預', settings:'設置'};

    const f = reactive({org:'',name:'',dob:'',adate:new Date().toISOString().slice(0,10),sex:'',obs1:'',obs2:'',obs3:'',
      dx:'',sev:'',therapist:'',license:'',signDate:new Date().toISOString().slice(0,10),signature:'',oralNote:'',foodNote:''});
    const selMax = ref(null);
    const compact = ref(false);
    const ageLabels = ['0 歲','1 歲','2 歲','3 歲','4 歲','5 歲','6 歲+'];
    const repWarn = ref('');
    const repHtml = ref('');
    const dxNote = computed(()=>{const d=dxs.find(x=>x.label===f.dx);return d?d.note:'';});

    const months = ()=>{
      if(!f.dob) return null;
      const d0=new Date(f.dob+'T00:00:00'), d1=f.adate?new Date(f.adate+'T00:00:00'):new Date();
      if(d1<d0) return null;
      let m=(d1.getFullYear()-d0.getFullYear())*12+(d1.getMonth()-d0.getMonth());
      if(d1.getDate()<d0.getDate()) m--;
      return Math.max(0,m);
    };
    const ageLabel = computed(()=>{
      const m=months(); return m===null?'—':Math.floor(m/12)+' 歲 '+(m%12)+' 個月';
    });
    function onDob(){
      const m=months();
      if(m!==null) selMax.value=Math.min(6,Math.floor(m/12));  // 自動選中同齡（含之前年齡）
    }
    function pickAge(i){ selMax.value = (selMax.value===i)? null : i; }  // 累積式：選 N 含 0..N
    const isDim = it => selMax.value!==null && it.a>selMax.value;
    // 點擊順序：未測試 → ✓ 獨立完成 → ◐ 需提示 → 未測試
    // 點擊順序：○ 未測試 → ✓ 獨立完成 → ✗ 回答錯誤 → ◐ 需提示 → ○
    function cycle(it){ it.s = it.s===0?2 : it.s===2?3 : it.s===3?1 : 0; }
    function toggleObs(o){ o.s = o.s===1?0:1; }  // 口肌觀察：正常⇄異常／無⇄有／攝取切換
    function onSignFile(file){
      const rd = new FileReader();
      rd.onload = e => { f.signImg = e.target.result; };
      rd.readAsDataURL(file.raw);
    }

    function selectAll(g, s){
      const vis = g.items.filter(it=>!isDim(it));          // 只作用於當前可見（未被年齡篩掉）的項目
      const allSame = vis.length && vis.every(it=>it.s===s);
      vis.forEach(it=>{ it.s = allSame ? 0 : s; });        // 已全部是該狀態 → 再點一次全部清空
    }

    function printForm(){
      document.body.classList.toggle('compact', compact.value);
      window.print();
    }

    // ── 報告 ──
    const esc = s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
    const top3 = a=>a.slice(0,3).join('、');
    const bandKey = m=>m<12?'0-1':m<24?'1-2':m<36?'2-3':m<48?'3-4':m<60?'4-5':'5-6';
    function collect(d){
      const done=[],part=[],none=[];
      PAGES.forEach(p=>p.groups.forEach(g=>{
        if(g.d!==d) return;
        g.items.forEach(it=>{
          (it.s===2?done:it.s===1?part:none).push(it.t);
        });
      }));
      return {done,part,none};
    }
    function ra(cls,label,text){return `<div class="ra ${cls}"><span class="ra-b">${label}</span><span class="ra-t">${text}</span></div>`;}
    function narrative(dom,st,bandIdx){
      const total=st.done.length+st.part.length+st.none.length;
      if(!total) return ra('none','未有記錄','此範疇暫未有實際記錄可供整理；建議治療師按臨床觀察及相關評估結果補充判讀。');
      const y=st.done.length
        ?ra('ok','已建立能力',`可獨立處理「${top3(st.done)}」等項目，顯示已有${dom.name}基礎。`)
        :ra('none','已建立能力',`本次未見能穩定獨立完成的${dom.name}項目，宜由較基礎的能力開始建立。`);
      const g=st.part.length?ra('hint','提示下表現',`在成人提示或示範下，可處理「${top3(st.part)}」；現階段仍需要清晰而一致的支持。`):'';
      let E;
      if(st.none.length) E=ra('need','需要支持',`在「${top3(st.none)}」等項目尚未穩定掌握。${bandIdx!==null?'同齡參考範圍內留空的項目已按未能做到處理。':''}`);
      else if(st.part.length) E=ra('hint','需要支持',`部分${dom.name}項目仍需成人提示，反映相關表現在互動情境中尚未穩定。`);
      else E=ra('none','需要支持','現時未見明顯的同齡能力落差；可繼續於不同情境中鞏固及泛化。');
      const v=st.none.length>st.done.length?dom.nextBase:dom.nextAdv;
      return y+g+E+ra('next','下一步',v);
    }

    // ═══════ 兒童檔案・種子庫・AI 干預方案 ═══════
    const DOM_NAME = {rec:'理解', exp:'表達', nar:'敘事/高階', pra:'語用', oral:'口肌/發音'};
    const DOM_TAG  = {rec:'primary', exp:'success', nar:'warning', pra:'danger', oral:'info'};
    const EFFECTS  = ['未見效','稍有進步','明顯進步','已達標'];


    // ── 數據層：localStorage db 全部改為後端 API（契約見設計 §3）──
    const children  = reactive([]);          // 輕量列表（下拉選單）
    const counts    = reactive({});          // id → 課程數（載入完整檔案時更新；輕量列表不含 sessions）
    const seeds     = reactive(DEFAULT_SEEDS.map(s=>({...s})));
    const aiCfg     = reactive({type:'openai', base:'https://api.openai.com/v1/chat/completions', key:'', model:'gpt-4o-mini'});

    function saveSeeds(){
      api.putSeeds(JSON.parse(JSON.stringify(seeds)))
        .catch(e=>ElementPlus.ElMessage.error('種子庫儲存失敗：'+e.message));
    }

    const curChildId = ref(null);
    const curChild   = ref(null);            // 選中後從後端載入的完整檔案
    async function refreshChildren(){
      try{ children.splice(0, children.length, ...await api.listChildren()); }
      catch(e){ console.warn('載入兒童列表失敗：', e.message); }
    }
    watch(curChildId, async id=>{
      if(!id){ curChild.value=null; return; }
      const c=await api.getChild(id).catch(e=>{ ElementPlus.ElMessage.error('載入檔案失敗：'+e.message); return null; });
      if(curChildId.value===id){ curChild.value=c; if(c){ counts[c.id]=(c.sessions?.length||0); applyChildToForm(c); } }
    });
    async function saveCurChild(){           // 整份替換寫回後端（PUT）
      const c=curChild.value; if(!c) return false;
      try{
        await api.putChild(c.id, JSON.parse(JSON.stringify(c)));
        counts[c.id]=(c.sessions?.length||0); refreshChildren();
        return true;
      }catch(e){ ElementPlus.ElMessage.error('儲存失敗：'+e.message); return false; }
    }
    watch(aiCfg, ()=>{ api.putAi(JSON.parse(JSON.stringify(aiCfg))).catch(()=>{}); }, {deep:true});
    const nextSessionNo = computed(()=>(curChild.value?.sessions?.length||0)+1);
    const ncDlg = ref(false);
    const nc = reactive({name:'',sex:'',dob:''});
    const seedDlg = ref(false);
    const seedForm = reactive({id:null,name:'',domain:'rec',amin:0,amax:6,goal:'',desc:''});
    const aiDlg = ref(false);
    const plan = ref(null);
    const planDate = ref(new Date().toISOString().slice(0,10));
    const genLoading = ref(false);
    const genSecs = ref(0);
    const openGoals = ref(['0']);
    const finalPlan = ref(null);

    function statesObj(){
      const m={};
      pages.forEach(p=>p.groups.forEach(g=>g.items.forEach(it=>{ if(it.s) m[it.id]=it.s; })));
      oralRows.forEach(r=>r.obs.forEach(o=>{ if(o.s) m[o.id]=o.s; }));
      dailyObs.forEach(o=>{ if(o.s) m[o.id]=o.s; });
      foodObs.forEach(o=>{ if(o.s) m[o.id]=o.s; });
      return m;
    }
    function applyStates(m){
      pages.forEach(p=>p.groups.forEach(g=>g.items.forEach(it=>{ it.s=(m&&m[it.id])||0; })));
      oralRows.forEach(r=>r.obs.forEach(o=>{ o.s=(m&&m[o.id])||0; }));
      dailyObs.forEach(o=>{ o.s=(m&&m[o.id])||0; });
      foodObs.forEach(o=>{ o.s=(m&&m[o.id])||0; });
    }
    async function addChild(){
      if(!nc.name.trim()){ ElementPlus.ElMessage.warning('請填寫姓名'); return; }
      const c={id:'c'+Date.now(), name:nc.name.trim(), sex:nc.sex, dob:nc.dob, org:f.org, states:{}, sessions:[], createdAt:new Date().toISOString().slice(0,10)};
      try{ await api.addChild(c); }catch(e){ ElementPlus.ElMessage.error('建立失敗：'+e.message); return; }
      children.unshift(c); counts[c.id]=0;
      curChildId.value=c.id; f.name=c.name; f.sex=c.sex; f.dob=c.dob; if(c.org)f.org=c.org;
      nc.name=''; nc.sex=''; nc.dob=''; ncDlg.value=false;
      ElementPlus.ElMessage.success('檔案已建立，完成評估後按「儲存目前評估到此檔案」');
    }
    async function saveAssessment(){
      const c=curChild.value; if(!c) return;
      Object.assign(c,{name:f.name.trim()||c.name, sex:f.sex, dob:f.dob, org:f.org, dx:f.dx, sev:f.sev,
        adate:f.adate, obs:{o1:f.obs1,o2:f.obs2,o3:f.obs3}, states:statesObj(), savedAt:new Date().toLocaleString('zh-HK',{hour12:false}),
        therapist:f.therapist, license:f.license, signDate:f.signDate, signature:f.signature, signImg:f.signImg,
        oralNote:f.oralNote, foodNote:f.foodNote});
      if(await saveCurChild()) ElementPlus.ElMessage.success('評估已存入 '+c.name+' 的檔案（'+c.savedAt+'）');
    }
    function applyChildToForm(c){
      f.name=c.name; f.sex=c.sex; f.dob=c.dob; if(c.org)f.org=c.org; f.dx=c.dx||''; f.sev=c.sev||'';
      f.obs1=c.obs?.o1||''; f.obs2=c.obs?.o2||''; f.obs3=c.obs?.o3||'';
      f.adate=c.adate||new Date().toISOString().slice(0,10);
      f.therapist=c.therapist||''; f.license=c.license||''; f.signDate=c.signDate||new Date().toISOString().slice(0,10);
      f.signature=c.signature||''; f.signImg=c.signImg||''; f.oralNote=c.oralNote||''; f.foodNote=c.foodNote||'';
      applyStates(c.states||{}); onDob();
    }
    function loadChild(){
      const c=curChild.value; if(!c) return;
      applyChildToForm(c);
      const hasStates=c.states&&Object.keys(c.states).some(k=>k!=='undefined');  // 舊版壞數據只有 undefined 鍵，視同未存過
      ElementPlus.ElMessage.success('已載入 '+c.name+' 的評估記錄'+(hasStates?'（存檔：'+c.savedAt+'）':'（此檔案尚未存過評估，各項為空白）'));
    }
    async function delChild(){
      const i=children.findIndex(c=>c.id===curChildId.value);
      if(i>-1){
        try{ await api.delChild(curChildId.value); }catch(e){ ElementPlus.ElMessage.error('刪除失敗：'+e.message); return; }
        children.splice(i,1); delete counts[curChildId.value]; curChildId.value=null;
      }
    }
    function openSeedDlg(row){
      Object.assign(seedForm, row?JSON.parse(JSON.stringify(row)):{id:null,name:'',domain:'rec',amin:0,amax:6,goal:'',desc:''});
      seedDlg.value=true;
    }
    function saveSeed(){
      if(!seedForm.name.trim()){ ElementPlus.ElMessage.warning('請填寫名稱'); return; }
      if(seedForm.id){ const s=seeds.find(x=>x.id===seedForm.id); if(s) Object.assign(s, JSON.parse(JSON.stringify(seedForm))); }
      else seeds.push({...seedForm, id:'s'+Date.now()});
      saveSeeds(); seedDlg.value=false;
    }
    function delSeed(row){ const i=seeds.findIndex(x=>x.id===row.id); if(i>-1)seeds.splice(i,1); saveSeeds(); }
    function resetSeeds(){
      ElementPlus.ElMessageBox.confirm('確定放棄所有修改，恢復預設範本？','恢復預設',{type:'warning'})
        .then(()=>{ seeds.splice(0,seeds.length,...DEFAULT_SEEDS.map(s=>({...s}))); saveSeeds(); })
        .catch(()=>{});
    }
    function exportSeeds(){
      const blob=new Blob([JSON.stringify(seeds,null,2)],{type:'application/json'});
      const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='干預種子庫.json';
      a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000);
    }
    function importSeeds(file){
      const rd=new FileReader();
      rd.onload=e=>{ try{
        const arr=JSON.parse(e.target.result);
        if(!Array.isArray(arr)||!arr.length) throw new Error('格式不正確');
        seeds.splice(0,seeds.length,...arr); saveSeeds();
        ElementPlus.ElMessage.success('已匯入 '+arr.length+' 項');
      }catch(err){ ElementPlus.ElMessage.error('匯入失敗：'+err.message); } };
      rd.readAsText(file.raw);
    }

    function weakByDomain(band){
      return ['rec','exp','nar','pra'].map(d=>{
        const items=[];
        PAGES.forEach(p=>p.groups.forEach(g=>{ if(g.d!==d) return;
          g.items.forEach(it=>{ if((it.s===1||it.s===0||it.s===3) && it.a<=band+1) items.push(it.t); }); }));
        return {d, items};
      }).filter(x=>x.items.length).sort((a,b)=>b.items.length-a.items.length);
    }
    function ruleGoals(band){
      const out=[];
      weakByDomain(band).forEach(w=>w.items.slice(0,2).forEach(t=>out.push(`提升${DOM_NAME[w.d]}：能在少許提示下穩定表現「${t}」`)));
      return out.slice(0,5);
    }
    function pickGames(band){
      const weak=weakByDomain(band).map(w=>w.d);
      const doms=weak.length?weak:['rec','exp'];
      const picked=[], used=new Set();
      for(const d of doms){
        for(const s of seeds.filter(s=>s.domain===d && s.amin<=band+1 && s.amax>=band)){
          if(picked.length>=5) break;
          if(!used.has(s.id)){ picked.push({name:s.name,domain:s.domain,target:s.goal,desc:s.desc}); used.add(s.id); }
        }
      }
      for(const s of seeds){ if(picked.length>=4) break; if(!used.has(s.id)){ picked.push({name:s.name,domain:s.domain,target:s.goal,desc:s.desc}); used.add(s.id); } }
      return picked;
    }
    function rulePlan(band){
      const goals=[], used=new Set();
      weakByDomain(band).forEach(w=>{
        const games=[];
        for(const s of seeds.filter(s=>s.domain===w.d && s.amin<=band+1 && s.amax>=band)){
          if(games.length>=2) break;
          if(!used.has(s.id)){ games.push({name:s.name,domain:s.domain,target:s.goal,desc:s.desc,checked:true}); used.add(s.id); }
        }
        if(w.items.length) goals.push({text:`提升${DOM_NAME[w.d]}：能在少許提示下穩定表現「${w.items.slice(0,2).join('、')}」`, games});
      });
      for(const s of seeds){
        if(goals.length && goals.every(g=>g.games.length>=1)) break;
        const gi=goals.findIndex(g=>g.games.length<1);
        if(gi>-1 && !used.has(s.id)){ goals[gi].games.push({name:s.name,domain:s.domain,target:s.goal,desc:s.desc,checked:true}); used.add(s.id); }
      }
      return {goals};
    }
    function domKeyOf(cn){ const e=Object.entries(DOM_NAME).find(([k,v])=>String(cn).includes(v)); return e?e[0]:'rec'; }
    const AI_PRESETS = [
      {n:'Claude',    type:'anthropic', base:'https://api.anthropic.com/v1/messages', model:'claude-sonnet-4-5'},
      {n:'OpenAI',    type:'openai', base:'https://api.openai.com/v1/chat/completions', model:'gpt-4o-mini'},
      {n:'DeepSeek',  type:'openai', base:'https://api.deepseek.com/v1/chat/completions', model:'deepseek-chat'},
      {n:'Moonshot',  type:'openai', base:'https://api.moonshot.cn/v1/chat/completions', model:'moonshot-v1-8k'},
      {n:'智譜 Coding-Claude',  type:'anthropic', base:'https://open.bigmodel.cn/api/anthropic', model:'glm-5.3'},
      {n:'智譜 Codex',          type:'responses', base:'https://open.bigmodel.cn/api/v1', model:'glm-5.3'},
      {n:'智譜 Coding-OpenAI',  type:'openai',    base:'https://open.bigmodel.cn/api/coding/paas/v4', model:'glm-5.3'},
      {n:'智譜 GLM(通用)',      type:'openai',    base:'https://open.bigmodel.cn/api/paas/v4/chat/completions', model:'glm-4-flash'},
      {n:'阿里通義',  type:'openai', base:'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', model:'qwen-plus'},
    ];
    function applyPreset(p){ aiCfg.base=p.base; aiCfg.model=p.model; aiCfg.type=p.type||'openai'; }
    const aiTesting = ref(false);
    const aiTest = ref('');
    const planErr = ref('');
    async function testAi(){
      await api.putAi(JSON.parse(JSON.stringify(aiCfg))).catch(()=>{});
      aiTesting.value=true; aiTest.value='';
      try{
        await callLLM('回應OK', 8);
        aiTest.value='✅ 連線成功（'+(isAnthropicCfg()?'Anthropic':'OpenAI 相容')+'格式），AI 生成可用';
      }catch(e){
        aiTest.value='❌ '+e.message;
      }
      aiTesting.value=false;
    }

    function isAnthropicCfg(){
      return (aiCfg.type==='anthropic') || /anthropic\.com/.test(aiCfg.base||'');
    }
    // 三協議（openai / responses / anthropic）分支與 CORS 處理已整體移至後端 ai.py，前端只調代理
    async function callLLM(prompt, maxTokens){
      try{
        const data=await api.aiChat(prompt, maxTokens||4000);
        return data.text || '';
      }catch(e){ throw new Error(e.message || 'AI 請求失敗'); }
    }

    function parsePlanJSON(txt){
      let t=(txt||'').replace(/```json|```/gi,'').trim();
      const tryParse=s=>{ try{ return JSON.parse(s); }catch(e){ return null; } };
      let j=tryParse(t);
      if(!j){ const a=t.indexOf('{'), b=t.lastIndexOf('}');
        if(a>-1 && b>a) j=tryParse(t.slice(a,b+1)); }
      if(!j){
        const a=t.indexOf('{');
        if(a>-1){ let s=t.slice(a).replace(/,\s*$/,'');
          const open=(s.match(/{/g)||[]).length-(s.match(/}/g)||[]).length;
          j=tryParse(s+'}'.repeat(Math.max(0,open))); }
      }
      if(!j || (!j.goals && !j.games))
        throw new Error('AI 回應中找不到有效的方案 JSON。回應開頭：「'+(t||'(空回應)').slice(0,120)+'…」— 可再試一次或更換模型');
      return j;
    }

    async function aiGenPlan(band){
      const weak=weakByDomain(band).map(w=>({範疇:DOM_NAME[w.d], 項目:w.items.slice(0,8)}));
      const lib=seeds.map(s=>({name:s.name, domain:DOM_NAME[s.domain], ages:`${s.amin}-${s.amax}歲`, goal:s.goal}));
      const prompt=`你是資深兒童言語治療師。根據以下評估結果，為兒童設計一次言語治療課堂的干預方案。\n兒童：${f.name||'未命名'}，${ageLabel.value}。\n評估弱項（需提示或未做到）：${JSON.stringify(weak)}\n可用遊戲／措施種子庫：${JSON.stringify(lib)}\n要求：4-5 個遊戲，優先從種子庫選取或改編，每個遊戲標明要達到的目標；訓練目標 3-5 條並對應弱項；全部用繁體中文。\n只輸出 JSON（無 markdown 代碼框）：{"goals":[{"text":"訓練目標","games":[{"name":"遊戲名稱","domain":"rec|exp|nar|pra|oral","target":"此遊戲要達到的目標","desc":"玩法"}]}]} 每個目標配 1-2 個遊戲，共 3-5 個遊戲。`;
      let txt=await callLLM(prompt, 4000);
      const j=parsePlanJSON(txt);
      const goals=(j.goals||[]).slice(0,6).map(g=>{
        if(typeof g==='string') return {text:g, games:[]};
        return {text:g.text||'', games:(g.games||[]).slice(0,5).map(gm=>({name:gm.name||'',domain:domKeyOf(gm.domain),target:gm.target||'',desc:gm.desc||'',checked:true}))};
      });
      // 舊格式相容：扁平 games 平均分配到各目標
      if(goals.length && goals.every(g=>!g.games.length) && (j.games||[]).length){
        (j.games||[]).slice(0,10).forEach((gm,i)=>{ const gi=i%goals.length;
          goals[gi].games.push({name:gm.name||'',domain:domKeyOf(gm.domain),target:gm.target||'',desc:gm.desc||'',checked:true}); });
      }
      return {goals, reply:j.reply||''};
    }
    async function genPlan(useAI){
      if(!curChild.value){ ElementPlus.ElMessage.warning('請先選擇兒童檔案'); return; }
      const m=months(); const band=m===null?3:Math.min(6,Math.floor(m/12));
      genLoading.value=true; planErr.value=''; genSecs.value=0;
      const tick = setInterval(()=>{ if(genLoading.value) genSecs.value++; else clearInterval(tick); }, 1000);
      let p=null, src='種子庫';
      if(useAI && aiCfg.key){
        try{ p=await aiGenPlan(band); src='AI'; }
        catch(e){ planErr.value='AI 生成失敗，已自動改用種子庫規則生成。原因：'+e.message; }
      } else if(useAI){
        planErr.value='尚未設定 AI（按「AI 設定」填入 API Key），已改用種子庫生成。';
      }
      if(!p) p=rulePlan(band);
      const nGames=p.goals.reduce((n,g)=>n+g.games.length,0);
      plan.value={no:nextSessionNo.value, date:planDate.value||new Date().toISOString().slice(0,10),
        curIdx:0,
        versions:[{label:'V1 · '+src+' 生成', goals:p.goals}],
        chat:[{role:'assistant', text:`已生成初始方案：${p.goals.length} 個訓練目標、${nGames} 個遊戲。\n可在左側勾選／編輯，或在右側輸入指示讓我修改（例如「第二個目標太難，換簡單的遊戲」）。`}]};
      openGoals.value=p.goals.map((_,i)=>String(i));
      finalPlan.value=null;
      genLoading.value=false; clearInterval(tick);
    }
    function curVer(){ return plan.value ? plan.value.versions[plan.value.curIdx] : null; }
    function newVersion(label){
      const v=JSON.parse(JSON.stringify(curVer()));
      const n=plan.value.versions.length;
      v.label='V'+(n+1)+' · '+label;
      plan.value.versions.push(v);
      plan.value.curIdx=n;
    }
    function addGoal(){ curVer().goals.push({text:'', games:[]}); openGoals.value.push(String(curVer().goals.length-1)); }
    function delGoal(gi){ curVer().goals.splice(gi,1); }
    function addGame(gi){ curVer().goals[gi].games.push({name:'',domain:'rec',target:'',desc:'',checked:true}); }
    function finalize(){
      const v=curVer(); if(!v) return;
      const goals=v.goals.map(g=>({text:g.text||'(未填寫)', games:g.games.filter(x=>x.checked)}));
      finalPlan.value={no:nextSessionNo.value, date:planDate.value||new Date().toISOString().slice(0,10), goals};
      ElementPlus.ElMessage.success('已生成最終方案，可儲存為課程記錄');
    }
    const chatInput=ref(''); const chatBoxEl=ref(null); const chatLoading=ref(false);
    async function sendChat(){
      const t=chatInput.value.trim();
      if(!t||!plan.value) return;
      plan.value.chat.push({role:'user', text:t});
      chatInput.value=''; chatLoading.value=true;
      await new Promise(r=>setTimeout(r,50));
      try{
        if(aiCfg.key){
          const cur=curVer();
          const prompt=`你是資深兒童言語治療師。以下是目前干預方案 JSON：\n${JSON.stringify({goals:cur.goals.map(g=>({text:g.text, games:g.games.map(x=>({name:x.name,domain:x.domain,target:x.target,desc:x.desc}))}))})}\n\n可用種子庫遊戲：${JSON.stringify(seeds.map(s=>({name:s.name,domain:DOM_NAME[s.domain],ages:s.amin+'-'+s.amax+'歲',goal:s.goal})))}\n\n治療師指示：${t}\n\n規則：只修改指示涉及的部分，其餘保留原樣；遊戲可從種子庫選取或改編；全部繁體中文。\n只輸出 JSON（無 markdown 代碼框）：{"goals":[{"text":"","games":[{"name":"","domain":"rec|exp|nar|pra|oral","target":"","desc":""}]}],"reply":"簡短說明做了什麼修改"}`;
          const j=parsePlanJSON(await callLLM(prompt, 4000));
          newVersion('修改：'+t.slice(0,10));
          const v=curVer();
          v.goals=(j.goals||[]).map(g=>({text:g.text||'', games:(g.games||[]).map(gm=>({name:gm.name||'',domain:domKeyOf(gm.domain),target:gm.target||'',desc:gm.desc||'',checked:true}))}));
          plan.value.chat.push({role:'assistant', text:j.reply||'已按指示更新方案（產生新版本，可於左上切換回舊版）'});
        } else {
          const v=curVer();
          if(/(加|增|多).{0,6}(遊戲|活動)/.test(t)){
            const used=new Set(v.goals.flatMap(g=>g.games.map(x=>x.name)));
            let added=0;
            for(const s of seeds){ if(added>=2) break;
              if(!used.has(s.name)){ (v.goals[0]?.games||v.goals[0].games).push({name:s.name,domain:s.domain,target:s.goal,desc:s.desc,checked:true}); added++; } }
            plan.value.chat.push({role:'assistant', text:added?`已從種子庫加入 ${added} 個遊戲到目標 1。`:'種子庫遊戲已全部使用。'});
          } else {
            plan.value.chat.push({role:'assistant', text:'尚未設定 AI 金鑰，目前只支援「加入遊戲」類簡單指令；完整對話修改請於 AI 設定填入金鑰。'});
          }
        }
      }catch(e){
        plan.value.chat.push({role:'assistant', text:'⚠️ 修改失敗：'+e.message+'（目前版本保持不變，可切換版本查看）'});
      }
      chatLoading.value=false;
      await nextTick();
      if(chatBoxEl.value) chatBoxEl.value.scrollTop = chatBoxEl.value.scrollHeight;
    }

    async function saveSession(){
      const v=curVer(); if(!plan.value||!curChild.value||!v) return;
      const goals=v.goals.map(g=>({text:g.text, games:g.games.filter(x=>x.checked)}));
      curChild.value.sessions.push({
        id:Date.now(), no:plan.value.no, date:plan.value.date,
        goals:goals.map(g=>g.text),
        games:goals.flatMap(g=>g.games.map(gm=>({...gm}))),
        homeTip:plan.value.homeTip||'', effect:{level:'待評', note:''}
      });
      if(await saveCurChild()) ElementPlus.ElMessage.success('已儲存為第 '+plan.value.no+' 次課程記錄');
    }
    function delSession(id){
      const c=curChild.value; if(!c) return;
      const i=c.sessions.findIndex(s=>s.id===id); if(i>-1){ c.sessions.splice(i,1); saveCurChild(); }
    }
    function saveAiCfg(){
      api.putAi(JSON.parse(JSON.stringify(aiCfg)))
        .then(()=>ElementPlus.ElMessage.success('AI 設定已儲存'))
        .catch(e=>ElementPlus.ElMessage.error('儲存失敗：'+e.message));
    }

    function genReport(){
      const m=months();
      repWarn.value = !f.dob ? '⚠️ 尚未填寫出生日期，報告中的實際年齡將顯示「—」。' : '';
      const am=m===null?0:m;
      const band=TYP[bandKey(am)];
      const bandIdx=m===null?null:Math.min(6,Math.floor(m/12));
      const ageL=ageLabel.value;
      const name=f.name.trim()||'學生';
      const stats=['rec','exp','nar','pra'].map(d=>({dom:DOMS[d],st:collect(d)}));
      const oral=collect('oral');
      const abn=[...oralRows.flatMap(r=>r.obs),...dailyObs].filter(o=>o.s===1).map(o=>'異常：'+o.t);
      const foods=foodObs.filter(o=>o.s===1).map(o=>o.t);

      const obs=[['一般觀察／行為表現',f.obs1],['言語特徵／發音情況',f.obs2],['主要關注／建議',f.obs3]]
        .map(([l,v])=>`<div class="rep-blk"><b>${l}：</b><span class="rev" contenteditable="true" data-ph="未有填寫，點此輸入">${v?esc(v):''}</span></div>`).join('');
      const dxLine=(f.dx||'未有選擇診斷')+(f.sev?'（'+f.sev+'）':'');

      const gapRows=stats.map(({dom,st})=>
        `<tr><td style="white-space:nowrap"><b>${dom.name}</b></td><td>${band[dom.typ]}</td><td>${narrative(dom,st,bandIdx)}</td></tr>`).join('');
      const oralCell=
        ra('ok','本次可完成',oral.done.length?esc(top3(oral.done)):'—')+
        ra('hint','提示下完成',oral.part.length?esc(top3(oral.part)):'—')+
        ra('need','未能完成',oral.none.length?esc(top3(oral.none)):'—')+
        ra('none','口肌觀察',abn.length?esc(top3(abn)):'各部位未見異常')+
        (f.oralNote?ra('none','補充',esc(f.oralNote)):'')+
        ra('none','攝取質地',(foods.length?esc(foods.join('、')):'—')+(f.foodNote?'（'+esc(f.foodNote)+'）':''));
      const oralRow=`<tr><td style="white-space:nowrap"><b>口肌能力</b></td><td>口肌動作及進食表現按年齡逐步發展。</td><td>${oralCell}</td></tr>`;

      const targets=[];
      stats.forEach(({dom,st})=>st.part.slice(0,2).forEach(t=>targets.push(`提升${dom.name}：能在少許提示下完成「${esc(t)}」`)));
      stats.forEach(({dom,st})=>st.none.slice(0,1).forEach(t=>targets.push(`鞏固${dom.name}：認識及穩定表現「${esc(t)}」`)));
      const goalHtml=targets.length?targets.slice(0,6).map((t,i)=>`${i+1}. ${t}`).join('<br>'):'按評估結果訂立個別化訓練目標（請治療師補充）。';

      const homeHtml=esc(HOME_BASE)+'<br><br>'+['rec','exp','nar','pra'].map(d=>'・'+DOMS[d].name+'：'+esc(DOMS[d].home)).join('<br>');

      repHtml.value=`
        ${f.org?`<div class="rep-org">${esc(f.org)}</div>`:''}
        <div class="rep-title">評 估 報 告</div>
        <div class="rep-meta">
          <span><b>兒童姓名</b>${esc(name)}</span><span><b>性別</b>${f.sex||'—'}</span>
          <span><b>出生日期</b>${f.dob||'—'}</span><span><b>評估日期</b>${f.adate||'—'}</span>
          <span><b>評估時實際年齡</b>${ageL}</span><span><b>評估治療師</b>${esc(f.therapist.trim()||'未有填寫')}</span>
        </div>
        <div class="rep-intro" contenteditable="true">${esc(`${name} 於 ${f.adate||'上述日期'} 到本中心接受言語治療評估服務。是次評估以廣東話進行，採用非標準化評估方式；評估當日實際年齡為 ${ageL}。截至評估當天，${name} 的口語能力結果如下：`)}</div>
        <div class="rep-h">一、臨床觀察、演繹與診斷</div>
        ${obs}<div class="rep-blk"><b>診斷：</b><span class="rev" contenteditable="true" data-ph="未有選擇診斷，點此輸入">${f.dx?esc(dxLine):''}</span></div>
        <div class="rep-h">二、發展與年齡差距分析表（同齡參考：${band.age}）</div>
        <table><tr><th style="width:100px">能力範疇</th><th style="width:27%">同齡典型發展兒童表現</th><th>發展落差分析</th></tr>${gapRows}${oralRow}</table>
        <div class="rep-h">三、言語治療訓練目標</div>
        <div contenteditable="true" class="rep-blk">${goalHtml}</div>
        <div class="rep-h">四、家居建議</div>
        <div contenteditable="true" class="rep-blk">${homeHtml}</div>
        <div class="rep-sign">
          <div class="sig"><div class="lab">評估治療師</div><div class="val">${f.signImg?`<img src="${f.signImg}" style="height:56px;object-fit:contain"/>`:esc(f.therapist.trim()||'　')}</div></div>
          <div class="sig"><div class="lab">簽署日期</div><div class="val" contenteditable="true">${f.signDate||'　'}</div></div>
        </div>`;
    }

    function buildDoc(){
      if(!repHtml.value) genReport();
      return `<!DOCTYPE html><html lang="zh-HK"><head><meta charset="utf-8"><title>評估報告</title><style>
        ${reportCss}        body{background:#fff}        .rev:empty::before{content:attr(data-ph);color:#c0c4cc}
  .rep-sign{display:flex;justify-content:flex-end;gap:60px;margin-top:34px;padding:0 20px}
        .rep-sign .sig{min-width:200px}
        .rep-sign .lab{font-size:12px;color:#8a94a3;letter-spacing:2px;margin-bottom:30px}
        .rep-sign .val{border-bottom:1.5px solid #7d8ba1;padding:0 12px 5px;min-height:30px;font-weight:600;letter-spacing:1px}
        @page{margin:1.5cm}
      </style></head><body><div id="repDoc">${repHtml.value.replace(/ contenteditable="true"/g,'')}</div></body></html>`;
    }

    async function downloadReport(){
      if(!repHtml.value) genReport();
      ElementPlus.ElMessage.info('正在生成 PDF，請稍候…');
      const holder = document.createElement('div');
      holder.style.cssText = 'position:fixed;left:-10000px;top:0;width:794px;background:#fff;font-family:-apple-system,"PingFang TC","Microsoft JhengHei",sans-serif';
      holder.innerHTML = repHtml.value.replace(/ contenteditable="true"/g,'');
      holder.querySelectorAll('.rev').forEach(e=>{ if(!e.textContent.trim()) e.textContent='—'; });
      document.body.appendChild(holder);
      try{
        await html2pdf().set({
          margin:[10,9],
          filename:`評估報告_${f.name.trim()||'兒童'}_${f.adate||''}.pdf`,
          image:{type:'jpeg',quality:0.96},
          html2canvas:{scale:2,useCORS:true,backgroundColor:'#ffffff'},
          jsPDF:{unit:'mm',format:'a4',orientation:'portrait'},
          pagebreak:{mode:['css','legacy']}
        }).from(holder).save();
        ElementPlus.ElMessage.success('PDF 已下載');
      }catch(err){
        ElementPlus.ElMessage.error('PDF 生成失敗：'+err.message);
      }
      holder.remove();
    }

    function printReport(){
      const w = window.open('', '_blank');
      if(!w){ElementPlus.ElMessage.error('瀏覽器阻擋了彈出視窗，請允許後重試');return;}
      w.document.write(buildDoc());
      w.document.close(); w.focus();   // 只開預覽，列印由使用者操作
    }

    // ── 存量 localStorage 一次性導入（設計 §6，防舊檔案因切庫丟失）──
    async function importLegacy(){
      const read=k=>{ try{ return JSON.parse(localStorage.getItem(k)); }catch(e){ return null; } };
      const kids=read('plas_children')||[], oldSeeds=read('plas_seeds')||[], oldAi=read('plas_ai');
      if(!kids.length && !oldSeeds.length) return;
      try{ await api.listChildren(); }catch(e){ return; }   // 後端未就緒：下次載入再提示
      try{
        await ElementPlus.ElMessageBox.confirm(
          '檢測到此瀏覽器存有舊版（單檔 HTML）的本地數據：'+kids.length+' 份兒童檔案、'+oldSeeds.length+' 項種子庫。是否導入伺服器？導入成功後將清除本機舊數據。',
          '舊數據遷移', {type:'info', confirmButtonText:'導入', cancelButtonText:'跳過'});
      }catch(e){ return; }
      for(const c of kids){ try{ await api.addChild(c); }catch(e){ console.warn('導入兒童檔案失敗：', c.name, e.message); } }
      if(oldSeeds.length){ try{ await api.putSeeds(oldSeeds); }catch(e){ console.warn('導入種子庫失敗：', e.message); } }
      if(oldAi){ try{ await api.putAi(oldAi); }catch(e){ console.warn('導入 AI 設定失敗：', e.message); } }
      ['plas_children','plas_seeds','plas_ai'].forEach(k=>localStorage.removeItem(k));
      ElementPlus.ElMessage.success('舊版本地數據已導入伺服器');
    }
    (async function init(){
      await importLegacy();
      try{
        let ss=await api.getSeeds();
        if(!ss || !ss.length){ ss=DEFAULT_SEEDS.map(s=>({...s})); api.putSeeds(ss.map(s=>({...s}))).catch(()=>{}); }
        seeds.splice(0, seeds.length, ...ss);
        const ai=await api.getAi(); if(ai) Object.assign(aiCfg, ai);
        await refreshChildren();
      }catch(e){ console.warn('後端未就緒：', e.message); }
    })();
</script>
