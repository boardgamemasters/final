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


## Custom Functions
import User_Ursula as ursula
import ameyfun as af
import funcrsys as pred

# Login Handler & other session varibles
if 'user_login' not in st.session_state:
    st.session_state['user_login'] = False
    st.session_state['user_name'] = ''

st.set_page_config(page_title='Boardgame Recommender', layout='wide')#, page_icon=logo)


@st.cache_data
def data_load():
    rating_df   =    pd.read_csv('data/final_ratings_v3.csv')
    games_df    =    pd.read_csv('data/game_learn_df_v3.csv')
    users_df    =    pd.read_csv('data/usernames_v2.csv')
    games_info  =    pd.read_csv('data/bgref.csv')
    cosine_df   =    pd.read_csv('data/bg_cosines_final.csv')
    amey_df     =    pd.read_csv('data/final_data.csv')
    return rating_df, games_df, users_df, games_info, cosine_df, amey_df


rating_df, games_df, users_df, games_info, cosine_df, amey_df = data_load()

# # Download the image using requests
# response = requests.get(logo_url)
# image_bytes = response.content

# # Open the image using PIL
# logo = Image.open(BytesIO(image_bytes))


st.header("Find awesome Games")

st.sidebar.header('What do you wanna do?')

custom = st.sidebar.checkbox('Personalized Experience', value=False, key='custom', help='Click this to get Custom recommendations')


placeholder = st.sidebar.empty()
if st.session_state['user_login'] == False:
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        User = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    if (
        submit 
        and users_df['Username'].str.fullmatch(User).any() == True
        # and password != ''
        ):
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        st.session_state['user_login'] = True
        st.session_state['user_name'] = User
        st.success("Login successful")
    elif (
        submit 
        and users_df['Username'].str.fullmatch(User).any() == False
          ):
        st.error(f"User: {User} not failed {(users_df['Username'].isin(list(User))).sum()}")
    else:
        pass

if st.session_state['user_login'] == True:
    byebye = st.sidebar.button("Logout")
    if byebye:
        placeholder.empty()
        st.session_state['user_login'] = False
        st.session_state['user_name'] = ''
        st.success("Logout successful")



if custom == True:
    rec_select = st.sidebar.radio(
        "What kind of recommendation do you like",
        (
            'Similar Games based of Description'
            , 'Similar Taste'
            , 'Amey likes you a lot'
            , 'Chatbot Recommender'
         ), key='rec_select')

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

    
    # ncol = 3#len(pop_movies)
    # with st.container():
    #     for i in range(0, ncol, 3):
    #         col1, col2, col3 = st.columns(3)
    #         with col1:
    #             # st.image(pop_movies.iloc[i]['img'])
    #             st.text('Spiel 1')    # (pop_movies.iloc[i]['title'])
    #         with col2:
    #             if i + 1 < ncol:
    #                 # st.image(pop_movies.iloc[i+1]['img'])
    #                 st.text('Spiel 2')    # (pop_movies.iloc[i+1]['title'])                    
    #         with col3:                 
    #             if i + 2 < ncol:
    #                 # st.image(pop_movies.iloc[i+2]['img'])
    #                 st.text('Spiel 3')    # (pop_movies.iloc[i+2]['title'])
                    

    

if rec_select == 'Similar Games based of Description':
    def game_like():
        title = st.sidebar.multiselect('Games like', games_info.sort_values('name')['name'])    # titles_df['title'], key = 'movie_like')
        #amount = st.sidebar.slider('Number of Recommendations', min_value=1, max_value=5, value=3, step=1, key='mln', help='Here you can specify the number of recommended Games')

        game_id = games_info.loc[games_info['name'].isin(title),'bgg_id']#.values[0]

        data = {'bgg_id': game_id#,    #    mov_id,
                #'amount': amount
                }
        return(data)
    sim_feature =  list(game_like()['bgg_id'])
    # st.write(len(sim_feature))
    ## similar_description_games(bg_input, bg_cosines_df, bgref_df)
    if (len(sim_feature)>0):
        sim_games = pred.similar_description_games(bg_input = sim_feature, bg_cosines_df = cosine_df, bgref_df = games_info)
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
                        st.image(sim_games.iloc[i+1]['image'])
                        st.text(sim_games.iloc[i+1]['name'])    
                with col3:                 
                    if i + 2 < ncol:
                        st.image(sim_games.iloc[i+2]['image'])
                        st.text(sim_games.iloc[i+2]['name'])
    else:
        st.header(f'Please select Games on the left side!')

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

elif rec_select == 'Amey likes you a lot':  
    def amey_like():
        gname = st.sidebar.selectbox('What Game do you like', amey_df['name_x'], key = 'amey_like')
        amount = st.sidebar.slider('Number of Recommendations', min_value=4, max_value=16, value=8, step=4, key='aln', help='Here you can specify the number of recommended Boardgames')

        data = {'amount': amount,
                'name' : gname}
        return(data)
    amey_feature =  amey_like()
    # st.sidebar.text('Login to use this Feature')    # (pop_movies.iloc[i+2]['title'])
    amey_games = pd.DataFrame({'bgg_id' : af.game_of_my_life(user_favorite_game=amey_feature['name'],data = amey_df, z=amey_feature['amount'])})
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
                    st.image(amey_games.iloc[i+1]['image'])
                    st.text(amey_games.iloc[i+1]['name'])                    
            with col3:                 
                if i + 2 < ncol:
                    st.image(amey_games.iloc[i+2]['image'])
                    st.text(amey_games.iloc[i+2]['name'])
            with col4:                 
                if i + 3 < ncol:
                    st.image(amey_games.iloc[i+3]['image'])
                    st.text(amey_games.iloc[i+3]['name'])



