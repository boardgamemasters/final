import streamlit as st
import pandas as pd
import ameyfun as amey

# Load the data
@st.cache_data
def data_load():
    rating_df = pd.read_csv('data/final_ratings_v3.csv')
    games_df = pd.read_csv('data/game_learn_df_v3.csv')
    users_df = pd.read_csv('data/usernames_v2.csv')
    games_info = pd.read_csv('data/bgref.csv')
    cosine_df = pd.read_csv('data/bg_cosines_final.csv')
    final_df = pd.read_csv('data/final_data.csv')
    return rating_df, games_df, users_df, games_info, cosine_df, final_df


rating_df, games_df, users_df, games_info, cosine_df, final_df = data_load()

# Function to find the correct category of the favorite game
def find_right_category(favorite_game, data):
    for i, row in data.iterrows():
        if favorite_game.lower() in row['game_name_lower']:
            return row['consolidated_category_name']

def game_recommendation(user_favorite_game, data, z=6):
    # Find the right category of the favorite game
    right_category_info = find_right_category(user_favorite_game, data)

    # Extract the categories of the favorite game
    favorite_game_categories = eval(right_category_info)  # Extract list in cell as unique values

    # Find games with at least one shared category from the favorite game's categories
    similar_games_with_shared_category = data[data['consolidated_category_name'].apply(lambda x: any(cat in x for cat in favorite_game_categories))]
    similar_games_with_shared_category = similar_games_with_shared_category[similar_games_with_shared_category['game_name'] != user_favorite_game]

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

    # Chat loop
    while True:
        # Ask for user's favorite game directly
        user_favorite_game = st.text_input("Please enter the name of the game that you like:")

        if user_favorite_game.strip():  # Check if the favorite game is not empty or only whitespace
            # Recommend games based on the user's favorite game
            recommended_game_ids = game_recommendation(user_favorite_game, final_df)
            recommended_games = final_df[final_df['bgg_id'].isin(recommended_game_ids)]['game_name'].tolist()

            # Display recommended games
            st.write(f"Based on your favorite game '{user_favorite_game}', I recommend the following games:")
            for game in recommended_games:
                st.write(f"- {game}")

        # Break the chat loop if user input is "quit"
        if user_favorite_game.lower() == "quit":
            break

if __name__ == "__main__":
    chatbot()
