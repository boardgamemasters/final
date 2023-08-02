###################################################### LIBRARIES ###########################################
import pandas as pd
import re
import nltk
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm  # For displaying progress bars
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from PIL import Image
import urllib.request

###################################################### FUNCTIONS ###########################################

######################################  GET_STEM ###########################################################
# Define the function get_stem with two input parameters: description (text to be stemmed) and stop_words 
# (list of words to be ignored during stemming)
############################################################################################################

def get_stem(description, language='english'):
    stop_words = list(set(stopwords.words(language)))
    ps = SnowballStemmer(language, ignore_stopwords=True)
    # Initialize an empty list named 'text' to store the stemmed words
    text = []
    # Split the 'description' input into individual words using the split() method
    for word in description.split():
        # Check if the current 'word' is not in the 'stop_words' list
        # If the word is not a stop word, stem it using the SnowballStemmer 
        # and append it to the 'text' list
        if word not in stop_words:
            text.append(ps.stem(word))
        else:
            continue
        # Join the stemmed words in the 'text' list back into a single string 
        # with words separated by spaces
    stem_text = ' '.join(text)
    return stem_text


######################################  CALCULATE_COSINE_SIMILARITY ########################################
# Calculates the cosine similarity matrix for the input DataFrame containing textual data. 
#It first converts the text data into numerical vectors using CountVectorizer with dimensionality reduction 
# using PCA to n_components, and then it computes the cosine similarity matrix using cosine_similarity. 
# The function returns the resulting cosine similarity matrix.
############################################################################################################

def calculate_cosine_similarity(bgdes, featotal=400, n_components=200):
    # Step 1: Convert textual data into numerical vectors using CountVectorizer
    cv = CountVectorizer(max_features=featotal)
    vectors = cv.fit_transform(bgdes).toarray()

    # Initialize the progress bar with a total of 3 steps
    progress_bar = tqdm(total=3, desc='Calculating', leave=False)

    # Step 1: CountVectorizer
    progress_bar.set_description('Step 1: CountVectorizer')
    progress_bar.update(1)

    # Step 2: Perform PCA (Principal Component Analysis) for dimensionality reduction
    pca = PCA(n_components=n_components)

    # Step 2: PCA
    progress_bar.set_description('Step 2: PCA')
    vectors_pca = pca.fit_transform(vectors)
    progress_bar.update(1)

    # Step 3: Compute Cosine Similarity
    # Cosine similarity measures the similarity between vectors in a multi-dimensional space
    progress_bar.set_description('Step 3: Cosine Similarity')
    csimlar = cosine_similarity(vectors_pca, dense_output=False)
    progress_bar.update(1)

    # Close the progress bar as all steps are complete
    progress_bar.close()

    # Return the cosine similarity matrix
    return csimlar


######################################  TRANSFORM_COSINE_DF ################################################
# Removes square brackets and trims leading and trailing whitespaces from the '0' column, splits it by comma
# delimiter into separate columns, converts the entire DataFrame to numeric data types with 'coerce' error 
# handling, and finally returns the transformed DataFrame.
############################################################################################################

def transform_cosine_df (df):
    # Remove square brackets from cos['0']
    df['0'] = df['0'].str.replace('[\[\]]', '', regex=True)
    df['0'] = df['0'].str.strip()
    
    # Split cos['0'] by comma (',') delimiter into separate columns
    df[['bgg_id', 'rec_1', 'rec_2', 'rec_3', 'rec_4', 
        'rec_5', 'rec_6', 'rec_7', 'rec_8', 'rec_9',
        'rec_10', 'rec_11', 'rec_12', 'rec_13', 'rec_14',
        'rec_15', 'rec_16', 'rec_17', 'rec_18', 'rec_19',
        'rec_20']] = df['0'].str.split(',', expand=True)
    
    # Drop cos['0'] as it's no longer needed
    df.drop('0', axis=1, inplace=True)
    
    # Converts to numeric.
    for c in df.columns:
        df[c]=pd.to_numeric(df[c], errors='coerce')
    
    return df


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
#      num = number of games to retrieve. Max 20. Default 10
# Returns: list: A list containing recommended board game IDs based on user's input.

############################################################################################################

