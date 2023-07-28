import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

# Function to find the correct category of the favorite game
def find_right_category(favorite_game, data):
    for i, row in data.iterrows():
        if favorite_game.lower() in row['name_lower']:
            return row['consolidated_category_name'] 
        
def game_of_my_life(user_favorite_game, data, z=6):
    # Find the right category of the favorite game
    right_category_info = find_right_category(user_favorite_game, data)

    # Extract the categories of the favorite game
    favorite_game_categories = eval(right_category_info)        #Extract list in cell as unique values

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

    return(sorted_indices[0:z])
