from social_network.redis import redis_client
import dotenv
import os

dotenv.load_dotenv()
CACHE_TIMEOUT = os.getenv('CACHE_TIMEOUT')

class Cache:
    record_name = 'likes:'
    timeout = CACHE_TIMEOUT

    def __init__(self, settings) -> None:
        self.settings = settings

    def get_cached_likes(self, post_id: int):
        if self.settings.caching:
            return redis_client.get(f'{self.record_name}{post_id}')
    
    def set_cached_likes(self, value, post_id: int):
        if self.settings.caching:
            redis_client.set(f'{self.record_name}{post_id}', value, ex=self.timeout) 

    def change_cached_value(self, post_id: int, value: int):
        if self.settings.caching:
            record = redis_client.get(f'{self.record_name}{post_id}')
            if record is None:
                return
            else:
                new_value = int(record) + value
                redis_client.set(f'{self.record_name}{post_id}', new_value, ex=self.timeout)
