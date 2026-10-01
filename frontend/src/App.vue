<template>
  <el-container class="app-shell">

    <!-- ═══════ 登入／註冊 ═══════ -->
    <div class="login-mask no-print" v-if="!me">
      <div class="login-card">
        <div class="login-logo">ST</div>
        <b style="font-size:17px">言語治療工作平台</b>
        <div class="note" style="margin:0 0 4px">學前兒童口語評估量表（0–6 歲）</div>
        <template v-if="loginState==='setup'">
          <el-form label-width="70px" @submit.prevent style="width:100%;margin-top:10px">
            <el-alert type="info" :closable="false" style="margin-bottom:12px;line-height:1.7"
              title="首次使用：請創建管理員帳號（帳號資訊僅保存在本平台，無任何預設密碼）"></el-alert>
            <el-form-item label="帳號"><el-input v-model="setupForm.username"></el-input></el-form-item>
            <el-form-item label="姓名"><el-input v-model="setupForm.display_name" placeholder="治療師姓名"></el-input></el-form-item>
            <el-form-item label="密碼"><el-input v-model="setupForm.password" type="password" show-password placeholder="至少 6 位"></el-input></el-form-item>
            <el-form-item label="確認"><el-input v-model="setupForm.password2" type="password" show-password @keyup.enter="doSetup"></el-input></el-form-item>
            <el-button type="primary" style="width:100%" :loading="loginBusy" @click="doSetup">初始化並登入</el-button>
          </el-form>
        </template>
        <template v-else>
          <div v-if="loginState==='checking'" style="width:100%;padding:30px 0;color:var(--el-text-color-secondary)">載入中…</div>
          <el-tabs v-model="loginTab" stretch v-else>
          <el-tab-pane label="登錄" name="in">
            <el-form label-width="70px" @submit.prevent>
              <el-form-item label="帳號"><el-input v-model="loginForm.username" placeholder="帳號" @keyup.enter="doLogin"></el-input></el-form-item>
              <el-form-item label="密碼"><el-input v-model="loginForm.password" type="password" show-password placeholder="密碼" @keyup.enter="doLogin"></el-input></el-form-item>
              <el-button type="primary" style="width:100%" :loading="loginBusy" @click="doLogin">登錄</el-button>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="註冊" name="up">
            <el-form label-width="70px" @submit.prevent>
              <el-form-item label="帳號"><el-input v-model="regForm.username"></el-input></el-form-item>
              <el-form-item label="姓名"><el-input v-model="regForm.display_name" placeholder="治療師姓名"></el-input></el-form-item>
              <el-form-item label="密碼"><el-input v-model="regForm.password" type="password" show-password placeholder="至少 6 位"></el-input></el-form-item>
              <el-form-item label="確認"><el-input v-model="regForm.password2" type="password" show-password @keyup.enter="doRegister"></el-input></el-form-item>
              <el-button type="primary" style="width:100%" :loading="loginBusy" @click="doRegister">註冊並登入</el-button>
            </el-form>
          </el-tab-pane>
        </el-tabs>
        </template>
      </div>
    </div>

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
      <div class="me" v-if="me">
        <div class="avatar">{{ (me.display_name||me.username||'?').slice(0,1) }}</div>
        <div style="flex:1;min-width:0"><b>{{ me.display_name||me.username }}</b><span>{{ me.role==='admin'?'管理員':'言語治療師' }}</span></div>
        <el-button link size="small" style="color:#9fb0c9" @click="doLogout">退出</el-button>
      </div>
      <div class="me" v-else>
        <div class="avatar">?</div>
        <div><b>未登入</b><span>請先登入</span></div>
      </div>
    </aside>

    <el-container class="main-col">
      <!-- ═══════ 頂欄 ═══════ -->
      <el-header class="topbar no-print" height="auto">
        <span class="crumb">首頁 / <b>{{ pageTitles[curPage] }}</b></span>
        <span class="sp"></span>
      </el-header>

      <el-main class="content">

        <!-- ═══════ 1. 兒童檔案 ═══════ -->
        <section v-show="curPage==='children'">

          <!-- 列表 -->
          <el-card v-if="!detailOpen" shadow="never" class="no-print">
            <template #header><b>兒童檔案</b><span class="sub-hint">點擊行查看/編輯詳情；「載入」選為當前兒童（自動載入已存檔評估）</span></template>
            <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:12px">
              <el-button type="primary" @click="ncDlg=true">＋ 新增兒童</el-button>
              <el-popconfirm title="確定刪除此檔案及全部課程記錄？" @confirm="delChild">
                <template #reference><el-button type="danger" plain :disabled="!curChild">刪除當前檔案</el-button></template>
              </el-popconfirm>
            </div>
            <el-table :data="children" size="small" border highlight-current-row @row-click="openDetail">
              <el-table-column label="姓名" min-width="140">
                <template #default="{row}"><b>{{ row.name }}</b><el-tag v-if="curChildId===row.id" size="small" effect="plain" style="margin-left:8px">目前</el-tag></template>
              </el-table-column>
              <el-table-column prop="sex" label="性別" width="60" align="center"></el-table-column>
              <el-table-column prop="dob" label="出生日期" width="110"></el-table-column>
              <el-table-column label="監護人 / 電話" min-width="150">
                <template #default="{row}">{{ [row.guardian,row.phone].filter(Boolean).join(' · ') || '—' }}</template>
              </el-table-column>
              <el-table-column prop="org" label="機構" min-width="120"></el-table-column>
              <el-table-column prop="updated_at" label="最近更新" width="170"></el-table-column>
              <el-table-column label="" width="130" align="center">
                <template #default="{row}"><el-button link type="primary" size="small" @click.stop="openDetail(row)">詳情</el-button><el-button link type="primary" size="small" @click.stop="curChildId=row.id">載入</el-button></template>
              </el-table-column>
            </el-table>
            <el-empty v-if="!children.length" description="尚無兒童檔案 — 按「＋ 新增兒童」建立第一份檔案" :image-size="80"></el-empty>
          </el-card>

          <!-- 詳情 -->
          <el-card v-else shadow="never">
            <template #header>
              <div style="display:flex;align-items:center;gap:12px">
                <el-button size="small" @click="detailOpen=false">← 返回列表</el-button>
                <b style="font-size:16px">{{ pf.name || '兒童詳情' }}</b>
                <el-tag v-if="curChild" size="small" effect="plain">評估記錄 {{ assessList.length }} 條</el-tag>
                <el-tag v-if="curChild" size="small" effect="plain" type="info">課程 {{ curChild.sessions?.length||0 }} 次</el-tag>
              </div>
            </template>
            <el-form label-width="100px" style="max-width:720px" v-if="curChild">
              <el-divider content-position="left">基本資料</el-divider>
              <el-row :gutter="16">
                <el-col :span="12"><el-form-item label="姓名"><el-input v-model="pf.name"></el-input></el-form-item></el-col>
                <el-col :span="12"><el-form-item label="性別">
                  <el-radio-group v-model="pf.sex"><el-radio-button value="男">男</el-radio-button><el-radio-button value="女">女</el-radio-button></el-radio-group>
                </el-form-item></el-col>
                <el-col :span="12"><el-form-item label="出生日期"><el-date-picker v-model="pf.dob" type="date" value-format="YYYY-MM-DD" style="width:100%"></el-date-picker></el-form-item></el-col>
                <el-col :span="12"><el-form-item label="機構"><el-input v-model="pf.org"></el-input></el-form-item></el-col>
                <el-col :span="12"><el-form-item label="就讀學校/班級"><el-input v-model="pf.school"></el-input></el-form-item></el-col>
                <el-col :span="12"><el-form-item label="家庭語言"><el-input v-model="pf.lang" placeholder="如：廣東話／普通話／雙語"></el-input></el-form-item></el-col>
              </el-row>
              <el-divider content-position="left">監護人聯絡</el-divider>
              <el-row :gutter="16">
                <el-col :span="12"><el-form-item label="監護人姓名"><el-input v-model="pf.guardian"></el-input></el-form-item></el-col>
                <el-col :span="12"><el-form-item label="關係">
                  <el-select v-model="pf.relation" style="width:100%" placeholder="選擇或輸入" filterable allow-create default-first-option>
                    <el-option v-for="r in ['父親','母親','祖父母','外傭','其他']" :key="r" :label="r" :value="r"></el-option>
                  </el-select>
                </el-form-item></el-col>
                <el-col :span="12"><el-form-item label="聯絡電話"><el-input v-model="pf.phone"></el-input></el-form-item></el-col>
                <el-col :span="12"><el-form-item label="電郵"><el-input v-model="pf.email"></el-input></el-form-item></el-col>
              </el-row>
              <el-divider content-position="left">其他</el-divider>
              <el-form-item label="轉介來源">
                <el-select v-model="pf.referral" style="max-width:300px" placeholder="選擇或輸入" filterable allow-create default-first-option>
                  <el-option v-for="r in ['自行報名','學校轉介','醫生轉介','機構轉介','其他']" :key="r" :label="r" :value="r"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="備註"><el-input v-model="pf.notes" type="textarea" :rows="3" placeholder="醫療史、相關診斷、注意事項…"></el-input></el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveProfile">儲存檔案</el-button>
              </el-form-item>
            </el-form>
            <el-empty v-else description="檔案載入中…"></el-empty>
          </el-card>
        </section>

        <!-- ═══════ 2. 評估 ═══════ -->
        <section v-show="curPage==='assess'" :class="{'assess-view':assessView}">

          <!-- 兒童/評估記錄欄：量表評估與評估報告共用，選兒童後默認載入最新一條 -->
          <div class="assess-bar no-print">
            <span style="font-weight:600">當前兒童</span>
            <el-select v-model="curChildId" placeholder="選擇兒童檔案" style="width:200px" clearable filterable>
              <el-option v-for="c in children" :key="c.id" :label="c.name" :value="c.id"></el-option>
            </el-select>
            <template v-if="curChild">
              <span class="note" style="margin:0">{{ curChild.sex||'—' }}・{{ curChild.dob||'—' }}・{{ ageLabel }}</span>
              <el-divider direction="vertical"></el-divider>
              <span style="font-weight:600">評估記錄</span>
              <el-select v-model="curAssessId" placeholder="選擇評估記錄" style="width:300px"
                         :disabled="!assessView || !assessList.length" @change="onPickAssess">
                <el-option v-for="a in assessList" :key="a.id" :label="assessLabel(a)" :value="a.id"></el-option>
              </el-select>
              <template v-if="assessView">
                <el-button :disabled="!curAssessId" @click="startEdit">編輯</el-button>
                <el-button type="primary" @click="startNew">{{ assessList.length ? '重新評估' : '立即評估' }}</el-button>
              </template>
              <el-tag v-else :type="assessMode==='new'?'success':'warning'" effect="dark">
                {{ assessMode==='new'?'撰寫新評估':'編輯現有評估' }}
              </el-tag>
              <span v-if="assessView && !assessList.length" class="note" style="margin:0">該兒童尚無評估記錄，量表為空白唯讀</span>
            </template>
            <span v-else class="note" style="margin:0">請先選擇兒童檔案（或到「兒童檔案」頁新增）</span>
          </div>

          <el-tabs v-model="assessTab">
            <el-tab-pane label="量表評估" name="scale">

    <!-- ═══════ 兒童資料（需先有兒童檔案）═══ -->
    <el-header class="metabar" height="auto" v-if="curChild">
      <el-form :inline="true" class="meta-form" size="default">
        <el-form-item label="機構"><el-input v-model="f.org" placeholder="機構名稱" style="width:170px" :disabled="assessView"></el-input></el-form-item>
        <el-form-item label="姓名"><el-input v-model="f.name" placeholder="兒童姓名" style="width:120px" :disabled="assessView"></el-input></el-form-item>
        <el-form-item label="出生日期"><el-date-picker v-model="f.dob" type="date" value-format="YYYY-MM-DD" placeholder="選擇日期" style="width:150px" :disabled="assessView" @change="onDob"></el-date-picker></el-form-item>
        <el-form-item label="年齡"><el-tag :type="f.dob?'primary':'info'" :effect="f.dob?'dark':'plain'" size="large" style="font-weight:700">{{ ageLabel }}</el-tag></el-form-item>
        <el-form-item label="性別">
          <el-radio-group v-model="f.sex" :disabled="assessView">
            <el-radio-button value="男">男</el-radio-button>
            <el-radio-button value="女">女</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="評估日期"><el-date-picker v-model="f.adate" type="date" value-format="YYYY-MM-DD" style="width:150px" :disabled="assessView"></el-date-picker></el-form-item>
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
            <el-input v-model="f.obs1" type="textarea" :rows="3" :disabled="assessView" placeholder="記錄兒童的一般行為、注意力、配合度、社交互動等臨床觀察…"></el-input>
            <div class="grp-h">言語特徵 / 發音情況</div>
            <el-input v-model="f.obs2" type="textarea" :rows="3" :disabled="assessView" placeholder="記錄兒童的發音清晰度、音韻過程、語速、語調、聲音品質等特徵…"></el-input>
            <div class="grp-h">主要關注 / 建議</div>
            <el-input v-model="f.obs3" type="textarea" :rows="3" :disabled="assessView" placeholder="記錄治療師的主要關注點、初步印象、後續建議或轉介意見…"></el-input>
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
                <el-input v-model="f.oralNote" placeholder="請補充…" style="width:230px" size="small" :disabled="assessView"></el-input>
              </div>
              <div class="items" style="margin-top:8px">
                <span class="note" style="margin-right:4px">進食食物種類／質地（有攝取請點選）：</span>
                <el-tag v-for="o in foodObs" :key="o.t" class="st" size="large" effect="plain" :type="o.s===1?'primary':'info'" @click.capture="toggleObs(o)">{{ (o.s===1?'✓ ':'○ ') + o.t }}</el-tag>
                <el-input v-model="f.foodNote" placeholder="請補充…" style="width:230px" size="small" :disabled="assessView"></el-input>
              </div>
              <el-divider></el-divider>
              <el-collapse>
                <el-collapse-item title="Speech Stimulability Test（HKCAT 後進行，只測未能正確發出的音）" name="stim">
                  <p class="note">跟住落嚟我哋會做一個測試，你重複我講嘅嘢……（Miccio, 2002）</p>
                  <el-table :data="stim" size="small" border>
                    <el-table-column prop="s" label="聲母" width="70" align="center"></el-table-column>
                    <el-table-column v-for="(v,i) in ['_a','_e','_i','_o','_u','隔離']" :key="v" :label="v" width="60" align="center">
                      <template #default="{row}"><el-checkbox v-model="row.c[i]" :disabled="assessView"></el-checkbox></template>
                    </el-table-column>
                    <el-table-column prop="wi" label="詞首 WI"></el-table-column>
                    <el-table-column prop="wf" label="詞尾 WF"></el-table-column>
                    <el-table-column label="% correct" width="100"><template #default="{row}"><el-input v-model="row.pct" size="small" :disabled="assessView"></el-input></template></el-table-column>
                  </el-table>
                </el-collapse-item>
              </el-collapse>
            </template>
          </el-card>
        </template>

        <!-- ═══════ 診斷 ═══════ -->
          <el-card shadow="never">
            <template #header><b>診斷 (Diagnosis)</b><span style="color:var(--el-text-color-secondary);font-size:13px;margin-left:12px">選擇診斷類別及嚴重程度</span></template>
            <el-select v-model="f.dx" placeholder="選擇診斷類別" style="width:100%;max-width:560px" size="large" clearable :disabled="assessView">
              <el-option v-for="d in dxs" :key="d.k" :label="d.k + ') ' + d.label" :value="d.label"></el-option>
            </el-select>
            <el-alert v-if="dxNote" :title="dxNote" type="info" :closable="false" style="margin:12px 0;line-height:1.8"></el-alert>
            <div style="display:flex;align-items:center;gap:12px;margin:14px 0">
              <span style="font-weight:600">嚴重程度：</span>
              <el-radio-group v-model="f.sev" :disabled="assessView">
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
              <el-form-item label="治療師姓名"><el-input v-model="f.therapist" :disabled="assessView"></el-input></el-form-item>
              <el-form-item label="專業資格 / 執照"><el-input v-model="f.license" :disabled="assessView"></el-input></el-form-item>
              <el-form-item label="簽署日期"><el-date-picker v-model="f.signDate" type="date" value-format="YYYY-MM-DD" style="width:100%" :disabled="assessView"></el-date-picker></el-form-item>
              <el-form-item label="簽名 / 簽署"><el-input v-model="f.signature" :disabled="assessView"></el-input></el-form-item>
              <el-form-item label="手寫簽名">
                <el-upload :auto-upload="false" :show-file-list="false" accept="image/*" :on-change="onSignFile" :disabled="assessView">
                  <el-button size="small" :disabled="assessView">匯入手寫簽名圖片</el-button>
                </el-upload>
                <img v-if="f.signImg" :src="f.signImg" style="height:46px;margin-left:12px;border:1px dashed var(--el-border-color);border-radius:6px;padding:4px;background:#fff"/>
                <el-button v-if="f.signImg && !assessView" link type="danger" size="small" @click="f.signImg=''">移除</el-button>
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

          <!-- 新評估/編輯：右下角懸浮 取消/提交 -->
          <div class="assess-float no-print" v-if="!assessView">
            <el-button @click="cancelAssess">取消</el-button>
            <el-button type="primary" @click="submitAssess">提交評估</el-button>
          </div>
        </section>
        <section v-show="curPage==='interv'">
          <div class="assess-bar">
            <span style="font-weight:600">當前兒童</span>
            <el-select v-model="curChildId" placeholder="選擇兒童檔案" style="width:200px" clearable filterable>
              <el-option v-for="c in children" :key="c.id" :label="c.name" :value="c.id"></el-option>
            </el-select>
            <template v-if="curChild">
              <span class="note" style="margin:0">{{ curChild.sex||'—' }}・{{ curChild.dob||'—' }}・{{ ageLabel }}｜已存 {{ curChild.sessions?.length||0 }} 次課程</span>
              <el-divider direction="vertical"></el-divider>
              <span style="font-weight:600">關聯評估</span>
              <el-select v-model="intervAssessId" placeholder="無評估記錄" style="width:280px" :disabled="!assessList.length">
                <el-option v-for="a in assessList" :key="a.id" :label="assessLabel(a)" :value="a.id"></el-option>
              </el-select>
            </template>
            <span v-else class="note" style="margin:0">請先選擇兒童檔案，生成方案與課程記錄需依評估結果</span>
          </div>
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
    <el-table-column label="關聯評估" width="120">
      <template #default="{row}"><span class="note">{{ assessById(row.assessId)?.adate || '—' }}</span></template>
    </el-table-column>
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
    <el-table-column label="" width="150" align="center">
      <template #default="{row}">
        <el-button link type="primary" size="small" @click="openSess(row)">回溯</el-button>
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
          <el-card shadow="never" v-if="me && me.role==='admin'">
            <template #header>
              <b>数据管理</b><span class="sub-hint">全量备份（用户/档案/评估/课程/种子库/AI 设定），JSON 文件跨设备恢复</span>
            </template>
            <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
              <el-button type="primary" :loading="exporting" @click="exportData">导出备份（JSON）</el-button>
              <el-upload :auto-upload="false" :show-file-list="false" accept=".json" :on-change="onImportFile">
                <el-button>导入备份（覆盖现有数据）</el-button>
              </el-upload>
              <span class="note" style="margin:0">备份含全部用户与密码材料，请妥善保管；导入会覆盖现有全部数据，完成后需重新登录。</span>
            </div>
          </el-card>
          <el-card shadow="never" v-if="me && me.role==='admin'">
            <template #header>
              <b>用戶管理</b><span class="sub-hint">不同用戶的兒童檔案、評估與干預數據相互隔離；種子庫為平台共享</span>
              <el-button size="small" type="primary" style="float:right" @click="usersDlg=true">＋ 新增用戶</el-button>
            </template>
            <el-table :data="users" size="small" border>
              <el-table-column label="用戶" min-width="130">
                <template #default="{row}"><b>{{ row.display_name||row.username }}</b><el-tag v-if="me && row.username===me.username" size="small" effect="plain" style="margin-left:6px">我</el-tag></template>
              </el-table-column>
              <el-table-column prop="username" label="帳號" width="110"></el-table-column>
              <el-table-column label="角色" width="110">
                <template #default="{row}"><el-tag :type="row.role==='admin'?'danger':'primary'" size="small" effect="plain">{{ row.role==='admin'?'管理員':'言語治療師' }}</el-tag></template>
              </el-table-column>
              <el-table-column label="狀態" width="80">
                <template #default="{row}"><el-tag :type="row.disabled?'info':'success'" size="small" effect="plain">{{ row.disabled?'停用':'啟用' }}</el-tag></template>
              </el-table-column>
              <el-table-column prop="created_at" label="建立時間" width="170"></el-table-column>
              <el-table-column label="操作" width="240" align="center">
                <template #default="{row}">
                  <el-button link type="primary" size="small" @click="resetPw(row)">重置密碼</el-button>
                  <el-button link size="small" :type="row.disabled?'success':'warning'" :disabled="me && row.username===me.username" @click="toggleU(row)">{{ row.disabled?'啟用':'停用' }}</el-button>
                  <el-popconfirm title="刪除該用戶並清除其全部數據？" width="240" @confirm="delU(row)">
                    <template #reference><el-button link type="danger" size="small" :disabled="me && row.username===me.username">刪除</el-button></template>
                  </el-popconfirm>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
          <el-card shadow="never">
            <template #header><b>AI 設定</b><span class="sub-hint">干預方案 AI 生成與對話修改所用的 LLM 連線</span></template>
            <p class="note" style="margin-top:0">API 金鑰儲存於後端伺服器，不存於瀏覽器；未設定時仍可用「依種子庫生成」方案。</p>
            <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
              <el-button type="primary" @click="aiDlg=true">開啟 AI 設定</el-button>
              <span class="note" style="margin:0">干預方案 AI 生成與對話修改均使用此連線</span>
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
<el-dialog v-model="ncDlg" title="新增兒童檔案" width="600px">
  <el-form label-width="100px">
    <el-divider content-position="left" style="margin:0 0 14px">基本資料</el-divider>
    <el-row :gutter="16">
      <el-col :span="12"><el-form-item label="姓名" required><el-input v-model="nc.name"></el-input></el-form-item></el-col>
      <el-col :span="12"><el-form-item label="性別">
        <el-radio-group v-model="nc.sex"><el-radio-button value="男">男</el-radio-button><el-radio-button value="女">女</el-radio-button></el-radio-group>
      </el-form-item></el-col>
      <el-col :span="12"><el-form-item label="出生日期"><el-date-picker v-model="nc.dob" type="date" value-format="YYYY-MM-DD" style="width:100%"></el-date-picker></el-form-item></el-col>
      <el-col :span="12"><el-form-item label="機構"><el-input v-model="nc.org"></el-input></el-form-item></el-col>
      <el-col :span="12"><el-form-item label="就讀學校/班級"><el-input v-model="nc.school"></el-input></el-form-item></el-col>
      <el-col :span="12"><el-form-item label="家庭語言"><el-input v-model="nc.lang" placeholder="如：廣東話／普通話／雙語"></el-input></el-form-item></el-col>
    </el-row>
    <el-divider content-position="left" style="margin:0 0 14px">監護人聯絡</el-divider>
    <el-row :gutter="16">
      <el-col :span="12"><el-form-item label="監護人姓名"><el-input v-model="nc.guardian"></el-input></el-form-item></el-col>
      <el-col :span="12"><el-form-item label="關係">
        <el-select v-model="nc.relation" style="width:100%" placeholder="選擇或輸入" filterable allow-create default-first-option>
          <el-option v-for="r in ['父親','母親','祖父母','外傭','其他']" :key="r" :label="r" :value="r"></el-option>
        </el-select>
      </el-form-item></el-col>
      <el-col :span="12"><el-form-item label="聯絡電話"><el-input v-model="nc.phone"></el-input></el-form-item></el-col>
      <el-col :span="12"><el-form-item label="電郵"><el-input v-model="nc.email"></el-input></el-form-item></el-col>
    </el-row>
    <el-divider content-position="left" style="margin:0 0 14px">其他</el-divider>
    <el-form-item label="轉介來源">
      <el-select v-model="nc.referral" style="max-width:300px" placeholder="選擇或輸入" filterable allow-create default-first-option>
        <el-option v-for="r in ['自行報名','學校轉介','醫生轉介','機構轉介','其他']" :key="r" :label="r" :value="r"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="備註"><el-input v-model="nc.notes" type="textarea" :rows="2" placeholder="醫療史、相關診斷、注意事項…"></el-input></el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="ncDlg=false">取消</el-button>
    <el-button type="primary" @click="addChild">建立</el-button>
  </template>
