# streamlit_app.py —— 3 modes + Summary + 力量模式(全黑霓虹, Q11~Q30, 一錯即止)
# 更新：
# 1) 力量模式整頁全黑（主區/側欄/頁首/容器）
# 2) 送出後按鈕改字為「下一題」
# 3) 模式二詳解：✅答對/❌答錯 徽章 + 中文(英文)
# 4) 模式三詳解：每個選項 英文(中文)（含✅正確）
# 5) 移除多餘空白（無分隔線、緊貼呈現）

import streamlit as st
import random

st.set_page_config(page_title="Cloze Test Practice (3 modes, rounds)", page_icon="📝", layout="centered")

# ===================== 題庫 =====================
QUESTION_BANK = [
    {'answer_en': 'adjust', 'cloze_en': 'He tried to a_____t his chair to be more comfortable.', 'sent_zh': '他試著調整椅子讓自己更舒服。', 'meaning_zh': '調整'},
    {'answer_en': 'adjustment', 'cloze_en': 'The teacher made an a_____t to the lesson plan.', 'sent_zh': '老師對課程計畫做了調整。', 'meaning_zh': '調整'},
    {'answer_en': 'architect', 'cloze_en': 'The city is famous for its modern a_____e.', 'sent_zh': '這座城市以其現代建築而聞名。', 'meaning_zh': '建築師；建築物'},
    {'answer_en': 'banishment', 'cloze_en': 'His crimes led to his b_____t from the country.', 'sent_zh': '他的罪行導致他的放逐。', 'meaning_zh': '放逐；驅逐'},
    {'answer_en': 'capable', 'cloze_en': 'She is c_____e of solving this problem.', 'sent_zh': '她有能力解決這個問題。', 'meaning_zh': '有能力的'},
    {'answer_en': 'capability', 'cloze_en': 'This device has the c_____y to store a large amount of data.', 'sent_zh': '這個裝置具有儲存大量資料的能力。', 'meaning_zh': '能力；容量'},
    {'answer_en': 'collapse', 'cloze_en': 'The building c_____d after the earthquake.', 'sent_zh': '地震後建築物倒塌了。', 'meaning_zh': '倒塌'},
    {'answer_en': 'comfort', 'cloze_en': 'A cup of hot tea gave her some c_____t.', 'sent_zh': '一杯熱茶給了她一些安慰。', 'meaning_zh': '安慰；舒適'},
    {'answer_en': 'commodity', 'cloze_en': 'Water is a precious c_____y in the desert.', 'sent_zh': '在沙漠中水是珍貴的商品。', 'meaning_zh': '商品；日用品'},
    {'answer_en': 'complicate', 'cloze_en': 'Do not c_____e the issue with too many details.', 'sent_zh': '不要用太多細節使問題複雜化。', 'meaning_zh': '使複雜'},
    {'answer_en': 'complication', 'cloze_en': 'The surgery went well without any c_____n.', 'sent_zh': '手術很順利，沒有任何併發症。', 'meaning_zh': '複雜；併發症'},
    {'answer_en': 'compliment', 'cloze_en': 'He received a c_____t on his new haircut.', 'sent_zh': '他的髮型獲得了稱讚。', 'meaning_zh': '稱讚'},
    {'answer_en': 'confine', 'cloze_en': 'The sick child was c_____d to bed for a week.', 'sent_zh': '生病的孩子臥床一週。', 'meaning_zh': '限制；禁閉'},
    {'answer_en': 'confined', 'cloze_en': 'Owing to his leg surgery, Mike has been c_____d to bed for a whole week.', 'sent_zh': '由於腿部手術，麥克已經臥床一整週了。', 'meaning_zh': '被限制的；受限的'},
    {'answer_en': 'construction', 'cloze_en': 'That tall building is a famous c_____n.', 'sent_zh': '那棟高樓是著名的建築。', 'meaning_zh': '建築物；建造'},
    {'answer_en': 'constructive', 'cloze_en': 'Thanks for your c_____e suggestions.', 'sent_zh': '感謝你具有建設性的建議。', 'meaning_zh': '有建設性的'},
    {'answer_en': 'consume', 'cloze_en': 'Americans c_____e a lot of energy every day.', 'sent_zh': '美國人每天消耗大量能源。', 'meaning_zh': '消耗；吃喝'},
    {'answer_en': 'consumer', 'cloze_en': 'The company listens to c_____r feedback.', 'sent_zh': '公司重視消費者回饋。', 'meaning_zh': '消費者'},
    {'answer_en': 'consumption', 'cloze_en': 'The c_____n of sugar has increased.', 'sent_zh': '糖的消耗量增加了。', 'meaning_zh': '消耗；消費'},
    {'answer_en': 'container', 'cloze_en': 'Please put the food in a c_____r.', 'sent_zh': '請把食物放進容器裡。', 'meaning_zh': '容器'},
    {'answer_en': 'convey', 'cloze_en': 'Pictures can c_____y emotions better than words.', 'sent_zh': '圖片能比文字更好地傳達情感。', 'meaning_zh': '傳達；運送'},
    {'answer_en': 'criticism', 'cloze_en': 'He faced a lot of c_____m for his decisions.', 'sent_zh': '他的決定面臨許多批評。', 'meaning_zh': '批評'},
    {'answer_en': 'criticize', 'cloze_en': 'It is easy to c_____e but hard to create.', 'sent_zh': '批評很容易，創造很難。', 'meaning_zh': '批評'},
    {'answer_en': 'cruel', 'cloze_en': 'It is c_____l to hurt animals.', 'sent_zh': '傷害動物是殘忍的。', 'meaning_zh': '殘酷的'},
    {'answer_en': 'cruelty', 'cloze_en': 'Animal c_____y is a serious issue.', 'sent_zh': '虐待動物是嚴重的問題。', 'meaning_zh': '殘忍；虐待'},
    {'answer_en': 'delight', 'cloze_en': 'The children shouted with d_____t.', 'sent_zh': '孩子們高興地大叫。', 'meaning_zh': '高興；喜悅'},
    {'answer_en': 'delightful', 'cloze_en': 'We had a d_____l evening.', 'sent_zh': '我們度過了一個愉快的夜晚。', 'meaning_zh': '令人愉快的'},
    {'answer_en': 'dependent', 'cloze_en': 'He is d_____t on his parents for money.', 'sent_zh': '他在金錢上依賴父母。', 'meaning_zh': '依賴的'},
    {'answer_en': 'dependable', 'cloze_en': 'She is a d_____e friend.', 'sent_zh': '她是個可靠的朋友。', 'meaning_zh': '可信賴的'},
    {'answer_en': 'depend', 'cloze_en': 'It d_____ds on the weather.', 'sent_zh': '這取決於天氣。', 'meaning_zh': '依賴；取決於'},
    {'answer_en': 'dependence', 'cloze_en': 'He developed a d_____e on coffee.', 'sent_zh': '他對咖啡產生依賴。', 'meaning_zh': '依賴'},
    {'answer_en': 'dependent', 'cloze_en': 'Many children are still d_____t on their parents.', 'sent_zh': '許多孩子仍依賴父母。', 'meaning_zh': '依賴的'},
    {'answer_en': 'drowsy', 'cloze_en': 'It was so hot that the students felt d_____y.', 'sent_zh': '天氣太熱，學生感到昏昏欲睡。', 'meaning_zh': '昏昏欲睡的'},
    {'answer_en': 'element', 'cloze_en': 'The key e_____t of a good story is an interesting plot.', 'sent_zh': '好故事的關鍵要素是有趣的情節。', 'meaning_zh': '元素；要素'},
    {'answer_en': 'enable', 'cloze_en': 'The Internet e_____es people to exchange information easily.', 'sent_zh': '網際網路讓人們可以輕鬆交換資訊。', 'meaning_zh': '使能夠'},
    {'answer_en': 'enemy', 'cloze_en': 'He treated me like an e_____y.', 'sent_zh': '他把我當敵人看待。', 'meaning_zh': '敵人'},
    {'answer_en': 'enormous', 'cloze_en': 'The elephant is e_____s.', 'sent_zh': '大象非常巨大。', 'meaning_zh': '巨大的'},
    {'answer_en': 'enthusiasm', 'cloze_en': 'She showed great e_____m for the project.', 'sent_zh': '她對這個計畫充滿熱情。', 'meaning_zh': '熱忱；熱情'},
    {'answer_en': 'enthusiastic', 'cloze_en': 'They were e_____c supporters.', 'sent_zh': '他們是熱情的支持者。', 'meaning_zh': '熱情的'},
    {'answer_en': 'entire', 'cloze_en': 'She read the e_____e book in one day.', 'sent_zh': '她一天讀完整本書。', 'meaning_zh': '全部的'},
    {'answer_en': 'entirely', 'cloze_en': 'I e_____ly agree with you.', 'sent_zh': '我完全同意你。', 'meaning_zh': '完全地'},
    {'answer_en': 'exploration', 'cloze_en': 'The scientist went on an e_____n.', 'sent_zh': '這位科學家進行了一次探索。', 'meaning_zh': '探索；探究'},
    {'answer_en': 'extend', 'cloze_en': 'Please e_____d your hand.', 'sent_zh': '請伸出你的手。', 'meaning_zh': '延伸；延長'},
    {'answer_en': 'extension', 'cloze_en': 'You can request an e_____n for the deadline.', 'sent_zh': '你可以申請延長截止日期。', 'meaning_zh': '延長；擴展'},
    {'answer_en': 'extent', 'cloze_en': 'To what e_____t do you agree?', 'sent_zh': '你在多大程度上同意？', 'meaning_zh': '程度；範圍'},
    {'answer_en': 'freeze', 'cloze_en': 'Water f_____es at 0°C.', 'sent_zh': '水在0度結冰。', 'meaning_zh': '結冰；凍結'},
    {'answer_en': 'freezes', 'cloze_en': 'After the surface of the lake f_____s every winter, an ice-skating contest will be held.', 'sent_zh': '湖面每年冬天結冰後，將舉辦溜冰比賽。', 'meaning_zh': '結冰；凍結'},
    {'answer_en': 'frighten', 'cloze_en': 'The ghost story f_____ed us to death.', 'sent_zh': '那個鬼故事把我們嚇壞了。', 'meaning_zh': '使害怕'},
    {'answer_en': 'frightened', 'cloze_en': 'The ghost story Jeremy told us f_____ed us to death.', 'sent_zh': '傑里米講的鬼故事把我們嚇得要死。', 'meaning_zh': '受驚嚇的'},
    {'answer_en': 'generous', 'cloze_en': 'She is g_____s to everyone.', 'sent_zh': '她對每個人都很慷慨。', 'meaning_zh': '慷慨的'},
    {'answer_en': 'humankind', 'cloze_en': 'Peace is important for all h_____d.', 'sent_zh': '和平對全人類都很重要。', 'meaning_zh': '人類'},
    {'answer_en': 'laughter', 'cloze_en': 'The room was full of l_____r.', 'sent_zh': '房間裡充滿了笑聲。', 'meaning_zh': '笑聲'},
    {'answer_en': 'meaning', 'cloze_en': 'What is the m_____g of this word?', 'sent_zh': '這個字的意思是什麼？', 'meaning_zh': '意思；意義'},
    {'answer_en': 'mechanic', 'cloze_en': 'The m_____c fixed my car.', 'sent_zh': '那位技工修好了我的車。', 'meaning_zh': '技工'},
    {'answer_en': 'medical', 'cloze_en': 'She needs m_____l care.', 'sent_zh': '她需要醫療照護。', 'meaning_zh': '醫療的'},
    {'answer_en': 'medicine', 'cloze_en': 'Take your m_____e twice a day.', 'sent_zh': '每天吃兩次藥。', 'meaning_zh': '藥；醫學'},
    {'answer_en': 'patient', 'cloze_en': 'The p_____t is waiting for the doctor.', 'sent_zh': '病人在等醫生。', 'meaning_zh': '病人；有耐心的'},
    {'answer_en': 'promise', 'cloze_en': 'Grace wins her friends’ trust by keeping every p_____e she makes.', 'sent_zh': '她透過信守每個承諾來贏得朋友的信任。', 'meaning_zh': '承諾'},
    {'answer_en': 'prompt', 'cloze_en': 'He gave a p_____t reply.', 'sent_zh': '他給了及時的回覆。', 'meaning_zh': '迅速的；提示'},
    {'answer_en': 'rely', 'cloze_en': 'You can r_____y on me.', 'sent_zh': '你可以依賴我。', 'meaning_zh': '依賴'},
    {'answer_en': 'route', 'cloze_en': 'This is the best r_____e to the museum.', 'sent_zh': '這是去博物館的最佳路線。', 'meaning_zh': '路線'},
    {'answer_en': 'slight', 'cloze_en': 'There is a s_____t chance of rain today.', 'sent_zh': '今天下雨的機會很小。', 'meaning_zh': '輕微的'},
    {'answer_en': 'slightly', 'cloze_en': 'The driver was only s_____y injured.', 'sent_zh': '駕駛只有輕傷。', 'meaning_zh': '稍微地'},
    {'answer_en': 'stability', 'cloze_en': 'Many years of hot sun affected the s_____y of the house.', 'sent_zh': '多年炎熱與暴風雨影響了房子的穩定性。', 'meaning_zh': '穩定性'},
    {'answer_en': 'terminal', 'cloze_en': 'The patient has t_____l lung cancer.', 'sent_zh': '病人罹患末期肺癌。', 'meaning_zh': '末期的；終端的'},
    {'answer_en': 'torture', 'cloze_en': 'Some prisoners were t_____d to death.', 'sent_zh': '有些囚犯被折磨致死。', 'meaning_zh': '拷打；折磨'},
    {'answer_en': 'tortured', 'cloze_en': 'Some of the prisoners were either beaten or t_____d to death.', 'sent_zh': '有些囚犯被毒打，或被折磨致死。', 'meaning_zh': '受折磨的'},
    {'answer_en': 'upright', 'cloze_en': 'Return your seats to the u_____t position.', 'sent_zh': '把座椅調回直立位置。', 'meaning_zh': '直立的'},
    {'answer_en': 'victim', 'cloze_en': 'The number of v_____s in plane crashes has increased.', 'sent_zh': '飛機失事的受害者人數增加。', 'meaning_zh': '受害者'},
    {'answer_en': 'warmth', 'cloze_en': 'Kind words create w_____h in people’s hearts.', 'sent_zh': '善意的話語帶來溫暖。', 'meaning_zh': '溫暖'},
]

