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
import User_Ursula as ursula

import funcrsys as pred

st.set_page_config(page_title='Boardgame Recommender')#, page_icon=logo)


@st.cache_data
def data_load():
    rating_df   =    pd.read_csv('data/final_ratings_v3.csv')
    games_df    =    pd.read_csv('data/game_learn_df_v3.csv')
    users_df    =    pd.read_csv('data/usernames_v2.csv')
    games_info  =    pd.read_csv('data/bgref.csv')
    cosine_df   =    pd.read_csv('data/bg_cosines_final.csv')
    return rating_df, games_df, users_df, games_info, cosine_df


rating_df, games_df, users_df, games_info, cosine_df = data_load()

# # Download the image using requests
# response = requests.get(logo_url)
# image_bytes = response.content

# # Open the image using PIL
# logo = Image.open(BytesIO(image_bytes))


st.header("Find awesome Games")

st.sidebar.header('What do you wanna do?')

custom = st.sidebar.checkbox('Personalized Experience', value=False, key='custom', help='Click this to get Custom recommendations')

if custom == True:
    rec_select = st.sidebar.radio(
        "What kind of recommendation do you like",
        ('Similar Games', 'Similar Taste', 'Games that are hot right now', 'All at once'), key='rec_select')
else:
    # st.write('Basic Bitch!')
    rec_select = ''
    # pop_movies = pred.pop_movies(wf = rating_df)
    # st.dataframe(pop_movies)

    # ncol = len(pop_movies)
    # cols = st.columns(ncol)
    # with st.container():
    #     for i, x in enumerate(cols):
    #         st.header(pop_movies.iloc[i]['title'])
    #         st.image(pop_movies.iloc[i]['img'])

    
    ncol = 3#len(pop_movies)
    with st.container():
        for i in range(0, ncol, 3):
            col1, col2, col3 = st.columns(3)
            with col1:
                # st.image(pop_movies.iloc[i]['img'])
                st.text('Spiel 1')    # (pop_movies.iloc[i]['title'])
            with col2:
                if i + 1 < ncol:
                    # st.image(pop_movies.iloc[i+1]['img'])
                    st.text('Spiel 2')    # (pop_movies.iloc[i+1]['title'])                    
            with col3:                 
                if i + 2 < ncol:
                    # st.image(pop_movies.iloc[i+2]['img'])
                    st.text('Spiel 3')    # (pop_movies.iloc[i+2]['title'])
                    

    

if rec_select == 'Similar Games':
    def game_like():
        title = st.sidebar.multiselect('Games like', games_info['name'])    # titles_df['title'], key = 'movie_like')
        #amount = st.sidebar.slider('Number of Recommendations', min_value=1, max_value=5, value=3, step=1, key='mln', help='Here you can specify the number of recommended Games')

        game_id = games_info.loc[games_info['name'].isin(title),'bgg_id']#.values[0]

        data = {'bgg_id': game_id#,    #    mov_id,
                #'amount': amount
                }
        return(data)
    sim_feature =  list(game_like()['bgg_id'])
    st.write(len(sim_feature))
    ## similar_description_games(bg_input, bg_cosines_df, bgref_df)
    sim_games = pred.similar_description_games(bg_input = sim_feature, bg_cosines_df = cosine_df, bgref_df = games_info)

    # mov_col = len(sim_movies)
    # m_cols = st.columns(mov_col)
    # with st.container():
    #     st.header(f'Users that liked {sim_feature["name"]}, also liked these {sim_feature["amount"]} movies')
    #     for i, x in enumerate(m_cols):
    #         st.header(sim_movies.iloc[i]['title'])
    #         st.image(sim_movies.iloc[i]['img'])
    ncol = 5#sim_feature['amount']#len(sim_movies)
    st.dataframe(sim_games)
    # with st.container():
    #     st.header(f'Here are 5 Games, that are similar to the games you selected')
    #     for i in range(0, ncol, 3):
    #         col1, col2, col3 = st.columns(3)
    #         with col1:
    #             st.image(sim_games.iloc[i]['image'])
    #             st.text(sim_games.iloc[i]['name'])
    #         with col2:
    #             if i + 1 < ncol:
    #                 st.image(sim_games.iloc[i+1]['image'])
    #                 st.text(sim_games.iloc[i+1]['name'])    
    #         with col3:                 
    #             if i + 2 < ncol:
    #                 st.image(sim_games.iloc[i+2]['image'])
    #                 st.text(sim_games.iloc[i+2]['name'])  

