import streamlit as st
import pandas as pd
from ameyfun import game_of_my_life
import User_Ursula as ursula

# Load the data
@st.cache
def data_load():
    final_df = pd.read_csv('data/final_data.csv')
    return final_df

final_df = data_load()

# Emoji characters for robot and user
robot_emoji = "🤖"
user_emoji = "👤"

# Chatbot function
def chatbot():
    st.title("Game Recommendation Chatbot")
    st.write("Welcome! Let's start chatting.")

    chat_history = []

    # User input
    user_input = st.text_input(f"{user_emoji} Please enter the name of the game that you like:")

    # Send button to handle user input
    send_button = st.button("Send")

    if user_input.strip() and send_button:  # Check if user input is not empty or only whitespace and the button is clicked
        # Use the game_of_my_life function to get game recommendations
        game_recommendations = game_of_my_life(user_input, final_df)

        if not game_recommendations:
            robot_response = f"{robot_emoji} Sorry, I couldn't find any game recommendations for '{user_input}'. Please try again with a different game name."
        else:
            robot_response = f"{robot_emoji} Sure! Based on '{user_input}', I recommend the following games:\n"
            for i, game_id in enumerate(game_recommendations, 1):
                # Use the get_feature function to get the game name from the game_id
                game_name = ursula.get_feature(result_file=game_id, feature_file=games_info)
                robot_response += f"{i}. {game_name}\n"

        # Add user input to chat history
        chat_history.append(("User", user_input))
        # Add robot response to chat history
        chat_history.append(("Robot", robot_response))

        # Display the last robot response
        if chat_history:
            last_sender, last_message = chat_history[-1]
            if last_sender == "Robot":
                st.text_area(f"{robot_emoji} Robot:", value=last_message, key="robot-response", disabled=True)

if __name__ == "__main__":
    chatbot()
