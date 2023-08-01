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
import  streamlit_toggle as tog


## Custom Functions
import User_Ursula as ursula
import ameyfun as af
import funcrsys as pred

# Login Handler & other session varibles
if 'user_login' not in st.session_state:
    st.session_state['user_login'] = False
    st.session_state['user_name'] = ''

if 'set_chat' not in st.session_state:
    st.session_state['set_chat'] = False

set_chat = st.session_state['set_chat']


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


####### Users Favorites
@st.cache_data
def user_fav():
    fav_games = pred.fav_bguser(user_id= st.session_state['user_name'], bg_num = 10, reviews_df = rating_df, bg_df=games_info)
    ncol = len(fav_games)
    with st.container():
        st.header(f'''Hey {st.session_state["user_name"]}. Your 10 Top Rated games are: ''')
        for i in range(0, ncol, 5):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.image(pred.make_square(fav_games.iloc[i]['image']))
                st.text(fav_games.iloc[i]['name'])
            with col2:
                if i + 1 < ncol:
                    st.image(pred.make_square(fav_games.iloc[i+1]['image']))
                    st.text(fav_games.iloc[i+1]['name'])                    
            with col3:                 
                if i + 2 < ncol:
                    st.image(pred.make_square(fav_games.iloc[i+2]['image']))
                    st.text(fav_games.iloc[i+2]['name'])
            with col4:                 
                if i + 3 < ncol:
                    st.image(pred.make_square(fav_games.iloc[i+3]['image']))
                    st.text(fav_games.iloc[i+3]['name'])
            with col5:                 
                if i + 4 < ncol:
                    st.image(pred.make_square(fav_games.iloc[i+4]['image']))
                    st.text(fav_games.iloc[i+4]['name'])
#####
####### Special Treats
@st.cache_data
def special_treat():
    user_games = ursula.gib_spiele_digga(rat_df = rating_df, s_alt = 10, user = st.session_state['user_name'], game_frame=games_df)
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
                    st.image(pred.make_square(user_games.iloc[i+1]['image']))
                    st.text(user_games.iloc[i+1]['name'])                    
            with col3:                 
                if i + 2 < ncol:
                    st.image(pred.make_square(user_games.iloc[i+2]['image']))
                    st.text(user_games.iloc[i+2]['name'])
            with col4:                 
                if i + 3 < ncol:
                    st.image(pred.make_square(user_games.iloc[i+3]['image']))
                    st.text(user_games.iloc[i+3]['name'])
            with col5:                 
                if i + 4 < ncol:
                    st.image(pred.make_square(user_games.iloc[i+4]['image']))
                    st.text(user_games.iloc[i+4]['name'])
#####


rating_df, games_df, users_df, games_info, cosine_df, amey_df = data_load()

# # Download the image using requests
# response = requests.get(logo_url)
# image_bytes = response.content

# # Open the image using PIL
# logo = Image.open(BytesIO(image_bytes))


st.header("Find awesome Games")


####### SIDEBAR
if st.session_state['chat_bot_only'] == False:
    st.sidebar.header('What do you wanna do?')
else:
    st.sidebar.header('Enjoy our amazing Boardgame-Bot')

## LOGIN HANDLING
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
        st.error(f"User: {User} not found")
    else:
        pass

if st.session_state['user_login'] == True:
    byebye = st.sidebar.button("Logout")
    if byebye:
        placeholder.empty()
        st.session_state['user_login'] = False
        st.session_state['user_name'] = ''
        st.success("Logout successful")
        special_treat.clear()
        user_fav.clear()
################

# custom = st.sidebar.checkbox('Personalized Experience', value=False, key='custom', help='Click this to get Custom recommendations')

if set_chat == False:
    u_fav_placeholder = st.sidebar.empty()
    u_rec_placeholder = st.sidebar.empty()
    with u_fav_placeholder:
        if st.session_state['user_login'] == True:
            u_fav = tog.st_toggle_switch(label=f"Your Favorite Games", 
                                key="u_f_sel", 
                                default_value=True, 
                                label_after = True, 
                                inactive_color = '#D3D3D3', 
                                active_color="#11567f", 
                                track_color="#29B5E8"
                                )
    with u_rec_placeholder:    
        if st.session_state['user_login'] == True:    
            u_rec = tog.st_toggle_switch(label=f"Special Treats for You", 
                                key="u_r_sel", 
                                default_value=True, 
                                label_after = True, 
                                inactive_color = '#D3D3D3', 
                                active_color="#11567f", 
                                track_color="#29B5E8"
                                )

    st.sidebar.divider()
    sim_desc_placeholder = st.sidebar.empty()
    with sim_desc_placeholder:
        sim_desc = tog.st_toggle_switch(label="Description based Recommender", 
                                key="sim_desc", 
                                default_value=True, 
                                label_after = True, 
                                inactive_color = '#D3D3D3', 
                                active_color="#11567f", 
                                track_color="#29B5E8"
                                )
    if sim_desc == True:
        def game_like():
            title = st.sidebar.multiselect('Games like', games_info.sort_values('name')['name'])

            game_id = games_info.loc[games_info['name'].isin(title),'bgg_id']

            data = {'bgg_id': game_id
                    }
            return(data)
        sim_feature =  list(game_like()['bgg_id'])
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
    st.sidebar.divider()
