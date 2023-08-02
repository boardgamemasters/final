# Import necessary libraries
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import requests
from urllib.request import urlopen
from io import BytesIO
from streamlit_chat import message

# Import custom functions
import User_Ursula as ursula
import ameyfun as af
import funcrsys as pred

# Login Handler & other session variables
# Check if the user is logged in or not
if 'user_login' not in st.session_state:
    st.session_state['user_login'] = False
    st.session_state['user_name'] = ''

# Set Streamlit page configuration
st.set_page_config(page_title='Boardgame Recommender', layout='wide')

# Function to load data from CSV files
# Caching the data loading process for faster access
@st.cache_data
def data_load():
    rating_df = pd.read_csv('data/final_ratings_v3.csv')
    games_df = pd.read_csv('data/game_learn_df_v3.csv')
    users_df = pd.read_csv('data/usernames_v2.csv')
    games_info = pd.read_csv('data/bgref.csv')
    cosine_df = pd.read_csv('data/bg_cosines_final.csv')
    amey_df = pd.read_csv('data/final_data.csv')
    return rating_df, games_df, users_df, games_info, cosine_df, amey_df

# Load data using cache
rating_df, games_df, users_df, games_info, cosine_df, amey_df = data_load()

# Custom function to display the user's top 10 favorite games
@st.cache_data
def user_fav():
    fav_games = pred.fav_bguser(user_id=st.session_state['user_name'], bg_num=10, reviews_df=rating_df, bg_df=games_info)
    ncol = len(fav_games)
    with st.container():
        st.header(f'Hey {st.session_state["user_name"]}. Your 10 Top Rated games are:')
        for i in range(0, ncol, 5):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.image(pred.make_square(fav_games.iloc[i]['image']))
                st.text(fav_games.iloc[i]['name'])
            with col2:
                if i + 1 < ncol:
                    st.image(pred.make_square(fav_games.iloc[i + 1]['image']))
                    st.text(fav_games.iloc[i + 1]['name'])
            with col3:
                if i + 2 < ncol:
                    st.image(pred.make_square(fav_games.iloc[i + 2]['image']))
                    st.text(fav_games.iloc[i + 2]['name'])
            with col4:
                if i + 3 < ncol:
                    st.image(pred.make_square(fav_games.iloc[i + 3]['image']))
                    st.text(fav_games.iloc[i + 3]['name'])
            with col5:
                if i + 4 < ncol:
                    st.image(pred.make_square(fav_games.iloc[i + 4]['image']))
                    st.text(fav_games.iloc[i + 4]['name'])

# Custom function to display personalized recommendations for the user
@st.cache_data
def special_treat():
    user_games = ursula.gib_spiele_digga(rat_df=rating_df, s_alt=10, user=st.session_state['user_name'], game_frame=games_df)
    user_games = ursula.get_feature(result_file=user_games, feature_file=games_info)
    ncol = len(user_games)
    with st.container():
        st.header(f'Special Treats for you {st.session_state["user_name"]}')
        for i in range(0, ncol, 5):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.image(pred.make_square(user_games.iloc[i]['image']))
                st.text(user_games.iloc[i]['name'])
            with col2:
                if i + 1 < ncol:
                    st.image(pred.make_square(user_games.iloc[i + 1]['image']))
                    st.text(user_games.iloc[i + 1]['name'])
            with col3:
                if i + 2 < ncol:
                    st.image(pred.make_square(user_games.iloc[i + 2]['image']))
                    st.text(user_games.iloc[i + 2]['name'])
            with col4:
                if i + 3 < ncol:
                    st.image(pred.make_square(user_games.iloc[i + 3]['image']))
                    st.text(user_games.iloc[i + 3]['name'])
            with col5:
                if i + 4 < ncol:
                    st.image(pred.make_square(user_games.iloc[i + 4]['image']))
                    st.text(user_games.iloc[i + 4]['name'])

# Load data and cache it for faster access

rating_df, games_df, users_df, games_info, cosine_df, amey_df = data_load()

# Streamlit app layout
st.header("Find awesome Games")
st.sidebar.header('What do you wanna do?')

# Check if the user wants a personalized experience
custom = st.sidebar.checkbox('Personalized Experience', value=False, key='custom',
                             help='Click this to get Custom recommendations')

# Placeholder for login form
placeholder = st.sidebar.empty()

# User login handling
if st.session_state['user_login'] == False:
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        User = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    # Check if login is successful and set user session variables
    if submit and users_df['Username'].str.fullmatch(User).any() == True:
        placeholder.empty()
        st.session_state['user_login'] = True
        st.session_state['user_name'] = User
        st.success("Login successful")
    elif submit and users_df['Username'].str.fullmatch(User).any() == False:
        st.error(f"User: {User} not found")
    else:
        pass

