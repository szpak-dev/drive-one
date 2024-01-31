from msal import ConfidentialClientApplication
import jwt


class OneDriveTokenProvider:
    def __init__(self, client_id, client_secret, tenant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.authority = "https://login.microsoftonline.com/{}".format(tenant_id)
        # self.scope = ["Files.ReadWrite.All"]
        self.scope = ["https://graph.microsoft.com/.default"]

        self.app = ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )

    def get_access_token(self):
        result = self.app.acquire_token_silent_with_error(scopes=self.scope, account=None)
        print(result)
        if not result:
            result = self.app.acquire_token_for_client(self.scope)
        if "access_token" in result:
            return result['access_token']
        else:
            raise Exception("Couldn't obtain access token. Ask IT (in particular Daniel Kuś) for help", result)

    def get_user_id_from_id_token(self, token: str):
        decoded_token = jwt.decode(token, verify=False)
        user_id = decoded_token.get('sub')
        return user_id
