import asyncio

from credentials import Credentials
from graph_client import make_client
from one_drive_api import OneDriveApi
from token_provider import OneDriveTokenProvider


def get_and_store_token():
    token_provider = OneDriveTokenProvider(**Credentials().__dict__)

    access_token = token_provider.get_access_token()
    with open('.access_token', 'w') as file:
        file.write(access_token)
    return access_token


def fetch_token():
    try:
        with open('.access_token', 'r') as file:
            return file.read()
    except FileNotFoundError:
        print('Re-generating access_token')
        return get_and_store_token()


def make_api_client(token: str):
    return OneDriveApi(access_token=token)


async def get_drives(gc):
    print(await gc.drives.get())


if __name__ == "__main__":
    credentials = Credentials().__dict__
    graph_client = make_client(**credentials)
    #https://stackoverflow.com/questions/46802055/tenant-does-not-have-a-spo-license
    asyncio.run(get_drives(graph_client))

