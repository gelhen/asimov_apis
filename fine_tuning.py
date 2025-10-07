import json
from pprint import pprint
import openai
from dotenv import load_dotenv, find_dotenv

from desafio_chatbot import client

_ = load_dotenv(find_dotenv())

# abre arquivo com perguntas e respostas
with open('arquivos/chatbot_respostas.json', encoding="utf8") as f:
    json_respostas = json.load(f)


# gerar arquivo json L
with open('arquivos/chatbot_respostas.jsonl', 'w') as f:
    for entrada in json_respostas:
        print(entrada)
        resposta = {
            'resposta': entrada.get('resposta'),
            'categoria': entrada.get('categoria'),
            'fonte': 'AsimmoBot'
        }
        entrada_jsonl = {
            'messages': [
                {'role': 'user', 'content': entrada['pergunta']},
                {'role': 'assistant', 'content': json.dumps(resposta, ensure_ascii=False, indent=2)}
            ]
        }
        json.dump(entrada_jsonl, f, ensure_ascii=False)
        f.write('\n')

file = client.files.create(
    file=open('arquivos/chatbot_respostas.jsonl', 'rb'),
    purpose='fine-tune'
)

client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-3.5-turbo"
)