import streamlit as st
import pandas as pd
from ameyfun import game_of_my_life

# Load the data
@st.cache
def data_load():
    final_df   =    pd.read_csv('data/final_data.csv')
    return final_data

final_data = data_load()

# Emoji characters for robot and user
robot_emoji = "🤖"
user_emoji = "👤"

# Chatbot function
def chatbot():
    st.title("Game Recommendation Chatbot")
    st.write("Welcome! Let's start chatting.")

    chat_history = []

    # Chat loop
    while True:
        user_favorite_game = st.text_input(f"{user_emoji} Please enter the name of the game that you like:")

        if user_favorite_game.strip():  # Check if user input is not empty or only whitespace
            game_recommendations = game_of_my_life(user_favorite_game, final_data)

            if not game_recommendations:
                robot_response = f"{robot_emoji} Sorry, I couldn't find any game recommendations for '{user_favorite_game}'. Please try again with a different game name."
            else:
                robot_response = f"{robot_emoji} Sure! Based on '{user_favorite_game}', I recommend the following games:\n"
                for i, game in enumerate(game_recommendations, 1):
                    robot_response += f"{i}. {game}\n"

            # Add user input to chat history
            chat_history.append(("User", user_favorite_game))
            # Add robot response to chat history
            chat_history.append(("Robot", robot_response))

            # Display the last robot response
            if chat_history:
                last_sender, last_message = chat_history[-1]
                if last_sender == "Robot":
                    st.text_area(f"{robot_emoji} Robot:", value=last_message, key="robot-response", disabled=True)

        # Break the chat loop if user input is "quit"
        if user_favorite_game.lower() == "quit":
            break

if __name__ == "__main__":
    chatbot()
