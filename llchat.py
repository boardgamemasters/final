import streamlit as st
import pandas as pd
import ameyfun as amey

# Load the data
@st.cache
def data_load():
    final_df = pd.read_csv('data/final_data.csv')
    return final_df

final_df = data_load()

# Function to check if game exists
def get_game_ids(game_name):
    game_ids = final_df.loc[final_df['game_name'] == game_name, 'game_name'].values
    return game_ids

# Game recommendation function
def game_of_my_life(user_favorite_game, data, z=6):
    # Implement your game recommendation logic here
    # I'm using your provided ameyfun.game_of_my_life function for now
    game_ids = amey.game_of_my_life(user_favorite_game, data, z)
    return game_ids

# Chatbot function
def chatbot():
    st.title("Game Recommendation Chatbot")
    st.write("Welcome! Let's start chatting.")

    chat_history = []

    # Chat loop
    while True:
        user_favorite_game = st.text_input("Please enter the name of the game that you like:")
        if user_favorite_game.strip():
            game_ids = get_game_ids(user_favorite_game)

            if len(game_ids) == 0:
                # Game name not found in the data
                robot_response = f"🤖 Hello, {user_favorite_game}! I couldn't find any game associated with the name. Please provide another game."
            elif len(game_ids) == 1:
                # Only one game found
                game_id = game_ids[0]
                robot_response = f"🤖 Hello, {user_favorite_game}! How can I assist you with game recommendations?"
                # Call the game recommendation function
                recommended_games = game_of_my_life(user_favorite_game, final_df)
                st.write(f"🤖 I recommend the following games similar to '{user_favorite_game}':")
                for idx, game_id in enumerate(recommended_games, 1):
                    st.write(f"{idx}. {game_id}")
            else:
                # Multiple games found
                robot_response = "🤖 Multiple games found. Please provide more specific details to narrow down the search."

            # Add user input to chat history
            chat_history.append(("User", user_favorite_game))
            # Add robot response to chat history
            chat_history.append(("Robot", robot_response))

            # Display the last robot response with icon
            if chat_history:
                last_sender, last_message = chat_history[-1]
                if last_sender == "Robot":
                    st.markdown(f"🤖 {last_message}")

        # Break the chat loop if user input is "quit"
        if user_favorite_game.lower() == "quit":
            break

if __name__ == "__main__":
    chatbot()

