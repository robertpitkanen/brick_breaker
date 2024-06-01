import streamlit as st
import pandas as pd
import subprocess

# Function to run the Pygame Brick Breaker
def run_game():
    subprocess.run(["python", "brick_breaker.py"])

# Initialize scoreboard
if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = pd.DataFrame(columns=["Player", "Score"])

# Streamlit UI
st.title("Brick Breaker Competition")
player_name = st.text_input("Enter your name:")
if st.button("Start Game"):
    run_game()

#Score input after game
score = st.number_input("Enter your score:", min_value=0, step=1)
if st.button("Submit Score"): 
    if player_name:
        st.session_state.scoreboard = st.session_state.scoreboard.append({"Player": player_name, "Score": score}, ignore_index=True)
        st.session_state.scoreboard.to_csv("scoreboard.csv", index=False)
        st.success("Score submitted!")

#Display the scoreboard
st.subheader("Scoreboard")
st.dataframe(st.session_state.scoreboard.sort_values(by="Score", ascending=False).reset_index(drop=True))