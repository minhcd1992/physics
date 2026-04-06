import streamlit as st
import time

# ==========================================
# CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Physics Glitch - Lỗi Vật Lý",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# NỘI DUNG (KHÔNG DÙNG DATABASE / API NGOÀI)
# ==========================================
WORLDS = {
    "no_friction": {
        "name": "🧊 Thế Giới Trơn Trượt (Không Ma Sát)",
        "description": "Một thế giới nơi các bề mặt nhẵn bóng hoàn hảo. Mọi thứ không bao giờ ngừng trượt!",
        "scenarios": [
            {
                "statement": "Lỗi: Một chiếc xe đang chạy cuối cùng sẽ tự động dừng lại hoàn toàn, ngay cả khi không có bất kỳ lực ma sát hay lực cản của không khí nào.",
                "correct_answer": "Sai",
                "explanation": "Theo Định luật 1 Newton (Quán tính), một vật đang chuyển động sẽ tiếp tục chuyển động thẳng đều trừ khi có ngoại lực tác dụng. Không có ma sát hay lực cản không khí, chiếc xe sẽ trượt đi mãi mãi!",
                "ai_followup": "Tôi hiểu rồi! Vậy ma sát chính là thứ thường làm mọi thứ chậm lại. Bạn có thể cho ví dụ về lúc nào lực ma sát lại có ích trong đời sống không?"
            },
            {
                "statement": "Lỗi: Nếu bạn ném một quả bóng chày trong môi trường chân không, không có trọng lực và không có lực cản, nó sẽ bay chậm dần, từ từ cong xuống và dừng lại.",
                "correct_answer": "Sai",
                "explanation": "Không có trọng lực kéo nó xuống, và không có lực cản không khí để làm chậm nó, quả bóng sẽ di chuyển theo một đường thẳng hoàn hảo với tốc độ không đổi đến vô tận.",
                "ai_followup": "Thật thú vị! Nếu nó bay mãi mãi theo đường thẳng, thì cần điều kiện gì để nó có thể đổi hướng?"
            }
        ]
    },
    "high_gravity": {
        "name": "🪐 Hành Tinh Nặng Trĩu (Trọng Lực Lớn)",
        "description": "Một hành tinh khổng lồ nơi trọng lực kéo mọi thứ xuống với sức mạnh khủng khiếp.",
        "scenarios": [
            {
                "statement": "Lỗi: Nếu bạn thả rơi tự do một quả bóng bowling nặng và một chiếc lông chim nhẹ trong phòng chân không (không có không khí) trên hành tinh này, quả bóng bowling sẽ chạm đất nhanh hơn nhiều.",
                "correct_answer": "Sai",
                "explanation": "Trong chân không, mọi vật đều rơi với cùng một gia tốc bất kể khối lượng của chúng. Trọng lực lớn chỉ có nghĩa là cả hai rơi nhanh hơn so với trên Trái Đất, nhưng chúng vẫn chạm đất cùng một lúc!",
                "ai_followup": "Chà, khối lượng không ảnh hưởng đến tốc độ rơi trong chân không! Vậy tại sao trên Trái Đất, lông chim lại rơi chậm hơn quả bóng bowling?"
            },
            {
                "statement": "Lỗi: Vì trọng lực ở hành tinh này mạnh gấp 10 lần Trái Đất, nên khối lượng (mass) cơ thể bạn sẽ lớn gấp 10 lần so với khi ở Trái Đất.",
                "correct_answer": "Sai",
                "explanation": "Khối lượng là lượng vật chất tạo nên một vật và không bao giờ thay đổi theo vị trí. Trọng lượng (weight) mới là lực hấp dẫn tác dụng lên khối lượng đó. TRỌNG LƯỢNG của bạn tăng gấp 10 lần, nhưng KHỐI LƯỢNG của bạn vẫn giữ nguyên không đổi.",
                "ai_followup": "À, trọng lượng khác với khối lượng! Nếu tôi bay ra ngoài không gian sâu thẳm nơi hoàn toàn không có trọng lực, thì trọng lượng và khối lượng của tôi sẽ ra sao?"
            }
        ]
    },
    "energy_loss": {
        "name": "⚡ Hư Vô Năng Lượng (Không Bảo Toàn)",
        "description": "Một thế giới hỗn loạn nơi các quy luật năng lượng dường như bị phá vỡ.",
        "scenarios": [
            {
                "statement": "Lỗi: Nếu thả một quả bóng cao su có độ nảy hoàn hảo, nó có thể nảy lên cao hơn một chút so với vị trí được thả ban đầu, tự tạo ra thêm năng lượng từ hư vô.",
                "correct_answer": "Sai",
                "explanation": "Định luật Bảo toàn Năng lượng phát biểu rằng năng lượng không tự sinh ra hay mất đi. Một quả bóng không bao giờ nảy cao hơn vị trí thả ban đầu vì nó không thể tự tăng năng lượng. Thực tế, nó luôn mất đi một phần động năng dưới dạng âm thanh và nhiệt năng!",
                "ai_followup": "Không có năng lượng miễn phí, tôi hiểu rồi! Vậy chính xác thì phần năng lượng bị 'mất đi' đó đi đâu khi quả bóng nảy chậm dần rồi dừng hẳn?"
            },
            {
                "statement": "Lỗi: Một chiếc quạt điện đang cắm điện sẽ chuyển hóa 100% điện năng hoàn toàn thành động năng (gió) mà tuyệt đối không sinh ra bất kỳ dạng năng lượng nào khác.",
                "correct_answer": "Sai",
                "explanation": "Không có cỗ máy nào đạt hiệu suất 100%. Điện năng được chuyển thành động năng (làm quay cánh quạt), nhưng một lượng đáng kể luôn bị 'thất thoát' ra môi trường dưới dạng nhiệt năng do ma sát cơ học bên trong thiết bị.",
                "ai_followup": "Vậy là máy móc luôn tỏa nhiệt! Tại sao chúng ta không thể chế tạo ra một cỗ máy hoàn hảo với hiệu suất 100%?"
            }
        ]
    }
}

