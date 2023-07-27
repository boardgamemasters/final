############################################################################################################
#########################################     LIBRARIES      ###############################################
import pandas as pd
import random
############################################################################################################
######################################                             #########################################
######################################  SIMILAR_DESCRIPTION_GAMES  #########################################
######################################                             #########################################
############################################################################################################
# Function to recommend similar games based on a user's input of liking certain games and their descriptions
# Parameters: 
#      bg_input (list): A list of board game IDs that the user likes.
#      df_cosines_distances: DataFrame containing cosine distances for different board games.
#      df_reference: A DataFrame containing reference information about board games (bgg_id, name, and image).
# Returns: list: A list containing recommended board game IDs based on user's input.

############################################################################################################

def similar_description_games(bg_input, bg_cosines_df, bgref_df):
    cos = bg_cosines_df
    reclist = [] # Creates empty list for recommended games
    result = [] # Creates empty list for recommended games
    inth = len(bg_input) # Variable that storages the amount of games the user has introduced as liking
    
    if inth >= 2:
        for b in bg_input:
            frames = [cos.loc[cos.bgg_id==b, ['rec_1']], 
                      cos.loc[cos.bgg_id==b, ['rec_2']].rename(columns={'rec_2': 'rec_1'}),
                      cos.loc[cos.bgg_id==b, ['rec_3']].rename(columns={'rec_3': 'rec_1'}),
                      cos.loc[cos.bgg_id==b, ['rec_4']].rename(columns={'rec_4': 'rec_1'})]
            
            # Concatenate frames and drop duplicates
            result_df = pd.concat(frames, ignore_index=True)
            result_df = result_df.drop_duplicates()
            
            # Append the unique recommendations to the result list
            result.extend(result_df['rec_1'].tolist())
        
        # Convert result list to a DataFrame and remove any recommendations in bg_input
        result = pd.DataFrame(result, columns=['rec_1'])
        result = result[~result['rec_1'].isin(bg_input)]
        
        # Sample 5 unique recommendations
        reclist = result['rec_1'].sample(n=5, replace=False).tolist()
        
    elif inth == 1:
        for i in range(1, 10):
            result.append(cos.loc[cos.bgg_id.isin(bg_input)].values[0][i])
        
        # Sample 5 unique recommendations
        reclist = random.sample(result, 5)

    games = bgref_df.loc[bgref_df.bgg_id.isin(reclist), ['bgg_id', 'name', 'image']]
    
    return games