elif rec_select == 'Similar Taste':
    def user_like():
        user = st.sidebar.selectbox('Who are you', users_df['Username'], key = 'user_like')
        amount = st.sidebar.slider('Number of Recommendations', min_value=3, max_value=15, value=9, step=3, key='uln', help='Here you can specify the number of recommended Boardgames')

        data = {'user_id': user,
                'amount': amount,
                'name' : user}
        return(data)
    user_feature =  user_like()
    # st.sidebar.text('Login to use this Feature')    # (pop_movies.iloc[i+2]['title'])
    user_games = ursula.gib_spiele_digga(rat_df = rating_df, s_alt = user_feature['amount'], user = user_feature['user_id'],game_frame=games_df)
    user_games = ursula.get_feature(result_file=user_games, feature_file=games_info)
    # user_col = len(user_games)
    # u_cols = st.columns(user_col)
    # with st.container():
    #     st.header(f'Special Treats for you {user_feature["name"]}')
    #     for i, x in enumerate(u_cols):
    # #         st.header(user_games.iloc[i]['title'])
    #         # st.image(user_games.iloc[i]['img'])
    #         st.header(user_games.iloc[i]['bgg_id'])
    #         st.text(user_games.iloc[i]['predicted_rating'])
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
                    st.image(user_games.iloc[i+1]['image'])
                    st.text(user_games.iloc[i+1]['name'])                    
            with col3:                 
                if i + 2 < ncol:
                    st.image(user_games.iloc[i+2]['image'])
                    st.text(user_games.iloc[i+2]['name'])

elif rec_select == 'Games that are hot right now':
    st.sidebar.text('Coming Soon')
#     st.write('Lets find some lit Movies.')

#     def pop_mov():
#         amount = st.sidebar.slider('Number of Recommendations', min_value=1, max_value=20, value=5, step=1, key='pln', help='Here you can specify the number of recommended Movies')
#         period = st.sidebar.radio(
#             "What Timespan do u want to include to calculate the right movies for you?",
#             ('all', 'weeks', 'months', 'years', 'days'), key='period')
#         if period != 'all':
#             start_time = st.sidebar.slider(f'Last {period}', min_value=2, max_value=40, value=5, key='stime', help=f'Here you can define what time period in {period} will be used to make recommendations')
#         else:
#             start_time = '1'


#         data = {'period': period,
#                 'time_mod':start_time,
#                 'amount': amount}
#         return(data)
#     pop_feature =  pop_mov()
#     pop_movies_custom = pred.pop_movies(wf = rating_df, alt = pop_feature['amount'], period = pop_feature['period'], time_mod = pop_feature['time_mod'])

#     # pop_col = len(pop_movies_custom)
#     # p_cols = st.columns(pop_col)
#     # with st.container():
#     #     st.header(f'These movies are Lit')
#     #     for i, x in enumerate(p_cols):
#     #         st.header(pop_movies_custom.iloc[i]['title'])
#     #         st.image(pop_movies_custom.iloc[i]['img'])
#     ncol = len(pop_movies_custom)
#     with st.container():
#         st.header(f'These movies are Lit')
#         for i in range(0, ncol, 3):
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.image(pop_movies_custom.iloc[i]['img'])
#                 st.text(pop_movies_custom.iloc[i]['title'])
#             with col2:
#                 if i + 1 < ncol:
#                     st.image(pop_movies_custom.iloc[i+1]['img'])
#                     st.text(pop_movies_custom.iloc[i+1]['title'])                    
#             with col3:                 
#                 if i + 2 < ncol:
#                     st.image(pop_movies_custom.iloc[i+2]['img'])
#                     st.text(pop_movies_custom.iloc[i+2]['title'])

elif rec_select == 'All at once':
    st.sidebar.text('Coming Soon')

#     st.write('Lets do all together!')

#     def movie_like():
#         title = st.sidebar.selectbox('Movie like', titles_df['title'], key = 'movie_like')
#         amount = st.sidebar.slider('Number of Recommendations', min_value=1, max_value=20, value=5, step=1, key='mln', help='Here you can specify the number of recommended Movies')

#         mov_id = titles_df.loc[titles_df['title']== title,'movieId'].values[0]

#         data = {'title': mov_id,
#                 'amount': amount,
#                 'name':title}
#         return(data)
#     sim_feature =  movie_like()
#     sim_movies = pred.similar_movies(wf = rating_df, alt = sim_feature['amount'], movie_id = sim_feature['title'])