else:
    st.write('')

def chat_select_change():
    st.experimental_rerun()

sel_chatbot_placeholder = st.sidebar.empty()
with sel_chatbot_placeholder:
    st.session_state['set_chat'] = st.checkbox(label="Chatbot Recommender", 
                            key="rec_chat", 
                            help = 'Use our awesome Chatbox to get Boardgame-Recommendations.',
                            value= True
                            )
    

if set_chat == True:
    games = amey_df['name_x']
    def on_input_change():
        user_input = st.session_state.user_input
        st.session_state.responses.append(user_input)
        st.session_state.user_input = ""  # Clear the input after processing

    def on_btn_click():
        del st.session_state['questions']
        del st.session_state['responses']
        selecthor = 0

    st.session_state.setdefault('questions', [])

    st.title("""May the Force....
             I meant... May the Games be with You""")
    questions_list = [
        # 0
        '''I would like to recommend you some Boardgames.
        What is your favorite one?'''    
        # 1
        , '''I dont know this Game.
        Please enter another one'''
        # 2
        , '''How many recommendations do you want to get?
        'Please enter a Number between 1 and 5'''
    ]

    if 'responses' not in st.session_state.keys():
        st.session_state.questions.extend(questions_list)
        st.session_state.responses = []

    chat_placeholder = st.empty()
    st.button("Clear message", on_click=on_btn_click)

    message(st.session_state.questions[0]) 

    with st.container():
        selecthor = 0
        count =0
        for response in (st.session_state.responses):
            count +=1
            if selecthor == 0:
                message(response, is_user = True, key=f"a1{count}")
                if games.str.fullmatch(response, case = False).any():
                    if ((games.str.fullmatch(response, case = False)).sum())!=1:
                       sel_game = games[games.str.fullmatch(response, case = False)][0].item()     
                    else:
                     sel_game = games[games.str.fullmatch(response, case = False)].item()     
                    selecthor = 1
                    message(st.session_state.questions[2], key=f"b2{count}")  
                    continue
                else:
                    message(st.session_state.questions[1], key=f"b1{count}")
            if selecthor == 1:
                message(response, is_user = True, key=f"a2{count}")
                if response.isnumeric():
                    alt = int(response)
                    if alt <1:
                        alt =1
                    elif alt >5:
                        alt = 5
                    else:
                        alt = alt
                    selecthor = 3
                    message(f'''Your favorite boardgame is {sel_game}.
                    And you would like to get {alt} recommendations for similar games.
                    Is that correct?
                    (y) , (n)''', key=f"b4{count}")
                    continue
                else:
                    message('Please enter a numeric value', key=f"b3{count}")
            if selecthor== 2:
                selecthor = 3
                continue
            if selecthor== 3:
                message(response, is_user = True, key=f"a3{count}")  
                if (pd.Series(['y', 'Y', 'yes', 'Yes'])).isin([response]).any():
                    message('I can recommend you the following games:', key=f"b5{count}")
                    amey_games = pd.DataFrame({'bgg_id' : af.game_of_my_life(user_favorite_game=sel_game,data = amey_df, z=alt)})
                    amey_games = ursula.get_feature(result_file=amey_games, feature_file=games_info)
                    res_co = 0
                    for i in  range(len(amey_games)):
                        message(
                            f'<img width="100%" height="200" src="{amey_games.iloc[res_co]["image"]}"/><br>{amey_games.iloc[res_co]["name"]}'
                            , key=f"img_{count}_{res_co}"
                            , allow_html=True
                        )
                        res_co +=1
                
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
else:
    aasdasfdgsdf =1

if set_chat == False:
    if st.session_state['user_login']==True:
        # user_games = ursula.gib_spiele_digga(rat_df = rating_df, s_alt = 10, user = st.session_state['user_name'], game_frame=games_df)
        # user_games = ursula.get_feature(result_file=user_games, feature_file=games_info)
        # ncol = len(user_games)
        with st.container():
            if u_fav == True:
                with st.expander(f"Your Top10 Games:"):
                    user_fav()

            if u_rec == True:
                with st.expander(f"10 Games we think you might enjoy:"):
                    special_treat()

            
    else:
        st.write('') 