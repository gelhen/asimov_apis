import json
from datetime import datetime

import yfinance as yf
import  openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

ticker = 'ABEV3'

#DEFINE FUNCOES
# Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
def retorna_cotacao_historica(ticker, periodo):
    ticker_obj = yf.Ticker(f'{ticker}.SA')
    hist = ticker_obj.history(period=periodo, auto_adjust=False)
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    hist.index = hist.index.strftime('%m-%d-%Y')
    return hist['Close'].to_json()


tools = [
    {
        "type": "function",
        "function": {
            "name": "retorna_cotacao_historica",
            "description": "Obtém o historico da cotação",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "O nome da ação. Ex: ambv",
                    },
                    "periodo": {
                        "type": "string",
                        "description": "A data para pesquisa",
                    },
                },
                "required": ["ticker", "periodo"],
            },
        },
    }
]

funcoes_disponiveis = {
        "retorna_cotacao_historica": retorna_cotacao_historica,
    }

mensagens = [
    {"role": "user",
     "content": "Qual é a cotação da ambev agora?"}
    ]

# chama o chat completions do modelo
resposta = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=mensagens,
    tools=tools, # ferramentas para o Modelo utilizar
    tool_choice="auto",
)

print(resposta)
#print(retorna_cotacao_historica(ticker=ticker, periodo='5d'))