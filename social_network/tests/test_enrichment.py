from aioresponses import aioresponses
import pytest
import dotenv
import os
import json

from social_network.tests.utils import UserForTesting
from social_network.tests.fixtures import database
from social_network.utils.enrichment_api import get_enrichment_data, save_enrichment_data
from social_network.db.db import get_test_db

dotenv.load_dotenv()
ENRICHMENT_URL = os.getenv('ENRICHMENT_URL')

db = get_test_db().__next__()

# exaple of data from API docs

test_data = {
  "id": "d54c54ad-40be-4305-8a34-0ab44710b90d",
  "name": {
    "fullName": "Alex MacCaw",
    "givenName": "Alex",
    "familyName": "MacCaw"
  },
  "email": "alex@clearbit.com",
  "location": "San Francisco, CA, US",
  "timeZone": "America/Los_Angeles",
  "utcOffset": -7,
  "geo": {
    "city": "San Francisco",
    "state": "California",
    "stateCode": "CA",
    "country": "United States",
    "countryCode": "US",
    "lat": 37.7749295,
    "lng": -122.4194155
  },
  "bio": "O'Reilly author, software engineer & traveller. Founder of https://clearbit.com",
  "site": "http://alexmaccaw.com",
  "avatar": "https://d1ts43dypk8bqh.cloudfront.net/v1/avatars/d54c54ad-40be-4305-8a34-0ab44710b90d",
  "employment": {
    "domain": "clearbit.com",
    "name": "Clearbit",
    "title": "Co-founder, CEO",
    "role": "leadership",
    "subRole": "ceo",
    "seniority": "executive"
  },
  "facebook": {
    "handle": "amaccaw"
  },
  "github": {
    "handle": "maccman",
    "id": "2142",
    "avatar": "https://avatars.githubusercontent.com/u/2142?v=2",
    "company": "Clearbit",
    "blog": "http://alexmaccaw.com",
    "followers": 3594,
    "following": 111
  },
  "twitter": {
    "handle": "maccaw",
    "id": "2006261",
    "bio": "O'Reilly author, software engineer & traveller. Founder of https://clearbit.com",
    "followers": 15248,
    "following": 1711,
    "statuses": 14300,
    "favorites": 21100,
    "location": "San Francisco",
    "site": "http://alexmaccaw.com",
    "avatar": "https://pbs.twimg.com/profile_images/1826201101/297606_10150904890650705_570400704_21211347_1883468370_n.jpeg"
  },
  "linkedin": {
    "handle": "in/alex-maccaw-ab592978"
  },
  "googleplus": {
    "handle": 'null'
  },
  "gravatar": {
    "handle": "maccman",
    "urls": [
      {
        "value": "http://alexmaccaw.com",
        "title": "Personal Website"
      }
    ],
    "avatar": "http://2.gravatar.com/avatar/994909da96d3afaf4daaf54973914b64",
    "avatars": [
      {
        "url": "http://2.gravatar.com/avatar/994909da96d3afaf4daaf54973914b64",
        "type": "thumbnail"
      }
    ]
  },
  "fuzzy": 'false',
  "emailProvider": 'false',
  "indexedAt": "2016-11-07T00:00:00.000Z",
  "phone": "+1 123-456-7890",
  "activeAt": "2014-11-25T18:56:43.000Z",
  "inactiveAt": "2021-11-25T18:56:43.000Z"
}

@pytest.mark.asyncio
async def test_get_enrichment_info(database):
    with aioresponses() as m:
        email = 'test@test.com'
        m.get(f'{ENRICHMENT_URL}{email}', body=json.dumps(test_data))
        result = await get_enrichment_data(email)
        assert result == test_data

def test_save_enrichment_data(database):
    user = UserForTesting(db).create_test_user()
    save_enrichment_data(test_data, db, user.user.id)

    assert user.user.enrichment_id == test_data['id']