#     # mov_col = len(sim_movies)
#     # m_cols = st.columns(mov_col)
#     # with st.container():
#     #     st.header(f'Users that liked {sim_feature["name"]}, also liked these {sim_feature["amount"]} movies')
#     #     for i, x in enumerate(m_cols):
#     #         st.header(sim_movies.iloc[i]['title'])
#     #         st.image(sim_movies.iloc[i]['img'])
#     ncol = len(sim_movies)
#     with st.container():
#         st.header(f'Users that liked {sim_feature["name"]}, also liked these {sim_feature["amount"]} movies')
#         for i in range(0, ncol, 3):
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.image(sim_movies.iloc[i]['img'])
#                 st.text(sim_movies.iloc[i]['title'])
#             with col2:
#                 if i + 1 < ncol:
#                     st.image(sim_movies.iloc[i+1]['img'])
#                     st.text(sim_movies.iloc[i+1]['title'])                    
#             with col3:                 
#                 if i + 2 < ncol:
#                     st.image(sim_movies.iloc[i+2]['img'])
#                     st.text(sim_movies.iloc[i+2]['title'])

#     def user_like():
#         user = st.sidebar.selectbox('Who are you', users_df['name'], key = 'user_like')
#         amount = st.sidebar.slider('Number of Recommendations', min_value=1, max_value=20, value=5, step=1, key='uln', help='Here you can specify the number of recommended Movies')

#         user_id = users_df.loc[users_df['name']== user,'userId'].values[0]

#         data = {'user_id': user_id,
#                 'amount': amount,
#                 'name' : user}
#         return(data)
#     user_feature =  user_like()
#     user_movies = pred.similar_taste(wf = rating_df, alt = user_feature['amount'], u_id = user_feature['user_id'])

#     # user_col = len(user_movies)
#     # u_cols = st.columns(user_col)
#     # with st.container():
#     #     st.header(f'Special Treats for you {user_feature["name"]}')
#     #     for i, x in enumerate(u_cols):
#     #         st.header(user_movies.iloc[i]['title'])
#     #         st.image(user_movies.iloc[i]['img'])
#     ncol = len(user_movies)
#     with st.container():
#         st.header(f'Special Treats for you {user_feature["name"]}')
#         for i in range(0, ncol, 3):
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.image(user_movies.iloc[i]['img'])
#                 st.text(user_movies.iloc[i]['title'])
#             with col2:
#                 if i + 1 < ncol:
#                     st.image(user_movies.iloc[i+1]['img'])
#                     st.text(user_movies.iloc[i+1]['title'])                    
#             with col3:                 
#                 if i + 2 < ncol:
#                     st.image(user_movies.iloc[i+2]['img'])
#                     st.text(user_movies.iloc[i+2]['title'])

#     def pop_mov():
#         amount = st.sidebar.slider('Number of Recommendations', min_value=1, max_value=20, value=5, step=1, key='pln', help='Here you can specify the number of recommended Movies')
#         period = st.sidebar.radio(
#             "What Timespan do u want to include to calculate the right movies for you?",
#             ('all', 'weeks', 'months', 'years', 'days'), key='period')
#         if period != 'all':
#             start_time = st.sidebar.slider(f'Last {period}', min_value=2, max_value=40, value=5, key='stime', help=f'Here you can define what time period in {period} will be used to make recommendations')
#         else:
#             start_time = '1'


#         data = {'period': period,
#                 'time_mod':start_time,
#                 'amount': amount}
#         return(data)
#     pop_feature =  pop_mov()
#     pop_movies_custom = pred.pop_movies(wf = rating_df, alt = pop_feature['amount'], period = pop_feature['period'], time_mod = pop_feature['time_mod'])

#     # pop_col = len(pop_movies_custom)
#     # p_cols = st.columns(pop_col)
#     # with st.container():
#     #     st.header(f'These movies are Lit')
#     #     for i, x in enumerate(p_cols):
#     #         st.header(pop_movies_custom.iloc[i]['title'])
#     #         st.image(pop_movies_custom.iloc[i]['img'])
#     ncol = len(pop_movies_custom)
#     with st.container():
#         st.header(f'These movies are Lit')
#         for i in range(0, ncol, 3):
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.image(pop_movies_custom.iloc[i]['img'])
#                 st.text(pop_movies_custom.iloc[i]['title'])
#             with col2:
#                 if i + 1 < ncol:
#                     st.image(pop_movies_custom.iloc[i+1]['img'])
#                     st.text(pop_movies_custom.iloc[i+1]['title'])                    
#             with col3:                 
#                 if i + 2 < ncol:
#                     st.image(pop_movies_custom.iloc[i+2]['img'])
#                     st.text(pop_movies_custom.iloc[i+2]['title'])

else:
    st.write('')
