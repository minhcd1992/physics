import streamlit as st
import google.generativeai as genai
import time

# ==========================================
# CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Physics Glitch",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS TOÀN CỤC - GIAO DIỆN "GLITCH / SCI-FI"
# ==========================================
# Đã đổi sang font Exo 2 (Tiêu đề) và Be Vietnam Pro (Nội dung) để hỗ trợ Tiếng Việt hoàn hảo
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;600&family=Exo+2:wght@400;700;900&display=swap');

/* ---- Reset & nền ---- */
html, body, [data-testid="stApp"] {
    background: #03040a !important;
    color: #e8f4ff !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #0a0f2e 0%, #03040a 60%) !important;
}
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 2rem 1.5rem 4rem !important; max-width: 780px !important; }

/* ---- Typography ---- */
h1, h2, h3 {
    font-family: 'Exo 2', sans-serif !important;
    letter-spacing: 0.05em;
}
p, label, span, div, li, a {
    font-family: 'Be Vietnam Pro', sans-serif !important;
    font-size: 16px;
}

/* ---- Tiêu đề chính ---- */
.hero-title {
    font-family: 'Exo 2', sans-serif;
    font-size: clamp(2.2rem, 6vw, 3.5rem);
    font-weight: 900;
    color: #00d4ff;
    text-shadow: 0 0 30px #00d4ff88, 0 0 60px #00d4ff33;
    line-height: 1.1;
    margin: 0;
}
.hero-sub {
    font-family: 'Be Vietnam Pro', sans-serif;
    font-size: 1.1rem;
    color: #7eb8d4;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.hero-tag {
    display: inline-block;
    background: linear-gradient(90deg, #00d4ff22, #7b2fff22);
    border: 1px solid #00d4ff44;
    color: #00d4ff;
    font-family: 'Be Vietnam Pro', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 1rem;
}

/* ---- Panel / Card ---- */
.glitch-card {
    background: linear-gradient(135deg, #0d1117 0%, #0a1628 100%);
    border: 1px solid #1a3a5c;
    border-radius: 12px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    margin: 1rem 0;
}
.glitch-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}

/* ---- World cards ---- */
.world-card {
    background: linear-gradient(135deg, #0d1117 0%, #0a1628 100%);
    border: 1px solid #1a3a5c;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin: 0.8rem 0;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
}
.world-card:hover {
    border-color: #00d4ff88;
    box-shadow: 0 0 20px #00d4ff18;
}
.world-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.world-card.ice::before  { background: linear-gradient(90deg, transparent, #4fc3f7, transparent); }
.world-card.planet::before { background: linear-gradient(90deg, transparent, #ab47bc, transparent); }
.world-card.energy::before { background: linear-gradient(90deg, transparent, #ffca28, transparent); }
.world-title {
    font-family: 'Exo 2', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
}
.world-desc {
    font-size: 0.9rem;
    color: #7eb8d4;
    margin: 0;
    line-height: 1.5;
}
.world-badge {
    display: inline-block;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 2px 10px;
    border-radius: 2px;
    margin-bottom: 0.5rem;
}

/* ---- Scenario box ---- */
.scenario-box {
    background: #07101e;
    border: 1px solid #ff4b4b55;
    border-left: 3px solid #ff4b4b;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    font-size: 1.05rem;
    line-height: 1.7;
    color: #e8f4ff;
    margin: 1rem 0;
}

/* ---- Status badges ---- */
.badge-correct {
    background: #00ff8822;
    border: 1px solid #00ff8866;
    color: #00ff88;
    padding: 6px 16px;
    border-radius: 4px;
    font-family: 'Exo 2', sans-serif;
    font-size: 0.85rem;
    display: inline-block;
    margin-bottom: 1rem;
}
.badge-wrong {
    background: #ff4b4b22;
    border: 1px solid #ff4b4b66;
    color: #ff4b4b;
    padding: 6px 16px;
    border-radius: 4px;
    font-family: 'Exo 2', sans-serif;
    font-size: 0.85rem;
    display: inline-block;
    margin-bottom: 1rem;
}
.badge-unsure {
    background: #ffca2822;
    border: 1px solid #ffca2866;
    color: #ffca28;
    padding: 6px 16px;
    border-radius: 4px;
    font-family: 'Exo 2', sans-serif;
    font-size: 0.85rem;
    display: inline-block;
    margin-bottom: 1rem;
}

/* ---- Explain box ---- */
.explain-box {
    background: #071c10;
    border: 1px solid #00ff8833;
    border-left: 3px solid #00ff88;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #b8ffe0;
    margin: 0.8rem 0;
}

/* ---- AI chat ---- */
.ai-bubble {
    background: linear-gradient(135deg, #0d1a2e, #0a1628);
    border: 1px solid #00d4ff33;
    border-radius: 12px 12px 12px 0;
    padding: 1.1rem 1.3rem;
    margin: 0.8rem 0;
    position: relative;
}
.ai-bubble::before {
    content: '⚡ AI';
    font-family: 'Exo 2', sans-serif;
    font-size: 0.65rem;
    color: #00d4ff;
    letter-spacing: 0.2em;
    display: block;
    margin-bottom: 0.5rem;
}
.user-bubble {
    background: #0f1f10;
    border: 1px solid #00ff8833;
    border-radius: 12px 12px 0 12px;
    padding: 1.1rem 1.3rem;
    margin: 0.8rem 0;
}
.user-bubble::before {
    content: '👤 BẠN';
    font-family: 'Exo 2', sans-serif;
    font-size: 0.65rem;
    color: #00ff88;
    letter-spacing: 0.2em;
    display: block;
    margin-bottom: 0.5rem;
}

/* ---- Progress bar ---- */
.prog-wrap {
    background: #0d1117;
    border: 1px solid #1a3a5c;
    border-radius: 6px;
    height: 6px;
    overflow: hidden;
    margin: 0.3rem 0 1rem;
}
.prog-fill {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #00d4ff, #7b2fff);
    transition: width 0.5s ease;
}

/* ---- Breadcrumb / step ---- */
.step-indicator {
    font-family: 'Exo 2', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #3a6a8c;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.step-active { color: #00d4ff; }

/* ---- Score display ---- */
.score-big {
    font-family: 'Exo 2', sans-serif;
    font-size: 3.5rem;
    font-weight: 900;
    color: #00d4ff;
    text-shadow: 0 0 30px #00d4ff88;
    line-height: 1;
}
.score-label {
    font-family: 'Be Vietnam Pro', sans-serif;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    color: #3a6a8c;
    text-transform: uppercase;
}

/* ---- Streamlit overrides ---- */
.stButton > button {
    background: transparent !important;
    border: 1px solid #00d4ff66 !important;
    color: #00d4ff !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 4px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: #00d4ff22 !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 12px #00d4ff44 !important;
}
button[kind="primary"] {
    background: linear-gradient(90deg, #00d4ff22, #7b2fff22) !important;
    border: 1px solid #00d4ff !important;
    box-shadow: 0 0 16px #00d4ff33 !important;
}
.stRadio > div {
    gap: 0.5rem !important;
}
.stRadio label {
    background: #0d1117 !important;
    border: 1px solid #1a3a5c !important;
    border-radius: 6px !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
    color: #7eb8d4 !important;
    font-family: 'Be Vietnam Pro', sans-serif !important;
    font-size: 1rem !important;
}
.stRadio label:hover {
    border-color: #00d4ff66 !important;
    color: #e8f4ff !important;
}
.stTextArea textarea {
    background: #07101e !important;
    border: 1px solid #1a3a5c !important;
    border-radius: 8px !important;
    color: #e8f4ff !important;
    font-family: 'Be Vietnam Pro', sans-serif !important;
    font-size: 1rem !important;
}
.stTextArea textarea:focus {
    border-color: #00d4ff66 !important;
    box-shadow: 0 0 8px #00d4ff22 !important;
}
[data-testid="stMarkdownContainer"] p { color: #c8dff0; }
.stSpinner > div { border-top-color: #00d4ff !important; }
[data-testid="stExpander"] {
    background: #0d1117 !important;
    border: 1px solid #1a3a5c !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# DỮ LIỆU NỘI DUNG
# ==========================================
WORLDS = {
    "no_friction": {
        "name": "Thế Giới Trơn Trượt",
        "emoji": "🧊",
        "subtitle": "Không Ma Sát",
        "color": "#4fc3f7",
        "css_class": "ice",
        "badge_bg": "#4fc3f722",
        "badge_border": "#4fc3f755",
        "description": "Một thế giới nơi mọi bề mặt nhẵn bóng hoàn hảo. Không có gì ngừng lại — mãi mãi.",
        "scenarios": [
            {
                "id": "nf1",
                "statement": "🔴 TÌNH HUỐNG LỖI: Một chiếc xe đang chạy sẽ tự động dừng lại hoàn toàn, ngay cả khi không có bất kỳ lực ma sát hay lực cản không khí nào tác dụng lên nó.",
                "correct_answer": "Sai",
                "explanation": "Theo Định luật 1 Newton (Quán tính), một vật đang chuyển động sẽ tiếp tục chuyển động thẳng đều vô tận trừ khi có ngoại lực tác dụng. Không có ma sát, không có lực cản — chiếc xe sẽ lướt đi mãi mãi không bao giờ dừng.",
                "concept": "Định luật 1 Newton — Quán tính",
                "ai_context": "Học sinh vừa học về Định luật 1 Newton (Quán tính). Tình huống sai: 'xe tự dừng khi không có ma sát'. Câu trả lời đúng là: Sai — không có lực tác dụng thì vật chuyển động mãi mãi."
            },
            {
                "id": "nf2",
                "statement": "🔴 TÌNH HUỐNG LỖI: Nếu ném một quả bóng trong môi trường hoàn toàn không có ma sát và không có trọng lực, quả bóng sẽ bay chậm dần rồi cong xuống và dừng lại.",
                "correct_answer": "Sai",
                "explanation": "Không có trọng lực kéo xuống, không có ma sát làm chậm — quả bóng sẽ di chuyển thẳng, đều, mãi mãi. Đây chính là nguyên lý mà các vệ tinh nhân tạo và phi thuyền trong không gian hoạt động.",
                "concept": "Chuyển động thẳng đều — Quán tính trong không gian",
                "ai_context": "Học sinh vừa học về chuyển động trong môi trường không có lực cản và trọng lực. Tình huống sai: 'bóng sẽ cong xuống và dừng lại'. Câu trả lời đúng: Sai — không có lực nào tác dụng thì vật đi thẳng đều mãi."
            },
            {
                "id": "nf3",
                "statement": "🔴 TÌNH HUỐNG LỖI: Khi trượt băng, nếu bạn đẩy mạnh hơn, bạn sẽ đạt tốc độ cao hơn. Điều này chứng minh rằng lực lớn hơn luôn tạo ra vận tốc lớn hơn, bất kể khối lượng.",
                "correct_answer": "Sai",
                "explanation": "Lực lớn hơn tạo ra gia tốc lớn hơn — không phải vận tốc trực tiếp. Theo F = ma, cùng một lực tác dụng lên vật nặng gấp đôi sẽ cho gia tốc bằng một nửa. Vận tốc phụ thuộc vào cả lực lẫn khối lượng của vật.",
                "concept": "Định luật 2 Newton — F = ma",
                "ai_context": "Học sinh vừa học về Định luật 2 Newton F=ma. Tình huống sai: 'lực lớn hơn luôn tạo vận tốc lớn hơn bất kể khối lượng'. Câu trả lời đúng: Sai — lực lớn tạo gia tốc lớn, nhưng vận tốc còn phụ thuộc khối lượng."
            }
        ]
    },
    "high_gravity": {
        "name": "Hành Tinh Nặng Trĩu",
        "emoji": "🪐",
        "subtitle": "Trọng Lực Cực Đại",
        "color": "#ab47bc",
        "css_class": "planet",
        "badge_bg": "#ab47bc22",
        "badge_border": "#ab47bc55",
        "description": "Một hành tinh khổng lồ nơi trọng lực kéo mọi thứ xuống với sức mạnh kinh khủng.",
        "scenarios": [
            {
                "id": "hg1",
                "statement": "🔴 TÌNH HUỐNG LỖI: Thả rơi tự do một quả bóng bowling nặng 5kg và một chiếc lông vũ 5g trong buồng chân không hoàn toàn trên hành tinh này — quả bóng bowling sẽ chạm đất nhanh hơn nhiều.",
                "correct_answer": "Sai",
                "explanation": "Trong chân không, mọi vật đều rơi với cùng gia tốc g bất kể khối lượng. Galileo đã chứng minh điều này từ thế kỷ 17. Trọng lực lớn hơn chỉ làm cả hai rơi nhanh hơn so với Trái Đất, nhưng chúng vẫn chạm đất đồng thời.",
                "concept": "Rơi tự do — Galileo & gia tốc trọng trường",
                "ai_context": "Học sinh vừa học về rơi tự do và gia tốc trọng trường. Tình huống sai: 'vật nặng hơn rơi nhanh hơn trong chân không'. Câu trả lời đúng: Sai — trong chân không mọi vật rơi cùng gia tốc g, bất kể khối lượng."
            },
            {
                "id": "hg2",
                "statement": "🔴 TÌNH HUỐNG LỖI: Trọng lực ở hành tinh này mạnh gấp 10 lần Trái Đất. Do đó, khối lượng cơ thể bạn sẽ tăng gấp 10 lần khi đứng trên hành tinh đó.",
                "correct_answer": "Sai",
                "explanation": "Khối lượng là lượng vật chất tạo nên một vật — nó không bao giờ thay đổi dù ở đâu trong vũ trụ. Thứ thay đổi là TRỌNG LƯỢNG (lực hấp dẫn tác dụng lên khối lượng). Trên hành tinh đó, trọng lượng bạn tăng 10 lần, nhưng khối lượng vẫn y nguyên.",
                "concept": "Phân biệt Khối lượng vs Trọng lượng",
                "ai_context": "Học sinh vừa học về sự khác biệt giữa khối lượng và trọng lượng. Tình huống sai: 'trọng lực lớn làm khối lượng tăng'. Câu trả lời đúng: Sai — khối lượng không đổi, chỉ trọng lượng (lực) mới thay đổi theo g."
            },
            {
                "id": "hg3",
                "statement": "🔴 TÌNH HUỐNG LỖI: Nếu bạn nhảy lên trên hành tinh có trọng lực gấp 10 lần, bạn sẽ chỉ lên cao bằng 1/10 so với trên Trái Đất vì trọng lực lớn hơn kéo bạn xuống nhanh hơn.",
                "correct_answer": "Sai",
                "explanation": "Thực ra bạn lên cao bằng 1/10 là đúng về kết quả nhưng sai về lý giải. Không chỉ trọng lực kéo xuống nhanh hơn — chính trọng lực lớn hơn còn làm bạn khó nhảy lên ngay từ đầu (chân phải đẩy mạnh hơn nhiều để nâng cơ thể nặng hơn gấp 10 lần). Cả hai chiều đều bị ảnh hưởng.",
                "concept": "Chuyển động ném — Gia tốc trọng trường",
                "ai_context": "Học sinh vừa học về chuyển động ném thẳng đứng dưới tác dụng của trọng lực. Tình huống sai: 'chỉ chiều xuống bị ảnh hưởng bởi trọng lực lớn hơn'. Câu trả lời đúng: Sai — cả chiều lên (lực đẩy cần thiết) và chiều xuống (gia tốc rơi) đều bị ảnh hưởng."
            }
        ]
    },
    "energy_loss": {
        "name": "Hư Vô Năng Lượng",
        "emoji": "⚡",
        "subtitle": "Không Bảo Toàn",
        "color": "#ffca28",
        "css_class": "energy",
        "badge_bg": "#ffca2822",
        "badge_border": "#ffca2855",
        "description": "Một thế giới hỗn loạn nơi năng lượng tự sinh ra và biến mất — hay có vẻ vậy.",
        "scenarios": [
            {
                "id": "el1",
                "statement": "🔴 TÌNH HUỐNG LỖI: Một quả bóng cao su có độ nảy hoàn hảo có thể nảy lên cao hơn một chút so với vị trí thả ban đầu, nhờ 'tích trữ thêm năng lượng' từ mặt đất khi va chạm.",
                "correct_answer": "Sai",
                "explanation": "Định luật Bảo toàn Năng lượng là tuyệt đối: năng lượng không tự sinh ra từ hư vô. Mỗi lần nảy, quả bóng luôn mất một phần năng lượng dưới dạng nhiệt và âm thanh. Không có vật liệu nào nảy cao hơn điểm thả — đó là điều vật lý không cho phép.",
                "concept": "Định luật Bảo toàn Năng lượng",
                "ai_context": "Học sinh vừa học về Định luật Bảo toàn Năng lượng. Tình huống sai: 'bóng có thể nảy cao hơn điểm thả nhờ tích năng lượng từ mặt đất'. Câu trả lời đúng: Sai — năng lượng không thể tự sinh ra, mỗi lần nảy đều mất năng lượng."
            },
            {
                "id": "el2",
                "statement": "🔴 TÌNH HUỐNG LỖI: Một chiếc quạt điện khi cắm điện sẽ chuyển hóa 100% điện năng hoàn toàn thành động năng (gió), không sinh ra bất kỳ dạng năng lượng nào khác.",
                "correct_answer": "Sai",
                "explanation": "Không có cỗ máy nào đạt hiệu suất 100% — đây là hệ quả trực tiếp của Định luật 2 Nhiệt động lực học. Điện năng được chuyển thành động năng quay cánh quạt, nhưng luôn có một lượng đáng kể 'thất thoát' thành nhiệt năng do ma sát trong ổ trục và điện trở trong dây đồng.",
                "concept": "Hiệu suất máy móc — Nhiệt động lực học",
                "ai_context": "Học sinh vừa học về hiệu suất chuyển hóa năng lượng và định luật nhiệt động lực học. Tình huống sai: 'quạt điện chuyển 100% điện năng thành động năng'. Câu trả lời đúng: Sai — không máy nào đạt 100% hiệu suất, luôn có thất thoát nhiệt."
            },
            {
                "id": "el3",
                "statement": "🔴 TÌNH HUỐNG LỖI: Nếu bạn xây dựng một cỗ máy đủ tinh vi và chính xác, cuối cùng bạn có thể tạo ra 'động cơ vĩnh cửu' — một máy chạy mãi mãi mà không cần thêm năng lượng từ bên ngoài.",
                "correct_answer": "Sai",
                "explanation": "Động cơ vĩnh cửu vi phạm cả Định luật 1 và 2 Nhiệt động lực học. Dù công nghệ có tiên tiến đến đâu, ma sát và sự phân tán nhiệt năng là không thể tránh khỏi. Bất kỳ máy nào cũng sẽ dần mất năng lượng và cuối cùng dừng lại — đây là giới hạn cơ bản của vũ trụ, không phải của kỹ thuật.",
                "concept": "Động cơ vĩnh cửu — Định luật Nhiệt động lực học 1 & 2",
                "ai_context": "Học sinh vừa học về tại sao động cơ vĩnh cửu là bất khả thi. Tình huống sai: 'công nghệ đủ tiên tiến có thể tạo động cơ vĩnh cửu'. Câu trả lời đúng: Sai — động cơ vĩnh cửu vi phạm định luật nhiệt động lực học, là giới hạn của vũ trụ không phải kỹ thuật."
            }
        ]
    }
}

# ==========================================
# KHỞI TẠO SESSION STATE
# ==========================================
defaults = {
    "page": "home",
    "selected_world": None,
    "scenario_idx": 0,
    "user_answer": None,
    "score": 0,
    "answered_scenarios": set(),
    "ai_chat_history": [],
    "ai_done": False,
    "show_explanation": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# HELPERS
# ==========================================
def progress_bar(value, max_val):
    pct = int((value / max_val) * 100)
    st.markdown(f"""
    <div class="prog-wrap">
        <div class="prog-fill" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# TRANG CHỦ
# ==========================================
def render_home():
    st.markdown('<div class="hero-tag">⚡ Physics Glitch — v2.0</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">PHYSICS<br>GLITCH</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Hiểu đúng Vật lý bằng cách khám phá những điều sai</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glitch-card">
        <p style="color:#7eb8d4;font-size:1rem;margin:0 0 1rem">
        Chào mừng đến với một vũ trụ nơi các định luật vật lý đã bị <span style="color:#ff4b4b">phá vỡ</span>.
        Nhiệm vụ của bạn: tìm ra lỗi sai, phân tích lý do — rồi dạy lại cho AI của chúng tôi.
        </p>
        <div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-top:0.5rem">
            <div style="text-align:center">
                <div style="font-family:'Exo 2',sans-serif;font-size:1.6rem;font-weight:700;color:#00d4ff">3</div>
                <div style="font-size:0.8rem;color:#3a6a8c;letter-spacing:0.1em;text-transform:uppercase">Thế giới</div>
            </div>
            <div style="text-align:center">
                <div style="font-family:'Exo 2',sans-serif;font-size:1.6rem;font-weight:700;color:#00d4ff">9</div>
                <div style="font-size:0.8rem;color:#3a6a8c;letter-spacing:0.1em;text-transform:uppercase">Tình huống</div>
            </div>
            <div style="text-align:center">
                <div style="font-family:'Exo 2',sans-serif;font-size:1.6rem;font-weight:700;color:#00d4ff">AI</div>
                <div style="font-size:0.8rem;color:#3a6a8c;letter-spacing:0.1em;text-transform:uppercase">Phản hồi thật</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Cách học:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="glitch-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.5rem">🔴</div>
            <div style="font-family:'Exo 2',sans-serif;font-size:0.7rem;color:#ff4b4b;margin:0.3rem 0">BƯỚC 1</div>
            <div style="font-size:0.9rem;color:#7eb8d4">Gặp tình huống lỗi vật lý</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="glitch-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.5rem">🧠</div>
            <div style="font-family:'Exo 2',sans-serif;font-size:0.7rem;color:#ffca28;margin:0.3rem 0">BƯỚC 2</div>
            <div style="font-size:0.9rem;color:#7eb8d4">Phân tích và giải thích sai lầm</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="glitch-card" style="text-align:center;padding:1rem">
            <div style="font-size:1.5rem">⚡</div>
            <div style="font-family:'Exo 2',sans-serif;font-size:0.7rem;color:#00d4ff;margin:0.3rem 0">BƯỚC 3</div>
            <div style="font-size:0.9rem;color:#7eb8d4">Dạy lại AI — nhận phản hồi thật</div>
        </div>""", unsafe_allow_html=True)

    # Kiểm tra API key Gemini
    has_api = False
    try:
        if st.secrets.get("GEMINI_API_KEY") or st.session_state.get("_temp_key"):
            has_api = True
    except Exception:
        pass

    if not has_api:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("⚠️ Chưa cấu hình API Key — nhấn để thiết lập"):
            st.markdown("""<p style="color:#7eb8d4;font-size:0.9rem">
            Thêm API key vào <code>.streamlit/secrets.toml</code>:<br><br>
            <code>GEMINI_API_KEY = "AIzaSy..."</code>
            </p>""", unsafe_allow_html=True)
            manual_key = st.text_input("Hoặc nhập Gemini API Key tạm thời:", type="password", placeholder="AIzaSy...")
            if manual_key:
                st.session_state["_temp_key"] = manual_key
                st.success("✅ Đã lưu key cho phiên này!")
                st.rerun()
                
    if has_api:
        st.markdown('<div style="color:#00ff88;font-size:0.85rem">✅ API key đã được cấu hình</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀  BẮT ĐẦU KHÁM PHÁ", type="primary", use_container_width=True):
        go("choose")

# ==========================================
# TRANG CHỌN THẾ GIỚI
# ==========================================
def render_choose():
    st.markdown('<div class="step-indicator">// CHỌN THẾ GIỚI //</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:\'Exo 2\',sans-serif;color:#e8f4ff;margin-bottom:0.2rem">Chọn chiều không gian</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#3a6a8c;margin-bottom:1.5rem">Mỗi thế giới mang một quy luật vật lý bị lỗi. Bạn sẽ phải tìm ra sai lầm.</p>', unsafe_allow_html=True)

    for wk, wd in WORLDS.items():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="world-card {wd['css_class']}">
                <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.4rem">
                    <span style="font-size:1.8rem">{wd['emoji']}</span>
                    <div>
                        <span class="world-badge" style="background:{wd['badge_bg']};border:1px solid {wd['badge_border']};color:{wd['color']}">{wd['subtitle']}</span><br>
                        <span class="world-title" style="color:{wd['color']}">{wd['name']}</span>
                    </div>
                </div>
                <p class="world-desc">{wd['description']}</p>
                <p style="font-size:0.8rem;color:#3a6a8c;margin:0.5rem 0 0">{len(wd['scenarios'])} tình huống • Định luật Newton & cơ học</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            if st.button("Vào →", key=f"enter_{wk}"):
                st.session_state.selected_world = wk
                st.session_state.scenario_idx = 0
                st.session_state.user_answer = None
                st.session_state.score = 0
                st.session_state.answered_scenarios = set()
                st.session_state.ai_chat_history = []
                st.session_state.ai_done = False
                st.session_state.show_explanation = False
                go("scenario")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Trang chủ"):
        go("home")

# ==========================================
# TRANG TÌNH HUỐNG
# ==========================================
def render_scenario():
    wk = st.session_state.selected_world
    wd = WORLDS[wk]
    idx = st.session_state.scenario_idx
    total = len(wd["scenarios"])

    if idx >= total:
        go("result")
        return

    scenario = wd["scenarios"][idx]

    # Header
    st.markdown(f'<div class="step-indicator step-active">// {wd["emoji"]} {wd["name"].upper()} — TÌNH HUỐNG {idx+1}/{total} //</div>', unsafe_allow_html=True)
    progress_bar(idx + 1, total)

    st.markdown(f'<h2 style="font-family:\'Exo 2\',sans-serif;font-size:1.1rem;color:{wd["color"]};margin-bottom:0.3rem">{scenario["concept"]}</h2>', unsafe_allow_html=True)

    # Scenario box
    st.markdown(f'<div class="scenario-box">{scenario["statement"]}</div>', unsafe_allow_html=True)

    st.markdown('<p style="color:#7eb8d4;margin-bottom:0.5rem">Theo khoa học thực tế, nhận định trên là:</p>', unsafe_allow_html=True)

    answer = st.radio(
        "Lựa chọn của bạn:",
        ["✅  Đúng", "❌  Sai", "🤔  Không chắc chắn"],
        index=None,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("⚡  GỬI PHÂN TÍCH", type="primary", use_container_width=True):
            if answer is None:
                st.error("Chọn một đáp án trước!")
            else:
                clean = answer.split("  ")[1]
                st.session_state.user_answer = clean
                st.session_state.show_explanation = True
                if clean == scenario["correct_answer"] and scenario["id"] not in st.session_state.answered_scenarios:
                    st.session_state.score += 10
                    st.session_state.answered_scenarios.add(scenario["id"])
                st.session_state.ai_chat_history = []
                st.session_state.ai_done = False
                go("analysis")

    with col2:
        if st.button("← Chọn thế giới khác"):
            go("choose")

# ==========================================
# TRANG PHÂN TÍCH
# ==========================================
def render_analysis():
    wk = st.session_state.selected_world
    wd = WORLDS[wk]
    idx = st.session_state.scenario_idx
    scenario = wd["scenarios"][idx]
    answer = st.session_state.user_answer

    is_correct = (answer == scenario["correct_answer"])
    is_unsure = (answer == "Không chắc chắn")

    st.markdown(f'<div class="step-indicator step-active">// PHÂN TÍCH KẾT QUẢ //</div>', unsafe_allow_html=True)

    # Badge kết quả
    if is_correct:
        st.markdown('<div class="badge-correct">✓ PHÁT HIỆN ĐÚNG — +10 ĐIỂM</div>', unsafe_allow_html=True)
    elif is_unsure:
        st.markdown('<div class="badge-unsure">~ CHƯA CHẮC — Xem giải thích bên dưới</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="badge-wrong">✗ CHƯA CHÍNH XÁC — Đáp án: {scenario["correct_answer"]}</div>', unsafe_allow_html=True)

    # Scenario lại
    st.markdown(f'<div class="scenario-box" style="opacity:0.7;font-size:0.9rem">{scenario["statement"]}</div>', unsafe_allow_html=True)

    # Giải thích
    st.markdown('<div class="explain-box">', unsafe_allow_html=True)
    st.markdown(f'<strong style="color:#00ff88;font-family:\'Exo 2\',sans-serif;font-size:0.8rem;letter-spacing:0.1em">GIẢI THÍCH KHOA HỌC</strong>', unsafe_allow_html=True)
    st.markdown(f'<p style="margin:0.5rem 0 0;color:#b8ffe0">{scenario["explanation"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🤖  TIẾP THEO: DẠY AI  →", type="primary", use_container_width=True):
        go("teach_ai")

# ==========================================
# TRANG DẠY AI
# ==========================================
def render_teach_ai():
    wk = st.session_state.selected_world
    wd = WORLDS[wk]
    idx = st.session_state.scenario_idx
    total = len(wd["scenarios"])
    scenario = wd["scenarios"][idx]

    # Khởi tạo Gemini client
    has_api = False
    try:
        key = st.secrets.get("GEMINI_API_KEY") or st.session_state.get("_temp_key")
        if key:
            genai.configure(api_key=key)
            has_api = True
    except Exception:
        pass

    st.markdown('<div class="step-indicator step-active">// MODULE 3 — DẠY AI //</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:\'Exo 2\',sans-serif;font-size:1.1rem;color:#00d4ff">AI đang cần sự giúp đỡ của bạn</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#7eb8d4">Giải thích lại khái niệm <strong style="color:#e8f4ff">"{scenario["concept"]}"</strong> cho AI bằng ngôn từ của chính bạn. AI sẽ đọc và phản hồi thật sự.</p>', unsafe_allow_html=True)

    # Hiển thị lịch sử chat
    for msg in st.session_state.ai_chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

    if not st.session_state.ai_done:
        placeholder_text = "Nhập lời giải thích của bạn... VD: 'Vì không có lực nào tác dụng, nên theo định luật Newton...'"
        user_input = st.text_area("", placeholder=placeholder_text, height=120, label_visibility="collapsed")

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("📡  GỬI CHO AI", type="primary", use_container_width=True):
                if len(user_input.strip()) < 10:
                    st.error("Hãy giải thích chi tiết hơn! (ít nhất 10 ký tự)")
                else:
                    st.session_state.ai_chat_history.append({"role": "user", "content": user_input})

                    system_prompt = f"""Bạn là một AI đang học vật lý và cần học sinh dạy lại cho bạn.
Context: {scenario['ai_context']}

Vai trò của bạn:
1. Ghi nhận lời giải thích của học sinh một cách tự nhiên, thân thiện
2. Đặt MỘT câu hỏi sâu hơn để kiểm tra sự hiểu biết của học sinh (hỏi về ứng dụng thực tế, ví dụ cụ thể, hoặc trường hợp đặc biệt)
3. Nếu giải thích CÓ LỖI, nhẹ nhàng chỉ ra và đặt câu hỏi gợi ý để học sinh tự sửa

Trả lời bằng tiếng Việt, ngắn gọn (3-5 câu), thân thiện và tò mò như một AI đang học hỏi."""

                    if has_api:
                        with st.spinner("AI đang suy nghĩ..."):
                            try:
                                # Dùng chính xác tên model trong danh sách của bạn
                                model = genai.GenerativeModel(
                                    model_name="gemini-2.5-flash",
                                    system_instruction=system_prompt
                                )
                                
                                # Chuyển đổi lịch sử chat
                                gemini_history = []
                                for m in st.session_state.ai_chat_history:
                                    role = "user" if m["role"] == "user" else "model"
                                    gemini_history.append({"role": role, "parts": [m["content"]]})
                                
                                # Gọi API Gemini
                                response = model.generate_content(gemini_history)
                                ai_reply = response.text
                            except Exception as e:
                                ai_reply = f"⚠️ Lỗi kết nối API Gemini: {str(e)}"
                    else:
                        # Fallback thông minh nếu không có API
                        time.sleep(1)
                        ai_reply = f"Cảm ơn bạn đã giải thích về **{scenario['concept']}**! Tôi hiểu hơn rồi. Vậy bạn có thể cho tôi một ví dụ thực tế trong cuộc sống hàng ngày mà bạn có thể quan sát nguyên lý này không? *(Lưu ý: Đang dùng AI mô phỏng — cần Gemini API key để nhận phản hồi thật)*"

                    st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_reply})

                    # Sau 2 lượt thì đánh dấu xong
                    user_turns = sum(1 for m in st.session_state.ai_chat_history if m["role"] == "user")
                    if user_turns >= 2:
                        st.session_state.ai_done = True

                    st.rerun()

        with col2:
            if st.button("Bỏ qua →"):
                st.session_state.ai_done = True
                st.rerun()

    else:
        # AI done — nút tiếp theo
        st.markdown('<div class="badge-correct" style="margin-top:1rem">✓ HOÀN THÀNH MODULE DẠY AI</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if idx < total - 1:
            if st.button(f"⚡  TÌNH HUỐNG TIẾP THEO ({idx+2}/{total})", type="primary", use_container_width=True):
                st.session_state.scenario_idx += 1
                st.session_state.user_answer = None
                st.session_state.ai_chat_history = []
                st.session_state.ai_done = False
                st.session_state.show_explanation = False
                go("scenario")
        else:
            if st.button("🏆  XEM KẾT QUẢ CUỐI CÙNG", type="primary", use_container_width=True):
                go("result")

# ==========================================
# TRANG KẾT QUẢ
# ==========================================
def render_result():
    wk = st.session_state.selected_world
    wd = WORLDS[wk]
    total = len(wd["scenarios"])
    max_score = total * 10
    score = st.session_state.score

    pct = int((score / max_score) * 100)

    st.markdown('<div class="step-indicator step-active">// NHIỆM VỤ HOÀN THÀNH //</div>', unsafe_allow_html=True)

    # Score display
    st.markdown(f"""
    <div class="glitch-card" style="text-align:center;padding:2rem">
        <div class="score-label">TỔNG ĐIỂM</div>
        <div class="score-big">{score}<span style="font-size:1.5rem;color:#3a6a8c">/{max_score}</span></div>
        <div style="margin:1rem auto;max-width:300px">
    """, unsafe_allow_html=True)
    progress_bar(score, max_score)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Nhận xét
    if pct == 100:
        st.markdown('<div class="badge-correct" style="display:block;text-align:center;padding:0.8rem">🌟 HOÀN HẢO — Bạn là bậc thầy vật lý!</div>', unsafe_allow_html=True)
        msg = "Xuất sắc! Bạn đã phát hiện tất cả lỗi sai và hiểu bản chất vật lý thật sự."
    elif pct >= 60:
        st.markdown('<div class="badge-unsure" style="display:block;text-align:center;padding:0.8rem">👍 TỐT — Còn vài điểm cần ôn lại</div>', unsafe_allow_html=True)
        msg = "Bạn đã hiểu phần lớn. Hãy đọc lại giải thích của những tình huống bạn chưa chắc chắn."
    else:
        st.markdown('<div class="badge-wrong" style="display:block;text-align:center;padding:0.8rem">📚 CẦN CỐ GẮNG — Đọc lại giải thích nhé!</div>', unsafe_allow_html=True)
        msg = "Những lỗi sai đã đánh lừa bạn — đó là bình thường! Khoa học chính là quá trình học từ sai lầm."

    st.markdown(f'<p style="color:#7eb8d4;text-align:center;margin:1rem 0">{msg}</p>', unsafe_allow_html=True)

    # Tổng kết kiến thức
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="font-family:\'Exo 2\',sans-serif;font-size:0.9rem;color:#3a6a8c;letter-spacing:0.15em">KIẾN THỨC ĐÃ TRẢI QUA</h3>', unsafe_allow_html=True)
    for sc in wd["scenarios"]:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid #1a3a5c">
            <span style="color:#00ff88;font-size:0.9rem">✓</span>
            <span style="font-size:0.9rem;color:#7eb8d4">{sc['concept']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄  THỬ THẾ GIỚI KHÁC", type="primary", use_container_width=True):
            for k in ["selected_world","scenario_idx","user_answer","score","answered_scenarios","ai_chat_history","ai_done","show_explanation"]:
                st.session_state[k] = defaults[k]
            go("choose")
    with col2:
        if st.button("↩  CHƠI LẠI THẾ GIỚI NÀY", use_container_width=True):
            st.session_state.scenario_idx = 0
            st.session_state.user_answer = None
            st.session_state.score = 0
            st.session_state.answered_scenarios = set()
            st.session_state.ai_chat_history = []
            st.session_state.ai_done = False
            st.session_state.show_explanation = False
            go("scenario")

# ==========================================
# ROUTER CHÍNH
# ==========================================
page = st.session_state.page
if page == "home":        render_home()
elif page == "choose":    render_choose()
elif page == "scenario":  render_scenario()
elif page == "analysis":  render_analysis()
elif page == "teach_ai":  render_teach_ai()
elif page == "result":    render_result()