# ===================== 樣式（基礎 / 全黑霓虹） =====================
def base_css():
    st.markdown("""
    <style>
    html, body, [class*="css"]  { font-size: 22px !important; }
    h2 { font-size: 26px !important; margin-top: 0 !important; margin-bottom: .22em !important; }
    .block-container { padding-top: .4rem !important; padding-bottom: .6rem !important; max-width: 1000px; }
    .progress-card { margin-bottom: 0 !important; }
    .stRadio { margin-top: 0 !important; }
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stRadio"]) { margin-top: 0 !important; }
    .stButton>button{ height: 44px; padding: 0 18px; }
    .explain { margin-top:.35rem; margin-bottom:.2rem; background:#f7f7f9; border-radius:12px; padding:10px 14px; border:1px solid #ececf1; }
    .badge { display:inline-block; padding:2px 10px; border-radius:999px; font-weight:700; font-size:16px; margin-right:6px; }
    .ok { background:#e9f7ef; color:#1a7f37; border:1px solid #a7dfb8; }
    .bad { background:#fdecea; color:#c62828; border:1px solid #f5b7ae; }
    .opt-list { line-height:1.8; margin:.2rem 0 0 0; }
    </style>
    """, unsafe_allow_html=True)

def neon_black_css():
    st.markdown("""
    <style>
      :root { --bg:#000; --panel:#000; --txt:#e7e9ee; --neon:#00f7ff; --neon2:#ff3d81; }
      html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #000 !important; color: var(--txt) !important;
      }
      section.main, .block-container { background:transparent !important; color:var(--txt) !important; }
      .progress-card { background:var(--panel) !important; border-radius:16px; box-shadow:0 0 12px rgba(0,247,255,.12) inset; }
      h2 { color:var(--txt) !important; margin-top:0 !important; text-shadow:0 0 6px rgba(0,247,255,.35); }
      .stButton>button{ background:#060606; color:var(--txt); border:1px solid rgba(0,247,255,.35); border-radius:12px; }
      .stButton>button:hover{ box-shadow:0 0 12px rgba(255,61,129,.45), inset 0 0 6px rgba(0,247,255,.35); }
      .explain { background:#0b0b0b; border:1px solid rgba(0,247,255,.2); }
      .badge.ok { background:#103a22; color:#7ae582; border-color:#255f3d; }
      .badge.bad { background:#2a0b0b; color:#ff6b6b; border-color:#7a2d2d; }
      .gameover { font-size: 48px; font-weight:900; letter-spacing:.12em; color:#ff3d81; text-align:center; margin:18px 0 8px;
                  text-shadow:0 0 10px rgba(255,61,129,.85), 0 0 22px rgba(0,247,255,.45); }
      .devil { font-size: 64px; text-align:center; filter: drop-shadow(0 0 14px rgba(255,61,129,.75)); }
    </style>
    """, unsafe_allow_html=True)

