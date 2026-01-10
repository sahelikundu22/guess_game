import streamlit as st
import random
import pandas as pd
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Mastermind Number Game", 
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
/* ================================
   STREAMLIT DARK MODE FIX (DESKTOP + MOBILE)
   ================================ */

/* Use Streamlit theme variables */
:root {
    --bg-color: var(--background-color);
    --text-color: var(--text-color);
    --secondary-bg: var(--secondary-background-color);
    --border-color: rgba(255,255,255,0.15);
}

/* App background */
.stApp {
    background-color: var(--bg-color);
    color: var(--text-color);
}

/* Titles & text */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: var(--text-color) !important;
}

/* ================================
   INPUT BOXES (OTP / TEXT INPUT)
   ================================ */

.stTextInput input {
    background-color: var(--secondary-bg) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    font-size: 1.4rem !important;
    text-align: center !important;
}

/* Placeholder */
.stTextInput input::placeholder {
    color: rgba(200,200,200,0.6) !important;
}

/* Focus */
.stTextInput input:focus {
    border-color: #4da3ff !important;
    box-shadow: 0 0 0 1px #4da3ff !important;
}

/* ================================
   HIDE "PRESS ENTER TO SUBMIT" TEXT
   ================================ */

div[data-testid="InputInstructions"],
div[data-testid="caption"],
.stTextInput > label + div[data-testid="caption"] {
    display: none !important;
}

/* ================================
   BUTTONS
   ================================ */

.stButton button {
    background-color: #4da3ff !important;
    color: #000 !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #3391ff !important;
    color: #000 !important;
}

/* ================================
   RESULT BOX
   ================================ */

