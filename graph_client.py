from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient


def make_client(client_id, client_secret, tenant_id):
    credentials = ClientSecretCredential(tenant_id, client_id, client_secret)
    scopes = ['https://graph.microsoft.com/.default']
    return GraphServiceClient(credentials=credentials, scopes=scopes)