</el-dialog>

<!-- 新增用戶 -->
<el-dialog v-model="usersDlg" title="新增用戶" width="440px">
  <el-form label-width="80px">
    <el-form-item label="帳號" required><el-input v-model="nu.username"></el-input></el-form-item>
    <el-form-item label="姓名"><el-input v-model="nu.display_name" placeholder="治療師姓名"></el-input></el-form-item>
    <el-form-item label="密碼" required><el-input v-model="nu.password" type="password" show-password placeholder="至少 6 位"></el-input></el-form-item>
    <el-form-item label="角色">
      <el-select v-model="nu.role" style="width:100%">
        <el-option label="言語治療師" value="therapist"></el-option>
        <el-option label="管理員" value="admin"></el-option>
      </el-select>
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="usersDlg=false">取消</el-button>
    <el-button type="primary" @click="createU">建立</el-button>
  </template>
</el-dialog>

<!-- 課程記錄回溯 -->
<el-dialog v-model="sessDlg" :title="'課程記錄回溯'+(sessDetail?' — 第 '+sessDetail.no+' 次':'')" width="780px" top="5vh">
  <template v-if="sessDetail">
    <el-descriptions :column="4" size="small" border style="margin-bottom:12px">
      <el-descriptions-item label="日期">{{ sessDetail.date||'—' }}</el-descriptions-item>
      <el-descriptions-item label="關聯評估">{{ assessById(sessDetail.assessId)?.adate || '—' }}</el-descriptions-item>
      <el-descriptions-item label="效果">{{ sessDetail.effect?.level||'待評' }}</el-descriptions-item>
      <el-descriptions-item label="遊戲數">{{ (sessDetail.games||[]).length }}</el-descriptions-item>
    </el-descriptions>
    <el-alert v-if="!sessDetail.planSnapshot && !sessDetail.goalsFull" type="info" :closable="false"
      title="此記錄為最早的簡化數據，僅存訓練目標文字，無法完整回溯。" style="margin-bottom:10px"></el-alert>
    <template v-if="sessDetail.planSnapshot">
      <div class="grp-h" style="margin-top:0">方案版本（儲存時快照）</div>
      <div class="ver-list" style="margin-bottom:12px">
        <button v-for="(v,i) in sessDetail.planSnapshot.versions" :key="i" :class="['ver',{on:i===sessVerIdx}]" @click="sessVerIdx=i">{{ v.label }}</button>
      </div>
    </template>
    <div class="grp-h">訓練目標與遊戲</div>
    <div v-for="(g,gi) in sessGoals()" :key="gi" style="margin-bottom:12px">
      <b>目標 {{ gi+1 }}：</b>{{ g.text||'(未填寫)' }}
      <div v-for="(gm,gmi) in g.games||[]" :key="gmi" style="margin:6px 0 0 18px;font-size:13px">
        ▪ <b>{{ gm.name }}</b>（{{ DOM_NAME[gm.domain]||gm.domain }}）─ 目標：{{ gm.target }}｜玩法：{{ gm.desc }}
      </div>
      <div v-if="!(g.games||[]).length" class="note" style="margin:4px 0 0 18px">（此目標未採用遊戲）</div>
    </div>
    <div v-if="!sessDetail.planSnapshot && !(sessDetail.goalsFull||[]).length && (sessDetail.games||[]).length">
      <div class="grp-h">遊戲（扁平記錄）</div>
      <div style="font-size:13px">▪ {{ sessDetail.games.map(g=>g.name).join('、') }}</div>
    </div>
    <template v-if="sessDetail.planSnapshot">
      <el-divider content-position="left">AI 對話紀錄</el-divider>
      <div class="chat-box" style="height:220px">
        <div v-for="(m,mi) in sessDetail.planSnapshot.chat||[]" :key="mi" :class="['msg',m.role]">{{ m.text }}</div>
        <div v-if="!(sessDetail.planSnapshot.chat||[]).length" class="note" style="margin:0">無 AI 對話紀錄（種子庫直接生成）</div>
      </div>
    </template>
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
    :title="api.standalone
      ? '填入 LLM API（OpenAI 相容 / Anthropic / Responses），金鑰僅存於本機瀏覽器；瀏覽器直連需服務商允許 CORS（OpenAI / Claude 官方、智譜等主流服務均可）。未填寫時仍可用「依種子庫生成」。'
      : '填入後端代連的 LLM API（OpenAI 相容 / Anthropic / Responses）。金鑰儲存於後端伺服器，不再存於瀏覽器；未填寫時仍可用「依種子庫生成」。'"></el-alert>
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
    <el-form-item label="思考檔位">
      <el-select v-model="aiCfg.thinking" clearable placeholder="跟隨服務商預設" style="width:100%">
        <el-option label="關閉思考（推薦：速度快，不會因推理耗盡輸出而截斷）" value="off"></el-option>
        <el-option label="開啟思考（推理更強，輸出上限已提高到 16384）" value="on"></el-option>
      </el-select>
    </el-form-item>
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


                <el-backtop :right="24" :bottom="88"></el-backtop>
        <div class="footer no-print">本量表供註冊言語治療師作臨床評估之用；評估結果須結合臨床觀察及專業判斷綜合解讀。</div>

      </el-main>
    </el-container>