# Logout button
if st.session_state['user_login'] == True:
    byebye = st.sidebar.button("Logout")
    if byebye:
        placeholder.empty()
        st.session_state['user_login'] = False
        st.session_state['user_name'] = ''
        st.success("Logout successful")
        special_treat.clear()
        user_fav.clear()

# Check if custom recommendation is selected
if custom == True:
    rec_select = st.sidebar.radio(
        "What kind of recommendation do you like",
        (
            'Similar Games based on Description',
            'Similar Taste',
            'Amey likes you a lot',
            'Chatbot Recommender'
         ), key='rec_select')
else:
    rec_select = ''

# Recommendation types
# 1. Similar Games based on Description
if rec_select == 'Similar Games based on Description':
    def game_like():
        title = st.sidebar.multiselect('Games like', games_info.sort_values('name')['name'])

        game_id = games_info.loc[games_info['name'].isin(title), 'bgg_id']

        data = {'bgg_id': game_id}
        return data

    sim_feature = list(game_like()['bgg_id'])

    if len(sim_feature) > 0:
        sim_games = pred.similar_description_games(bg_input=sim_feature, bg_cosines_df=cosine_df, bgref_df=games_info)
        ncol = len(sim_games)
        with st.container():
            st.header(f'Here are 5 Games, that are similar to the {len(sim_feature)} games you selected')
            for i in range(0, ncol, 3):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(sim_games.iloc[i]['image'])
                    st.text(sim_games.iloc[i]['name'])
                with col2:
                    if i + 1 < ncol:
                        st.image(sim_games.iloc[i + 1]['image'])
                        st.text(sim_games.iloc[i + 1]['name'])
                with col3:
                    if i + 2 < ncol:
                        st.image(sim_games.iloc[i + 2]['image'])
                        st.text(sim_games.iloc[i + 2]['name'])
    else:
        st.header(f'Please select Games on the left side!')

# 2. Similar Taste
elif rec_select == 'Similar Taste':
    def user_like():
        user = st.sidebar.selectbox('Who are you', users_df['Username'], key='user_like')
        amount = st.sidebar.slider('Number of Recommendations', min_value=3, max_value=15, value=9, step=3, key='uln',
                                   help='Here you can specify the number of recommended Boardgames')

        data = {'user_id': user,
                'amount': amount,
                'name': user}
        return data

    user_feature = user_like()
    user_games = ursula.gib_spiele_digga(rat_df=rating_df, s_alt=user_feature['amount'], user=user_feature['user_id'],
                                         game_frame=games_df)
    user_games = ursula.get_feature(result_file=user_games, feature_file=games_info)

    ncol = len(user_games)
    with st.container():
        st.header(f'Special Treats for you {user_feature["name"]}')
        for i in range(0, ncol, 3):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(user_games.iloc[i]['image'])
                st.text(user_games.iloc[i]['name'])
            with col2:
                if i + 1 < ncol:
                    st.image(user_games.iloc[i + 1]['image'])
                    st.text(user_games.iloc[i + 1]['name'])
            with col3:
                if i + 2 < ncol:
                    st.image(user_games.iloc[i + 2]['image'])
                    st.text(user_games.iloc[i + 2]['name'])

# 3. Amey likes you a lot
elif rec_select == 'Amey likes you a lot':
    def amey_like():
        gname = st.sidebar.selectbox('What Game do you like', amey_df['name_x'], key='amey_like')
        amount = st.sidebar.slider('Number of Recommendations', min_value=4, max_value=16, value=8, step=4, key='aln',
                                   help='Here you can specify the number of recommended Boardgames')

        data = {'amount': amount,
                'name': gname}
        return data

    amey_feature = amey_like()
    amey_games = pd.DataFrame({'bgg_id': af.game_of_my_life(user_favorite_game=amey_feature['name'], data=amey_df,
                                                            z=amey_feature['amount'])})
    amey_games = ursula.get_feature(result_file=amey_games, feature_file=games_info)

    ncol = len(amey_games)
    with st.container():
        st.header(f'Games similar to  {amey_feature["name"]}')
        for i in range(0, ncol, 4):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.image(amey_games.iloc[i]['image'])
                st.text(amey_games.iloc[i]['name'])
            with col2:
                if i + 1 < ncol:
                    st.image(amey_games.iloc[i + 1]['image'])
                    st.text(amey_games.iloc[i + 1]['name'])
            with col3:
                if i + 2 < ncol:
                    st.image(amey_games.iloc[i + 2]['image'])
                    st.text(amey_games.iloc[i + 2]['name'])
            with col4:
                if i + 3 < ncol:
                    st.image(amey_games.iloc[i + 3]['image'])
                    st.text(amey_games.iloc[i + 3]['name'])

