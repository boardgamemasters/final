import streamlit as st

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
