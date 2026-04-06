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
# CSS TOÀN CỤC & ANIMATION
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;600&family=Exo+2:wght@400;700;900&display=swap');

html, body, [data-testid="stApp"] {
    background: #03040a !important;
    color: #e8f4ff !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #0a102e 0%, #03040a 60%) !important;
}
.block-container { padding: 2rem 1.5rem 4rem !important; max-width: 800px !important; }

h1, h2, h3 { font-family: 'Exo 2', sans-serif !important; }
p, label, span, div { font-family: 'Be Vietnam Pro', sans-serif !important; }

.hero-title {
    font-size: clamp(2.5rem, 8vw, 4rem);
    font-weight: 900;
    color: #00d4ff;
    text-shadow: 0 0 20px #00d4ff55;
    text-align: center;
    margin-bottom: 0.5rem;
}

.glitch-card {
    background: rgba(13, 17, 23, 0.8);
    border: 1px solid #1a3a5c;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-top: 2px solid #00d4ff;
}

.scenario-box {
    background: #07101e;
    border-left: 4px solid #ff4b4b;
    padding: 1.2rem;
    font-size: 1.1rem;
    margin: 1rem 0;
}

.explain-box {
    background: #071c10;
    border-left: 4px solid #00ff88;
    padding: 1.2rem;
    color: #b8ffe0;
    margin: 1rem 0;
}

.ai-bubble {
    background: #0d1a2e;
    border: 1px solid #00d4ff33;
    padding: 1rem;
    border-radius: 12px 12px 12px 0;
    margin: 0.8rem 0;
}

.user-bubble {
    background: #0f1f10;
    border: 1px solid #00ff8833;
    padding: 1rem;
    border-radius: 12px 12px 0 12px;
    margin: 0.8rem 0;
}

