import openai
from openai import api_key
from dotenv import load_dotenv, find_dotenv

#carrega a chave OPENAI_API_KEY
_ = load_dotenv(find_dotenv())

client = openai.Client()

