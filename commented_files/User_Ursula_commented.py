# Import necessary modules
import pandas as pd
import math
import warnings
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Ignore warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)

# Function to scale the dataset using MinMaxScaler
def ScaleMeUpScotty(wf):
    # Set 'bgg_id' as the index
    wf.set_index('bgg_id', inplace=True)
    scaler = MinMaxScaler()

    # Scale each column using MinMaxScaler
    for col in wf.columns:
        colly = wf.loc[:, col].values.reshape(-1, 1)
        wf.loc[:, col] = scaler.fit_transform(colly)

    # Reset the index and return the scaled DataFrame
    wf['avg_rating'] = wf['avg_rating']
    wf['complexity'] = wf['complexity']
    wf.reset_index(inplace=True)
    return wf

# Function to adjust game ratings based on user's preferences
def weight_game(user_id, wd):
    wd = wd.loc[wd['Username'] == user_id]
    if (((wd['Rating'].max()) - (wd['Rating'].min())) <= 2):
        substractor = 5
    else:
        substractor = wd['Rating'].mean()
    wd['Rating'] = wd['Rating'] - substractor
    result_dict = wd.set_index('bgg_id')['Rating'].to_dict()
    return result_dict

# Function to drop columns with zero values for specified bgg_id list
def col_dropper(wd, bgg_id_list=[]):
    wd_red = wd.loc[wd['bgg_id'].isin(bgg_id_list)]
    wd_red = wd_red.sum()
    wd_red = list(wd_red.loc[wd_red == 0].reset_index()['index'])
    answer = wd.drop(columns=(wd_red))
    return answer

# Function to find games with similar attributes
def similar_games(games_df, alt=10, bgg_ids_with_weights={}):
    # Drop columns with zero values for specified bgg_id list
    games_df = col_dropper(wd=games_df, bgg_id_list=list(bgg_ids_with_weights.keys()))
    selected_games_attributes = games_df[games_df['bgg_id'].isin(bgg_ids_with_weights.keys())].iloc[:, 2:]

    if selected_games_attributes.empty:
        print("No games found for the specified bgg_ids.")
        return pd.DataFrame()

    # Calculate the similarity between all games and the specified games using cosine similarity
    similarity_scores = cosine_similarity(selected_games_attributes, games_df.iloc[:, 2:])

    # Apply the weights to the similarity scores
    for bgg_id, weight in bgg_ids_with_weights.items():
        indices = games_df[games_df['bgg_id'] == bgg_id].index
        if len(indices) > 0:
            index = indices[0]
            similarity_scores[:, index] *= weight

    # Sum the similarity scores across the rows
    total_similarity_scores = similarity_scores.mean(axis=0)

    # Add similarity scores as a new column to the DataFrame
    games_with_similarity = games_df.assign(similarity=total_similarity_scores)

    # Get rid of games in rated frame
    games_with_similarity = games_with_similarity.loc[~games_with_similarity['bgg_id'].isin(list(bgg_ids_with_weights.keys()))]

    # Sort the games based on similarity scores in descending order
    top_similar_games = games_with_similarity.sort_values('similarity', ascending=False).head(alt)

    return list(top_similar_games['bgg_id'])

# Function to perform MinBO reduction on the dataset
def minbo_reduction(wf, user):
    minbo = math.floor((wf.loc[wf['Username'] == user, 'count']))
    print(f'start minbo: {minbo}')
    correction = 1
    while correction == 1:
        wt = wf.loc[wf['count'] >= minbo]
        if len(wt) <= 150:
            minbo = math.floor(minbo * 0.99)
        elif minbo <= 1:
            sys.exit("not enough Ratings")
        else:
            print(f'Minbo set to {minbo}')
            correction = 0
            wf = wt
    return wf

# Function to find games with similar taste
def similar_taste(wf, include_games, u_id, alt=10):
    filtered_df = wf[wf['Username'] == u_id]
    games = filtered_df['bgg_id'].unique()
    filtered_df = wf[wf['bgg_id'].isin(games)]
    count_table = filtered_df['Username'].value_counts().reset_index()
    count_table.columns = ['Username', 'count']

    count_table = minbo_reduction(wf=count_table, user=u_id)

    user_filter = wf[wf['bgg_id'].isin(include_games)]['Username'].unique()

    count_table = count_table.loc[(count_table['Username'].isin(user_filter)) | (count_table['Username'] == u_id), 'Username']

    keeper = wf.copy()

    wf = wf.loc[wf['Username'].isin(count_table)]

    only_known = wf.copy()
    only_known.loc[only_known['Username'] == u_id, 'bgg_id']
    only_known.loc[only_known['bgg_id'].isin(only_known.loc[only_known['Username'] == u_id, 'bgg_id'])]

    users_items = pd.pivot_table(
        data=wf.loc[wf['bgg_id'].isin(include_games)],
        values='Rating',
        index='Username',
        columns='bgg_id'
    )

    known_items = pd.pivot_table(
        data=only_known,
        values='Rating',
        index='Username',
        columns='bgg_id'
    )

    users_items.fillna(0, inplace=True)
    known_items.fillna(0, inplace=True)

    user_similarities = pd.DataFrame(
        cosine_similarity(known_items),
        columns=known_items.index,
        index=known_items.index
    )

    weights = (
        user_similarities.query("Username!=@u_id")[u_id] / sum(user_similarities.query("Username!=@u_id")[u_id])
    )

    # Select restaurants that the input user has not visited
    not_visited_restaurants = users_items

    # Dot product between the not-visited-restaurants and the weights
    weighted_averages = pd.DataFrame(not_visited_restaurants.T.dot(weights), columns=["predicted_rating"])

    result = weighted_averages.sort_values("predicted_rating", ascending=False).head(alt)

    result.reset_index(inplace=True)

    return result

# Main function to recommend games based on user's preferences
def gib_spiele_digga(rat_df, game_frame, f_alt=1000, s_alt=10, user='beastvol'):
    answer = similar_taste(
        wf=rat_df,
        include_games=similar_games(
            games_df=ScaleMeUpScotty(wf=game_frame),
            alt=f_alt,
            bgg_ids_with_weights=weight_game(user_id=user, wd=rat_df)
        ),
        alt=s_alt,
        u_id=user
    )
    return answer

# Function to get features of the recommended games
def get_feature(result_file, feature_file):
    return feature_file.loc[feature_file['bgg_id'].isin(result_file['bgg_id'])]
