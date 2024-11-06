import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações do projeto
URL = os.getenv("URL")
SEARCH_VALUE = os.getenv("SEARCH_VALUE")
PAGINATION = os.getenv("PAGINATION", "True").lower() == "true"
SCORE_THRESHOLD = int(os.getenv("SCORE_THRESHOLD", 0))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
