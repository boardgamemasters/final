import streamlit as st
import pandas as pd
import ameyfun as amey

# Load the data
@st.cache(allow_output_mutation=True)
def data_load():
    final_df = pd.read_csv('data/final_data.csv')
    return final_df

final_df = data_load()

# Function to check if game exists
def get_game_ids(game_name):
    game_ids = final_df.loc[final_df['Name'] == game_name, 'Name'].values
    return game_ids

# Function to recommend games based on user input
def recommend_games(user_favorite_game, data, z=6):
    # Use the ameyfun function to get game recommendations
    similar_game_bgg_ids = amey.game_of_my_life(user_favorite_game, data, z)
    return similar_game_bgg_ids

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
        user_name = st.text_input("Please enter the Name of Game that you like:", key=key_a)

        if user_name.strip():  # Check if user_name is not empty or only whitespace
            game_ids = get_game_ids(user_name)

            if len(game_ids) == 0:
                # Game name not found in the data
                robot_response = f"🤖 Hello, {user_name}! I couldn't find any game associated with your input. Please provide me with another game name."
            elif len(game_ids) == 1:
                # Only one game found
                robot_response = f"🤖 Hello, {user_name}! How can I assist you with game recommendations?"
            else:
                # Multiple games found
                robot_response = f"🤖 Hello, {user_name}! I found multiple games associated with your input. Please enter a more specific game name."

            # Add user input to chat history
            chat_history.append(("User", user_name))
            # Add robot response to chat history
            chat_history.append(("Robot", robot_response))

            # Display the last robot response
            if chat_history:
                last_sender, last_message = chat_history[-1]
                if last_sender == "Robot":
                    st.text_area("🤖 Robot:", value=last_message, key="robot-response", disabled=True)

        # Game recommendation
        user_favorite_game = st.text_input("👤 Please enter the name of the game that you like:", key=key_b)
        if user_favorite_game.strip():
            similar_game_bgg_ids = recommend_games(user_favorite_game, final_df)
            st.write("Recommended Games:")
            st.write(similar_game_bgg_ids)

        # Break the chat loop if user input is "quit"
        if user_name.lower() == "quit":
            break

if __name__ == "__main__":
    chatbot()
