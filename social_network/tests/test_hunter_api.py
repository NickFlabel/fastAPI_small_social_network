from aioresponses import aioresponses
import pytest
import dotenv
import os
import json

from social_network.tests.utils import UserForTesting
from social_network.utils.hunter_api import get_hunter_data, validate_email

HUNTER_API_KEY = os.getenv('HUNTER_API_KEY')
HUNTER_URL = os.getenv('HUNTER_URL')

test_data = {
    'data': {
        'status': 'valid'
    }
}

test_data_false = {
    'data': {
        'status': 'invalid'
    }
}

@pytest.mark.asyncio
async def test_get_enrichment_info():
    with aioresponses() as m:
        email = 'test@test.com'
        m.get(f'{HUNTER_URL}?email={email}&api_key={HUNTER_API_KEY}', body=json.dumps(test_data))
        result = await get_hunter_data(email)
        assert result == test_data

def test_validate_email():
    assert validate_email(test_data)

def test_validate_invalid_email():
    assert not validate_email(test_data_false)
