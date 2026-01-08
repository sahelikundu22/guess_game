import streamlit as st
import random
import pandas as pd
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Mastermind Number Game", 
    page_icon="🎯",
    layout="wide"
)

# Add custom CSS for dark mode and mobile compatibility
st.markdown("""
<style>
    /* Base responsive settings */
    .mobile-container {
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Dark mode text color fixes */
    @media (prefers-color-scheme: dark) {
        .stDataFrame {
            color: #ffffff !important;
        }
        .stDataFrame th {
            color: #ffffff !important;
        }
        .stDataFrame td {
            color: #ffffff !important;
        }
    }
    
    /* Dark mode form improvements */
    .stTextInput input {
        background-color: transparent;
    }
    
    /* Dark mode result box */
    .result-box {
        background-color: #262730 !important;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #555;
    }
    
    /* Ensure form text is visible in dark mode */
    div[data-baseweb="input"] > div {
        background-color: transparent !important;
    }
    
    /* Better contrast for table cells */
    .dataframe {
        background-color: transparent !important;
    }
    
    /* Status metrics styling for mobile */
    [data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
    }
    
    /* Make placeholder text visible */
    input::placeholder {
        color: #888 !important;
        opacity: 1 !important;
    }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        /* Title and header adjustments */
        h1 {
            font-size: 1.8rem !important;
            text-align: center !important;
        }
        
        h3 {
            font-size: 1.3rem !important;
        }
        
        /* Metrics adjustments */
        .stMetric {
            padding: 0.3rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.1rem !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.7rem !important;
        }
        
        /* Form input adjustments */
        .stTextInput input {
            height: 2.5rem !important;
            font-size: 1.1rem !important;
            text-align: center !important;
        }
        
        /* Button adjustments */
        .stButton button {
            width: 100% !important;
            padding: 0.6rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Data table adjustments */
        .dataframe {
            font-size: 0.85rem !important;
        }
        
        .dataframe th {
            padding: 0.3rem !important;
            font-size: 0.8rem !important;
        }
        
        .dataframe td {
            padding: 0.3rem !important;
        }
        
        /* Secret code display */
        code {
            font-size: 0.9rem !important;
            word-break: break-all;
        }
        
        /* Result box adjustments */
        .result-box h4 {
            font-size: 1.1rem !important;
        }
        
        .result-box p {
            font-size: 0.9rem !important;
            margin: 0.3rem 0 !important;
        }
    }
    
    /* Tablet adjustments */
    @media (max-width: 1024px) and (min-width: 769px) {
        .stTextInput input {
            height: 3rem !important;
            font-size: 1.2rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }
    }
    
    /* Extra small mobile adjustments */
    @media (max-width: 480px) {
        h1 {
            font-size: 1.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stTextInput input {
            height: 2.2rem !important;
            font-size: 1rem !important;
        }
        
        .stButton button {
            padding: 0.5rem !important;
            font-size: 0.8rem !important;
        }
        
        /* Adjust column spacing for guess inputs */
        [data-testid="column"] {
            padding: 0.1rem !important;
        }
    }
    
    /* Game history table responsive */
    .history-table {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    
    /* Form container responsive */
    .form-container {
        width: 100%;
        margin: 1rem 0;
    }
    
    /* Mobile-friendly grid for guess inputs */
    .guess-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    @media (max-width: 480px) {
        .guess-grid {
            gap: 0.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main container for better mobile layout
st.markdown('<div class="mobile-container">', unsafe_allow_html=True)

st.title("🎯 Mastermind Number Game")

n = 4
MAX_TURNS = 20

# Initialize game state
if "comp" not in st.session_state:
    st.session_state.comp = [random.randint(0, 9) for _ in range(n)]
    st.session_state.turn = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.last_guess = None
    st.session_state.form_key = 0
    st.session_state.just_submitted = False

# Game instructions
with st.expander("ℹ️ How to Play", expanded=False):
    st.write("""
    - Guess the 4-digit secret number (0-9)
    - Digits can repeat
    - You have 20 attempts
    - **Count**: How many digits are correct (any position)
    - **Position**: How many digits are in the correct position
    - **Auto-tab**: Automatically moves to next box
    - **Enter key**: Press Enter to submit
    """)

# Display the secret code for debugging
if st.checkbox("👁️ Show secret code (for testing)"):
    st.code(f"Secret: {st.session_state.comp}")

# Current game status - Responsive columns
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Turns Used", f"{st.session_state.turn}/{MAX_TURNS}")
with col2:
    remaining = MAX_TURNS - st.session_state.turn
    st.metric("Turns Remaining", remaining)
with col3:
    status = "Playing" if not st.session_state.game_over else "Game Over"
    status_icon = "▶️" if not st.session_state.game_over else "⏹️"
    st.metric("Status", f"{status_icon} {status}")

st.markdown("### Your Guess")

# Use a form to handle input clearing properly - Mobile optimized
with st.form(key=f"guess_form_{st.session_state.form_key}", clear_on_submit=True):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Mobile-friendly input layout using columns with responsive widths
    cols = st.columns([1, 1, 1, 1, 1.5])
    guess = []
    
    for i in range(n):
        with cols[i]:
            val = st.text_input(
                label=f"**{i+1}**",
                max_chars=1,
                key=f"digit_{st.session_state.form_key}_{i}",
                label_visibility="collapsed",
                placeholder="0-9",
                help=f"Digit {i+1} (0-9)"
            )
            guess.append(val)
    
    with cols[-1]:
        st.write("")  # Spacer
        # Mobile-friendly button with full width on small screens
        submit_clicked = st.form_submit_button(
            "Submit Guess",
            type="primary",
            disabled=st.session_state.game_over,
            use_container_width=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Process submission
if submit_clicked and not st.session_state.game_over:
    st.session_state.just_submitted = True
    
    # Validation
    if "" in guess:
        st.error("⚠️ Please fill all 4 boxes.")
    elif not all(g.isdigit() for g in guess):
        st.error("❌ Only digits (0–9) are allowed.")
    elif any(int(g) < 0 or int(g) > 9 for g in guess if g.isdigit()):
        st.error("❌ Digits must be between 0-9.")
    else:
        guess = list(map(int, guess))
        st.session_state.turn += 1

        # Calculate matches
        pos = 0
        count = 0
        comp_copy = st.session_state.comp.copy()
        guess_copy = guess.copy()
        
        # First pass: correct position
        for i in range(n):
            if comp_copy[i] == guess_copy[i]:
                pos += 1
                count += 1
                comp_copy[i] = guess_copy[i] = None
        
        # Second pass: correct number, wrong position
        for i in range(n):
            if comp_copy[i] is not None:
                for j in range(n):
                    if guess_copy[j] is not None and comp_copy[i] == guess_copy[j]:
                        count += 1
                        comp_copy[i] = guess_copy[j] = None
                        break
        
        # Store in history
        st.session_state.history.append({
            "Turn": st.session_state.turn,
            "Guess": guess.copy(),
            "Count": count,
            "Position": pos
        })
        
        st.session_state.last_guess = guess.copy()
        st.session_state.form_key += 1

        # Display result immediately with mobile-friendly styling
        st.markdown(f"""
        <div class='result-box'>
        <h4 style='color: #ff4b4b;'>Turn {st.session_state.turn} Result</h4>
        <p><strong style='color: #ffffff;'>Guess:</strong> <code style='background: #555; padding: 2px 6px; border-radius: 3px; font-size: 0.9rem;'>{guess}</code></p>
        <p><strong style='color: #ffffff;'>Correct digits:</strong> <span style='color: #4CAF50; font-weight: bold;'>{count}</span></p>
        <p><strong style='color: #ffffff;'>Correct positions:</strong> <span style='color: #2196F3; font-weight: bold;'>{pos}</span></p>
        </div>
        """, unsafe_allow_html=True)

        # Check win/lose conditions
        if pos == n:
            st.balloons()
            st.success(f"""
            🎉 **Congratulations!**  
            You guessed the code in {st.session_state.turn} turns!  
            Secret code was: `{st.session_state.comp}`
            """)
            st.session_state.game_over = True
        elif st.session_state.turn >= MAX_TURNS:
            st.error(f"""
            ❌ **Game Over!**  
            Maximum {MAX_TURNS} turns reached.  
            The secret code was: `{st.session_state.comp}`
            """)
            st.session_state.game_over = True
        
        st.rerun()

# Show last guess result if available
if st.session_state.last_guess and not st.session_state.game_over:
    st.info(f"Last guess: `{st.session_state.last_guess}`")

# Display history table with mobile-friendly container
if st.session_state.history:
    st.markdown("### 📊 Guess History")
    st.markdown('<div class="history-table">', unsafe_allow_html=True)
    
    # Convert history to DataFrame
    display_data = []
    for entry in st.session_state.history:
        display_data.append({
            "Turn": entry["Turn"],
            "Guess": ' '.join(str(d) for d in entry["Guess"]),
            "Count": f"✅ {entry['Count']}",
            "Position": f"🎯 {entry['Position']}"
        })
    
    df_display = pd.DataFrame(display_data)
    
    # Apply styling
    def color_rows(row):
        if row['Position'] == f"🎯 {n}":
            return ['background-color: #2e7d32'] * len(row)
        elif int(row['Turn']) == st.session_state.turn and not st.session_state.game_over:
            return ['background-color: #5d4037'] * len(row)
        else:
            return [''] * len(row)
    
    # Display dataframe with responsive settings
    st.dataframe(
        df_display.style.apply(color_rows, axis=1),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Turn": st.column_config.NumberColumn(
                "Turn",
                help="Turn number",
                width="small"
            ),
            "Guess": st.column_config.TextColumn(
                "Guess",
                help="Your guess (4 digits)",
                width="medium"
            ),
            "Count": st.column_config.TextColumn(
                "Count",
                help="Correct digits (any position)",
                width="small"
            ),
            "Position": st.column_config.TextColumn(
                "Position",
                help="Correct positions",
                width="small"
            )
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Restart button with mobile-friendly layout
st.markdown("---")
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("🔄 Restart Game", type="secondary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Display win/lose message at bottom if game over
if st.session_state.game_over:
    st.markdown("---")
    if st.session_state.turn <= MAX_TURNS and st.session_state.last_guess == st.session_state.comp:
        st.balloons()
        st.success("### 🏆 You Win!")
    else:
        st.error("### 💔 Game Over")
    
    # Secret code display with mobile-friendly styling
    st.markdown(f"""
    <div style='background: #333; padding: 0.8rem; border-radius: 0.5rem; margin: 1rem 0; text-align: center;'>
    <p style='color: white; margin: 0; font-size: 0.9rem;'>The secret code was:</p>
    <h2 style='color: #FFD700; letter-spacing: 0.3rem; margin: 0.5rem 0; font-size: 1.5rem; word-break: break-all;'>
    {' '.join(str(d) for d in st.session_state.comp)}
    </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Show final statistics in responsive columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Score", f"{st.session_state.turn} turns")
    with col2:
        efficiency = (st.session_state.turn / MAX_TURNS) * 100
        st.metric("Efficiency", f"{100 - efficiency:.0f}%")
    with col3:
        st.metric("Success", "Yes" if st.session_state.last_guess == st.session_state.comp else "No")

# Footer with mobile-friendly text
st.markdown("---")
st.caption("🎯 Mastermind Game | Mobile optimized | Enjoy playing!")

# Close the mobile container
st.markdown('</div>', unsafe_allow_html=True)