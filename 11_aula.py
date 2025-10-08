from pprint import pprint

import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

# para ter a resposta formatada
system_mes = '''
Responda as perguntas em um parágrafo de até 20 palavras. Categorize as respostas no seguintes conteúdos: física, matemática, língua portuguesa ou outros.
Retorne a resposta em um formato json, com as keys: 
fonte: valor deve ser sempre AsimoBot
resposta: a resposta para a pergunta
categoria: a categoria da pergunta
'''
mensagens = [
    {'role': 'system', 'content': system_mes},
    {'role': 'user', 'content': 'O que é uma equação quadrática?'}
]

resposta = client.chat.completions.create(
    messages=mensagens,
    model='gpt-3.5-turbo',
    max_tokens=1000,
    temperature=0
)

pprint(resposta.choices[0].message.content)