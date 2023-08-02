# Import necessary libraries
import requests
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

# Load the data
@st.cache_data
def data_load():
    # Read the necessary CSV files into DataFrames
    rating_df = pd.read_csv('data/final_ratings_v3.csv')
    games_df = pd.read_csv('data/game_learn_df_v3.csv')
    users_df = pd.read_csv('data/usernames_v2.csv')
    games_info = pd.read_csv('data/bgref.csv')
    cosine_df = pd.read_csv('data/bg_cosines_final.csv')
    return rating_df, games_df, users_df, games_info, cosine_df

#Remove unnecessary columns and rename columns for Surprise compatibility
surprise_data = rating_df [['bgg_id', 'name', 'year', 'avg_rating']]
surprise_data = surprise_data.rename(columns={'bgg_id': 'itemID', 'avg_rating': 'rating'})

# Drop rows with missing or invalid 'rating' values
subset_data = surprise_data.dropna(subset=['rating'])
subset_data = subset_data[subset_data['rating'] != '[None]']
subset_data['rating'] = subset_data['rating'].astype(float)

# Generate unique user IDs
subset_data['userID'] = range(1, len(subset_data) + 1)

# Convert 'itemID' column to integers
subset_data['itemID'] = subset_data['itemID'].astype(int)

# Ask the user for preferred year or decade
user_input = input("Enter the year or decade (e.g., 2000 or 2000s) for game recommendations: ")
if 's' in user_input:
    # If the user specified a decade (e.g., 2000s), extract the starting and ending years
    start_year = int(user_input[:-1])
    end_year = start_year + 9
else:
    # If the user specified a single year (e.g., 2000), use that year as both start and end year
    start_year = int(user_input)
    end_year = start_year

# Filter the data based on the user's input
decade_data = subset_data[(subset_data['year'] >= start_year) & (subset_data['year'] <= end_year)]

# Load the Surprise data from the DataFrame
reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(decade_data[['userID', 'itemID', 'rating']], reader)

# Split the data into training and testing sets
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Create the SVD model and train it on the training data
model = SVD()
model.fit(trainset)

# Get a list of all item IDs in the dataset
item_ids = decade_data['itemID'].unique()

# Make predictions for all items for the specified user (userID=0 for simplicity)
user_id = 0
predictions = [model.predict(user_id, item_id) for item_id in item_ids]

# Sort the predictions based on estimated ratings in descending order
sorted_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)

# Get the top recommended items
top_recommendations = sorted_predictions[:10]

# Print the top recommended items
print(f"\nTop 10 recommended games for the {user_input}:")
for recommendation in top_recommendations:
    item_id = recommendation.iid
    item_name = decade_data.loc[decade_data['itemID'] == item_id, 'name'].iloc[0]
    estimated_rating = recommendation.est
    print(f"Item ID: {item_id}, Item Name: {item_name}, Estimated Rating: {estimated_rating:.2f}")


