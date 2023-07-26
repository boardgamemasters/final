import streamlit as st
import pandas as pd

# Load the data
extra_rating_new_url = "https://drive.google.com/file/d/1L5_vqmVCQkJmpif3b6378QEgJ-L94Nmj/view?usp=sharing"
extra_rating_new_path = 'https://drive.google.com/uc?export=download&id=' + extra_rating_new_url.split('/')[-2]
extra_rating = pd.read_csv(extra_rating_new_path)

# Function to get user IDs from user name
def get_user_ids(user_name):
    user_ids = extra_rating.loc[extra_rating['Username'] == user_name, 'user_Id'].values
    return user_ids

# Chatbot function
def chatbot():
    st.title("Movie Recommendation Chatbot")
    st.write("Welcome! Let's start chatting.")

    chat_history = []

    # Chat loop
    while True:
        user_name = st.text_input("Enter your name:")

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
                user_id_input = st.text_input("Multiple user IDs found. Please enter your preferred user ID:")

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

