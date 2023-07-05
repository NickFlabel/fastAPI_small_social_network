import os

class Settings:
    def __init__(self):
        self.email_validation = True
        self.caching = True

def get_settings():
    return Settings()
