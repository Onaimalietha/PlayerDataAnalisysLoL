import pandas as pd
import streamlit as st

#função para retornar se o jogador venceu ou nao a partida
def did_win(match_data, puuid):
    player_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][player_index]['win']

def cs_count(match_data, puuid):
    player_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][player_index]['totalMinionsKilled']

def deathTime(match_data, puuid):
    player_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][player_index]['totalTimeSpentDead']

def wards_placed(match_data, puuid):
    player_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][player_index]['wardsPlaced']

def wards_broken(match_data, puuid):
    player_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][player_index]['wardsKilled']

def match_time(match_data, puuid):
    player_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][player_index]['timePlayed']