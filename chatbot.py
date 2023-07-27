import streamlit as st
import pandas as pd
import User_Ursula as ursula


# Load the data
rating_url = "https://drive.google.com/file/d/1fiU-bQOIyyjoRRB8uSJ7_oodFRo5wr30/view?usp=drive_link"
rating_path = 'https://drive.google.com/uc?export=download&id=' + rating_url.split('/')[-2]
rating_df = pd.read_csv(rating_path)
games_url = "https://drive.google.com/file/d/1aOw0TeVXaToN1t0CE-vN3tXQEZXPpTzq/view?usp=drive_link"
games_path = 'https://drive.google.com/uc?export=download&id=' + games_url.split('/')[-2]
games_df = pd.read_csv(games_path)

# Function to get user IDs from user name
def get_user_ids(user_name):
    user_ids = rating_df.loc[rating_df['Username'] == user_name, 'user_Id'].values
    return user_ids

# Chatbot function
def chatbot():
    st.title("Game Recommendation Chatbot")
    st.write("Welcome! Let's start chatting.")

    chat_history = []

    # Chat loop
    while True:
        user_name = st.text_input("Please enter your name:")

        if user_name.strip():  # Check if user_name is not empty or only whitespace
            user_ids = get_user_ids(user_name)

            if len(user_ids) == 0:
                # User name not found in the data
                robot_response = f"Hello, {user_name}! I couldn't find any user ID associated with your name. Please provide me with your user ID so I can assist you better."
            elif len(user_ids) == 1:
                # Only one user ID found
                user_id = user_ids[0]
                robot_response = f"Hello, {user_name}! How can I assist you with Game recommendations ?"
            else:
                # Multiple user IDs found
                user_games = ursula.gib_spiele_digga(rat_df = rating_df, s_alt = 9, user = user_name, game_frame=games_df)
                #user_id_input = st.text_input("Multiple user IDs found. Please enter your preferred user ID:")  

                #if user_id_input:
                 
                #    try:
                #        user_id_input = int(user_id_input)
                #        if user_id_input in user_ids:
                #            robot_response = f"Hello, {user_name}! How can I assist you with Game recommendations?"
                #        else:
                #             robot_response = f"Sorry, {user_name}! The provided user ID does not match any of the user IDs associated with your name. Please enter your user ID again."
                #    except ValueError:
                #         robot_response = "Please enter a valid numeric user ID."
                #else:
                #    continue

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

