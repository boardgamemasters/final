import streamlit as st
import pandas as pd
import ameyfun as amey

# Load the data
@st.cache_data
def data_load():
    # Your data loading code here
    # For example:
    rating_df = pd.read_csv('data/final_rating.csv')
    games_df = pd.read_csv('data/games_data.csv')
    users_df = pd.read_csv('data/users_data.csv')
    games_info = pd.read_csv('data/games_info.csv')
    cosine_df = pd.read_csv('data/cosine_data.csv')
    final_df = pd.read_csv('data/final_data.csv')
    return rating_df, games_df, users_df, games_info, cosine_df, final_df

rating_df, games_df, users_df, games_info, cosine_df, final_df = data_load()

# Function to check if game exists
def get_game_ids(game_name):
    game_ids = final_df.loc[final_df['game_name'] == game_name, 'game_id'].values
    return game_ids

# Chatbot function
def chatbot():
    st.title("Game Recommendation Chatbot")
    st.write("Welcome! Let's start chatting.")

    chat_history = []

    # Chat loop
    loopy = 0
    while True:
        loopy += 1
        key_a = f'blabla{loopy}'
        key_b = f'boob{loopy}'
        user_favorite_game = st.text_input("Please enter the name of the game that you like:", key=key_a)

        if user_favorite_game.strip():  # Check if user input is not empty or only whitespace
            game_ids = get_game_ids(user_favorite_game)

            if len(game_ids) == 0:
                # Game name not found in the data
                robot_response = f"Hello, {user_favorite_game}! I couldn't find any game associated with the name you provided. Please enter another game name."
            else:
                # Game name found
                recommended_games = amey.game_of_my_life(user_favorite_game, final_df)
                robot_response = f"Hello, {user_favorite_game}! Based on your favorite game, here are some game recommendations for you:\n"
                for game_id in recommended_games:
                    game_name = final_df.loc[final_df['game_id'] == game_id, 'game_name'].values[0]
                    robot_response += f"- {game_name}\n"

            # Add user input to chat history
            chat_history.append(("User", user_favorite_game))
            # Add robot response to chat history
            chat_history.append(("Robot", robot_response))

            # Display the last robot response
            if chat_history:
                last_sender, last_message = chat_history[-1]
                if last_sender == "Robot":
                    st.text_area("Robot:", value=last_message, key="robot-response", disabled=True)

        # Break the chat loop if user input is "quit"
        if user_favorite_game.lower() == "quit":
            break

if __name__ == "__main__":
    chatbot()
