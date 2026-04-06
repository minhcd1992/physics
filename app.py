import streamlit as st
import google.generativeai as genai
import time

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
def progress_bar(value, max_val):
    pct = int((value / max_val) * 100)
    st.markdown(f"""
    <div class="prog-wrap">
        <div class="prog-fill" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)

def detect_misconception(user_answer, scenario):
    text = scenario["statement"].lower()
    # Phân tích dựa trên các từ khóa trong tình huống
    if "truyền thẳng" in text:
        return "Lỗi tư duy: Tin rằng ánh sáng không bao giờ bị bẻ cong (bỏ qua sự thay đổi môi trường)."
    if "vị trí thực tế" in text:
        return "Lỗi tư duy: Áp đặt trực giác đời thường, nhầm lẫn giữa ảnh ảo do khúc xạ tạo ra và vật thật."
    if "góc nghiêng lớn" in text:
        return "Lỗi tư duy: Chưa biết về hiện tượng Phản xạ toàn phần và góc tới hạn."
    if "tăng tốc độ" in text:
        return "Lỗi tư duy: Hiểu ngược mối quan hệ giữa chiết suất (n) và vận tốc truyền sáng (v)."
    if "nhuộm màu" in text:
        return "Lỗi tư duy: Hiểu sai bản chất ánh sáng trắng (cho rằng nó là đơn sắc)."
    if "chặn bớt ánh sáng" in text:
        return "Lỗi tư duy: Hiểu sai cơ chế tạo ảnh của thấu kính hội tụ (bỏ qua sự giao hội tia sáng)."
    
    return f"Lỗi tư duy: Nhầm lẫn cơ bản về {scenario['concept']}."

def render_svg_simulation(svg_type):
    """Hàm vẽ các mô phỏng hiện tượng khúc xạ bằng HTML/SVG"""
    
    if svg_type == "basic":
        # Khúc xạ cơ bản (Không khí -> Nước)
        svg = """
        <div style="background:#07101e; border: 1px solid #1a3a5c; border-radius: 8px; padding: 10px; margin-bottom: 1rem; text-align: center;">
            <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
              <rect x="0" y="100" width="400" height="100" fill="#00d4ff33" />
              <line x1="0" y1="100" x2="400" y2="100" stroke="#00d4ff" stroke-width="2" />
              <line x1="200" y1="20" x2="200" y2="180" stroke="#ffffff55" stroke-dasharray="5,5" />
              <line x1="50" y1="20" x2="200" y2="100" stroke="#ffca28" stroke-width="3" class="ray" />
              <line x1="200" y1="100" x2="350" y2="180" stroke="#ffffff33" stroke-width="1" stroke-dasharray="2,2" />
              <line x1="200" y1="100" x2="260" y2="180" stroke="#ffca28" stroke-width="3" class="ray" />
              <text x="10" y="90" fill="#ffffff" font-size="12" font-family="sans-serif">KHÔNG KHÍ (n1)</text>
              <text x="10" y="120" fill="#00d4ff" font-size="12" font-family="sans-serif">NƯỚC (n2 > n1)</text>
              <path d="M 180 89 A 20 20 0 0 1 200 80" fill="none" stroke="#ffca28" stroke-width="1"/>
              <path d="M 200 120 A 20 20 0 0 1 215 120" fill="none" stroke="#ffca28" stroke-width="1"/>
            </svg>
            <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Tia sáng bị bẻ cong về phía pháp tuyến khi đi vào môi trường đặc hơn.</div>
        </div>
        """
    elif svg_type == "depth":
        # Độ sâu ảo
        svg = """
        <div style="background:#07101e; border: 1px solid #1a3a5c; border-radius: 8px; padding: 10px; margin-bottom: 1rem; text-align: center;">
            <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
              <rect x="0" y="80" width="400" height="120" fill="#00d4ff33" />
              <line x1="0" y1="80" x2="400" y2="80" stroke="#00d4ff" stroke-width="2" />
              <circle cx="200" cy="180" r="10" fill="#ffca28" />
              <text x="220" y="185" fill="#ffffff" font-size="12" font-family="sans-serif">Vị trí thật</text>
              <circle cx="160" cy="120" r="10" fill="#ffca2855" class="pulse"/>
              <text x="180" y="125" fill="#00d4ff" font-size="12" font-family="sans-serif">Vị trí ảo (Mắt thấy)</text>
              <line x1="200" y1="180" x2="140" y2="80" stroke="#ffffff88" stroke-width="2" />
              <line x1="140" y1="80" x2="100" y2="20" stroke="#ffffff" stroke-width="2" class="ray" />
              <line x1="140" y1="80" x2="160" y2="120" stroke="#00d4ff88" stroke-dasharray="4,4" />
              <path d="M 80 10 Q 100 -5 120 10 Q 100 25 80 10 Z" fill="none" stroke="#ffffff" stroke-width="2"/>
              <circle cx="100" cy="10" r="4" fill="#ffffff" />
            </svg>
            <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Mắt nhìn theo đường thẳng kéo dài của tia khúc xạ tạo ra ảnh ảo.</div>
        </div>
        """
    elif svg_type == "total_reflection":
        # Phản xạ toàn phần
        svg = """
        <div style="background:#07101e; border: 1px solid #1a3a5c; border-radius: 8px; padding: 10px; margin-bottom: 1rem; text-align: center;">
            <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
              <rect x="0" y="100" width="400" height="100" fill="#00d4ff33" />
              <line x1="0" y1="100" x2="400" y2="100" stroke="#00d4ff" stroke-width="2" />
              <line x1="200" y1="20" x2="200" y2="180" stroke="#ffffff55" stroke-dasharray="5,5" />
              <circle cx="200" cy="180" r="6" fill="#ffca28" class="pulse"/>
              
              <line x1="200" y1="180" x2="180" y2="100" stroke="#ffffff55" stroke-width="1" />
              <line x1="180" y1="100" x2="150" y2="20" stroke="#ffffff55" stroke-width="1" />
              
              <line x1="200" y1="180" x2="250" y2="100" stroke="#ffffff88" stroke-width="2" />
              <line x1="250" y1="100" x2="380" y2="100" stroke="#ffffff88" stroke-width="2" />
              
              <line x1="200" y1="180" x2="280" y2="100" stroke="#ff4b4b" stroke-width="3" class="ray" />
              <line x1="280" y1="100" x2="360" y2="180" stroke="#ff4b4b" stroke-width="3" class="ray" />
              <text x="290" y="140" fill="#ff4b4b" font-size="12" font-family="sans-serif">Phản xạ toàn phần</text>
            </svg>
            <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Khi góc tới quá lớn, tia sáng không thể thoát ra ngoài môi trường.</div>
        </div>
        """
    elif svg_type == "prism":
        # Tán sắc qua lăng kính
        svg = """
        <div style="background:#07101e; border: 1px solid #1a3a5c; border-radius: 8px; padding: 10px; margin-bottom: 1rem; text-align: center;">
            <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
              <polygon points="200,40 120,160 280,160" fill="#ffffff11" stroke="#ffffff" stroke-width="2" />
              <line x1="50" y1="130" x2="160" y2="100" stroke="#ffffff" stroke-width="4" class="ray" />
              <text x="50" y="120" fill="#ffffff" font-size="10" font-family="sans-serif">Ánh sáng trắng</text>
              
              <line x1="160" y1="100" x2="240" y2="100" stroke="#ff4b4b" stroke-width="2" />
              <line x1="160" y1="100" x2="250" y2="115" stroke="#00ff88" stroke-width="2" />
              <line x1="160" y1="100" x2="260" y2="130" stroke="#9900ff" stroke-width="2" />
              
              <line x1="240" y1="100" x2="350" y2="60" stroke="#ff4b4b" stroke-width="2" class="ray"/>
              <line x1="250" y1="115" x2="350" y2="100" stroke="#00ff88" stroke-width="2" class="ray"/>
              <line x1="260" y1="130" x2="350" y2="140" stroke="#9900ff" stroke-width="2" class="ray"/>
              
              <text x="360" y="65" fill="#ff4b4b" font-size="10" font-family="sans-serif">ĐỎ (Ít lệch)</text>
              <text x="360" y="145" fill="#9900ff" font-size="10" font-family="sans-serif">TÍM (Lệch nhiều)</text>
            </svg>
            <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Lăng kính bẻ cong các tia màu khác nhau với mức độ khác nhau.</div>
        </div>
        """
    elif svg_type == "lens":
        # Thấu kính thiên văn
        svg = """
        <div style="background:#07101e; border: 1px solid #1a3a5c; border-radius: 8px; padding: 10px; margin-bottom: 1rem; text-align: center;">
            <svg viewBox="0 0 400 200" width="100%" style="max-width: 500px;">
              <line x1="0" y1="100" x2="400" y2="100" stroke="#ffffff55" stroke-dasharray="5,5" />
              <path d="M 200 40 Q 220 100 200 160 Q 180 100 200 40 Z" fill="#00d4ff33" stroke="#00d4ff" stroke-width="2" />
              
              <line x1="50" y1="60" x2="195" y2="60" stroke="#ffca28" stroke-width="2" class="ray" />
              <line x1="50" y1="100" x2="200" y2="100" stroke="#ffca28" stroke-width="2" class="ray" />
              <line x1="50" y1="140" x2="195" y2="140" stroke="#ffca28" stroke-width="2" class="ray" />
              
              <line x1="195" y1="60" x2="300" y2="100" stroke="#ffca28" stroke-width="2" class="ray" />
              <line x1="200" y1="100" x2="350" y2="100" stroke="#ffca28" stroke-width="2" class="ray" />
              <line x1="195" y1="140" x2="300" y2="100" stroke="#ffca28" stroke-width="2" class="ray" />
              
              <circle cx="300" cy="100" r="4" fill="#ff4b4b" class="pulse"/>
              <text x="290" y="85" fill="#ff4b4b" font-size="12" font-family="sans-serif">Tiêu điểm</text>
            </svg>
            <div style="color:#7eb8d4; font-size:0.85rem; margin-top:5px; font-family:'Be Vietnam Pro', sans-serif;">Mô phỏng: Vật kính hội tụ các tia sáng song song để tạo ảnh thật.</div>
        </div>
        """
    else:
        # Trống (Dành cho câu hỏi lý thuyết ko cần hình)
        svg = ""
        
    if svg:
        st.components.v1.html(svg, height=260)


# ==========================================
# DỮ LIỆU NỘI DUNG (CHỈ GIỮ LẠI THẾ GIỚI KHÚC XẠ)
# ==========================================
WORLDS = {
    "refraction_world": {
        "name": "Đại Dương Ảo Ảnh",
        "emoji": "🌊",
        "subtitle": "Khúc Xạ Ánh Sáng",
        "color": "#00d4ff",
        "css_class": "refraction",
        "badge_bg": "#00d4ff22",
        "badge_border": "#00d4ff55",
        "description": "Nơi ánh sáng bị bẻ cong khi bước qua ranh giới giữa các môi trường. Hãy cẩn thận, mắt bạn sẽ đánh lừa bạn!",
        "scenarios": [
            {
                "id": "re1",
                "concept": "Sự bẻ cong tia sáng",
                "statement": "🔴 TÌNH HUỐNG LỖI: Một tia sáng khi đi từ không khí vào mặt nước phẳng lặng sẽ luôn giữ nguyên đường thẳng ban đầu vì ánh sáng có tính chất truyền thẳng tuyệt đối trong mọi tình huống.",
                "correct_answer": "Sai",
                "explanation": "Ánh sáng chỉ truyền thẳng trong môi trường ĐỒNG TÍNH. Khi đi qua mặt phân cách giữa hai môi trường có chiết suất khác nhau (như không khí và nước), tốc độ ánh sáng thay đổi khiến tia sáng bị bẻ cong. Hiện tượng này gọi là khúc xạ.",
                "ai_context": "Học sinh hiểu sai về tính truyền thẳng của ánh sáng khi qua mặt phân cách. Concept: Khúc xạ là sự thay đổi phương truyền do thay đổi tốc độ ánh sáng giữa 2 môi trường.",
                "svg_type": "basic"
            },
            {
                "id": "re2",
                "concept": "Độ sâu ảo (Apparent Depth)",
                "statement": "🔴 TÌNH HUỐNG LỖI: Khi bạn nhìn một đồng xu dưới đáy hồ bơi, vị trí bạn nhìn thấy chính là vị trí thực tế của đồng xu đó. Mắt con người luôn nhìn thấy vật thể đúng nơi chúng tọa lạc.",
                "correct_answer": "Sai",
                "explanation": "Do hiện tượng khúc xạ, các tia sáng từ đồng xu dưới nước khi đi ra ngoài không khí sẽ bị lệch xa pháp tuyến hơn. Mắt người có thói quen nội suy ngược tia sáng theo đường thẳng, khiến chúng ta thấy một 'ảnh ảo' của đồng xu nằm nông hơn vị trí thật sự của nó dưới đáy hồ.",
                "ai_context": "Học sinh nhầm lẫn giữa ảnh ảo và vật thật dưới nước. Concept: Ảnh ảo nằm cao hơn (nông hơn) vật thật khi nhìn từ môi trường chiết suất thấp vào môi trường chiết suất cao.",
                "svg_type": "depth"
            },
            {
                "id": "re3",
                "concept": "Phản xạ toàn phần",
                "statement": "🔴 TÌNH HUỐNG LỖI: Một bóng đèn đặt dưới đáy bể bơi có thể chiếu tia sáng thoát ra ngoài không khí theo MỌI HƯỚNG, bất kể bạn chiếu góc nghiêng gắt đến mức nào đi chăng nữa.",
                "correct_answer": "Sai",
                "explanation": "Khi tia sáng truyền từ môi trường chiết suất LỚN (nước) sang môi trường chiết suất NHỎ (không khí), nếu góc tới vượt quá một giá trị gọi là 'góc tới hạn', tia sáng sẽ KHÔNG THỂ thoát ra ngoài mà bị phản xạ ngược trở lại hoàn toàn vào trong nước. Hiện tượng này gọi là Phản xạ toàn phần.",
                "ai_context": "Học sinh chưa biết về góc tới hạn và hiện tượng phản xạ toàn phần. Concept: Phản xạ toàn phần chỉ xảy ra khi ánh sáng đi từ môi trường đặc sang loãng và góc tới vượt ngưỡng.",
                "svg_type": "total_reflection"
            },
            {
                "id": "re4",
                "concept": "Chiết suất và Vận tốc",
                "statement": "🔴 TÌNH HUỐNG LỖI: Chiết suất của kim cương rất lớn (n ≈ 2.4). Điều này có nghĩa là ánh sáng khi bay vào bên trong viên kim cương sẽ tăng tốc và di chuyển nhanh gấp 2.4 lần so với khi bay trong chân không.",
                "correct_answer": "Sai",
                "explanation": "Ngược lại hoàn toàn! Chiết suất của một môi trường tỷ lệ NGHỊCH với tốc độ ánh sáng trong môi trường đó ($n = c/v$). Chiết suất càng lớn, ánh sáng di chuyển càng chậm. Trong kim cương, ánh sáng bị 'hãm' lại chỉ còn khoảng 124.000 km/s (thay vì 300.000 km/s). Sự chậm trễ này khiến nó bị khúc xạ cực mạnh, tạo ra vẻ lấp lánh.",
                "ai_context": "Học sinh nhầm lẫn mối quan hệ giữa chiết suất và vận tốc ánh sáng. Concept: Môi trường có chiết suất n càng lớn thì vận tốc truyền sáng v càng nhỏ.",
                "svg_type": "none"
            },
            {
                "id": "re5",
                "concept": "Sự Tán sắc ánh sáng",
                "statement": "🔴 TÌNH HUỐNG LỖI: Ánh sáng trắng từ mặt trời là một màu đơn sắc. Khi đi qua một lăng kính thủy tinh, chất liệu thủy tinh đặc biệt của lăng kính đã tự động nhuộm màu cho tia sáng để tạo ra bảy sắc cầu vồng.",
                "correct_answer": "Sai",
                "explanation": "Lăng kính không tự nhuộm màu. Bản thân ánh sáng trắng đã là hỗn hợp của vô số dải màu. Vì mỗi màu có một chiết suất khác nhau đối với thủy tinh (màu tím bị bẻ cong nhiều nhất, màu đỏ ít nhất), lăng kính chỉ làm nhiệm vụ 'tách' các tia màu vốn đã có sẵn này ra thành các góc khác nhau, gọi là hiện tượng tán sắc.",
                "ai_context": "Học sinh hiểu sai bản chất ánh sáng trắng. Concept: Tán sắc là do chiết suất của môi trường phụ thuộc vào màu sắc (bước sóng) của ánh sáng.",
                "svg_type": "prism"
            },
            {
                "id": "re6",
                "concept": "Thấu kính thiên văn",
                "statement": "🔴 TÌNH HUỐNG LỖI: Để kính thiên văn có thể phóng đại những hành tinh xa xôi, vật kính (thấu kính ở đầu kính) đơn thuần là một tấm kính phẳng có đục một lỗ tròn nhỏ để giới hạn lượng ánh sáng đi vào mắt.",
                "correct_answer": "Sai",
                "explanation": "Một kính phẳng không có khả năng tạo ảnh. Vật kính của kính thiên văn phải là một THẤU KÍNH HỘI TỤ (mặt lồi). Lợi dụng hiện tượng khúc xạ, độ cong của thấu kính bẻ cong đồng loạt các tia sáng song song chiếu tới từ các vì sao xa xôi, hội tụ chúng lại tại tiêu điểm để tạo ra một ảnh thật, sau đó dùng thị kính để phóng đại ảnh đó lên.",
                "ai_context": "Học sinh hiểu sai cơ chế tạo ảnh của thấu kính. Concept: Thấu kính hội tụ sử dụng sự khúc xạ qua bề mặt cong để bẻ gãy và gom tia sáng về một điểm.",
                "svg_type": "lens"
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
    "scenario_idx": 0,          # Dùng để đếm xem đang ở câu thứ mấy
    "current_sc_id": None,      # ID của tình huống hiện tại (phục vụ adaptive)
    "user_answer": None,
    "score": 0,
    "answered_scenarios": set(),
    "ai_chat_history": [],
    "ai_done": False,
    "show_explanation": False,
    # THÊM BỘ NÃO AI (MEMORY LAYER)
    "student_model": {
        "concept_mastery": {},   # Điểm số hiểu biết từng khái niệm (-1 đến 1)
        "mistakes": [],          # Lịch sử sai lầm cụ thể
    }
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
    if "svg_type" in scenario and scenario["svg_type"] != "none":
        render_svg_simulation(scenario["svg_type"])

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
                
                # KIỂM TRA VÀ CẬP NHẬT STUDENT MODEL
                if clean == scenario["correct_answer"]:
                    # Cộng điểm nếu đúng, tối đa là 1.0
                    st.session_state.student_model["concept_mastery"][concept] = min(1.0, st.session_state.student_model["concept_mastery"][concept] + 0.2)
                    if scenario["id"] not in st.session_state.answered_scenarios:
                        st.session_state.score += 10
                else:
                    # Trừ điểm nếu sai, tối thiểu là 0.0
                    st.session_state.student_model["concept_mastery"][concept] = max(0.0, st.session_state.student_model["concept_mastery"][concept] - 0.3)
                    # Ghi nhận sai lầm vào lịch sử
                    mistake_type = detect_misconception(clean, scenario)
                    st.session_state.student_model["mistakes"].append({
                        "concept": concept,
                        "type": mistake_type,
                        "user_chose": clean
                    })

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
                    
                    # Chuẩn bị dữ liệu học sinh dạng chuỗi để đưa cho AI
                    student_data = f"""
                    - Lịch sử sai lầm: {[m['type'] for m in st.session_state.student_model['mistakes'][-3:]]} 
                    - Điểm nắm vững kiến thức này (0-1.0): {st.session_state.student_model['concept_mastery'].get(scenario['concept'], 0.5)}
                    """

                    # 2. Prompt hợp nhất: Giao quyền tự quyết & Đưa bộ nhớ vào
                    system_prompt = f"""Bạn là một Gia sư AI cá nhân hóa chuyên Vật lý.
Context bài học hiện tại: {scenario['ai_context']}

--- DỮ LIỆU NHẬN THỨC CỦA HỌC SINH NÀY ---
{student_data}
------------------------------------------

Đây là lượt chat thứ {user_turns}.
Nhiệm vụ của bạn:
1. Đọc kỹ lời giảng của học sinh. PHẢI CĂN CỨ VÀO DỮ LIỆU NHẬN THỨC Ở TRÊN:
   - Nếu học sinh từng có "Lịch sử sai lầm" liên quan: Hãy đặt câu hỏi xoáy sâu vào chính sai lầm đó để xem họ thực sự hiểu chưa.
   - Nếu "Điểm nắm vững" thấp (<0.5): Giải thích bằng ngôn ngữ cực kỳ đời thường, đưa ví dụ thực tế gần gũi.
   - Nếu "Điểm nắm vững" cao (>0.8): Hãy hỏi một câu mở rộng, nâng cao, hoặc đố mẹo.
2. Nếu lời giảng CHƯA ĐỦ RÕ: Hãy hỏi THÊM 1 câu hỏi phụ gợi mở (ngắn gọn 2-3 câu). Tuyệt đối KHÔNG dùng từ khóa bí mật.
3. Nếu học sinh giải thích RẤT CHÍNH XÁC hoặc bảo "không biết/chịu thua": 
   - Tóm tắt lại kiến thức một cách thân thiện.
   - BẮT BUỘC chèn cụm từ [ĐÃ_HIỂU] vào cuối câu.
4. Lượt chat thứ 5 bắt buộc phải chốt vấn đề và dùng cụm từ [ĐÃ_HIỂU]."""

                    # 3. Gọi API Gemini
                    if has_api:
                        with st.spinner("AI đang suy nghĩ..."):
                            try:
                                # Sử dụng dòng model cực nhanh và hạn mức cao để tránh lỗi 429
                                model = genai.GenerativeModel(
                                    model_name="gemini-2.0-flash-lite",
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

    # Nhận xét
    if pct == 100:
        st.markdown('<div class="badge-correct" style="display:block;text-align:center;padding:0.8rem">🌟 HOÀN HẢO — Bạn là bậc thầy quang học!</div>', unsafe_allow_html=True)
        msg = "Xuất sắc! Bạn đã phát hiện tất cả lỗi sai và hiểu bản chất hiện tượng khúc xạ thật sự."
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
elif page == "Đào sâu Bản chất":  render_teach_ai()
elif page == "result":    render_result()
