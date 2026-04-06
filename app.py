import streamlit as st
import google.generativeai as genai
import time
import copy
from worlds_data import WORLDS

# ==========================================
# CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Physics Glitch - Khúc Xạ Ánh Sáng",
    page_icon="🌈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS TOÀN CỤC - GIAO DIỆN "GLITCH / SCI-FI" & ANIMATION
# ==========================================
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
/* Thêm màu viền cho thế giới khúc xạ */
.world-card.refraction::before { background: linear-gradient(90deg, transparent, #00d4ff, transparent); }

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

/* ---- Animation SVG Mô phỏng ---- */
@keyframes ray-flow {
  to { stroke-dashoffset: -20; }
}
.ray {
  stroke-dasharray: 10, 5;
  animation: ray-flow 1s linear infinite;
}
.pulse {
  animation: opacity-pulse 2s ease-in-out infinite;
}
@keyframes opacity-pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPERS & MÔ PHỎNG SVG
# ==========================================
def detect_misconception(user_answer, scenario):
    # Trực tiếp lấy câu báo lỗi từ file dữ liệu
    if user_answer == "Đúng" and scenario["correct_answer"] == "Sai":
        return scenario.get("misconception_msg", f"Lỗi tư duy: Nhầm lẫn cơ bản về {scenario['concept']}.")
            
    if user_answer == "Không chắc chắn":
        return "lack_of_confidence: Học sinh thiếu tự tin hoặc chưa từng học khái niệm này."
        
    return "unidentified_error"

def render_svg_simulation(scenario):
    # Trực tiếp lấy mã SVG từ file dữ liệu
    svg_content = scenario.get("svg_code", "").strip()
    
    if svg_content:
        # Bọc thẻ div định dạng viền xanh cho đẹp mắt
        full_html = f"""
        <div style="background:#07101e; border: 1px solid #1a3a5c; border-radius: 8px; padding: 10px; margin-bottom: 1rem; text-align: center;">
            {svg_content}
        </div>
        """
        st.components.v1.html(full_html, height=260)
# ==========================================
# KHỞI TẠO SESSION STATE
# ==========================================
defaults = {
    "page": "home",
    "selected_world": None,
    "scenario_idx": 0,
    "current_sc_id": None,
    "user_answer": None,
    "score": 0,
    "answered_scenarios": set(),
    "ai_chat_history": [],
    "ai_done": False,
    "show_explanation": False,
    "student_model": {
        "concept_mastery": {},   
        "mistakes": [],          
        "learning_state": {      # Chuẩn bị cho các bản nâng cấp sau
            "fatigue": 0.0,
            "consecutive_errors": 0
        }
    }
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = copy.deepcopy(v) # Sửa lỗi Shared Reference

def go(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# TRANG CHỦ
# ==========================================
def render_home():
    # 1. Tự động đếm số lượng thế giới và tổng số tình huống
    total_worlds = len(WORLDS)
    total_scenarios = sum(len(w["scenarios"]) for w in WORLDS.values())

    st.markdown('<div class="hero-tag">⚡ Physics Glitch — v3.0 (Optics Edition)</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">PHYSICS<br>GLITCH</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Hiểu đúng Vật lý bằng cách khám phá những điều sai</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Thêm chữ 'f' trước dấu ba nháy kép và truyền biến vào
    st.markdown(f"""
    <div class="glitch-card">
        <p style="color:#7eb8d4;font-size:1rem;margin:0 0 1rem">
        Chào mừng đến với một vũ trụ nơi các định luật vật lý đã bị <span style="color:#ff4b4b">phá vỡ</span>.
        Nhiệm vụ của bạn: tìm ra lỗi sai, phân tích lý do — rồi dạy lại cho AI của chúng tôi.
        </p>
        <div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-top:0.5rem">
            <div style="text-align:center">
                <div style="font-family:'Exo 2',sans-serif;font-size:1.6rem;font-weight:700;color:#00d4ff">{total_worlds}</div>
                <div style="font-size:0.8rem;color:#3a6a8c;letter-spacing:0.1em;text-transform:uppercase">Thế giới</div>
            </div>
            <div style="text-align:center">
                <div style="font-family:'Exo 2',sans-serif;font-size:1.6rem;font-weight:700;color:#00d4ff">{total_scenarios}</div>
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
                <p style="font-size:0.8rem;color:#3a6a8c;margin:0.5rem 0 0">{len(wd['scenarios'])} tình huống • Quang học</p>
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

    if len(st.session_state.answered_scenarios) >= total:
        go("result")
        return

    scenario = wd["scenarios"][idx]

    # Header: Tính toán số câu đã hoàn thành để hiển thị thanh tiến trình chuẩn xác
    current_step = len(st.session_state.answered_scenarios) + 1
    
    st.markdown(f'<div class="step-indicator step-active">// {wd["emoji"]} {wd["name"].upper()} — TÌNH HUỐNG {current_step}/{total} //</div>', unsafe_allow_html=True)
    progress_bar(current_step, total)

    st.markdown(f'<h2 style="font-family:\'Exo 2\',sans-serif;font-size:1.1rem;color:{wd["color"]};margin-bottom:0.3rem">{scenario["concept"]}</h2>', unsafe_allow_html=True)

    # Render SVG Simulation nếu có
    render_svg_simulation(scenario)
    
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
                
                concept = scenario["concept"]
                
                # Khởi tạo điểm concept nếu chưa có
                if concept not in st.session_state.student_model["concept_mastery"]:
                    st.session_state.student_model["concept_mastery"][concept] = 0.5
                
                # Áp dụng thuật toán EMA (Exponential Moving Average)
                old_mastery = st.session_state.student_model["concept_mastery"][concept]
                
                if clean == scenario["correct_answer"]:
                    # Trả lời đúng: 70% cũ + 30% mới (1.0)
                    new_mastery = 0.7 * old_mastery + 0.3 * 1.0
                    st.session_state.student_model["concept_mastery"][concept] = new_mastery
                    st.session_state.student_model["learning_state"]["consecutive_errors"] = 0
                    
                    if scenario["id"] not in st.session_state.answered_scenarios:
                        st.session_state.score += 10
                else:
                    # Trả lời sai/Không chắc: 70% cũ + 30% mới (0.0)
                    new_mastery = 0.7 * old_mastery + 0.3 * 0.0
                    st.session_state.student_model["concept_mastery"][concept] = new_mastery
                    st.session_state.student_model["learning_state"]["consecutive_errors"] += 1
                    
                    # Ghi nhận sai lầm và chặn Memory Leak (Giới hạn 20 lỗi gần nhất)
                    mistake_type = detect_misconception(clean, scenario)
                    mistakes = st.session_state.student_model["mistakes"]
                    mistakes.append({
                        "concept": concept,
                        "type": mistake_type,
                        "user_chose": clean
                    })
                    if len(mistakes) > 20:
                        mistakes.pop(0)

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

    # Giải thích đã được gộp lại thành 1 khối
    st.markdown(f"""
    <div class="explain-box">
        <strong style="color:#00ff88;font-family:'Exo 2',sans-serif;font-size:0.8rem;letter-spacing:0.1em">GIẢI THÍCH KHOA HỌC</strong>
        <p style="margin:0.5rem 0 0;color:#b8ffe0">{scenario["explanation"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🤖  TIẾP THEO: ĐÀO SÂU BẢN CHẤT  →", type="primary", use_container_width=True):
        go("Đào sâu Bản chất")

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

    st.markdown('<div class="step-indicator step-active">// MODULE 3 — ĐÀO SÂU BẢN CHẤT //</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:\'Exo 2\',sans-serif;font-size:1.1rem;color:#00d4ff">Cùng thảo luận sâu hơn</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#7eb8d4">Thảo luận thêm về <strong style="color:#e8f4ff">"{scenario["concept"]}"</strong> để hiểu sâu hơn những khía cạnh khác, đừng ngại sai</p>', unsafe_allow_html=True)

    # Hiển thị lịch sử chat
    for msg in st.session_state.ai_chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

    if not st.session_state.ai_done:
        placeholder_text = "Nhập lời giải thích của bạn... VD: 'Vì chiết suất lớn nên...'"
        user_input = st.text_area("", placeholder=placeholder_text, height=120, label_visibility="collapsed")

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("📡  GỬI CHO AI", type="primary", use_container_width=True):
                if len(user_input.strip()) < 10:
                    st.error("Hãy giải thích chi tiết hơn! (ít nhất 10 ký tự)")
                else:
                    # 1. Lưu tin nhắn của người dùng
                    st.session_state.ai_chat_history.append({"role": "user", "content": user_input})
                    
                    user_turns = sum(1 for m in st.session_state.ai_chat_history if m["role"] == "user")
                    
                    # 1. Tổng hợp Learning State & Trend
                    mistakes_list = [m['type'] for m in st.session_state.student_model['mistakes'][-3:]]
                    mastery_score = st.session_state.student_model['concept_mastery'].get(scenario['concept'], 0.5)
                    consecutive_errors = st.session_state.student_model["learning_state"]["consecutive_errors"]
                    
                    student_data = f"""
                    - Điểm nắm vững (Mastery): {mastery_score:.2f} (Dưới 0.5 là Yếu, trên 0.8 là Giỏi)
                    - Lỗi tư duy gần đây: {mistakes_list}
                    - Trạng thái: Sai {consecutive_errors} câu liên tiếp (Mức độ mệt mỏi/nản chí).
                    """

                    # 2. Prompt hợp nhất tiến hóa
                    system_prompt = f"""Bạn là một Hệ thống Gia sư AI cá nhân hóa (Adaptive Tutor) chuyên Vật lý.
Context bài học: {scenario['ai_context']}

--- DỮ LIỆU NHẬN THỨC CỦA HỌC SINH ---
{student_data}
--------------------------------------

Đây là lượt chat thứ {user_turns}. Nhiệm vụ của bạn:
1. Đọc lời giải thích của học sinh và PHÂN TÍCH DỰA TRÊN DỮ LIỆU NHẬN THỨC:
   - Nếu học sinh đang "Sai liên tiếp nhiều câu": Hãy an ủi, giảm độ khó xuống mức tối thiểu, dùng ví dụ cực kỳ đời thường để lấy lại tự tin.
   - Nếu có "Lỗi tư duy gần đây": Hỏi xoáy vào điểm mù đó theo phương pháp Socratic để họ tự nhận ra lỗi.
   - Nếu "Mastery" cao (>0.8): Hãy hỏi một câu đố mẹo hoặc ứng dụng kỹ thuật nâng cao.
2. Đặt THÊM 1 câu hỏi phụ gợi mở (Tuyệt đối KHÔNG dùng từ khóa bí mật).
3. Nếu học sinh giải thích CHÍNH XÁC hoặc bảo "không biết/chịu thua": 
   - Tóm tắt lại kiến thức một cách thân thiện để vá lỗ hổng tư duy.
   - BẮT BUỘC chèn cụm từ [ĐÃ_HIỂU] vào cuối câu.
4. Lượt chat thứ 5 bắt buộc chốt vấn đề bằng cụm từ [ĐÃ_HIỂU]."""

                    # 3. Gọi API Gemini
                    if has_api:
                        with st.spinner("AI đang suy nghĩ..."):
                            try:
                                # Sử dụng dòng model cực nhanh và hạn mức cao để tránh lỗi 429
                                model = genai.GenerativeModel(
                                    model_name="gemini-flash-latest",
                                    system_instruction=system_prompt
                                )
                                gemini_history = []
                                for m in st.session_state.ai_chat_history:
                                    role = "user" if m["role"] == "user" else "model"
                                    gemini_history.append({"role": role, "parts": [m["content"]]})
                                
                                response = model.generate_content(gemini_history)
                                ai_reply = response.text
                            except Exception as e:
                                error_msg = str(e)
                                if "429" in error_msg or "quota" in error_msg.lower():
                                    ai_reply = "⏳ Tín hiệu kết nối vũ trụ đang bị nghẽn (AI đang quá tải). Bạn vui lòng đợi khoảng 1 phút rồi thử gửi lại nhé!"
                                else:
                                    ai_reply = f"⚠️ Lỗi kết nối hệ thống: {error_msg}"
                    else:
                        time.sleep(1)
                        if user_turns >= 3:
                            ai_reply = f"À, mình hiểu hoàn toàn rồi! Hóa ra {scenario['concept']} là như vậy. Cảm ơn bạn đã kiên nhẫn giảng giải cho mình nhé! [ĐÃ_HIỂU]"
                        else:
                            ai_reply = f"Cảm ơn bạn! Mình hiểu một phần rồi. Vậy bạn có thể giải thích rõ hơn về ví dụ thực tế được không?"

                    # 4. Kiểm tra từ khóa ẩn để kết thúc bài học
                    if "[ĐÃ_HIỂU]" in ai_reply:
                        st.session_state.ai_done = True
                        # Cắt bỏ từ khóa để không hiển thị lên giao diện
                        ai_reply = ai_reply.replace("[ĐÃ_HIỂU]", "").strip()

                    # 5. Lưu phản hồi của AI
                    st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_reply})

                    st.rerun()

        with col2:
            if st.button("Kết thúc thảo luận →"):
                st.session_state.ai_done = True
                st.rerun()

    else:
        # AI done — nút tiếp theo
        st.markdown('<div class="badge-correct" style="margin-top:1rem">✓ HOÀN THÀNH MODULE</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if len(st.session_state.answered_scenarios) < total:
            if st.button(f"⚡  TÌNH HUỐNG TIẾP THEO ({len(st.session_state.answered_scenarios)+1}/{total})", type="primary", use_container_width=True):
                # LOGIC ADAPTIVE: Chọn câu hỏi tiếp theo
                unanswered = [sc for sc in wd["scenarios"] if sc["id"] not in st.session_state.answered_scenarios]
                
                # Sắp xếp các câu chưa trả lời dựa trên điểm mastery (Ưu tiên điểm thấp nhất)
                unanswered.sort(key=lambda sc: st.session_state.student_model["concept_mastery"].get(sc["concept"], 0.5))
                
                # Chọn câu có điểm mastery thấp nhất
                next_sc = unanswered[0]
                
                # Tìm lại index của câu đó để render
                st.session_state.scenario_idx = wd["scenarios"].index(next_sc)
                
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

    # Nhận xét chung
    if pct == 100:
        st.markdown('<div class="badge-correct" style="display:block;text-align:center;padding:0.8rem">🌟 HOÀN HẢO — Bạn là bậc thầy quang học!</div>', unsafe_allow_html=True)
        msg = "Xuất sắc! Bạn đã phát hiện tất cả lỗi sai và hiểu bản chất hiện tượng khúc xạ thật sự."
    elif pct >= 60:
        st.markdown('<div class="badge-unsure" style="display:block;text-align:center;padding:0.8rem">👍 TỐT — Còn vài điểm cần ôn lại</div>', unsafe_allow_html=True)
        msg = "Bạn đã hiểu phần lớn. Hãy chú ý đến danh sách kiến thức cần ôn tập bên dưới nhé."
    else:
        st.markdown('<div class="badge-wrong" style="display:block;text-align:center;padding:0.8rem">📚 CẦN CỐ GẮNG — Đừng nản chí!</div>', unsafe_allow_html=True)
        msg = "Những lỗi sai đã đánh lừa bạn — đó là bình thường! Hãy xem lại các khái niệm chưa nắm vững và thử sức lần nữa."

    st.markdown(f'<p style="color:#7eb8d4;text-align:center;margin:1rem 0">{msg}</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # PHÂN LOẠI KIẾN THỨC DỰA VÀO STUDENT MODEL
    # ==========================================
    mastered = []
    needs_review = []
    
    for sc in wd["scenarios"]:
        concept = sc['concept']
        # Lấy điểm mastery (Mặc định khởi tạo là 0.5. Nếu trả lời đúng lên 0.65, sai tụt xuống 0.35)
        mastery = st.session_state.student_model["concept_mastery"].get(concept, 0.5)
        
        # Phân loại: Ngưỡng 0.6 là chuẩn xác để biết học sinh có làm đúng hay không
        if mastery >= 0.6:
            mastered.append(concept)
        else:
            needs_review.append(concept)

    # 1. Hiển thị nhóm Cần ôn tập (Ưu tiên đập vào mắt trước)
    if needs_review:
        st.markdown('<h3 style="font-family:\'Exo 2\',sans-serif;font-size:0.9rem;color:#ffca28;letter-spacing:0.15em">⚠️ KIẾN THỨC CHƯA NẮM VỮNG (CẦN ÔN LẠI)</h3>', unsafe_allow_html=True)
        for concept in needs_review:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid #1a3a5c">
                <span style="color:#ffca28;font-size:1.1rem">✗</span>
                <span style="font-size:0.95rem;color:#e8f4ff">{concept}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # 2. Hiển thị nhóm Đã nắm vững
    if mastered:
        st.markdown('<h3 style="font-family:\'Exo 2\',sans-serif;font-size:0.9rem;color:#00ff88;letter-spacing:0.15em">✅ KIẾN THỨC ĐÃ NẮM VỮNG</h3>', unsafe_allow_html=True)
        for concept in mastered:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid #1a3a5c">
                <span style="color:#00ff88;font-size:1.1rem">✓</span>
                <span style="font-size:0.95rem;color:#7eb8d4;opacity:0.8">{concept}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄  THỬ THẾ GIỚI KHÁC", type="primary", use_container_width=True):
            for k in ["selected_world","scenario_idx","user_answer","score","answered_scenarios","ai_chat_history","ai_done","show_explanation"]:
                st.session_state[k] = defaults[k]
            go("choose")
    with col2:
        # Nếu chơi lại, giữ nguyên Student Model để Adaptive Learning phát huy tác dụng
        if st.button("↩  ÔN TẬP LẠI THẾ GIỚI NÀY", use_container_width=True):
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
elif page == "Đào sâu Bản chất":  render_teach_ai()
elif page == "result":    render_result()