<!-- ═══════ 全局 AI 助理浮窗 ═══════ -->
    <div class="ai-fab no-print" @click="chatOpen=!chatOpen" title="AI 助理">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:24px;height:24px"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    </div>
    <div class="ai-panel no-print" v-if="chatOpen">
      <div class="ai-hd">
        <b>AI 助理</b>
        <span class="note" style="margin:0;flex:1">{{ curChild ? '正在讀取：'+curChild.name+' 的檔案／評估／干預' : '未選擇兒童，可先問一般問題' }}</span>
        <el-button link @click="chatOpen=false" style="font-size:16px">✕</el-button>
      </div>
      <div class="chat-box" ref="gChatBoxEl" style="height:340px;flex:1">
        <div v-if="!gChatMsgs.length" class="msg assistant">我是平台 AI 助理，可查詢所有兒童的檔案、評估記錄、課程與干預方案，也能搜尋遊戲庫。試試：「列出所有兒童」「小明的評估結果怎樣？」「小美最近上課效果如何？」「5 歲理解類有什麼遊戲？」</div>
        <div v-for="(m,i) in gChatMsgs" :key="i" :class="['msg',m.role]">
          <template v-if="m.role==='assistant' && ((m.steps&&m.steps.length)||m.reasoning)">
            <div class="ai-trace" @click="m.open=!m.open">⚙ 執行過程（{{ m.steps?.length||0 }} 次工具調用{{ m.reasoning?'・含思考過程':'' }}）{{ m.open?'▴':'▾' }}</div>
            <div v-if="m.open" class="ai-trace-body">
              <div v-if="m.reasoning" class="ai-step"><div class="ai-step-t">💭 思考過程</div><pre>{{ m.reasoning }}</pre></div>
              <div v-for="(st,si) in m.steps||[]" :key="si" class="ai-step">
                <div class="ai-step-t">🔧 {{ si+1 }}. {{ st.tool }} <span class="ai-args">{{ JSON.stringify(st.args) }}</span></div>
                <pre>{{ st.result }}</pre>
              </div>
            </div>
          </template>
          <span style="white-space:pre-wrap">{{ m.text }}</span>
        </div>
        <div v-if="gChatLoading" class="msg assistant">⏳ {{ gChatStatus || '思考中…' }}</div>
      </div>
      <div style="display:flex;gap:8px">
        <el-input v-model="gChatInput" placeholder="輸入問題…" @keyup.enter="sendGlobalChat" :disabled="gChatLoading"></el-input>
        <el-button type="primary" @click="sendGlobalChat" :loading="gChatLoading">送出</el-button>
      </div>
    </div>
  </el-container>
