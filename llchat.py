import streamlit as st
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the data
@st.cache_data
def data_load():
    rating_df   =    pd.read_csv('data/final_ratings_v3.csv')
    games_df    =    pd.read_csv('data/game_learn_df_v3.csv')
    users_df    =    pd.read_csv('data/usernames_v2.csv')
    games_info  =    pd.read_csv('data/bgref.csv')
    cosine_df   =    pd.read_csv('data/bg_cosines_final.csv')
    return rating_df, games_df, users_df, games_info, cosine_df

rating_df, games_df, users_df, games_info, cosine_df = data_load()

# Function to check if user exists
def get_user_ids(user_name):
    user_ids = rating_df.loc[rating_df['Username'] == user_name, 'user_name'].values
    return user_ids

# Function to find the correct category of the favorite game
def find_right_category(favorite_game, data):
    for i, row in data.iterrows():
        if favorite_game.lower() in row['name_lower']:
            return row['consolidated_category_name']

def game_of_my_life(user_favorite_game, data, z=6):
    # Find the right category of the favorite game
    right_category_info = find_right_category(user_favorite_game, data)

    # Extract the categories of the favorite game
    favorite_game_categories = eval(right_category_info)  # Extract list in cell as unique values

    # Find games with at least one shared category from the favorite game's categories
    similar_games_with_shared_category = data[data['consolidated_category_name'].apply(lambda x: any(cat in x for cat in favorite_game_categories))]
    similar_games_with_shared_category = similar_games_with_shared_category[similar_games_with_shared_category['name_x'] != user_favorite_game]

    # Convert consolidated_category_name to list of strings
    similar_games_with_shared_category['consolidated_category_name'] = similar_games_with_shared_category['consolidated_category_name'].apply(eval)

    # Convert the categories of each game into binary vectors using MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    similar_games_category_vectors = mlb.fit_transform(similar_games_with_shared_category['consolidated_category_name'])
    user_favorite_game_category_vector = mlb.transform([favorite_game_categories])

    # Calculate cosine similarity between user favorite game and all other games
    similarity_scores = cosine_similarity(user_favorite_game_category_vector, similar_games_category_vectors)

    # Get the similarity scores for the user favorite game with all other games
    user_similarity_scores = similarity_scores[0]

    # Sort the indices based on similarity scores in descending order
    sorted_indices = np.argsort(user_similarity_scores)[::-1]

    # Get the bgg_id of the top z similar games
    similar_game_bgg_ids = similar_games_with_shared_category.iloc[sorted_indices[:z]]['bgg_id'].tolist()

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

        # Ask for user's favorite game directly
        user_favorite_game = st.text_input("Please enter your favorite game:", key=key_a)

        if user_favorite_game.strip():  # Check if the favorite game is not empty or only whitespace
            # Recommend games based on the user's favorite game
            recommended_game_ids = game_of_my_life(user_favorite_game, games_df)
            recommended_games = games_df[games_df['bgg_id'].isin(recommended_game_ids)]['name_x'].tolist()

            # Add user input to chat history
            chat_history.append(("User", user_favorite_game))
            # Add robot response to chat history
            chat_history.append(("Robot", f"Based on your favorite game '{user_favorite_game}', I recommend the following games: {', '.join(recommended_games)}. Enjoy gaming!"))

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
  
