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
    )
    print(resposta.choices[0].message.content)
    print('consumo ', resposta.usage)
    #mensagens.append({"role": "assistant", "content": resposta.choices[0].message.content})
    # o mesmo que 
    mensagens.append(resposta.choices[0].message.model_dump(exclude_none=True))
    return mensagens

#cria lista de dicts para enviar ao modelo
mensagens = [
    {"role": "user", "content": "O que é uma maçã em 5 palavras?"},
]
#chama o modelo
mensagens = geracao_texto(mensagens=mensagens)

mensagens.append({"role": "user", "content": "E qual sua cor?"})
#chama o modelo
mensagens = geracao_texto(mensagens=mensagens)

pprint(mensagens)