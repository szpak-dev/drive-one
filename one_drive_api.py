import requests
import jwt


class OneDriveApi:
    def __init__(self, access_token):
        self.access_token = access_token
        self.user_id = jwt.decode(access_token, algorithms=['RS256'], verify=False).get('sub')

    def upload_file(self, file_path, target_folder="/"):
        if self.access_token:
            upload_url = self.get_upload_url(target_folder)
            if upload_url:
                headers = {
                    "Authorization": "Bearer {}".format(self.access_token),
                    "Content-Type": "application/octet-stream",
                }

                with open(file_path, "rb") as file:
                    response = requests.put(upload_url, headers=headers, data=file)

                if response.status_code == 201:
                    print("File uploaded successfully.")
                else:
                    print("Failed to upload file. Status Code:", response.status_code)
                    print("Response:", response.text)
            else:
                print("Failed to get upload URL.")
        else:
            print("Access token not provided.")

    def get_upload_url(self, target_folder):
        if self.user_id:
            graph_url = "https://graph.microsoft.com/v1.0/users/{}/drive/root:{}:/content".format(self.user_id,
                                                                                                  target_folder)
        else:
            graph_url = "https://graph.microsoft.com/v1.0/me/drive/root:{}:/content".format(target_folder)

        if self.access_token:
            headers = {"Authorization": "Bearer {}".format(self.access_token)}
            response = requests.post(graph_url, headers=headers)

            if response.status_code == 200:
                return response.json().get("@microsoft.graph.uploadUrl")
            else:
                print("Failed to get upload URL. Status Code:", response.status_code)
                print("Response:", response.text)
        else:
            print("Access token not provided.")
        return None
