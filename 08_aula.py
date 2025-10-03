import json

import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = openai.Client()

#1 - desenvolver a funcao para enviar ao modelo, resposta deve ser string
#2 - criar o tools, descrevendo a funcao, campos da função que não tem valor default informar no campo required
#3 - passa para o chat completion
def obter_temperatura_atual(local, unidade="celsius"):
    if "são paulo" in local.lower():
        return json.dumps(
            {"local": "São Paulo", "temperatura": "32", "unidade": unidade}, ensure_ascii=False
            )
    elif "porto alegre" in local.lower():
        return json.dumps(
            {"local": "Porto Alegre", "temperatura": "25", "unidade": unidade}, ensure_ascii=False
            )
    elif "rio de janeiro" in local.lower():
        return json.dumps(
            {"local": "Rio de Janeiro", "temperatura": "35", "unidade": unidade}, ensure_ascii=False
            )
    else:
        return json.dumps(
            {"local": local, "temperatura": "unknown"}
            )


# uma lista de dicionarios, pois o modelo permite que envie mais de uma
# no funcion.name tem que ser um nome sugestivo para que o modelo possa identificar mais facilmente
# mesmo para a funcion.description
# funciton.enum significa que só pode ter os valores contidos no enum
# funciton.required quais parametros sao obrigatorios
tools = [
    {
        "type": "function",
        "function": {
            "name": "obter_temperatura_atual",
            "description": "Obtém a temperatura atual em uma dada cidade",
            "parameters": {
                "type": "object",
                "properties": {
                    "local": {
                        "type": "string",
                        "description": "O nome da cidade. Ex: São Paulo",
                    },
                    "unidade": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    },
                },
                "required": ["local"],
            },
        },
    }
    ]
# somente para facilitar a busca pela função
funcoes_disponiveis = {
        "obter_temperatura_atual": obter_temperatura_atual,
    }
# já passando uma mensage de busca
mensagens = [
    {"role": "user",
     "content": "Qual é a temperatura em São Paulo e Porto Alegre?"}
    ]
#chama o chat completions do modelo
resposta = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=mensagens,
    tools=tools, # ferramentas para o Modelo utilizar
    tool_choice="auto",
)

#pega a mensagem resposta, ate este momento a função ainda não foi executada
# o modelo retorna que precisa rodar duas vezes  a funcion, uma para uma São Pauslo e outra para Porto Alegre
mensagem_resp = resposta.choices[0].message
# me respondeu e avisa se precisa rodar alguma fun
tool_calls = mensagem_resp.tool_calls
# ai ver se precia rodar algua tool
if tool_calls:
    mensagens.append(mensagem_resp)
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = funcoes_disponiveis[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            local=function_args.get("local"),
            unidade=function_args.get("unidade"),
        )
        mensagens.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )
    segunda_resposta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=mensagens,
    )

mensagem_resp = segunda_resposta.choices[0].message
print(mensagem_resp.content)