# 4. Chatbot Recommender
elif rec_select == 'Chatbot Recommender':
    games = amey_df['name_x']
    st.sidebar.text('Coming Soon')

    # Function to handle user input change
    def on_input_change():
        user_input = st.session_state.user_input
        st.session_state.responses.append(user_input)
        st.session_state.user_input = ""  # Clear the input after processing

    # Function to clear the chat
    def on_btn_click():
        del st.session_state['questions']
        del st.session_state['responses']
        selecthor = 0

    st.session_state.setdefault('questions', [])

    # List of chat questions
    questions_list = [
        # 0
        '''I would like to recommend you some Boardgames.
        What is your favorite one?''',
        # 1
        '''I don't know this Game.
        Please enter another one''',
        # 2
        '''How many recommendations do you want to get?
        Please enter a Number between 1 and 5'''
    ]

    # Initialize chat session
    if 'responses' not in st.session_state.keys():
        st.session_state.questions.extend(questions_list)
        st.session_state.responses = []

    chat_placeholder = st.empty()
    st.button("Clear message", on_click=on_btn_click)

    message(st.session_state.questions[0])

    with st.container():
        selecthor = 0
        count = 0
        for response in (st.session_state.responses):
            count += 1
            if selecthor == 0:
                message(response, is_user=True, key=f"a1{count}")
                if games.str.fullmatch(response, case=False).any():
                    if ((games.str.fullmatch(response, case=False)).sum()) != 1:
                        sel_game = games[games.str.fullmatch(response, case=False)][0].item()
                    else:
                        sel_game = games[games.str.fullmatch(response, case=False)].item()
                    selecthor = 1
                    message(st.session_state.questions[2], key=f"b2{count}")
                    continue
                else:
                    message(st.session_state.questions[1], key=f"b1{count}")

            if selecthor == 1:
                message(response, is_user=True, key=f"a2{count}")
                if response.isnumeric():
                    alt = int(response)
                    if alt < 1:
                        alt = 1
                    elif alt > 5:
                        alt = 5
                    else:
                        alt = alt
                    selecthor = 3
                    message(f'''Your favorite boardgame is {sel_game}.
                    And you would like to get {alt} recommendations for similar games.
                    Is that correct?
                    (y), (n)''', key=f"b4{count}")
                    continue
                else:
                    message('Please enter a numeric value', key=f"b3{count}")

            if selecthor == 2:
                selecthor = 3
                continue

            if selecthor == 3:
                message(response, is_user=True, key=f"a3{count}")
                if (pd.Series(['y', 'Y', 'yes', 'Yes'])).isin([response]).any():
                    message('I can recommend you the following games:', key=f"b5{count}")
                    amey_games = pd.DataFrame(
                        {'bgg_id': af.game_of_my_life(user_favorite_game=sel_game, data=amey_df, z=alt)})
                    amey_games = ursula.get_feature(result_file=amey_games, feature_file=games_info)
                    res_co = 0
                    for i in range(len(amey_games)):
                        message(
                            f'<img width="100%" height="200" src="{amey_games.iloc[res_co]["image"]}"/><br>{amey_games.iloc[res_co]["name"]}',
                            key=f"img_{count}_{res_co}",
                            allow_html=True
                        )
                        res_co += 1

                elif (pd.Series(['n', 'N', 'no', 'No'])).isin([response]).any():
                    message('Lets try again', key=f"b6{count}")
                    selecthor = 0
                    continue
                else:
                    message(f'''{response} is not a valid input. Please try again
                    What is your favorite Boardgame?''', key=f"b7{count}")
                    selecthor = 0
                    continue

    with st.container():
        st.text_input("User Response:", on_change=on_input_change, key="user_input")

# Display the user's top 10 favorite games and personalized recommendations if the user is logged in
if st.session_state['user_login'] == True:
    user_games = ursula.gib_spiele_digga(rat_df=rating_df, s_alt=10, user=st.session_state['user_name'],
                                         game_frame=games_df)
    user_games = ursula.get_feature(result_file=user_games, feature_file=games_info)
    ncol = len(user_games)
    with st.container():
        with st.expander(f"Your Top10 Games:"):
            user_fav()

        with st.expander(f"10 Games we think you might enjoy:"):
            special_treat()

else:
    st.write('')


