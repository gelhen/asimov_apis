import openai
from pprint import pprint
from openai import api_key
from dotenv import load_dotenv, find_dotenv

#carrega a chave OPENAI_API_KEY
_ = load_dotenv(find_dotenv())

#inicializa o client
client = openai.Client()

def geracao_texto(mensagens, model="gpt-3.5-turbo-0125", max_tokens=1000, temperature=0):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True  # TEM A FUNÇÃO DE RETURNAR IN INTERRADOR COM O RETORNO DE CADA PEDAÇO DO TEXTO
    )
    # COM STREAM A RESPOSTA NAO PODE SER ACESSADA PELO CHOICES
    #print(resposta.choices[0].message.content)
    #print('consumo ', resposta.usage)
    resposta_completa = ''
    for strema_resposta in resposta:
        texto = strema_resposta.choices[0].delta.content
        if texto:
            resposta_completa += texto
            print(texto, end='')
    return resposta_completa


mensagens = [{"role": "user", "content": "Crie uma história sobre uma viagem a marte"}]
#chama o modelo
mensagens = geracao_texto(mensagens=mensagens)
print('Resposta completa /n')
pprint(mensagens)