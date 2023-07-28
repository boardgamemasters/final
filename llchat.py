import streamlit as st
import pandas as pd

# Load your data
@st.cache_data
def data_load():
    rating_df = pd.read_csv('data/final_ratings_v3.csv')
    games_df = pd.read_csv('data/game_learn_df_v3.csv')
    users_df = pd.read_csv('data/usernames_v2.csv')
    games_info = pd.read_csv('data/bgref.csv')
    cosine_df = pd.read_csv('data/bg_cosines_final.csv')
    return rating_df, games_df, users_df, games_info, cosine_df

rating_df, games_df, users_df, games_info, cosine_df = data_load()

# Function to check if user exists
def get_user_ids(user_name):
    user_ids = rating_df.loc[rating_df['Username'] == user_name, 'user_name'].values
    return user_ids

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
        user_name = st.text_input("Please enter your name:", key=key_a)

        if user_name.strip():  # Check if user_name is not empty or only whitespace
            user_ids = get_user_ids(user_name)

            if len(user_ids) == 0:
                # User name not found in the data
                robot_response = f"Hello, {user_name}! I couldn't find any user ID associated with your name. Please provide me with your user ID so I can assist you better."
            elif len(user_ids) == 1:
                # Only one user ID found
                user_id = user_ids[0]
                robot_response = f"Hello, {user_name}! How can I assist you with Game recommendations?"
            else:
                # Multiple user IDs found
                user_id_input = st.text_input("Multiple user IDs found. Please enter your preferred user ID:", key=key_b)

                if user_id_input:
                    try:
                        user_id_input = int(user_id_input)
                        if user_id_input in user_ids:
                            robot_response = f"Hello, {user_name}! How can I assist you with Game recommendations?"
                        else:
                            robot_response = f"Sorry, {user_name}! The provided user ID does not match any of the user IDs associated with your name. Please enter your user ID again."
                    except ValueError:
                        robot_response = "Please enter a valid numeric user ID."
                else:
                    continue

            # Add user input to chat history
            chat_history.append(("User", user_name))
            # Add robot response to chat history
            chat_history.append(("Robot", robot_response))

            # Display the last robot response
            if chat_history:
                last_sender, last_message = chat_history[-1]
                if last_sender == "Robot":
                    st.text_area("Robot:", value=last_message, key="robot-response", disabled=True)

        # Break the chat loop if user input is "quit"
        if user_name.lower() == "quit":
            break

if __name__ == "__main__":
    chatbot()
