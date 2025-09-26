import os

import dotenv
import requests
import streamlit as st

dotenv.load_dotenv(dotenv.find_dotenv())

dict_clima = {
    'céu limpo': 'Céu limpo ☀️',
    'algumas nuvens': 'Céu com algumas nuvens ⛅',
    'nublado': 'Nublado ☁️',
    'névoa': 'Névoa 🌫️',
}


def fazer_request(url, params=None):
    resposta = requests.get(url=url, params=params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"Erro no request: {e}")
        resultado = None
    else:
        resultado = resposta.json()
    return resultado


def pegar_tempo_para_local(local):
    app_id = os.environ['CHAVE_API_OPENWEATHER']
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': local,
        'appid': app_id,
        'units': 'metric',
        'lang': 'pt_br',
    }
    dados_tempo = fazer_request(url=url, params=params)
    return dados_tempo


def main():
    # Cabeçalho do Web App
    st.title('Web App Tempo ☀️')
    st.write('Dados do OpenWeather (fonte: https://openweathermap.org/current)')
    local = st.text_input('Busque uma cidade:')
    if not local:
        st.stop()

    # Acessa dados do OpenWeather
    dados_tempo = pegar_tempo_para_local(local=local)
    if not dados_tempo:  # Sem dados para este local
        st.warning(f'Localidade "{local}" não foi encontrada no banco de dados da OpenWeather!')
        st.stop()

    # extrai dados retornados para variáveis
    clima_atual = dados_tempo['weather'][0]['description']
    clima_atual = dict_clima.get(clima_atual, clima_atual)
    temperatura = dados_tempo['main']['temp']
    sensacao_termica = dados_tempo['main']['feels_like']
    umidade = dados_tempo['main']['humidity']
    cobertura_nuvens = dados_tempo['clouds']['all']

    # Exibe no Web App
    # metric deixa um numer grande com um título pequeno
    st.metric(label='Tempo atual', value=clima_atual)
    # Cria duas colunas de mesmo tamanho, neste caso não foi informado o tamanho
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label='Temperatura', value=f'{temperatura} °C')
        st.metric(label='Sensação térmica', value=f'{sensacao_termica} °C')
    with col2:
        st.metric(label='Umidade do ar', value=f'{umidade}%')
        st.metric(label='Cobertura de nuvens', value=f'{cobertura_nuvens}%')


if __name__ == '__main__':
    main()