</template>

<script setup>
// 學前兒童口語評估量表 — 自單檔 HTML 原樣遷移（Vite + Vue3 SFC），UI/交互保持不變
import { reactive, ref, computed, watch, nextTick } from 'vue';
import * as ElementPlus from 'element-plus';   // 業務邏輯大量使用 ElementPlus.ElMessage / ElMessageBox
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import { PAGES, oralRows as oralRowsD, dailyObs as dailyObsD, foodObs as foodObsD, stim as stimD,
         dxs, TYP, DOMS, HOME_BASE, DEFAULT_SEEDS } from './data.js';
import { api } from './api.js';
import reportCss from './styles.css?inline';   // buildDoc() 列印預覽視窗的獨立樣式
import { DOM_NAME, profileText, assessText, makeTools } from './assistant.js';

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
    // 評估記錄：view 查看唯讀 / edit 編輯現有記錄 / new 撰寫新評估
    const assessMode  = ref('view');
    const assessView  = computed(()=>assessMode.value==='view');
    const curAssessId = ref(null);
    const assessList  = computed(()=>curChild.value?.assessments||[]);
    const intervAssessId = ref(null);   // 干預方案/課程關聯的評估記錄（默認最新）
    let prevAssessId = null;   // 「重新評估」前的選中記錄，取消時回到原處

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
    const DOM_TAG  = {rec:'primary', exp:'success', nar:'warning', pra:'danger', oral:'info'};
    const EFFECTS  = ['未見效','稍有進步','明顯進步','已達標'];


    // ── 數據層：localStorage db 全部改為後端 API（契約見設計 §3）──
    const children  = reactive([]);          // 輕量列表（下拉選單）
    const counts    = reactive({});          // id → 課程數（載入完整檔案時更新；輕量列表不含 sessions）
    const seeds     = reactive(DEFAULT_SEEDS.map(s=>({...s})));
    const aiCfg     = reactive({type:'openai', base:'https://api.openai.com/v1/chat/completions', key:'', model:'gpt-4o-mini', thinking:'off'});

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
      if(!id){ curChild.value=null; curAssessId.value=null; intervAssessId.value=null; assessMode.value='view'; return; }
      const c=await api.getChild(id).catch(e=>{ ElementPlus.ElMessage.error('載入檔案失敗：'+e.message); return null; });
      if(curChildId.value===id){ curChild.value=c; if(c){ counts[c.id]=(c.sessions?.length||0); normalizeAssessments(c); applyChildToForm(c); viewAssess(null); intervAssessId.value=curAssessId.value; if(detailOpen.value) fillProfileForm(c); } }
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
    // ── 兒童詳情頁（檔案頁點行進入，可編輯儲存）──
    const detailOpen = ref(false);
    const pf = reactive({name:'',sex:'',dob:'',org:'',guardian:'',relation:'',phone:'',email:'',school:'',lang:'',referral:'',notes:''});
    function fillProfileForm(c){
      Object.assign(pf,{name:c.name||'',sex:c.sex||'',dob:c.dob||'',org:c.org||'',guardian:c.guardian||'',relation:c.relation||'',
        phone:c.phone||'',email:c.email||'',school:c.school||'',lang:c.lang||'',referral:c.referral||'',notes:c.notes||''});
    }
    function openDetail(c){
      if(curChildId.value!==c.id) curChildId.value=c.id;   // 觸發載入；watch 載入完後填表
      else if(curChild.value) fillProfileForm(curChild.value);
      detailOpen.value=true;
    }
    async function saveProfile(){
      const c=curChild.value; if(!c) return;
      Object.assign(c,{name:pf.name.trim()||c.name, sex:pf.sex, dob:pf.dob, org:pf.org, guardian:pf.guardian, relation:pf.relation,
        phone:pf.phone, email:pf.email, school:pf.school, lang:pf.lang, referral:pf.referral, notes:pf.notes});
      f.name=c.name; f.sex=c.sex; f.dob=c.dob; f.org=c.org;   // 同步評估表單兒童身份欄
      if(await saveCurChild()) ElementPlus.ElMessage.success('檔案已更新');
    }

    const nextSessionNo = computed(()=>(curChild.value?.sessions?.length||0)+1);
    const ncDlg = ref(false);
    const nc = reactive({name:'',sex:'',dob:'',org:'',guardian:'',relation:'',phone:'',email:'',school:'',lang:'',referral:'',notes:''});
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
      const c={id:'c'+Date.now(), name:nc.name.trim(), sex:nc.sex, dob:nc.dob, org:nc.org, guardian:nc.guardian, relation:nc.relation,
        phone:nc.phone, email:nc.email, school:nc.school, lang:nc.lang, referral:nc.referral, notes:nc.notes,
        states:{}, sessions:[], createdAt:new Date().toISOString().slice(0,10)};
      try{ await api.addChild(c); }catch(e){ ElementPlus.ElMessage.error('建立失敗：'+e.message); return; }
      children.unshift(c); counts[c.id]=0;
      curChildId.value=c.id;
      Object.keys(nc).forEach(k=>nc[k]=''); ncDlg.value=false;
      ElementPlus.ElMessage.success('檔案已建立並選中；可到「評估」頁按「立即評估」開始第一次評估');
    }
    function applyChildToForm(c){
      f.name=c.name; f.sex=c.sex; f.dob=c.dob; if(c.org)f.org=c.org;
      onDob();
    }
    // ── 評估記錄（child.assessments[]，舊數據無此欄時自動包裝為一條記錄）──
    function assessLabel(a){ return (a.adate||'未填日期')+' 評估'+(a.savedAt?'（存檔 '+a.savedAt+'）':''); }
    function assessById(id){ return (curChild.value?.assessments||[]).find(a=>a.id===id); }
    function normalizeAssessments(c){
      if(Array.isArray(c.assessments)) return;
      const has=c.states&&Object.keys(c.states).some(k=>k!=='undefined');
      if(has||c.savedAt||c.dx){
        c.assessments=[{id:'a0',adate:c.adate||'',states:c.states||{},obs:c.obs||{},dx:c.dx||'',sev:c.sev||'',
          therapist:c.therapist||'',license:c.license||'',signDate:c.signDate||'',signature:c.signature||'',signImg:c.signImg||'',
          oralNote:c.oralNote||'',foodNote:c.foodNote||'',savedAt:c.savedAt||'',ts:0}];
        (c.sessions||[]).forEach(s=>{ if(!s.assessId) s.assessId='a0'; });   // 舊課程歸入唯一評估
      } else c.assessments=[];
    }
    function applyAssessToForm(a){
      f.dx=a.dx||''; f.sev=a.sev||''; f.adate=a.adate||new Date().toISOString().slice(0,10);
      f.obs1=a.obs?.o1||''; f.obs2=a.obs?.o2||''; f.obs3=a.obs?.o3||'';
      f.therapist=a.therapist||''; f.license=a.license||''; f.signDate=a.signDate||new Date().toISOString().slice(0,10);
      f.signature=a.signature||''; f.signImg=a.signImg||''; f.oralNote=a.oralNote||''; f.foodNote=a.foodNote||'';
      applyStates(a.states||{}); onDob();
    }
    function viewAssess(id){
      const list=assessList.value;
      const a=id?list.find(x=>x.id===id)
        :[...list].sort((x,y)=>(y.ts||0)-(x.ts||0)||(y.adate||'').localeCompare(x.adate||''))[0];   // 默認最新一條
      curAssessId.value=a?a.id:null;
      if(a) applyAssessToForm(a); else applyAssessToForm({states:{}});
      assessMode.value='view';
    }
    function onPickAssess(id){ const a=id&&assessList.value.find(x=>x.id===id); if(a){ applyAssessToForm(a); assessMode.value='view'; } }
    function startEdit(){ if(curAssessId.value) assessMode.value='edit'; }
    function startNew(){ prevAssessId=curAssessId.value; curAssessId.value=null; applyAssessToForm({states:{}}); assessMode.value='new'; }
    function cancelAssess(){ viewAssess(prevAssessId); }
    async function submitAssess(){
      const c=curChild.value; if(!c) return;
      const rec={adate:f.adate, states:statesObj(), obs:{o1:f.obs1,o2:f.obs2,o3:f.obs3}, dx:f.dx, sev:f.sev,
        therapist:f.therapist, license:f.license, signDate:f.signDate, signature:f.signature, signImg:f.signImg,
        oralNote:f.oralNote, foodNote:f.foodNote, savedAt:new Date().toLocaleString('zh-HK',{hour12:false}), ts:Date.now()};
      Object.assign(c,{name:f.name.trim()||c.name, sex:f.sex, dob:f.dob, org:f.org});
      if(assessMode.value==='edit'){
        const a=c.assessments.find(x=>x.id===curAssessId.value);
        if(!a){ ElementPlus.ElMessage.error('找不到要更新的評估記錄'); return; }
        Object.assign(a, rec);
      }else{
        rec.id='a'+Date.now();
        c.assessments.push(rec);
        curAssessId.value=rec.id;
      }
      c.savedAt=rec.savedAt;   // 頂欄「評估存檔」顯示用
      if(await saveCurChild()){
        assessMode.value='view';
        intervAssessId.value=curAssessId.value;   // 新提交的評估成為干預默認關聯
        ElementPlus.ElMessage.success('評估已提交：'+c.name+'（'+rec.adate+'）');
      }
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
        await callLLM('回應OK', 512);   // 思考模型需餘量；測試連線非測輸出上限
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
        const data=await api.aiChat(prompt, maxTokens||16384);
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
        throw new Error('AI 回應中找不到有效的方案 JSON。回應開頭：「'+(t||'(空回應)').slice(0,400)+'…」— 可再試一次或更換模型');
      return j;
    }

    async function aiGenPlan(band){
      const weak=weakByDomain(band).map(w=>({範疇:DOM_NAME[w.d], 項目:w.items.slice(0,8)}));
      const lib=seeds.map(s=>({name:s.name, domain:DOM_NAME[s.domain], ages:`${s.amin}-${s.amax}歲`, goal:s.goal}));
      const prompt=`你是資深兒童言語治療師。根據以下評估結果，為兒童設計一次言語治療課堂的干預方案。\n兒童：${f.name||'未命名'}，${ageLabel.value}。\n評估弱項（需提示或未做到）：${JSON.stringify(weak)}\n可用遊戲／措施種子庫：${JSON.stringify(lib)}\n要求：4-5 個遊戲，優先從種子庫選取或改編，每個遊戲標明要達到的目標；訓練目標 3-5 條並對應弱項；全部用繁體中文。\n只輸出 JSON（無 markdown 代碼框）：{"goals":[{"text":"訓練目標","games":[{"name":"遊戲名稱","domain":"rec|exp|nar|pra|oral","target":"此遊戲要達到的目標","desc":"玩法"}]}]} 每個目標配 1-2 個遊戲，共 3-5 個遊戲。`;
      let txt=await callLLM(prompt, 16384);
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
        planErr.value='尚未設定 AI（到「設置」頁開啟 AI 設定填入 API Key），已改用種子庫生成。';
      }
      if(!p) p=rulePlan(band);
      const nGames=p.goals.reduce((n,g)=>n+g.games.length,0);
      plan.value={no:nextSessionNo.value, date:planDate.value||new Date().toISOString().slice(0,10),
        assessId:intervAssessId.value||null,
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
          const m2=months(); const band=m2===null?3:Math.min(6,Math.floor(m2/12));
          const norm=g=>JSON.stringify({goals:(g||[]).map(x=>({text:x.text||'', games:(x.games||[]).map(gm=>({name:gm.name||'',domain:gm.domain||'',target:gm.target||'',desc:gm.desc||''}))}))});
          const before=norm(cur.goals);
          const prompt=`你是資深兒童言語治療師，正在與治療師對話。兒童：${f.name||'未命名'}（${ageLabel.value}）。
目前干預方案 JSON：\n${JSON.stringify({goals:cur.goals.map(g=>({text:g.text, games:g.games.map(x=>({name:x.name,domain:x.domain,target:x.target,desc:x.desc}))}))})}
評估弱項：${JSON.stringify(weakByDomain(band).map(w=>({範疇:DOM_NAME[w.d],項目:w.items.slice(0,8)})))}
可用種子庫遊戲：${JSON.stringify(seeds.map(s=>({name:s.name,domain:DOM_NAME[s.domain],ages:s.amin+'-'+s.amax+'歲',goal:s.goal})))}

治療師訊息：${t}

規則：
1. 訊息是「修改指示」（換遊戲、改目標、加項目等）→ 只修改涉及部分，goals 輸出修改後的完整方案，reply 簡短說明改動。
2. 訊息是「提問／諮詢」（問安排原因、遊戲是否合適、兒童情況等）→ goals 原樣保留完全不變，reply 詳細回答。
全部繁體中文。只輸出 JSON（無 markdown 代碼框）：{"goals":[{"text":"","games":[{"name":"","domain":"rec|exp|nar|pra|oral","target":"","desc":""}]}],"reply":""}`;
          const j=parsePlanJSON(await callLLM(prompt, 16384));
          const after=(j.goals||[]).map(g=>({text:g.text||'', games:(g.games||[]).map(gm=>({name:gm.name||'',domain:domKeyOf(gm.domain),target:gm.target||'',desc:gm.desc||'',checked:true}))}));
          if(norm(after)!==before){
            newVersion('修改：'+t.slice(0,10));
            curVer().goals=after;
            plan.value.chat.push({role:'assistant', text:(j.reply||'已按指示更新方案')+'（產生新版本，可於左上切換回舊版）'});
          }else{
            plan.value.chat.push({role:'assistant', text:j.reply||'（方案未變更）'});
          }
        } else {
          const v=curVer();
          if(/(加|增|多).{0,6}(遊戲|活動)/.test(t)){
            const used=new Set(v.goals.flatMap(g=>g.games.map(x=>x.name)));
            let added=0;
            for(const s of seeds){ if(added>=2) break;
              if(!used.has(s.name)){ (v.goals[0]?.games||v.goals[0].games).push({name:s.name,domain:s.domain,target:s.goal,desc:s.desc,checked:true}); added++; } }
            plan.value.chat.push({role:'assistant', text:added?`已從種子庫加入 ${added} 個遊戲到目標 1。`:'種子庫遊戲已全部使用。'});
          } else {
            plan.value.chat.push({role:'assistant', text:'尚未設定 AI 金鑰，目前只支援「加入遊戲」類簡單指令；完整對話修改請到「設置」頁填入金鑰。'});
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
      const goals=v.goals.map(g=>({text:g.text, games:g.games.filter(x=>x.checked).map(x=>({...x}))}));
      curChild.value.sessions.push({
        id:Date.now(), no:plan.value.no, date:plan.value.date,
        assessId:plan.value.assessId||intervAssessId.value||null,
        goals:goals.map(g=>g.text),                          // 舊欄位：列表顯示用
        games:goals.flatMap(g=>g.games.map(gm=>({...gm}))),   // 舊欄位：列表顯示用
        goalsFull:goals,                                     // 完整結構：目標→遊戲對應
        planSnapshot:{                                       // 完整快照：可回溯
          no:plan.value.no, date:plan.value.date,
          assessId:plan.value.assessId||intervAssessId.value||null,
          versions:JSON.parse(JSON.stringify(plan.value.versions)),
          curIdx:plan.value.curIdx,
          chat:JSON.parse(JSON.stringify(plan.value.chat||[]))
        },
        homeTip:plan.value.homeTip||'', effect:{level:'待評', note:''}
      });
      if(await saveCurChild()) ElementPlus.ElMessage.success('已儲存為第 '+plan.value.no+' 次課程記錄（含完整方案快照，可回溯）');
    }
    // ── 課程回溯 ──
    const sessDlg=ref(false), sessDetail=ref(null), sessVerIdx=ref(0);
    function openSess(row){ sessDetail.value=row; sessVerIdx.value=row.planSnapshot?row.planSnapshot.curIdx:0; sessDlg.value=true; }
    function sessGoals(){
      const d=sessDetail.value; if(!d) return [];
      if(d.planSnapshot){ const v=d.planSnapshot.versions[d.planSnapshot.curIdx]||d.planSnapshot.versions[0]; return (v&&v.goals)||[]; }
      if(d.goalsFull) return d.goalsFull;
      return (d.goals||[]).map(t=>({text:t, games:[]}));   // 最舊數據：僅目標文字
    }
    function delSession(id){
      const c=curChild.value; if(!c) return;
      const i=c.sessions.findIndex(s=>s.id===id); if(i>-1){ c.sessions.splice(i,1); saveCurChild(); }
    }

    // ═══════ 全局 AI 助理浮窗：工具呼叫式查詢（可跨全部兒童） ═══════
    const chatOpen     = ref(false);
    const gChatInput   = ref('');
    const gChatLoading = ref(false);
    const gChatMsgs    = ref([]);   // {role:'user'|'assistant', text}
    const gChatBoxEl   = ref(null);
    const gChatStatus  = ref('');
    const gChatScroll  = async ()=>{ await nextTick(); if(gChatBoxEl.value) gChatBoxEl.value.scrollTop=gChatBoxEl.value.scrollHeight; };
    function childContext(){   // 當前兒童速覽（進提示詞用）
      const c=curChild.value;
      if(!c) return '（尚未選擇兒童檔案）';
      const as=c.assessments||[];
      const cur=as.find(a=>a.id===curAssessId.value)||[...as].sort((a,b)=>(b.ts||0)-(a.ts||0))[0];
      return profileText(c)+(cur?`\n最新評估（${cur.adate||'未填日期'}）：\n${assessText(cur)}`:'');
    }
    async function sendGlobalChat(){
      const t=gChatInput.value.trim(); if(!t||gChatLoading.value) return;
      gChatMsgs.value.push({role:'user', text:t}); gChatInput.value='';
      gChatLoading.value=true; gChatScroll();
      try{
        if(!aiCfg.key) throw new Error('尚未設定 AI — 請到「設置」頁開啟 AI 設定填入');
        const tools=makeTools({children, curChild, curAssessId, plan, curVer, seeds, api, normalizeAssessments});
        const hist=gChatMsgs.value.slice(-8,-1).map(m=>`${m.role==='user'?'治療師':'助理'}：${m.text}`).join('\n');
        let transcript=`【當前兒童速覽】\n${childContext()}\n${hist?'【最近對話】\n'+hist+'\n':''}【治療師問題】${t}`;
        let answer='', reasoning='';
        const steps=[];
        for(let i=0;i<6;i++){
          gChatStatus.value = steps.length ? `已查詢 ${steps.length} 次，繼續分析…` : '正在分析問題…';
          const prompt=`你是兒童言語治療工作平台的 AI 助理，服務對象是註冊言語治療師，透過工具查詢平台資料回答（最多可連續呼叫 6 次）。全部繁體中文；資料不足如實說明，不要編造。\n${tools.spec}\n\n【已收集資訊與對話】\n${transcript}\n\n請只輸出 JSON（無 markdown 代碼框）：{"tool":"...","args":{...}} 或 {"answer":"..."}`;
          const data=await api.aiChat(prompt, 4096);
          if(data.reasoning) reasoning+=data.reasoning+'\n';
          let j=null; try{ j=JSON.parse(String(data.text||'').replace(/```json|```/gi,'').trim()); }catch(e){}
          if(j && j.tool){
            gChatStatus.value=`執行工具 ${j.tool}…`;
            const out=await tools.run(j.tool, j.args).catch(e=>'工具錯誤：'+e.message);
            steps.push({tool:j.tool, args:j.args||{}, result:String(out)});
            transcript+=`\n助理：${j.tool}(${JSON.stringify(j.args||{})})\n[結果]\n${out}`;
            continue;
          }
          answer=(j && j.answer!=null) ? String(j.answer) : String(data.text||'');
          break;
        }
        if(!answer){   // 工具次數用完：強制總結
          gChatStatus.value='整理最終回答…';
          const data=await api.aiChat(`根據以下已收集資訊，直接以 {"answer":"..."} 回答治療師最初的問題。\n${transcript}\n\n請只輸出 JSON。`, 4096);
          if(data.reasoning) reasoning+=data.reasoning+'\n';
          let j=null; try{ j=JSON.parse(String(data.text||'').replace(/```json|```/gi,'').trim()); }catch(e){}
          answer=(j && j.answer!=null) ? String(j.answer) : String(data.text||'（未能取得回答，請重試）');
        }
        gChatMsgs.value.push({role:'assistant', text:answer, steps:steps.length?steps:undefined, reasoning:reasoning.trim()||undefined});
        gChatStatus.value='';
      }catch(e){
        gChatMsgs.value.push({role:'assistant', text:'⚠️ '+e.message});
      }
      gChatLoading.value=false; gChatScroll();
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
        const canvas = await html2canvas(holder, {scale:2, useCORS:true, backgroundColor:'#ffffff', logging:false});
        const pdf = new jsPDF({unit:'mm', format:'a4', orientation:'portrait'});
        const pw = pdf.internal.pageSize.getWidth(), ph = pdf.internal.pageSize.getHeight();
        const img = canvas.toDataURL('image/jpeg', 0.95);
        const imgH = canvas.height * pw / canvas.width;
        for(let pos=0, page=0; pos < imgH-1; pos+=ph, page++){
          if(page>0) pdf.addPage();
          pdf.addImage(img, 'JPEG', 0, -pos, pw, imgH);
        }
        pdf.save(`評估報告_${f.name.trim()||'兒童'}_${f.adate||''}.pdf`);
        ElementPlus.ElMessage.success('PDF 已下載');
      }catch(err){
        console.error('PDF 生成失敗：', err);
        ElementPlus.ElMessage.error('PDF 生成失敗：'+(err&&err.message||err)+' — 已改用列印視窗，可在預覽中另存 PDF');
        printReport();   // 兜底：列印視窗可「另存為 PDF」，保證一定拿得到報告
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
      if(api.standalone) return;   // 單檔模式：本地鍵同名，舊數據本就生效
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
    // ── 登入與初始化 ──
    const me = ref(null);
    const loginState = ref('checking');   // checking | setup（首次：創建管理員）| auth（登入/註冊）
    const setupForm  = reactive({username:'', display_name:'', password:'', password2:''});
    const loginTab  = ref('in');
    const loginBusy = ref(false);
    const loginForm = reactive({username:'', password:''});
    const regForm   = reactive({username:'', display_name:'', password:'', password2:''});
    const users     = ref([]);
    const usersDlg  = ref(false);
    const nu        = reactive({username:'', display_name:'', password:'', role:'therapist'});

    async function afterLogin(){
      await importLegacy();
      try{
        let ss=await api.getSeeds();
        if(!ss || !ss.length){ ss=DEFAULT_SEEDS.map(s=>({...s})); api.putSeeds(ss.map(s=>({...s}))).catch(()=>{}); }
        seeds.splice(0, seeds.length, ...ss);
        const ai=await api.getAi(); if(ai) Object.assign(aiCfg, ai);
        if(!aiCfg.thinking) aiCfg.thinking='off';   // 舊配置默認關閉思考，避免推理耗盡輸出
        await refreshChildren();
        if(me.value && me.value.role==='admin') await refreshUsers();
      }catch(e){ console.warn('初始化失敗：', e.message); }
    }
    async function doSetup(){
      if(!setupForm.username.trim() || setupForm.password.length<6){ ElementPlus.ElMessage.warning('帳號必填，密碼至少 6 位'); return; }
      if(setupForm.password!==setupForm.password2){ ElementPlus.ElMessage.warning('兩次密碼不一致'); return; }
      loginBusy.value=true;
      try{
        const res=await api.setup({username:setupForm.username, display_name:setupForm.display_name, password:setupForm.password});
        me.value=res.user; loginState.value='auth';
        ElementPlus.ElMessage.success('管理員已創建，歡迎，'+(me.value.display_name||me.value.username));
        await afterLogin();
      }catch(e){ ElementPlus.ElMessage.error(e.message); }
      loginBusy.value=false;
    }
    async function doLogin(){
      if(!loginForm.username.trim() || !loginForm.password){ ElementPlus.ElMessage.warning('請輸入帳號與密碼'); return; }
      loginBusy.value=true;
      try{
        const res=await api.login({username:loginForm.username, password:loginForm.password});
        me.value=res.user; loginForm.password='';
        ElementPlus.ElMessage.success('歡迎，'+(me.value.display_name||me.value.username));
        await afterLogin();
      }catch(e){ ElementPlus.ElMessage.error(e.message); }
      loginBusy.value=false;
    }
    async function doRegister(){
      if(regForm.password!==regForm.password2){ ElementPlus.ElMessage.warning('兩次密碼不一致'); return; }
      loginBusy.value=true;
      try{
        const res=await api.register({username:regForm.username, display_name:regForm.display_name, password:regForm.password});
        me.value=res.user;
        ElementPlus.ElMessage.success('註冊完成，已登入');
        await afterLogin();
      }catch(e){ ElementPlus.ElMessage.error(e.message); }
      loginBusy.value=false;
    }
    async function doLogout(){
      try{ await api.logout(); }catch(e){}
      me.value=null; users.value=[];
      children.splice(0, children.length);
      curChildId.value=null; curAssessId.value=null; intervAssessId.value=null;
      plan.value=null; repHtml.value=''; assessMode.value='view';
      gChatMsgs.value=[]; chatOpen.value=false;
      ElementPlus.ElMessage.success('已登出');
    }
    async function refreshUsers(){ try{ users.value=await api.listUsers(); }catch(e){} }
    async function createU(){
      if(!nu.username.trim() || !nu.password){ ElementPlus.ElMessage.warning('帳號與密碼必填'); return; }
      try{ await api.createUser({username:nu.username, display_name:nu.display_name, password:nu.password, role:nu.role});
        usersDlg.value=false; nu.username=''; nu.display_name=''; nu.password='';
        await refreshUsers(); ElementPlus.ElMessage.success('用戶已建立');
      }catch(e){ ElementPlus.ElMessage.error(e.message); }
    }
    function resetPw(u){
      ElementPlus.ElMessageBox.prompt('為「'+(u.display_name||u.username)+'」設置新密碼（至少 6 位）', '重置密碼',
        {inputType:'password', inputPattern:/.{6,}/, inputErrorMessage:'密碼至少 6 位'})
        .then(async ({value})=>{ try{ await api.updateUser(u.id, {password:value}); ElementPlus.ElMessage.success('密碼已重置'); }catch(e){ ElementPlus.ElMessage.error(e.message); } })
        .catch(()=>{});
    }
    async function toggleU(u){ try{ await api.updateUser(u.id, {disabled:u.disabled?0:1}); await refreshUsers(); }catch(e){ ElementPlus.ElMessage.error(e.message); } }
    async function delU(u){
      try{ await api.delUser(u.id); await refreshChildren(); await refreshUsers();
        if(curChildId.value && !children.some(c=>c.id===curChildId.value)) curChildId.value=null;
        ElementPlus.ElMessage.success('已刪除');
      }catch(e){ ElementPlus.ElMessage.error(e.message); }
    }
    (async function initAuth(){
      try{
        const u=await api.me();
        if(u && u.username){ me.value=u; loginState.value='auth'; await afterLogin(); return; }
      }catch(e){}
      try{ loginState.value = (await api.hasUsers()) ? 'auth' : 'setup'; }
      catch(e){ loginState.value='auth'; }
    })();
</script>
