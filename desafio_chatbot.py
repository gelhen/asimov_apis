import openai
from dotenv import load_dotenv, find_dotenv

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
    print("Assistent: ", end='')
    texto_completo = ''
    for strema_resposta in resposta:
        texto = strema_resposta.choices[0].delta.content
        if texto:
            print(texto, end='')
            texto_completo += texto
    print()
    mensagens.append({'role': 'assistant', 'content': texto_completo})
    return mensagens


if __name__ == '__main__':
    print('Bem vindo ao chatbot com python da Asimov :)')
    mensagens = []
    while True:
        input_usuario  = input('User: ')
        if input_usuario.lower() == 'sair':
            break

        mensagens.append({"role": "user", "content": input_usuario})
        #chama o modelo
        mensagens = geracao_texto(mensagens=mensagens)
