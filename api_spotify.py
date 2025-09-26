import os
from pprint import pprint
import dotenv
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st

dotenv.load_dotenv(dotenv.find_dotenv())


def autenticar():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

    #converte para base64
    auth = HTTPBasicAuth(username=client_id, password=client_secret)

    url = f"https://accounts.spotify.com/api/token"
    body = {
        'grant_type': 'client_credentials'
    }
    resposta = requests.post(url=url, data=body, auth=auth)

    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"Erro no request: {e}")
        token = None
    else:
        resultado = resposta.json()
        print('Token obtido com sucesso!')
    token =  resultado['access_token']
    return token

def busca_artista(nome_artista, headers):
    url = "https://api.spotify.com/v1/search"
    params = {
        'q': nome_artista,
        'type': 'artist',
    }
    resposta = requests.get(url, params=params, headers=headers)
    try:
        primeiro_resultado = resposta.json()['artists']['items'][0]
    except IndexError:
        primeiro_resultado = None

    return  primeiro_resultado


def busca_top_musicas(id_artista, headers):
    url = f"https://api.spotify.com/v1/artists/{id_artista}/top-tracks"
    resposta = requests.get(url,  headers=headers)
    return resposta.json()['tracks']


def main():
    # Cabeçalho do Web App
    st.title('Web App Spotify')
    st.write('Dados da API do Spotify (fonte: https://developer.spotify.com/)')
    nome_artista = st.text_input('Busque um artista:')
    if not nome_artista:
        st.stop()

    token = autenticar()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    artista = busca_artista(nome_artista=nome_artista, headers=headers)
    if not artista:  # Sem dados para este local
        st.warning(f'Artista "{nome_artista}" não foi encontrado!')
        st.stop()

    id_artista = artista['id']
    nome_artista = artista['name']
    popularidade_artista = artista['popularity']

    melhores_musicas = busca_top_musicas(id_artista=id_artista, headers=headers)

    #Cria sub header
    st.subheader(f'Artista: {nome_artista} (pop: {popularidade_artista})')


    for musica in melhores_musicas:
        nome_musica = musica['name']
        popularidade_musica = musica['popularity']
        link_musica = musica['external_urls']['spotify']
        link_em_markdown = f'[{nome_musica}]({link_musica})'
        st.write(f'{link_em_markdown} (pop: {popularidade_musica})')


if __name__ == '__main__':
    main()