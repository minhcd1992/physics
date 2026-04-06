import streamlit as st
import time

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Physics Glitch",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# HARDCODED CONTENT (NO DATABASE / EXTERNAL API)
# ==========================================
WORLDS = {
    "no_friction": {
        "name": "🧊 The Slippery Realm (No Friction)",
        "description": "A world where surfaces are perfectly smooth. Things never stop sliding!",
        "scenarios": [
            {
                "statement": "Glitch Statement: A moving car will eventually stop completely on its own, even if there is absolutely zero friction or air resistance.",
                "correct_answer": "Incorrect",
                "explanation": "According to Newton's First Law (Inertia), an object in motion stays in motion at a constant velocity unless acted upon by an external force. Without friction or air resistance, the car glides forever!",
                "ai_followup": "I understand now! So friction is what usually slows things down. What are some examples of friction acting as a helpful force in our daily lives?"
            },
            {
                "statement": "Glitch Statement: If you throw a baseball in a vacuum with zero gravity and zero friction, it will slowly curve downward and lose speed.",
                "correct_answer": "Incorrect",
                "explanation": "Without gravity to pull it down, and without friction (air resistance) to slow it down, the baseball will travel in a perfectly straight line at a constant speed infinitely.",
                "ai_followup": "Fascinating! If it travels forever in a straight line, what exactly would it take to change its direction?"
            }
        ]
    },
    "high_gravity": {
        "name": "🪐 The Heavy Planet (High Gravity)",
        "description": "A massive planet where gravity pulls everything down with incredible force.",
        "scenarios": [
            {
                "statement": "Glitch Statement: If you drop a heavy bowling ball and a light feather in a vacuum room (no air) on this high gravity planet, the heavy bowling ball will hit the ground much faster.",
                "correct_answer": "Incorrect",
                "explanation": "In a vacuum, all objects fall at the exact same rate of acceleration regardless of their mass. The high gravity just means they both fall faster than they would on Earth, but they still hit the ground at the exact same time!",
                "ai_followup": "Wow, mass doesn't affect fall speed in a vacuum! Then why does a feather fall slower than a bowling ball here on Earth?"
            },
            {
                "statement": "Glitch Statement: Because the gravity is 10 times stronger here, your body's mass will be 10 times larger than it is on Earth.",
                "correct_answer": "Incorrect",
                "explanation": "Mass is the amount of matter in an object and never changes based on location. Weight is the force of gravity acting on that mass. Your WEIGHT increases by 10x, but your MASS stays exactly the same.",
                "ai_followup": "Ah, weight vs mass! If I go to deep space where there is zero gravity, what happens to my weight and my mass?"
            }
        ]
    },
    "energy_loss": {
        "name": "⚡ The Energy Void (No Energy Conservation)",
        "description": "A chaotic world where energy rules seem to be broken.",
        "scenarios": [
            {
                "statement": "Glitch Statement: If a perfectly bouncy rubber ball is dropped, it can bounce back slightly higher than the point it was dropped from, creating extra energy out of nowhere.",
                "correct_answer": "Incorrect",
                "explanation": "The Law of Conservation of Energy states energy cannot be created or destroyed. A ball can never bounce higher than its initial drop height because it cannot gain energy. In reality, it always loses some kinetic energy to sound and heat!",
                "ai_followup": "No free energy, got it! Where exactly does the 'lost' energy go when a bouncing ball eventually comes to a complete stop?"
            },
            {
                "statement": "Glitch Statement: A plug-in electric fan converts 100% of its electrical energy purely into kinetic energy (wind) with absolutely zero other byproducts.",
                "correct_answer": "Incorrect",
                "explanation": "No machine is 100% efficient. Electrical energy is converted into kinetic energy (moving the blades), but a significant amount is always 'lost' to the environment as thermal energy (heat) due to internal mechanical friction.",
                "ai_followup": "So machines always produce some heat! Why is it impossible for us to invent a machine that is perfectly 100% efficient?"
            }
        ]
    }
}

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "Home"
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
# NAVIGATION HELPER FUNCTIONS
# ==========================================
def navigate_to(page_name):
    st.session_state.page = page_name