/* Animation cho SVG */
@keyframes ray-flow {
  to { stroke-dashoffset: -20; }
}
.ray {
  stroke-dasharray: 10, 5;
  animation: ray-flow 1s linear infinite;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# THẾ GIỚI DUY NHẤT: KHÚC XẠ ÁNH SÁNG
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
                "statement": "🔴 TÌNH HUỐNG LỖI: Một tia sáng khi đi từ không khí vào nước sẽ luôn giữ nguyên đường thẳng ban đầu vì ánh sáng có tính chất truyền thẳng tuyệt đối trong mọi tình huống.",
                "correct_answer": "Sai",
                "explanation": "Ánh sáng chỉ truyền thẳng trong môi trường ĐỒNG TÍNH. Khi đi qua mặt phân cách giữa hai môi trường có chiết suất khác nhau (như không khí và nước), tốc độ ánh sáng thay đổi khiến tia sáng bị bẻ cong. Đây gọi là hiện tượng khúc xạ.",
                "ai_context": "Học sinh hiểu sai về tính truyền thẳng của ánh sáng khi qua mặt phân cách. Concept: Khúc xạ là sự thay đổi phương truyền do thay đổi tốc độ.",
                "svg_type": "basic"
            },
            {
                "id": "re2",
                "concept": "Độ sâu ảo (Apparent Depth)",
                "statement": "🔴 TÌNH HUỐNG LỖI: Khi bạn nhìn một đồng xu dưới đáy hồ, vị trí bạn nhìn thấy chính là vị trí thực tế của đồng xu đó. Mắt con người luôn nhìn thấy vật thể đúng nơi chúng tọa lạc.",
                "correct_answer": "Sai",
                "explanation": "Do hiện tượng khúc xạ, các tia sáng từ đồng xu khi đi từ nước ra không khí bị lệch xa pháp tuyến. Mắt ta theo thói quen kéo dài tia sáng theo đường thẳng, khiến đồng xu trông như nằm 'nông' hơn so với thực tế.",
                "ai_context": "Học sinh nhầm lẫn giữa ảnh ảo và vật thật dưới nước. Concept: Ảnh ảo nằm cao hơn vật thật khi nhìn từ môi trường chiết suất thấp vào môi trường chiết suất cao.",
                "svg_type": "depth"
            },
            {
                "id": "re3",
                "concept": "Phản xạ toàn phần",
                "statement": "🔴 TÌNH HUỐNG LỖI: Ánh sáng luôn luôn có thể đi từ nước ra ngoài không khí, bất kể bạn chiếu tia sáng với góc nghiêng lớn đến mức nào đi chăng nữa.",
                "correct_answer": "Sai",
                "explanation": "Khi góc tới vượt quá một giá trị gọi là 'góc tới hạn', tia sáng không thể thoát ra ngoài mà bị phản xạ ngược trở lại hoàn toàn vào trong nước. Hiện tượng này gọi là Phản xạ toàn phần, là nền tảng của cáp quang internet ngày nay.",
                "ai_context": "Học sinh chưa biết về góc tới hạn. Concept: Phản xạ toàn phần xảy ra khi đi từ môi trường chiết suất cao sang thấp với góc tới lớn hơn góc tới hạn.",
                "svg_type": "total_reflection"
            },
            {
                "id": "re4",
                "concept": "Chiết suất và Tốc độ",
                "statement": "🔴 TÌNH HUỐNG LỖI: Chiết suất của kim cương rất lớn (n ≈ 2.4). Điều này có nghĩa là ánh sáng khi đi vào kim cương sẽ tăng tốc độ và di chuyển nhanh hơn so với khi ở trong chân không.",
                "correct_answer": "Sai",
                "explanation": "Ngược lại! Chiết suất tỷ lệ nghịch với tốc độ ($n = c/v$). Chiết suất càng lớn, ánh sáng di chuyển càng chậm. Trong kim cương, ánh sáng bị 'hãm' lại chỉ còn khoảng 124.000 km/s, khiến nó bị khúc xạ cực mạnh, tạo nên sự lấp lánh đặc trưng.",
                "ai_context": "Học sinh nhầm lẫn mối quan hệ giữa chiết suất và vận tốc. Concept: n lớn thì v nhỏ.",
                "svg_type": "speed"
            },
            {
                "id": "re5",
                "concept": "Tán sắc ánh sáng",
                "statement": "🔴 TÌNH HUỐNG LỖI: Ánh sáng trắng là đơn sắc. Khi đi qua lăng kính, lăng kính tự nhuộm màu cho tia sáng để tạo ra bảy sắc cầu vồng.",
                "correct_answer": "Sai",
                "explanation": "Lăng kính không tự nhuộm màu. Ánh sáng trắng là hỗn hợp của nhiều màu. Mỗi màu có chiết suất khác nhau (màu tím bị bẻ cong nhiều nhất, màu đỏ ít nhất). Lăng kính chỉ làm 'tách' các màu có sẵn này ra bằng hiện tượng tán sắc.",
                "ai_context": "Học sinh hiểu sai bản chất ánh sáng trắng. Concept: Tán sắc là do chiết suất của môi trường phụ thuộc vào màu sắc (bước sóng).",
                "svg_type": "prism"
            },
            {
                "id": "re6",
                "concept": "Thấu kính thiên văn (Sở thích của bạn Minh)",
                "statement": "🔴 TÌNH HUỐNG LỖI: Để một kính thiên văn khúc xạ phóng đại vật thể lớn hơn, thấu kính hội tụ (vật kính) chỉ đơn giản là chặn bớt ánh sáng lại để mắt tập trung nhìn vào tâm.",
                "correct_answer": "Sai",
                "explanation": "Thấu kính phóng đại dựa trên việc bẻ cong đồng loạt các tia sáng từ vật ở xa, hội tụ chúng lại tại một điểm tiêu điểm. Sự khúc xạ có tính toán qua độ cong của bề mặt thấu kính mới là thứ tạo nên ảnh phóng đại, không phải do chặn ánh sáng.",
                "ai_context": "Học sinh hiểu sai cơ chế thấu kính. Concept: Thấu kính hội tụ bẻ cong tia sáng song song về tiêu điểm nhờ sự thay đổi độ dày mặt kính.",
                "svg_type": "lens"
            }
        ]
    }
}