base_css()

# ===================== 常數 & 模式 =====================
QUESTIONS_PER_ROUND = 10
MODE_1 = "模式一\n-   【手寫輸入】"
MODE_2 = "模式二\n-   【中文選擇】"
MODE_3 = "模式三\n-   【英文選擇】"

# ===================== 判分（詞形彈性） =====================
def _norm(s: str) -> str:
    return (s or "").strip().lower()

def _variants(correct: str):
    c = _norm(correct)
    vs = {c, c+"s", c+"es"}
    if c.endswith("y"):
        vs.add(c[:-1]+"ies")
    vs.add(c+"ed")
    if c.endswith("y"):
        vs.add(c[:-1]+"ied")
    if c.endswith("e") and not c.endswith("ee"):
        vs.add(c[:-1]+"ing")
    else:
        vs.add(c+"ing")
    if c.endswith("y"):
        vs.add(c[:-1]+"ying")
    return vs

def is_free_text_correct(user_ans: str, correct_en: str) -> bool:
    u = _norm(user_ans)
    if not u:
        return False
    c = _norm(correct_en)
    if u == c or u in _variants(c):
        return True
    if u.endswith("s") and u[:-1] == c:
        return True
    if u.endswith("es") and (u[:-2] == c or c+"e" == u[:-1]):
        return True
    if u.endswith("ies") and c.endswith("y") and u[:-3]+"y" == c:
        return True
    return False