def next_scenario():
    st.session_state.current_scenario_idx += 1
    st.session_state.user_answer = None
    st.session_state.ai_response_shown = False
    navigate_to("Scenario")

def reset_game():
    st.session_state.selected_world = None
    st.session_state.current_scenario_idx = 0
    st.session_state.user_answer = None
    st.session_state.score = 0
    st.session_state.ai_response_shown = False
    navigate_to("Choose World")

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
def render_sidebar():
    st.sidebar.title("🌌 Physics Glitch")
    st.sidebar.markdown("---")
    
    # Navigation menu
    pages = ["Home", "Choose World", "Scenario", "Analysis", "Teach the AI", "Result"]
    
    # We use radio to show current location, but disable it from controlling state wildly 
    # to enforce linear progression, unless specifically selected.
    selected_page = st.sidebar.radio(
        "Navigation", 
        pages, 
        index=pages.index(st.session_state.page)
    )
    
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    st.sidebar.markdown("---")
    
    # Progress Indicator
    if st.session_state.selected_world:
        st.sidebar.subheader("📊 Your Progress")
        world_name = WORLDS[st.session_state.selected_world]["name"]
        st.sidebar.write(f"**World:** {world_name}")
        st.sidebar.write(f"**Scenario:** {st.session_state.current_scenario_idx + 1} / 2")
        st.sidebar.write(f"**Score:** {st.session_state.score}")

# ==========================================
# PAGE RENDERING FUNCTIONS
# ==========================================

def render_home():
    st.title("🌌 Physics Glitch")
    st.subheader("Understand Physics by Finding What's Wrong")
    st.markdown("""
    Welcome to a universe where the laws of physics are broken! 
    
    Your mission is to explore these glitched worlds, identify the scientific errors, and teach our onboard AI how real physics actually works.
    
    **How you will learn:**
    1. 🛑 Experience a broken concept.
    2. 🧠 Critically analyze why it's wrong.
    3. 🗣️ Explain the truth to cement your understanding.
    """)
    st.write("")
    if st.button("🚀 Start Learning", type="primary"):
        navigate_to("Choose World")
        st.rerun()

def render_choose_world():
    st.title("🌍 Choose a World")
    st.write("Select a corrupted dimension to investigate:")
    
    for world_key, world_data in WORLDS.items():
        with st.container():
            st.markdown(f"### {world_data['name']}")
            st.write(world_data['description'])
            if st.button(f"Enter {world_data['name'].split()[0]}", key=f"btn_{world_key}"):
                st.session_state.selected_world = world_key
                st.session_state.current_scenario_idx = 0
                st.session_state.score = 0
                navigate_to("Scenario")
                st.rerun()
            st.markdown("---")

def render_scenario():
    if not st.session_state.selected_world:
        st.warning("Please choose a world first!")
        st.button("Go to World Selection", on_click=lambda: navigate_to("Choose World"))
        return

    world = WORLDS[st.session_state.selected_world]
    scenario = world["scenarios"][st.session_state.current_scenario_idx]
    
    st.caption(f"📍 {world['name']} | Scenario {st.session_state.current_scenario_idx + 1} of 2")
    st.title("🧩 Analyze the Glitch")
    
    st.info(scenario["statement"])
    
    st.write("Is this statement Correct or Incorrect in reality?")
    answer = st.radio("Your analysis:", ["Correct", "Incorrect", "Not sure"], index=None)
    
    if st.button("Submit Analysis", type="primary"):
        if answer:
            st.session_state.user_answer = answer
            navigate_to("Analysis")
            st.rerun()
        else:
            st.error("Please select an answer before submitting.")