# ==========================================
# KHỞI TẠO TRẠNG THÁI (SESSION STATE)
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "Trang chủ"
if "selected_world" not in st.session_state:
    st.session_state.selected_world = None
if "current_scenario_idx" not in st.session_state:
    st.session_state.current_scenario_idx = 0
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "ai_response_shown" not in st.session_state:
    st.session_state.ai_response_shown = False

# ==========================================
# CÁC HÀM ĐIỀU HƯỚNG
# ==========================================
def navigate_to(page_name):
    st.session_state.page = page_name

def next_scenario():
    st.session_state.current_scenario_idx += 1
    st.session_state.user_answer = None
    st.session_state.ai_response_shown = False
    navigate_to("Tình huống")

def reset_game():
    st.session_state.selected_world = None
    st.session_state.current_scenario_idx = 0
    st.session_state.user_answer = None
    st.session_state.score = 0
    st.session_state.ai_response_shown = False
    navigate_to("Chọn Thế Giới")

# ==========================================
# THANH ĐIỀU HƯỚNG (SIDEBAR)
# ==========================================
def render_sidebar():
    st.sidebar.title("🌌 Physics Glitch")
    st.sidebar.markdown("---")
    
    pages = ["Trang chủ", "Chọn Thế Giới", "Tình huống", "Phân tích", "Dạy AI", "Kết quả"]
    
    selected_page = st.sidebar.radio(
        "Điều hướng", 
        pages, 
        index=pages.index(st.session_state.page)
    )
    
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    st.sidebar.markdown("---")
    
    if st.session_state.selected_world:
        st.sidebar.subheader("📊 Tiến trình của bạn")
        world_name = WORLDS[st.session_state.selected_world]["name"]
        st.sidebar.write(f"**Thế giới:** {world_name}")
        st.sidebar.write(f"**Tình huống:** {st.session_state.current_scenario_idx + 1} / 2")
        st.sidebar.write(f"**Điểm số:** {st.session_state.score}")

