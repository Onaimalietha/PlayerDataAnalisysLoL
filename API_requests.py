import requests
import streamlit as st
import pandas as pd

#personal (reseta a cada 24h, proposito de desenvolvimento unico)
api_key = 'RGAPI-23b98332-3076-47cf-b6f4-7305279c2ae5'

#API request url para acessar dados de um jogador através do nick
url = 'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'

region = 'americas'

def get_player_info(nick):
    api_url = url + nick + '?api_key=' + api_key
    resp = requests.get(api_url)

    player_info = resp.json() 
    return player_info

def get_puuid(nick):
    api_url = url + nick + '?api_key=' + api_key
    resp = requests.get(api_url)

    player_info = resp.json() 

    # player_info  
    # 'puuid' é importante para localizar o player dentro de partidas
    #armazena ID do jogador
    puuid = player_info['puuid']
    return puuid


def get_match_list(nick, nMatches, game_mode):
    api_url = url + nick + '?api_key=' + api_key
    resp = requests.get(api_url)

    player_info = resp.json() 

    # player_info  
    # 'puuid' é importante para localizar o player dentro de partidas
    #armazena ID do jogador
    puuid = player_info['puuid']

    #API request url para acessar em quais partidas o jogador identificado pelo puuid participou
    match_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={game_mode}&start=0&count={nMatches}'
    match_url = match_url + '&api_key=' + api_key

    #response [200] para sucesso
    match_resp = requests.get(match_url)

    match_list = match_resp.json()
    return match_list


#Função para retornar os dados da partida do jogador
def get_match_data(region, match_id):
    match_url = ('https://' + region + '.api.riotgames.com/lol/match/v5/matches/' + match_id + '?api_key=' + api_key)
    match_resp = requests.get(match_url)
    match_data = match_resp.json()
    return match_data

#cs_per_min = df.plot(x = 'match time', y = 'cs per minute', kind = 'scatter')
#plt.show(cs_per_min)