# ===================== 狀態 =====================
def init_state():
    st.session_state.mode = MODE_1
    st.session_state.round_active = True
    st.session_state.cur_round_qidx = []
    st.session_state.cur_ptr = 0
    st.session_state.records = []     # (idx_label, prompt, chosen, correct_en, is_correct, mode, qidx_cache)
    st.session_state.submitted = False
    st.session_state.options_cache = {}
    st.session_state.text_input_cache = ""
    # Summary & 力量模式
    st.session_state.summary_records = None
    st.session_state.power_mode = False
    st.session_state.power_qidx = []
    st.session_state.power_ptr = 0
    st.session_state.power_failed = False

def start_round10():
    all_idx = list(range(len(QUESTION_BANK)))
    chosen = random.sample(all_idx, k=min(QUESTIONS_PER_ROUND, len(all_idx)))
    st.session_state.cur_round_qidx = chosen
    st.session_state.cur_ptr = 0
    st.session_state.submitted = False
    st.session_state.options_cache = {}
    st.session_state.text_input_cache = ""
    st.session_state.records = []

if "round_active" not in st.session_state:
    init_state()
    start_round10()

# ===================== 側欄 =====================
with st.sidebar:
    st.markdown("### 設定")
    can_change_mode = (
        st.session_state.cur_ptr == 0 and
        not st.session_state.submitted and
        st.session_state.round_active and
        len(st.session_state.records) == 0 and
        not st.session_state.power_mode
    )
    st.session_state.mode = st.radio("選擇練習模式", [MODE_1, MODE_2, MODE_3], index=0, disabled=not can_change_mode)
    if st.button("🔄 重新開始"):
        init_state(); start_round10(); st.rerun()

