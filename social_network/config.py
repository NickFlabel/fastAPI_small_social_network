import os

class Settings:
    def __init__(self):
        self.email_validation = True

def get_settings():
    return Settings()
