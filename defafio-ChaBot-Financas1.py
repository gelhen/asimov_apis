import json
from datetime import datetime
from pprint import pprint
from pyexpat.errors import messages

import yfinance as yf
import  openai
from dotenv import load_dotenv, find_dotenv
from openai import models

_ = load_dotenv(find_dotenv())

client = openai.Client()

ticker = 'ABEV3'

#DEFINE FUNCOES
# Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
def retorna_cotacao_historica(ticker, periodo='1mo'):
    ticker_obj = yf.Ticker(f'{ticker}.SA')
    hist = ticker_obj.history(period=periodo, auto_adjust=False)
    #limita em 30 amostras de 30 em 30
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    hist.index = hist.index.strftime('%Y-%m-%d')
    return hist['Close'].to_json()


tools = [
    {
        "type": "function",
        "function": {
            "name": "retorna_cotacao_historica",
            "description": "Retorna a cotação diária histórica para uma ação da bovespa",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "O nome da ação. Ex: AMBEV3 para ambev3, 'PETR4 para petrobras, etc'",
                    },
                    "periodo": {
                        "type": "string",
                        "description": "O período que será retornado de dados históricos sendo  '1mo' equivale \
                                       a um mês de dados, '1d' a 1 dias e '1y' a 1 anod",
                        "enum": ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]
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

def gera_texto(mensagens):
    # chama o chat completions do modelo
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=mensagens,
        tools=tools, # ferramentas para o Modelo utilizar
        tool_choice="auto",
    )
    # se não retornar nada para o tool_calls é porque o modelo não precisou e já trouxe o retorno que precisava
    tool_calls = resposta.choices[0].message.tool_calls
    pprint(tool_calls)
    if tool_calls:
        mensagens.append(resposta.choices[0].message)
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            function_to_call = funcoes_disponiveis[func_name]
            func_args = json.loads(tool_call.function.arguments)
            func_return = function_to_call(**func_args)
            mensagens.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": func_name,
                 "content": func_return
            })
        segunda_resposta = client.chat.completions.create(
            messages=mensagens,
            model="gpt-3.5-turbo-0125",
        )
        mensagens.append(segunda_resposta.choices[0].message)
        print(segunda_resposta.choices[0].message.content)
    print(f"Assinstant: {mensagens[-1].content}")
    return mensagens

if __name__ == '__main__':
    print('Bem vindo ao ChatBot Financeiro da Asimov.')
    while True:
        input_usuario = input('User: ')
        if input_usuario.lower() == 'sair':
            break
        mensagens = [
            {"role": "user",
             "content": input_usuario}
        ]
        mensagens = gera_texto(mensagens)