# ==========================================
# CÁC HÀM HIỂN THỊ TRANG
# ==========================================

def render_home():
    st.title("🌌 Physics Glitch")
    st.subheader("Hiểu Vật Lý Bằng Cách Tìm Lỗi Sai")
    st.markdown("""
    Chào mừng bạn đến với một vũ trụ nơi các định luật vật lý đã bị phá vỡ! 
    
    Nhiệm vụ của bạn là khám phá những thế giới bị lỗi này, xác định các sai lầm khoa học và dạy cho AI trên tàu của chúng ta cách vật lý thực sự hoạt động.
    
    **Cách bạn sẽ học tập:**
    1. 🛑 Trải nghiệm một khái niệm bị sai lệch.
    2. 🧠 Phân tích tư duy xem tại sao nó sai.
    3. 🗣️ Giải thích sự thật để củng cố kiến thức của bạn.
    """)
    st.write("")
    if st.button("🚀 Bắt đầu học ngay", type="primary"):
        navigate_to("Chọn Thế Giới")
        st.rerun()

def render_choose_world():
    st.title("🌍 Chọn một Thế Giới")
    st.write("Chọn một chiều không gian bị lỗi để tiến hành điều tra:")
    
    for world_key, world_data in WORLDS.items():
        with st.container():
            st.markdown(f"### {world_data['name']}")
            st.write(world_data['description'])
            if st.button(f"Tiến vào thế giới này", key=f"btn_{world_key}"):
                st.session_state.selected_world = world_key
                st.session_state.current_scenario_idx = 0
                st.session_state.score = 0
                navigate_to("Tình huống")
                st.rerun()
            st.markdown("---")

def render_scenario():
    if not st.session_state.selected_world:
        st.warning("Vui lòng chọn một thế giới trước!")
        st.button("Về trang Chọn Thế Giới", on_click=lambda: navigate_to("Chọn Thế Giới"))
        return

    world = WORLDS[st.session_state.selected_world]
    scenario = world["scenarios"][st.session_state.current_scenario_idx]
    
    st.caption(f"📍 {world['name']} | Tình huống {st.session_state.current_scenario_idx + 1} / 2")
    st.title("🧩 Phân tích Lỗi Sai")
    
    st.info(scenario["statement"])
    
    st.write("Theo khoa học thực tế, nhận định trên là Đúng hay Sai?")
    answer = st.radio("Lựa chọn của bạn:", ["Đúng", "Sai", "Không chắc chắn"], index=None)
    
    if st.button("Gửi phân tích", type="primary"):
        if answer:
            st.session_state.user_answer = answer
            navigate_to("Phân tích")
            st.rerun()
        else:
            st.error("Vui lòng chọn một câu trả lời trước khi gửi.")

def render_analysis():
    if not st.session_state.selected_world or not st.session_state.user_answer:
        st.warning("Vui lòng hoàn thành tình huống trước!")
        return

    world = WORLDS[st.session_state.selected_world]
    scenario = world["scenarios"][st.session_state.current_scenario_idx]
    
    st.title("📊 Kết quả Phân tích")
    
    is_correct = (st.session_state.user_answer == scenario["correct_answer"])
    
    if is_correct:
        st.success("✅ Tuyệt vời! Bạn đã phát hiện ra lỗi sai.")
    elif st.session_state.user_answer == "Không chắc chắn":
        st.warning("🤔 Không sao cả nếu bạn chưa chắc chắn! Hãy cùng xem lời giải thích khoa học dưới đây.")
    else:
        st.error(f"❌ Thực ra, nhận định vừa rồi là {scenario['correct_answer']}.")
    
    st.markdown("### Giải thích Khoa học:")
    st.write(scenario["explanation"])
    
    st.markdown("---")
    if st.button("Tiếp tục để Dạy AI 🧠", type="primary"):
        if is_correct and not st.session_state.ai_response_shown:
             st.session_state.score += 10 
        navigate_to("Dạy AI")
        st.rerun()