def render_analysis():
    if not st.session_state.selected_world or not st.session_state.user_answer:
        st.warning("Please complete the scenario first!")
        return

    world = WORLDS[st.session_state.selected_world]
    scenario = world["scenarios"][st.session_state.current_scenario_idx]
    
    st.title("📊 Analysis Results")
    
    # Check answer
    is_correct = (st.session_state.user_answer == scenario["correct_answer"])
    
    if is_correct:
        st.success("✅ Spot on! You identified the glitch.")
        # Only increment score if they just answered (to prevent refreshing abuse)
        # For simplicity in this single-file app, we won't strictly lock the score.
        # But we'll add a small text.
    elif st.session_state.user_answer == "Not sure":
        st.warning("🤔 It's okay to be unsure! Let's look at the science.")
    else:
        st.error(f"❌ Actually, that is {scenario['correct_answer']}.")
    
    st.markdown("### The Science:")
    st.write(scenario["explanation"])
    
    st.markdown("---")
    if st.button("Continue to Teach AI 🧠", type="primary"):
        if is_correct and not st.session_state.ai_response_shown:
             st.session_state.score += 10 # Award points
        navigate_to("Teach the AI")
        st.rerun()

def render_teach_ai():
    if not st.session_state.selected_world:
        st.warning("Please complete the scenario first!")
        return

    world = WORLDS[st.session_state.selected_world]
    scenario = world["scenarios"][st.session_state.current_scenario_idx]
    
    st.title("🤖 Teach the AI")
    st.write("The AI needs your help to understand this concept. Explain it in your own words.")
    
    user_explanation = st.text_area("Your explanation to the AI:", placeholder="Type your explanation here...")
    
    if not st.session_state.ai_response_shown:
        if st.button("Submit Explanation"):
            if len(user_explanation.strip()) < 5:
                st.error("Please write a bit more to help the AI understand!")
            else:
                with st.spinner("AI is processing your explanation..."):
                    time.sleep(1.5) # Simulate AI thinking
                st.session_state.ai_response_shown = True
                st.rerun()
    
    if st.session_state.ai_response_shown:
        st.success("Explanation submitted!")
        
        # Simulated AI Response box
        st.markdown("### AI Response:")
        st.info(f"**AI:** \"Thank you for explaining! {scenario['ai_followup']}\"")
        
        st.write("*(Think about the AI's question to deepen your understanding!)*")
        st.markdown("---")
        
        # Navigation based on progress
        if st.session_state.current_scenario_idx < len(world["scenarios"]) - 1:
            if st.button("Next Scenario ➡️", type="primary"):
                next_scenario()
        else:
            if st.button("View Final Results 🏆", type="primary"):
                navigate_to("Result")
                st.rerun()

def render_result():
    st.title("🏆 Mission Complete!")
    
    st.markdown(f"### You successfully repaired the physics logic in **{WORLDS[st.session_state.selected_world]['name']}**!")
    
    # Score display
    st.metric(label="Total Score", value=f"{st.session_state.score} / 20")
    
    if st.session_state.score == 20:
        st.success("🌟 Perfect Score! You are a master of physics concepts.")
    elif st.session_state.score == 10:
        st.warning("👍 Good job! You found some glitches, but there's still room to learn.")
    else:
        st.error("📚 The glitches tricked you! Remember, science is about learning from mistakes.")
        
    st.markdown("### What you learned:")
    st.write("- Critical thinking by questioning false statements.")
    st.write("- Solidifying knowledge by teaching concepts to an AI.")
    
    st.markdown("---")
    if st.button("🔄 Try Another World", type="primary"):
        reset_game()

# ==========================================
# MAIN APP ROUTER
# ==========================================
def main():
    render_sidebar()
    
    if st.session_state.page == "Home":
        render_home()
    elif st.session_state.page == "Choose World":
        render_choose_world()
    elif st.session_state.page == "Scenario":
        render_scenario()
    elif st.session_state.page == "Analysis":
        render_analysis()
    elif st.session_state.page == "Teach the AI":
        render_teach_ai()
    elif st.session_state.page == "Result":
        render_result()

if __name__ == "__main__":
    main()