# ===================== 選項 =====================
def get_options_for_q(qidx, mode):
    key = (qidx, mode)
    if key in st.session_state.options_cache:
        return st.session_state.options_cache[key]
    item = QUESTION_BANK[qidx]
    correct_en = item["answer_en"].strip()
    correct_zh = (item.get("meaning_zh") or "").strip()

    if mode == MODE_2:  # 中文選
        pool = list({(it.get("meaning_zh") or "").strip()
                     for it in QUESTION_BANK
                     if (it.get("meaning_zh") or "").strip() and (it.get("meaning_zh") or "").strip() != correct_zh})
        distractors = random.sample(pool, k=min(3, len(pool)))
        display = list(dict.fromkeys([correct_zh] + distractors))
        random.shuffle(display)
        payload = {"display": display, "value": display[:]}

    elif mode == MODE_3:  # 英文選
        pool = list({it["answer_en"].strip()
                     for it in QUESTION_BANK
                     if it["answer_en"].strip() and it["answer_en"].strip() != correct_en})
        distractors = random.sample(pool, k=min(3, len(pool)))
        display = list(dict.fromkeys([correct_en] + distractors))
        random.shuffle(display)
        payload = {"display": display, "value": display[:]}

    else:
        payload = {"display": [], "value": []}

    st.session_state.options_cache[key] = payload
    return payload

