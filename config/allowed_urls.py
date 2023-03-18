import os
from dotenv import load_dotenv
load_dotenv()
pass_jwt_check = []
pass_api_key_check=[f'/{os.getenv("API_VERSION")}/swagger', f'/openapi.json']