# ==========================================
# HELPERS & MÔ PHỎNG SVG
# ==========================================
def render_svg_simulation(type):
    if type == "basic":
        svg = """
        <svg viewBox="0 0 400 200" width="100%">
          <rect x="0" y="100" width="400" height="100" fill="#00d4ff33" />
          <line x1="0" y1="100" x2="400" y2="100" stroke="#00d4ff" stroke-width="2" />
          <line x1="200" y1="50" x2="200" y2="150" stroke="#ffffff55" stroke-dasharray="5,5" />
          <line x1="50" y1="20" x2="200" y2="100" stroke="#ff4b4b" stroke-width="3" class="ray" />
          <line x1="200" y1="100" x2="280" y2="180" stroke="#ff4b4b" stroke-width="3" class="ray" />
          <text x="10" y="90" fill="#ffffff" font-size="12">KHÔNG KHÍ</text>
          <text x="10" y="120" fill="#00d4ff" font-size="12">NƯỚC (Bị bẻ cong!)</text>
        </svg>
        """
    elif type == "prism":
        svg = """
        <svg viewBox="0 0 400 200" width="100%">
          <polygon points="200,40 120,160 280,160" fill="none" stroke="#ffffff" stroke-width="2" />
          <line x1="50" y1="130" x2="160" y2="100" stroke="#ffffff" stroke-width="3" class="ray" />
          <line x1="240" y1="100" x2="350" y2="60" stroke="#ff0000" stroke-width="2" />
          <line x1="240" y1="100" x2="350" y2="140" stroke="#9900ff" stroke-width="2" />
          <text x="360" y="65" fill="#ff0000" font-size="10">ĐỎ</text>
          <text x="360" y="145" fill="#9900ff" font-size="10">TÍM</text>
        </svg>
        """
    else:
        svg = """<svg viewBox="0 0 400 50" width="100%"><text x="100" y="30" fill="#ffffff55">Mô phỏng đang tải...</text></svg>"""
    
    st.components.v1.html(svg, height=220)

def detect_misconception(user_answer, scenario):
    text = scenario["statement"].lower()
    if "truyền thẳng" in text: return "Lỗi: Tin rằng ánh sáng không bao giờ bị bẻ cong."
    if "vị trí thực tế" in text: return "Lỗi: Nhầm lẫn giữa ảnh ảo và vật thật."
    if "nhuộm màu" in text: return "Lỗi: Chưa hiểu bản chất ánh sáng trắng là đa sắc."
    return "Lỗi: Chưa nắm rõ quy luật khúc xạ."