def similar_description_games(bg_input, bg_cosines_df, bgref_df, num=10):
    cos = bg_cosines_df
    reclist = [] # Creates empty list for recommended games
    result = [] # Creates empty list for recommended games
    inth = len(bg_input) # Variable that storages the amount of games the user has introduced as liking
    
    if inth >= 2:
        for b in bg_input:
            frames = [cos.loc[cos.bgg_id==b, ['rec_1']], 
                      cos.loc[cos.bgg_id==b, ['rec_2']].rename(columns={'rec_2': 'rec_1'}),
                      cos.loc[cos.bgg_id==b, ['rec_3']].rename(columns={'rec_3': 'rec_1'}),
                      cos.loc[cos.bgg_id==b, ['rec_4']].rename(columns={'rec_4': 'rec_1'}),
                      cos.loc[cos.bgg_id==b, ['rec_5']].rename(columns={'rec_5': 'rec_1'}),
                      cos.loc[cos.bgg_id==b, ['rec_6']].rename(columns={'rec_6': 'rec_1'}), 
                      cos.loc[cos.bgg_id==b, ['rec_7']].rename(columns={'rec_7': 'rec_1'}),
                      cos.loc[cos.bgg_id==b, ['rec_8']].rename(columns={'rec_8': 'rec_1'})]
            
            # Concatenate frames and drop duplicates
            result_df = pd.concat(frames, ignore_index=True)
            result_df = result_df.drop_duplicates()
            
            # Append the unique recommendations to the result list
            result.extend(result_df['rec_1'].tolist())
        
        # Convert result list to a DataFrame and remove any recommendations in bg_input
        result = pd.DataFrame(result, columns=['rec_1'])
        result = result[~result['rec_1'].isin(bg_input)]
        
        # Sample 5 unique recommendations
        reclist = result['rec_1'].sample(n=num, replace=False).tolist()
        
    elif inth == 1:
        for i in range(1, 21):
            result.append(cos.loc[cos.bgg_id.isin(bg_input)].values[0][i])
        
        # Sample x unique recommendations
        reclist = random.sample(result, num)

    games = bgref_df.loc[bgref_df.bgg_id.isin(reclist), ['bgg_id', 'name', 'image']]
    
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
def best_general(bg, max_gm=10, year=2000, price=28, minplay=5, minage=15):

    best_min_page = bg.loc[(bg.year >= year) & 
                        (bg.num_votes >= bg.num_votes.quantile(q=0.70)) & 
                        (bg.avg_rating >= bg.avg_rating.quantile(q=0.80)) & 
                        (bg.min_players <= minplay) & 
                        (bg.min_age <= minage), 
                        ['bgg_id']].sample(max_gm)
    
    return best_min_page
    
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

############################################################################################################
######################################                             #########################################
######################################        MAKE_SQUARE          #########################################
######################################                             #########################################
############################################################################################################
# Takes an image URL (or a local image file path), resizes the image to form a square with a minimum size, 
# and then pastes the original image onto the center of the square canvas with a specified fill color.
############################################################################################################

def make_square(im, min_size=1, fill_color=(0, 0, 0, 0)):
    # Open the downloaded image using Pillow's Image.open() as "im"
    urllib.request.urlretrieve(im, "bgimage")
    with Image.open("bgimage") as im:
        # Get the original width (x) and height (y) of the image
        x, y = im.size
        # Determine the size of the square canvas (size) based on the original image's dimensions 
        # and the specified minimum size
        size = max(min_size, x, y)
        # Create a new square image with a transparent background (RGBA) of the determined size
        new_im = Image.new('RGBA', (size, size), fill_color)
        # Paste the original image onto the center of the square canvas
        new_im.paste(im, (int((size - x) / 2), int((size - y))))
    return new_im

############################################################################################################
######################################                             #########################################
######################################        FAV_BGUSER           #########################################
######################################                             #########################################
############################################################################################################
# Inputs: An user id, the number of games to retrieve, dataframes of reviews and reference
# Returns a DataFrame containing the favorite board games of the given user
############################################################################################################

def fav_bguser(user_id, bg_num, reviews_df, bg_df):

    bg_id = []
    bg_name = []
    bg_image = []

    # Extract the 'bgg_id'
    bg = list(reviews_df.loc[reviews_df.Username == user_id].sort_values(
                'Rating', ascending=False)['bgg_id'].drop_duplicates().head(bg_num).values)
    

    # Iterate over the 'bgg_id' values of the top board games
    for b in bg:
        # Find the index (position) of the matching row in the 'bg_df' and append values
        p = int(bg_df.loc[bg_df.bgg_id == b].index[0])
        bg_id.append(int(bg_df.loc[bg_df.bgg_id == b, 'bgg_id']))
        bg_name.append(bg_df.loc[bg_df.bgg_id == b, 'name'][p])
        bg_image.append(bg_df.loc[bg_df.bgg_id == b, 'image'][p])

    # Create a DataFrame 'bgames' from the lists
    bgames = pd.DataFrame(list(zip(bg_id, bg_name, bg_image)), columns=['bgg_id', 'name', 'image'])

    return bgames
