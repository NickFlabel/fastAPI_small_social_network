import dotenv
import os
import aiohttp
import json
from social_network.utils.crud import UserCrud

dotenv.load_dotenv()

ENRICHMENT_API_KEY = os.getenv('ENRICHMENT_API_KEY')
ENRICHMENT_URL = os.getenv('ENRICHMENT_URL')

async def get_enrichment_data(email: str):
    headers = {
        'Authorization': f'Bearer {ENRICHMENT_API_KEY}',
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(f'{ENRICHMENT_URL}{email}', headers=headers) as resp:
            result = await resp.read()
            return json.loads(result)

def save_enrichment_data(data, db, id):
    new_data = {
        'enrichment_id': data['id'],
        'full_name': data['name']['fullName'],
        'given_name': data['name']['givenName'],
        'family_name': data['name']['familyName']
    }
    UserCrud(db).put(id, new_data)