elif rec_select == 'Chatbot Recommender':
    games = amey_df['name_x']
    st.sidebar.text('Coming Soon')

    def on_input_change():
        user_input = st.session_state.user_input
        st.session_state.responses.append(user_input)
        st.session_state.user_input = ""  # Clear the input after processing

    def on_btn_click():
        del st.session_state['questions']
        del st.session_state['responses']
        selecthor = 0

    st.session_state.setdefault('questions', [])
    st.session_state.setdefault('responses', [])
    selecthor = 0

    st.title("Boardgame Recommender Chatbot")

    # Add CSS for styling the chat window
    st.markdown(
        """
        <style>
        .chat-window {
            padding: 10px;
            border: 1px solid #d8d8d8;
            border-radius: 10px;
            background-color: #f9f9f9;
            margin-bottom: 10px;
        }
        .chat-message {
            margin-bottom: 10px;
            padding: 8px;
            border-radius: 5px;
            background-color: #d8d8d8;
        }
        .user-message {
            background-color: #0071bc;
            color: white;
            text-align: right;
        }
        .bot-message {
            background-color: #f9f9f9;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="chat-window">', unsafe_allow_html=True)

    # Greeting message
    st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
    st.write("Hi there! I'm your Boardgame Recommender Chatbot.")
    st.write("I can recommend you some awesome board games based on your preferences.")
    st.write("Let's get started!")
    st.markdown('</div>', unsafe_allow_html=True)

    questions_list = [
        '''What is your favorite board game?'''
        # Add other questions here...
    ]

    for response in (st.session_state.responses):
        if selecthor == 0:
            st.markdown('<div class="user-message chat-message">', unsafe_allow_html=True)
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)

            if games.str.fullmatch(response, case=False).any():
                if ((games.str.fullmatch(response, case=False)).sum()) != 1:
                    sel_game = games.loc[games.str.fullmatch(response, case=False)][0].item()
                else:
                    sel_game = games.loc[games.str.fullmatch(response, case=False)].item()
                selecthor = 1
                st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                st.write("How many recommendations do you want to get? Please enter a number between 1 and 5.")
                st.markdown('</div>', unsafe_allow_html=True)
                continue
            else:
                st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                st.write("I don't know this game. Please enter another one.")
                st.markdown('</div>', unsafe_allow_html=True)
                selecthor = 0
                continue

        if selecthor == 1:
            st.markdown('<div class="user-message chat-message">', unsafe_allow_html=True)
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)

            if response.isnumeric():
                alt = int(response)
                if alt < 1:
                    alt = 1
                elif alt > 5:
                    alt = 5
                else:
                    alt = alt
                selecthor = 3
                st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                st.write(f"Your favorite board game is {sel_game}. And you would like to get {alt} recommendations for similar games. Is that correct? (y) , (n)")
                st.markdown('</div>', unsafe_allow_html=True)
                continue
            else:
                st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                st.write("Please enter a numeric value.")
                st.markdown('</div>', unsafe_allow_html=True)
                selecthor = 1
                continue

        if selecthor == 3:
            st.markdown('<div class="user-message chat-message">', unsafe_allow_html=True)
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)

            if pd.Series(['y', 'Y', 'yes', 'Yes']).isin([response]).any():
                st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                st.write('I can recommend you the following games:')
                st.markdown('</div>', unsafe_allow_html=True)

                amey_games = pd.DataFrame({'bgg_id': af.game_of_my_life(user_favorite_game=sel_game, data=amey_df, z=alt)})
                amey_games = ursula.get_feature(result_file=amey_games, feature_file=games_info)

                res_co = 0
                for i in range(len(amey_games)):
                    st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                    st.image(amey_games.iloc[res_co]['image'], use_column_width=True)
                    st.write(amey_games.iloc[res_co]['name'])
                    st.markdown('</div>', unsafe_allow_html=True)
                    res_co += 1

                st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                st.write("Thank you for using our Boardgame Recommender Chatbot. Have a great day!")
                st.markdown('</div>', unsafe_allow_html=True)
                selecthor = 4
                continue

            elif pd.Series(['n', 'N', 'no', 'No']).isin([response]).any():
                st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                st.write("Let's try again.")
                st.markdown('</div>', unsafe_allow_html=True)
                selecthor = 0
                continue

            else:
                st.markdown('<div class="bot-message chat-message">', unsafe_allow_html=True)
                st.write(f"{response} is not a valid input. Please try again.")
                st.markdown('</div>', unsafe_allow_html=True)
                selecthor = 0
                continue

    st.markdown('</div>', unsafe_allow_html=True)
