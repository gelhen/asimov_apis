import openai
from pprint import pprint
from openai import api_key
from dotenv import load_dotenv, find_dotenv

#carrega a chave OPENAI_API_KEY
_ = load_dotenv(find_dotenv())

#inicializa o client
client = openai.Client()

#cria lista de dicts para enviar ao modelo
messages = [
    {"role": "user", "content": "O que é uma maçã em 50 palavras?"},
]
#chama o modelo
resposta = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo-0125",
    max_tokens=1000,
    temperature=0,
)

pprint(resposta.choices[0].message.content)

messages.append({"role": "assistant", "content": resposta.choices[0].message.content})

pprint(messages)    
messages.append({"role": "user", "content": "E qual sua cor?"})