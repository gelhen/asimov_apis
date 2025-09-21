from pprint import pprint
import requests

nome = 'daniela'
url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"
resposta = requests.get(url=url)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f"Erro no request: {e}")
    resultado = None
else:
    resultado = resposta.json()

pprint(resultado)
