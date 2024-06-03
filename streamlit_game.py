import streamlit as st
import pandas as pd
import subprocess
import time

# Function to run the Pygame Brick Breaker
def run_game():
    process = subprocess.Popen(["python", "brick_breaker.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    process.wait()

# Initialize scoreboard if not already defined
if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = pd.DataFrame(columns=["Player", "Score"])

# Streamlit UI
st.title("Brick Breaker Competition")
player_name = st.text_input("Enter your name:")

if st.button("Start Game"):
    run_game()
    time.sleep(1)  # Ensure the game has time to save the score
    with open("score.txt", "r") as file:
        score = int(file.read())
    if player_name:
        if isinstance(st.session_state.scoreboard, pd.DataFrame):
            new_entry = pd.DataFrame([{"Player": player_name, "Score": score}])
            st.session_state.scoreboard = pd.concat([st.session_state.scoreboard, new_entry], ignore_index=True)
            st.session_state.scoreboard.to_csv("scoreboard.csv", index=False)
            st.success(f"Score submitted! Your score: {score}")
        else:
            st.error("Error: Scoreboard is not properly initialized as a DataFrame.")

# Display the scoreboard
st.subheader("Scoreboard")
st.dataframe(st.session_state.scoreboard.sort_values(by="Score", ascending=False).reset_index(drop=True))