# ==========================================
# KHỞI TẠO SESSION STATE
# ==========================================
defaults = {
    "page": "home",
    "selected_world": "refraction_world",
    "scenario_idx": 0,
    "user_answer": None,
    "score": 0,
    "answered_scenarios": set(),
    "ai_chat_history": [],
    "ai_done": False,
    "student_model": {"concept_mastery": {}, "mistakes": []}
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()

# ==========================================
# GIAO DIỆN TRANG CHỦ
# ==========================================
def render_home():
    st.markdown('<h1 class="hero-title">ĐẠI DƯƠNG ẢO ẢNH</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#7eb8d4; font-size:1.2rem">Thế giới chuyên sâu về Khúc xạ ánh sáng</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glitch-card">
        Chào bạn Minh! Trong thế giới này, chúng ta sẽ tập trung phá vỡ những lầm tưởng về cách ánh sáng di chuyển. 
        Mỗi tình huống sẽ đi kèm một mô phỏng trực quan để bạn "nhìn tận mắt" lỗi sai của vũ trụ này.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 BẮT ĐẦU HIỆU CHỈNH", type="primary", use_container_width=True):
        go("scenario")

# ==========================================
# TRANG TÌNH HUỐNG (ADAPTIVE)
# ==========================================
def render_scenario():
    wd = WORLDS["refraction_world"]
    total = len(wd["scenarios"])
    idx = st.session_state.scenario_idx
    scenario = wd["scenarios"][idx]

    current_step = len(st.session_state.answered_scenarios) + 1
    st.markdown(f"### 📍 Tình huống {current_step}/{total}")
    
    # Mô phỏng ban đầu
    render_svg_simulation(scenario.get("svg_type", "basic"))
    
    st.markdown(f'<div class="scenario-box">{scenario["statement"]}</div>', unsafe_allow_html=True)
    
    answer = st.radio("Đánh giá của bạn:", ["Đúng", "Sai", "Không chắc chắn"], index=None)
    
    if st.button("⚡ GỬI PHÂN TÍCH", type="primary", use_container_width=True):
        if answer:
            st.session_state.user_answer = answer
            # Cập nhật Mastery
            concept = scenario["concept"]
            if concept not in st.session_state.student_model["concept_mastery"]:
                st.session_state.student_model["concept_mastery"][concept] = 0.5
            
            if answer == scenario["correct_answer"]:
                st.session_state.student_model["concept_mastery"][concept] += 0.2
                st.session_state.score += 10
            else:
                st.session_state.student_model["concept_mastery"][concept] -= 0.3
                st.session_state.student_model["mistakes"].append({"concept": concept, "type": detect_misconception(answer, scenario)})
            
            st.session_state.answered_scenarios.add(scenario["id"])
            go("analysis")
        else:
            st.error("Chọn một đáp án!")

# ==========================================
# TRANG PHÂN TÍCH
# ==========================================
def render_analysis():
    wd = WORLDS["refraction_world"]
    scenario = wd["scenarios"][st.session_state.scenario_idx]
    
    st.markdown("### 📊 Kết quả phân tích")
    if st.session_state.user_answer == scenario["correct_answer"]:
        st.success("✅ Chính xác! Bạn đã nhìn thấu ảo ảnh.")
    else:
        st.error(f"❌ Sai lầm! Đáp án đúng là: {scenario['correct_answer']}")
    
    st.markdown(f'<div class="explain-box"><strong>GIẢI THÍCH:</strong><br>{scenario["explanation"]}</div>', unsafe_allow_html=True)
    
    if st.button("🤖 ĐÀO SÂU BẢN CHẤT →", type="primary", use_container_width=True):
        go("Phản biện")

# ==========================================
# TRANG PHẢN BIỆN (AI)
# ==========================================
def render_teach_ai():
    scenario = WORLDS["refraction_world"]["scenarios"][st.session_state.scenario_idx]
    
    # Client Gemini
    key = st.secrets.get("GEMINI_API_KEY") or st.session_state.get("_temp_key")
    if key: genai.configure(api_key=key)

    st.markdown(f"### 🤖 Phản biện về: {scenario['concept']}")
    
    for msg in st.session_state.ai_chat_history:
        role = "ai-bubble" if msg["role"] == "assistant" else "user-bubble"
        st.markdown(f'<div class="{role}">{msg["content"]}</div>', unsafe_allow_html=True)

    if not st.session_state.ai_done:
        user_input = st.text_area("Giải thích của bạn:", placeholder="Tại sao hiện tượng này lại xảy ra?")
        if st.button("📡 GỬI CHO AI", type="primary"):
            st.session_state.ai_chat_history.append({"role": "user", "content": user_input})
            user_turns = sum(1 for m in st.session_state.ai_chat_history if m["role"] == "user")
            
            # Prompt cá nhân hóa
            mastery = st.session_state.student_model["concept_mastery"].get(scenario["concept"], 0.5)
            system_prompt = f"""Bạn là gia sư vật lý. Học sinh này có Mastery={mastery}. 
            Nếu Mastery thấp, hãy giải thích cực kỳ đơn giản. Nếu cao, hãy đố mẹo.
            Nhiệm vụ: Thảo luận về {scenario['concept']}.
            Kết thúc và thêm [ĐÃ_HIỂU] nếu học sinh giải thích đúng hoặc sau 3 lượt."""

            if key:
                model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite", system_instruction=system_prompt)
                response = model.generate_content([m["content"] for m in st.session_state.ai_chat_history])
                reply = response.text
            else:
                reply = "AI đang offline, nhưng bạn giải thích rất tốt! [ĐÃ_HIỂU]"

            if "[ĐÃ_HIỂU]" in reply:
                st.session_state.ai_done = True
                reply = reply.replace("[ĐÃ_HIỂU]", "")
            
            st.session_state.ai_chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
    else:
        if st.button("⚡ TÌNH HUỐNG TIẾP THEO", type="primary", use_container_width=True):
            unanswered = [sc for sc in WORLDS["refraction_world"]["scenarios"] if sc["id"] not in st.session_state.answered_scenarios]
            if unanswered:
                unanswered.sort(key=lambda x: st.session_state.student_model["concept_mastery"].get(x["concept"], 0.5))
                st.session_state.scenario_idx = WORLDS["refraction_world"]["scenarios"].index(unanswered[0])
                st.session_state.ai_chat_history, st.session_state.ai_done = [], False
                go("scenario")
            else:
                go("result")

# ==========================================
# TRANG KẾT QUẢ
# ==========================================
def render_result():
    st.title("🏆 Hoàn thành khóa học!")
    st.metric("Tổng điểm", f"{st.session_state.score}/60")
    st.write("Dữ liệu sai lầm đã lưu:", st.session_state.student_model["mistakes"])
    if st.button("🔄 Chơi lại", type="primary"):
        for k, v in defaults.items(): st.session_state[k] = v
        go("home")

# ==========================================
# ROUTER
# ==========================================
page = st.session_state.page
if page == "home": render_home()
elif page == "scenario": render_scenario()
elif page == "analysis": render_analysis()
elif page == "Phản biện": render_teach_ai()
elif page == "result": render_result()