.result-box {
    background-color: var(--secondary-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}

/* ================================
   METRICS
   ================================ */

[data-testid="stMetricValue"] {
    color: var(--text-color) !important;
    font-size: 1.3rem !important;
}

[data-testid="stMetricLabel"] {
    color: rgba(200,200,200,0.8) !important;
}

/* ================================
   DATAFRAME (HISTORY TABLE) - CONSISTENT STYLING
   ================================ */

.stDataFrame {
    background-color: var(--secondary-bg) !important;
    border-radius: 8px;
    margin-bottom: 2rem !important;
}

/* Header */
.stDataFrame thead tr th {
    background-color: rgba(255,255,255,0.08) !important;
    color: #ffffff !important; /* White text for header */
    font-weight: bold !important;
    border-bottom: 2px solid rgba(255,255,255,0.2) !important;
}

/* Cells - All rows same color */
.stDataFrame tbody tr td {
    background-color: transparent !important;
    color: #ffffff !important; /* White text for cells */
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
}

/* Row hover - subtle effect */
.stDataFrame tbody tr:hover td {
    background-color: rgba(255,255,255,0.05) !important;
}

/* Remove any previous highlighting styles */
.dataframe {
    color: #ffffff !important;
}

.dataframe th {
    color: #ffffff !important;
}

.dataframe td {
    color: #ffffff !important;
}

/* All table-related elements with consistent styling */
.stDataFrame,
.stDataFrame *,
.dataframe,
.dataframe *,
table,
table * {
    color: #ffffff !important;
}

/* Remove any special styling for highlighted rows */
div[data-testid="StyledDataFrame"] {
    color: #ffffff !important;
}

div[data-testid="StyledDataFrame"] th {
    color: #ffffff !important;
}

div[data-testid="StyledDataFrame"] td {
    color: #ffffff !important;
    background-color: transparent !important;
}

/* Force consistent background for all cells */
.stDataFrame tbody tr:nth-child(even) td,
.stDataFrame tbody tr:nth-child(odd) td {
    background-color: transparent !important;
}

/* ================================
   MOBILE ADJUSTMENTS
   ================================ */

@media (max-width: 768px) {
    .stTextInput input {
        font-size: 1.1rem !important;
        height: 3rem !important;
    }

    h1 {
        font-size: 1.7rem !important;
        text-align: center;
    }
    
    /* Consistent table text on mobile */
    .stDataFrame,
    .stDataFrame * {
        color: #ffffff !important;
    }
    
    /* Input section styling for mobile */
    .input-section {
        margin-top: 1.5rem !important;
        padding: 1rem !important;
        background-color: rgba(255,255,255,0.05) !important;
        border-radius: 10px !important;
    }
}

/* ================================
   REMOVE WHITE ARTIFACTS
   ================================ */

div[data-baseweb="input"] > div {
    background-color: transparent !important;
}

/* Table border styling */
.stDataFrame {
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* Input section styling */
.input-section {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: rgba(255,255,255,0.05);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Game status styling */
.game-status {
    margin-bottom: 2rem;
    padding: 1rem;
    background-color: rgba(255,255,255,0.05);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.1);
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

# Display history table FIRST (if there is history)
if st.session_state.history:
    st.markdown("### 📊 Guess History")
    
    # Convert history to DataFrame
    display_data = []
    for entry in st.session_state.history:
        # Convert array to string representation
        guess_str = ''.join(str(d) for d in entry["Guess"])
        display_data.append({
            "Turn": entry["Turn"],
            "Guess": guess_str,
            "Count": f"✅ {entry['Count']}",
            "Position": f"🎯 {entry['Position']}"
        })
    
    df_display = pd.DataFrame(display_data)
    
    # Display the dataframe without any special styling
    st.dataframe(
        df_display,
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
                help=f"Your guess ({n} digits)",
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


# Helper function to convert 4-digit number to array
def number_to_array(number, n=4):
    """Convert a 4-digit number to an array of digits"""
    if number == 0:
        return [0] * n
    
    # Create array to store digits
    digits = []
    
    # Extract digits using division
    temp = number
    for i in range(n-1, -1, -1):
        divisor = 10 ** i
        digit = temp // divisor
        digits.append(digit)
        temp = temp % divisor
    
    return digits

# Use a form to handle input clearing properly - Mobile optimized
with st.form(key=f"guess_form_{st.session_state.form_key}", clear_on_submit=True):
    # Single input for the entire 4-digit number
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input(
            label="Enter 4-digit number",
            max_chars=4,
            key=f"number_input_{st.session_state.form_key}",
            placeholder="e.g., 1234",
            help=f"Enter a {n}-digit number (0-9)",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # Spacer
        # Mobile-friendly button with full width on small screens
        submit_clicked = st.form_submit_button(
            "Submit",
            type="primary",
            disabled=st.session_state.game_over,
            use_container_width=True
        )

# Add JavaScript for numeric keyboard
st.markdown("""
<script>
// Function to force numeric keyboard on mobile
function setupNumericInputs() {
    const inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach(input => {
        // Set inputmode to numeric for mobile keyboards
        input.setAttribute('inputmode', 'numeric');
        input.setAttribute('pattern', '[0-9]*');
    });
}

// Run on page load and after each Streamlit update
document.addEventListener('DOMContentLoaded', setupNumericInputs);
if (typeof Streamlit !== 'undefined') {
    Streamlit.onMessage(function(event) {
        setTimeout(setupNumericInputs, 100);
    });
}
</script>
""", unsafe_allow_html=True)

# Process submission
if submit_clicked and not st.session_state.game_over:
    st.session_state.just_submitted = True
    
    # Validation
    if not user_input:
        st.error("⚠️ Please enter a 4-digit number.")
    elif not user_input.isdigit():
        st.error("❌ Only digits (0–9) are allowed.")
    elif len(user_input) != n:
        st.error(f"❌ Please enter exactly {n} digits.")
    elif any(int(digit) < 0 or int(digit) > 9 for digit in user_input):
        st.error("❌ Digits must be between 0-9.")
    else:
        # Convert the string to integer
        user_number = int(user_input)
        
        # Convert to array using our helper function
        guess = number_to_array(user_number, n)
        
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
        <p><strong style='color: #ffffff;'>Your guess:</strong> <code style='background: #555; padding: 2px 6px; border-radius: 3px; font-size: 1rem;'>{user_input}</code></p>
        <p><strong style='color: #ffffff;'>As array:</strong> <code style='background: #555; padding: 2px 6px; border-radius: 3px; font-size: 0.9rem;'>{guess}</code></p>
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


# Show last guess result if available (below input section)
if st.session_state.last_guess and not st.session_state.game_over and st.session_state.turn > 0:
    st.markdown("### Your Guess")
    st.info(f"**Last guess:** `{st.session_state.last_guess}` (as number: {''.join(map(str, st.session_state.last_guess))})")


# Game instructions
with st.expander("ℹ️ How to Play", expanded=False):
    st.write(f"""
    - Guess the {n}-digit secret number (0-9)
    - Digits can repeat
    - You have {MAX_TURNS} attempts
    - **Count**: How many digits are correct (any position)
    - **Position**: How many digits are in the correct position
    - **Input**: Enter all {n} digits as one number (e.g., 1234)
    - **Mobile**: Uses number keyboard for easy input
    """)

# Display the secret code for debugging
if st.checkbox("👁️ Show secret code (for testing)"):
    st.code(f"Secret: {st.session_state.comp}")


st.markdown("---")
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
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
    secret_str = ''.join(str(d) for d in st.session_state.comp)
    st.markdown(f"""
    <div style='background: #333; padding: 0.8rem; border-radius: 0.5rem; margin: 1rem 0; text-align: center;'>
    <p style='color: white; margin: 0; font-size: 0.9rem;'>The secret code was:</p>
    <h2 style='color: #FFD700; letter-spacing: 0.3rem; margin: 0.5rem 0; font-size: 1.5rem; word-break: break-all;'>
    {secret_str}
    </h2>
    <p style='color: #aaa; margin: 0; font-size: 0.8rem;'>As array: {st.session_state.comp}</p>
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