# ===================== UI =====================
def render_top_card(title_round, i, n):
    percent = int(i / n * 100) if n else 0
    st.markdown(
        f"""
        <div class="progress-card" style='background-color:#f5f5f5; padding:9px 14px; border-radius:12px;'>
            <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;'>
                <div style='font-size:18px;'>🎯 {title_round}｜進度：{i} / {n}</div>
                <div style='font-size:16px; color:#555;'>{percent}%</div>
            </div>
            <progress value='{i}' max='{n if n else 1}' style='width:100%; height:14px;'></progress>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_question_by_index(global_idx, label_no, power=False):
    if power: neon_black_css()
    q = QUESTION_BANK[global_idx]
    mode = st.session_state.mode

    if mode == MODE_3:
        prompt = q.get("sent_zh", "").strip()
        st.markdown(f"<h2>Q{label_no}. {prompt if prompt else '（此題缺少中文題幹）'}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2>Q{label_no}. {q['cloze_en']}</h2>", unsafe_allow_html=True)
        if mode == MODE_1 and q.get("sent_zh"):
            st.markdown(f"<div class='zh-blue' style='margin-top:.1rem;'>📘 {q['sent_zh']}</div>", unsafe_allow_html=True)

    # 模式一輸入框（無標籤）
    if mode == MODE_1:
        user_text = st.text_input("", key=f"ti_{global_idx}_{label_no}",
                                  value=st.session_state.text_input_cache,
                                  label_visibility="collapsed",
                                  placeholder="")
        return q, ("TEXT", user_text)
    else:
        payload = get_options_for_q(global_idx, mode)
        options_disp = payload["display"]
        choice = st.radio("", options_disp if options_disp else [],
                          key=f"mc_{global_idx}_{label_no}", label_visibility="collapsed") if options_disp else None
        if not options_disp:
            st.info("No options to select.")
        return q, ("MC", (choice, payload))

def record(idx_label, q, chosen_label, is_correct, qidx_cache):
    st.session_state.records.append((
        idx_label,
        q["cloze_en"] if st.session_state.mode != MODE_3 else q.get("sent_zh", ""),
        chosen_label,
        q["answer_en"].strip(),
        is_correct,
        st.session_state.mode,
        qidx_cache
    ))

def explain_block(q, mode, is_correct, payload=None):
    """payload 僅模式三需要（顯示各選項 英文(中文)）"""
    en = q["answer_en"].strip()
    zh = (q.get("meaning_zh") or "").strip()

    # 標題徽章（模式二要顏色狀態）
    if mode == MODE_2:
        badge = "<span class='badge ok'>✅ 答對</span>" if is_correct else "<span class='badge bad'>❌ 答錯</span>"
        body = f"{zh}（{en}）"
        st.markdown(f"<div class='explain'>{badge}{body}</div>", unsafe_allow_html=True)

    elif mode == MODE_3:
        # 每個選項：英文(中文)，並標示正確
        en2zh = {it['answer_en'].strip(): (it.get('meaning_zh') or '').strip() for it in QUESTION_BANK}
        opts = (payload or {}).get("display", [])
        lines = []
        for e in opts:
            e_s = str(e).strip()
            tag = " ✅" if _norm(e_s) == _norm(en) else ""
            lines.append(f"- {e_s}（{en2zh.get(e_s, '')}）{tag}")
        st.markdown(f"<div class='explain'><div class='opt-list'>{'<br/>'.join(lines)}</div></div>", unsafe_allow_html=True)

    else:
        # 模式一：英文(中文)
        st.markdown(f"<div class='explain'><span class='badge {'ok' if is_correct else 'bad'}'>{'✅ 答對' if is_correct else '❌ 答錯'}</span>{en}（{zh}）</div>", unsafe_allow_html=True)

# ===================== 一般模式 =====================
def normal_mode_page():
    cur_ptr = st.session_state.cur_ptr
    show_qidx = st.session_state.cur_round_qidx[cur_ptr]
    label_no = cur_ptr + 1

    render_top_card("第 1 回合", cur_ptr + 1, len(st.session_state.cur_round_qidx))
    q, uinput = render_question_by_index(show_qidx, label_no, power=False)

    # 單一主按鈕：送出 →（留在本頁顯示詳解 & 按鈕改文案）→ 下一題
    action_label = "下一題" if st.session_state.submitted else "送出答案"
    if st.button(action_label, key="action_btn_normal", use_container_width=True):
        mode = st.session_state.mode
        correct_en = q["answer_en"].strip()
        correct_zh = (q.get("meaning_zh") or "").strip()

        if not st.session_state.submitted:
            if uinput[0] == "TEXT":
                ans = (uinput[1] or "").strip()
                is_correct = is_free_text_correct(ans, correct_en)
                record(label_no, q, ans, is_correct, show_qidx)
            else:
                chosen_disp, _ = uinput[1]
                if chosen_disp is None:
                    st.warning("請先選擇一個選項。"); st.stop()
                is_correct = (_norm(chosen_disp) == _norm(correct_zh)) if mode == MODE_2 else (_norm(chosen_disp) == _norm(correct_en))
                record(label_no, q, chosen_disp, is_correct, show_qidx)

            st.session_state.submitted = True
            # 不 rerun：當頁顯示詳解、按鈕即時變成「下一題」

        else:
            # 下一題
            st.session_state.submitted = False
            st.session_state.text_input_cache = ""
            st.session_state.cur_ptr += 1
            if st.session_state.cur_ptr >= len(st.session_state.cur_round_qidx):
                st.session_state.round_active = False
                st.session_state.summary_records = st.session_state.records[:]
            st.rerun()

    # 顯示詳解（緊貼，無分隔線）
    if st.session_state.submitted:
        last_is_correct = st.session_state.records[-1][4] if st.session_state.records else False
        payload = uinput[1][1] if (uinput[0] == "MC") else None
        explain_block(q, st.session_state.mode, last_is_correct, payload)

# ===================== Summary（10 題後） =====================
def summary_page():
    recs = st.session_state.summary_records or []
    total = len(recs)
    correct = sum(1 for r in recs if r[4])
    acc = (correct / total * 100) if total else 0.0

    st.subheader("📊 總結")
    st.markdown(f"**Total Answered:** {total}")
    st.markdown(f"**Total Correct:** {correct}")
    st.markdown(f"**Accuracy:** {acc:.1f}%")

    wrongs = [r for r in recs if not r[4]]
    st.markdown("### ❌ 錯題總覽")
    if not wrongs:
        st.info("本回合無錯題！")
    else:
        for idx_label, prompt, chosen, correct_en, _, _, _ in wrongs:
            en2zh = {it["answer_en"].strip(): (it.get("meaning_zh") or "").strip() for it in QUESTION_BANK}
            st.markdown(f"- **Q{idx_label}**：{prompt}")
            st.markdown(f"　你的答案：`{chosen}`")
            st.markdown(f"　正確答案：`{correct_en}`（{en2zh.get(correct_en, '')}）")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔁 再玩一次", use_container_width=True):
            init_state(); start_round10(); st.rerun()
    with c2:
        if correct == total and total == QUESTIONS_PER_ROUND:
            if st.button("⚡ 你渴望力量嗎", use_container_width=True):
                used_answers = {QUESTION_BANK[i]["answer_en"] for i in st.session_state.cur_round_qidx}
                remain_idx = [i for i, it in enumerate(QUESTION_BANK) if it["answer_en"] not in used_answers]
                pick_n = min(20, len(remain_idx))
                st.session_state.power_qidx = random.sample(remain_idx, k=pick_n)
                st.session_state.power_ptr = 0
                st.session_state.power_failed = False
                st.session_state.power_mode = True
                st.session_state.submitted = False
                st.rerun()

# ===================== 力量模式（全黑霓虹 Q11~Q30 一錯即止） =====================
def power_mode_page():
    neon_black_css()
    total = len(st.session_state.power_qidx)

    # 完結（過關或失敗）
    if st.session_state.power_ptr >= total or (st.session_state.power_failed and not st.session_state.submitted):
        if st.session_state.power_failed:
            st.markdown("<div class='gameover'>GAME OVER</div>", unsafe_allow_html=True)
            st.markdown("<div class='devil'>😈</div>", unsafe_allow_html=True)
            st.caption("力量模式：答錯即止。再接再厲！")
        else:
            st.markdown("<h2>🎉 你征服了力量模式！</h2>", unsafe_allow_html=True)
            st.write(f"你通過了 **{total} / {total}** 題。")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔁 回到一般模式再來", use_container_width=True):
                init_state(); start_round10(); st.rerun()
        with c2:
            if st.button("🏁 結束", use_container_width=True):
                st.stop()
        st.stop()

    cur = st.session_state.power_ptr
    show_qidx = st.session_state.power_qidx[cur]
    label_no = 11 + cur

    render_top_card("⚡ 力量模式", cur + 1, total)
    q, uinput = render_question_by_index(show_qidx, label_no, power=True)

    # 單一按鈕（送出→顯示詳解→下一題）
    action_label = "下一題" if st.session_state.submitted else "送出答案"
    if st.button(action_label, key="action_btn_power", use_container_width=True):
        correct_en = q["answer_en"].strip()
        correct_zh = (q.get("meaning_zh") or "").strip()
        mode = st.session_state.mode

        if not st.session_state.submitted:
            if uinput[0] == "TEXT":
                ans = (uinput[1] or "").strip()
                is_correct = is_free_text_correct(ans, correct_en)
            else:
                chosen_disp, _ = uinput[1]
                if chosen_disp is None:
                    st.warning("請先選擇一個選項。"); st.stop()
                is_correct = (_norm(chosen_disp) == _norm(correct_zh)) if mode == MODE_2 else (_norm(chosen_disp) == _norm(correct_en))

            st.session_state.submitted = True
            if not is_correct:
                st.session_state.power_failed = True  # 顯示詳解後下一步結束

        else:
            st.session_state.submitted = False
            if not st.session_state.power_failed:
                st.session_state.power_ptr += 1
            st.rerun()

    # 詳解（無分隔線、緊貼）
    if st.session_state.submitted:
        # 建 payload 給模式三使用（顯示每個選項）
        payload = uinput[1][1] if (uinput[0] == "MC") else None
        # 判定對錯（從 UI 值重新取）
        mode = st.session_state.mode
        en = q["answer_en"].strip()
        zh = (q.get("meaning_zh") or "").strip()
        if uinput[0] == "TEXT":
            was_correct = is_free_text_correct(uinput[1] or "", en)
        else:
            chosen_disp, _ = uinput[1]
            was_correct = (_norm(chosen_disp) == _norm(zh)) if mode == MODE_2 else (_norm(chosen_disp) == _norm(en))
        explain_block(q, mode, was_correct, payload)

# ===================== 路由 =====================
if st.session_state.round_active:
    normal_mode_page()
else:
    if not st.session_state.power_mode:
        summary_page()
    else:
        power_mode_page()
