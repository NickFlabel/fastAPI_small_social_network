import dotenv
import os
import aiohttp
import json
from social_network.utils.crud import UserCrud

dotenv.load_dotenv()

HUNTER_API_KEY = os.getenv('HUNTER_API_KEY')
HUNTER_URL = os.getenv('HUNTER_URL')

async def get_hunter_data(email: str):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(f'{HUNTER_URL}?email={email}&api_key={HUNTER_API_KEY}') as resp:
            result = await resp.read()
            return json.loads(result)

def validate_email(data: dict) -> bool:
    if data['data']['status'] == 'valid':
        return True
