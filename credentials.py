from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Credentials:
    def __init__(self):
        self.client_id = getenv('CLIENT_ID')
        self.client_secret = getenv('CLIENT_SECRET')
        self.tenant_id = getenv('TENANT_ID')