def render_teach_ai():
    if not st.session_state.selected_world:
        st.warning("Vui lòng hoàn thành tình huống trước!")
        return

    world = WORLDS[st.session_state.selected_world]
    scenario = world["scenarios"][st.session_state.current_scenario_idx]
    
    st.title("🤖 Dạy AI")
    st.write("AI đang cần sự giúp đỡ của bạn để hiểu khái niệm này. Hãy giải thích lại cho nó bằng ngôn từ của chính bạn.")
    
    user_explanation = st.text_area("Lời giải thích của bạn dành cho AI:", placeholder="Nhập lời giải thích của bạn vào đây...")
    
    if not st.session_state.ai_response_shown:
        if st.button("Gửi lời giải thích"):
            if len(user_explanation.strip()) < 5:
                st.error("Hãy viết dài thêm một chút để giúp AI thực sự hiểu nhé!")
            else:
                with st.spinner("AI đang xử lý lời giải thích của bạn..."):
                    time.sleep(1.5) 
                st.session_state.ai_response_shown = True
                st.rerun()
    
    if st.session_state.ai_response_shown:
        st.success("Đã gửi lời giải thích!")
        
        st.markdown("### Phản hồi từ AI:")
        st.info(f"**AI:** \"Cảm ơn bạn đã giải thích! {scenario['ai_followup']}\"")
        
        st.write("*(Hãy thử tự suy nghĩ về câu hỏi của AI để đào sâu hơn sự hiểu biết của mình nhé!)*")
        st.markdown("---")
        
        if st.session_state.current_scenario_idx < len(world["scenarios"]) - 1:
            if st.button("Tình huống tiếp theo ➡️", type="primary"):
                next_scenario()
        else:
            if st.button("Xem Kết Quả Cuối Cùng 🏆", type="primary"):
                navigate_to("Kết quả")
                st.rerun()

def render_result():
    st.title("🏆 Hoàn thành Nhiệm vụ!")
    
    st.markdown(f"### Bạn đã sửa chữa thành công các lỗi logic vật lý tại **{WORLDS[st.session_state.selected_world]['name']}**!")
    
    st.metric(label="Tổng Điểm", value=f"{st.session_state.score} / 20")
    
    if st.session_state.score == 20:
        st.success("🌟 Điểm tối đa! Bạn đúng là một bậc thầy về các khái niệm Vật Lý.")
    elif st.session_state.score == 10:
        st.warning("👍 Làm tốt lắm! Bạn đã tìm ra một số lỗi, nhưng vẫn còn không gian để học hỏi thêm.")
    else:
        st.error("📚 Những lỗi sai đã đánh lừa bạn! Hãy nhớ rằng khoa học chính là quá trình học hỏi từ những sai lầm.")
        
    st.markdown("### Những gì bạn đã học được:")
    st.write("- Rèn luyện tư duy phản biện bằng cách đặt câu hỏi về những nhận định sai lệch.")
    st.write("- Củng cố vững chắc kiến thức bằng cách dạy lại cho AI.")
    
    st.markdown("---")
    if st.button("🔄 Thử thách ở Thế Giới Khác", type="primary"):
        reset_game()

# ==========================================
# CHẠY ỨNG DỤNG
# ==========================================
def main():
    render_sidebar()
    
    if st.session_state.page == "Trang chủ":
        render_home()
    elif st.session_state.page == "Chọn Thế Giới":
        render_choose_world()
    elif st.session_state.page == "Tình huống":
        render_scenario()
    elif st.session_state.page == "Phân tích":
        render_analysis()
    elif st.session_state.page == "Dạy AI":
        render_teach_ai()
    elif st.session_state.page == "Kết quả":
        render_result()

if __name__ == "__main__":
    main()
