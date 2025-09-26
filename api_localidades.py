import requests


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


def pegar_id_estados():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    dados_estados = fazer_request(url=url, params={'view': 'nivelado'})
    dict_estados = {}
    for dados in dados_estados:
        id_estado = dados['UF-id']
        nome_estado = dados['UF-nome']
        dict_estados[id_estado] = nome_estado
    return dict_estados


def pegar_frequencia_nome_por_estado(nome):
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"
    frequencias_nome_por_estado = fazer_request(url=url, params={'groupBy': 'UF'})
    dict_frequencia = {}
    for dados in frequencias_nome_por_estado:
        id_estado = int(dados['localidade'])
        frequencia = dados['res'][0]['proporcao']
        dict_frequencia[id_estado] = frequencia
    return dict_frequencia


def main(nome):
    dict_estados = pegar_id_estados()
    dict_frequencia = pegar_frequencia_nome_por_estado(nome=nome)
    print(f'--- Frequência do nome "{nome}" no Estados (por 100.000 habitantes)')
    for id_estado, nome_estado in dict_estados.items():
        frequencia_estado = dict_frequencia[id_estado]
        print(f'-> {nome_estado}: {frequencia_estado}')


if __name__ == '__main__':
    main(nome='juliano')