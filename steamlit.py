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

# import predictors as pred

# logo_url = 'https://img.freepik.com/premium-vector/cute-couple-panda-watching-movie-eating-popcorn-cartoon-vector-icon-illustration-animal-food_138676-6443.jpg'

rating_url = 'https://drive.google.com/file/d/1fiU-bQOIyyjoRRB8uSJ7_oodFRo5wr30/view?usp=sharing'
games_url =  'https://drive.google.com/file/d/1aOw0TeVXaToN1t0CE-vN3tXQEZXPpTzq/view?usp=sharingg'
users_url =  'https://drive.google.com/file/d/159oociMXgvsSOlRltLhUQ1TgY1wA-RGK/view?usp=sharing'

path = 'https://drive.google.com/uc?export=download&id='
rating_df = pd.read_csv(path+rating_url.split('/')[-2])
games_df = pd.read_csv(path+games_url.split('/')[-2])
users_df = pd.read_csv(path+users_url.split('/')[-2])

# rating_df    =    pd.read_csv('data/reduced_movies.csv')
# titles_df    =    pd.read_csv('data/movie_names.csv')
# users_df     =    pd.read_csv('data/user_df.csv')


# # Download the image using requests
# response = requests.get(logo_url)
# image_bytes = response.content

# # Open the image using PIL
# logo = Image.open(BytesIO(image_bytes))

st.set_page_config(page_title='Boardgame Recommender')#, page_icon=logo)

st.header("Find awesome Games")

st.sidebar.header('What do you wanna do?')
# st.dataframe(games_df)

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
    def movie_like():
        title = st.sidebar.selectbox('Games like', ('Catan', 'Risk', 'Monopoly'))    # titles_df['title'], key = 'movie_like')
        amount = st.sidebar.slider('Number of Recommendations', min_value=1, max_value=20, value=5, step=1, key='mln', help='Here you can specify the number of recommended Games')

        # mov_id = titles_df.loc[titles_df['title']== title,'movieId'].values[0]

        data = {'title': 1,    #    mov_id,
                'amount': amount,
                'name':title}
        return(data)
    sim_feature =  movie_like()
    # sim_movies = pred.similar_movies(wf = rating_df, alt = sim_feature['amount'], movie_id = sim_feature['title'])

    # mov_col = len(sim_movies)
    # m_cols = st.columns(mov_col)
    # with st.container():
    #     st.header(f'Users that liked {sim_feature["name"]}, also liked these {sim_feature["amount"]} movies')
    #     for i, x in enumerate(m_cols):
    #         st.header(sim_movies.iloc[i]['title'])
    #         st.image(sim_movies.iloc[i]['img'])
    ncol = sim_feature['amount']#len(sim_movies)
    with st.container():
        st.header(f'Users that liked {sim_feature["name"]}, also liked these {sim_feature["amount"]} Games')
        for i in range(0, ncol, 3):
            col1, col2, col3 = st.columns(3)
            with col1:
                # st.image(pop_movies.iloc[i]['img'])
                st.text(f'Spiel {i}')    # (pop_movies.iloc[i]['title'])
            with col2:
                if i + 1 < ncol:
                    # st.image(sim_movies.iloc[i+1]['img'])
                    st.text(f'Spiel {i+1}')    # (pop_movies.iloc[i]['title'])
            with col3:                 
                if i + 2 < ncol:
                    # st.image(sim_movies.iloc[i+2]['img'])
                    st.text(f'Spiel {i+2}')    # (pop_movies.iloc[i+2]['title'])

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
                st.header(user_games.iloc[i]['title'])
                st.text(user_games.iloc[i]['predicted_rating'])
                # st.image(user_games.iloc[i]['img'])
                # st.text(user_games.iloc[i]['title'])
            with col2:
                if i + 1 < ncol:
                    st.header(user_games.iloc[i+1]['title'])
                    st.text(user_games.iloc[i+1]['predicted_rating'])
                    # st.image(user_games.iloc[i+1]['img'])
                    # st.text(user_games.iloc[i+1]['title'])                    
            with col3:                 
                if i + 2 < ncol:
                    st.header(user_games.iloc[i+2]['title'])
                    st.text(user_games.iloc[i+2]['predicted_rating'])
                    # st.image(user_games.iloc[i+2]['img'])
                    # st.text(user_games.iloc[i+2]['title'])

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
