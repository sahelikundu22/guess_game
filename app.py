import streamlit as st
import random
import pandas as pd
from streamlit.components.v1 import html

st.set_page_config(page_title="Mastermind Number Game", page_icon="🎯")
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
    st.session_state.just_submitted = False  # New flag to track submission

# Game instructions
with st.expander("ℹ️ How to Play"):
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


# Current game status
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Turns Used", f"{st.session_state.turn}/{MAX_TURNS}")
with col2:
    remaining = MAX_TURNS - st.session_state.turn
    st.metric("Turns Remaining", remaining)
with col3:
    status = "Playing" if not st.session_state.game_over else "Game Over"
    st.metric("Status", status)

st.markdown("### Your Guess")

# Use a form to handle input clearing properly
with st.form(key=f"guess_form_{st.session_state.form_key}", clear_on_submit=True):
    cols = st.columns([1, 1, 1, 1, 2])
    guess = []
    
    for i in range(n):
        with cols[i]:
            val = st.text_input(
                label=f"**{i+1}**",
                max_chars=1,
                key=f"digit_{st.session_state.form_key}_{i}",
                label_visibility="collapsed",
                placeholder=str(i+1)
            )
            guess.append(val)
    
    with cols[-1]:
        st.write("")  # Spacer
        submit_clicked = st.form_submit_button(
            "Submit Guess (Enter)",
            type="primary",
            disabled=st.session_state.game_over,
            use_container_width=True
        )

# Process submission
if submit_clicked and not st.session_state.game_over:
    # Set flag to indicate we just submitted
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
        
        # Store in history (appends to end - will appear at bottom)
        st.session_state.history.append({
            "Turn": st.session_state.turn,
            "Guess": guess.copy(),
            "Count": count,
            "Position": pos
        })
        
        st.session_state.last_guess = guess.copy()
        
        # Increment form key to force new form instance
        st.session_state.form_key += 1

        # Display result immediately
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
        <h4>Turn {st.session_state.turn} Result</h4>
        <p><strong>Guess:</strong> <code>{guess}</code></p>
        <p><strong>Correct digits:</strong> {count}</p>
        <p><strong>Correct positions:</strong> {pos}</p>
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
        
        # Force a rerun to update the table
        st.rerun()

# Show last guess result if available
if st.session_state.last_guess and not st.session_state.game_over:
    st.info(f"Last guess: `{st.session_state.last_guess}`")

# Display history table ALWAYS (at the top) - CHRONOLOGICAL ORDER (latest at bottom)
if st.session_state.history:
    st.markdown("### 📊 Guess History (Chronological)")
    
    # Convert history to DataFrame (already in chronological order)
    display_data = []
    for entry in st.session_state.history:
        display_data.append({
            "Turn": entry["Turn"],
            "Guess": ' '.join(str(d) for d in entry["Guess"]),
            "Count": f"✅ {entry['Count']}",
            "Position": f"🎯 {entry['Position']}"
        })
    
    df_display = pd.DataFrame(display_data)
    
    # Apply styling for better readability - highlight the latest row
    def color_rows(row):
        if row['Position'] == f"🎯 {n}":
            return ['background-color: #d4edda'] * len(row)  # Green for win
        elif int(row['Turn']) == st.session_state.turn and not st.session_state.game_over:
            return ['background-color: #fff3cd'] * len(row)  # Yellow for current/latest
        else:
            return [''] * len(row)
    
    # Display the dataframe
    st.dataframe(
        df_display.style.apply(color_rows, axis=1),
        use_container_width=True,
        hide_index=True
    )


# Restart button
if st.button("🔄 Restart Game", type="secondary"):
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
    st.write(f"The secret code was: **`{st.session_state.comp}`**")
    
    # Show final statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Score", f"{st.session_state.turn} turns")
    with col2:
        efficiency = (st.session_state.turn / MAX_TURNS) * 100
        st.metric("Efficiency", f"{100 - efficiency:.0f}%")
    with col3:
        st.metric("Success", "Yes" if st.session_state.last_guess == st.session_state.comp else "No")