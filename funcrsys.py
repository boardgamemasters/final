############################################################################################################
#########################################     LIBRARIES      ###############################################
import pandas as pd
import random
from PIL import Image
import urllib.request
############################################################################################################
######################################                             #########################################
######################################  SIMILAR_DESCRIPTION_GAMES  #########################################
######################################                             #########################################
############################################################################################################
# Function to recommend similar games based on a user's input of liking certain games and their descriptions
# Parameters: 
#       bg_input (list): A list of board game IDs that the user likes.
#       df_cosines_distances: DataFrame containing cosine distances for different board games.
#       df_reference: A DataFrame containing reference information about board games (bgg_id, name, and image).
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

    games = bgref_df.loc[bgref_df.bgg_id.isin(reclist), ['bgg_id', 'name', 'image', 'video']]
    
    return games


############################################################################################################
######################################                             #########################################
######################################  BEST_GENERAL               #########################################
######################################                             #########################################
############################################################################################################
#    Get the best items from the provided pandas DataFrame based on various conditions.
#    Parameters:
#            bg (pandas.DataFrame): The DataFrame containing the board game data.
#            max_gm (int): The maximum number of items to sample for each condition.
#            year (int, optional): The year to consider. Default is 2012.
#            price (int, optional): The maximum price (europrice) to consider. Default is 28.
#            minplay (int, optional): The minimum number of players to consider. Default is 2.
#            minage (int, optional): The minimum age to consider. Default is 10.
#    Returns:
#            tuple: A tuple containing multiple DataFrames, each representing the best items
#            that satisfy specific conditions.
############################################################################################################
def best_general(bg, max_gm, year=2012, price=28, minplay=2, minage=10):

    # Filter and sample the best items for a particular year
    best_year = bg.loc[(bg.year == year) & 
                       (bg.num_votes >= bg.num_votes.quantile(q=0.75)) & 
                       (bg.avg_rating >= bg.avg_rating.quantile(q=0.85)), 
                       ['bgg_id', 'name_x', 'image', 'video']].sample(max_gm)

    # Filter and sample the best items based on price and other conditions
    best_price = bg.loc[(bg.year == year) & 
                        (bg.num_votes >= bg.num_votes.quantile(q=0.70)) & 
                        (bg.avg_rating >= bg.avg_rating.quantile(q=0.70)) & 
                        (bg.europrice <= price), 
                        ['bgg_id', 'name_x', 'image', 'video']].sample(max_gm)
    
    # Filter and sample the best items based on minimum number of players and other conditions
    best_min_players = bg.loc[(bg.year == year) & 
                              (bg.num_votes >= bg.num_votes.quantile(q=0.70)) & 
                              (bg.avg_rating >= bg.avg_rating.quantile(q=0.70)) & 
                              (bg.min_players <= minplay), 
                              ['bgg_id', 'name_x', 'image', 'video']].sample(max_gm)
    
    # Filter and sample the best items based on minimum age and other conditions
    best_min_age = bg.loc[(bg.year == year) & 
                          (bg.num_votes >= bg.num_votes.quantile(q=0.70)) & 
                          (bg.avg_rating >= bg.avg_rating.quantile(q=0.70)) & 
                          (bg.min_age <= minage), 
                          ['bgg_id', 'name_x', 'image', 'video']].sample(max_gm)
    
    # Filter and sample the best items based on both minimum number of players and minimum age, along with other conditions
    best_min_page = bg.loc[(bg.year == year) & 
                           (bg.num_votes >= bg.num_votes.quantile(q=0.70)) & 
                           (bg.avg_rating >= bg.avg_rating.quantile(q=0.70)) & 
                           (bg.min_players <= minplay) & 
                           (bg.min_age <= minage), 
                           ['bgg_id', 'name_x', 'image', 'video']].sample(max_gm)
    
    return best_year, best_price, best_min_players, best_min_age, best_min_page
    
############################################################################################################
######################################                             #########################################
######################################        RESIZE_IMG           #########################################
######################################                             #########################################
############################################################################################################
# Takes an image URL and optional width (w) and height (h) parameters to resize the image and returns the
# resized image.
############################################################################################################

def resize_img(url, w=400, h=400):
    # Download the image from the provided URL and save it as "bgimage"
    urllib.request.urlretrieve(url, "bgimage")
    
    # Open the downloaded image and resize it to the desired size
    with Image.open("bgimage") as im:
        imageres = im.resize((w, h), Image.LANCZOS)
    
    return imageres

def make_square(im, min_size=600, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y))))
    return new_im