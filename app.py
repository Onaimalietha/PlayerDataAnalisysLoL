#import requests
import streamlit as st
import pandas as pd

from API_requests import get_player_info, get_puuid, get_match_list, get_match_data
from data import did_win, cs_count, deathTime, match_time, wards_placed, wards_broken
from graphs import wr_pie_graph

st.set_page_config(page_title = "League Dashboard", 
                   layout = 'wide')
nickname = 'kometa18'
nMatches = 20

# Sidebar
st.sidebar.header('Options')
nickname = st.sidebar.text_input('Summoner name')
game_mode = st.sidebar.selectbox('Choose game mode', ('normal', 'ranked', 'tourney', 'tutorial'))
nMatches = st.sidebar.selectbox('Choose the number of games', (20, 50, 100))
# eu meio q tenho q aprender a lidar com exceções do tipo, e se um nome q nao existe for inserido?

st.title('Player data analysis')

player_info = get_player_info(nickname)
player_level = player_info['summonerLevel']
puuid = get_puuid(nickname)
match_list = get_match_list(nickname, nMatches, game_mode)
region = 'americas'

win_count = 0
lst_cs = []
lst_cs_per_minute = []
lst_wards_placed = []
lst_wards_broken = []
lst_match_time = []
lst_bWin = []

# vision socre analysis, bar graph
# dependency of vision socre on farming
lst_vision_score_win = []
lst_vision_score_lose = []

# dependecy of winning on farming
lst_cs_per_minute_win = []
lst_cs_per_minute_lose = []

for match_id in match_list:
    match_data = get_match_data(region, match_id)
    
    if did_win(match_data, puuid):
        win_count = win_count + 1
        lst_bWin.append('Victory')
        lst_vision_score_win.append(wards_broken(match_data, puuid) + wards_placed(match_data, puuid))
        lst_vision_score_lose.append(0)
        lst_cs_per_minute_win.append(cs_count(match_data, puuid)/(match_time(match_data, puuid)/60))
    else:
        lst_bWin.append('Defeat')
        lst_vision_score_lose.append(wards_broken(match_data, puuid) + wards_placed(match_data, puuid))
        lst_vision_score_win.append(0)
        lst_cs_per_minute_lose.append(cs_count(match_data, puuid)/(match_time(match_data, puuid)/60))
        
    lst_cs.append(cs_count(match_data, puuid))
    lst_cs_per_minute.append(cs_count(match_data, puuid)/(match_time(match_data, puuid)/60))
    lst_wards_placed.append(wards_placed(match_data, puuid))
    lst_wards_broken.append(wards_broken(match_data, puuid))
    lst_match_time.append(match_time(match_data, puuid))

myWinR = []
myWinR.append(win_count)
myWinR.append(nMatches - win_count)

lst_data = list(zip(lst_cs, lst_cs_per_minute, lst_wards_placed, lst_wards_broken, lst_match_time, lst_bWin))
matches_df = pd.DataFrame(lst_data, columns = ['cs', 'cs p/min','wards placed', 'wards broken', 'match time', 'match result'])

lst_vision_score = lst_vision_score_win + lst_vision_score_lose
lst_vision = list(zip(lst_vision_score_win, lst_vision_score_lose, lst_cs_per_minute, lst_vision_score))
vision_df = pd.DataFrame(lst_vision, columns = ['winning vision score', 'losing vision socre', 'cs p/min','total vision score'])

avg_farm_win = (sum(lst_cs_per_minute_win))/nMatches
avg_farm_lose = (sum(lst_cs_per_minute_lose))/nMatches
farm_dependency = {'avg farm': [avg_farm_win, avg_farm_lose]}
farming_df = pd.DataFrame(farm_dependency, index = ['Victory', 'Defeat'])

# KPI's
avg_farm = sum(lst_cs_per_minute)/nMatches
avg_farm = round(avg_farm, 2)
avg_vision_score = (sum(lst_wards_placed)+sum(lst_wards_broken))/nMatches
avg_vision_score = round(avg_vision_score, 2)
win_rate = (win_count/nMatches)*100
win_rate = round(win_rate, 2)

col1, col2 = st.columns(2)
with col1:
    st.subheader(f'From the last {nMatches} played')
    st.write(matches_df)
with col2: 
    st.header(nickname)
    st.subheader(f'level: {player_level}')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Avg cs/min')
        st.subheader(avg_farm)
    with col2:
        st.subheader('Avg vision score')
        st.subheader(avg_vision_score)
    with col3:
        st.subheader('Win rate (%)')
        st.subheader(win_rate)
st.markdown('---')

# Simple charts
with st.container():
    st.subheader(f'Last {nMatches} matches tendencies')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.line_chart(matches_df, y = 'wards placed')
    with col2:
        st.line_chart(matches_df, y = 'wards broken')
    with col3:
        st.line_chart(matches_df, y = 'cs p/min')
st.markdown('---')

# More complex charts
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1: # relation between vision score and match result
        st.subheader('Correlation between vision score and match result')
        st.bar_chart(vision_df, y = ['winning vision score', 'losing vision socre'])
    with col2: # dependency of vision score on farming
        st.subheader('Dependency of vision score on farming')
        st.scatter_chart(vision_df, y = 'total vision score', x = 'cs p/min')
    with col3: # dependency of match result on farming
        st.subheader('Dependency of match result on farming')
        st.bar_chart(farming_df)
        
#mt feio bixo, vai se fude
#wr_pie_graph(myWinR) 

