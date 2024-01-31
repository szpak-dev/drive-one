#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import json
import logging

import requests
import msal


parser = argparse.ArgumentParser(description='Script to upload files to sharepoint')

parser.add_argument('--config', type=argparse.FileType('r'), required=True, help='Config file')
parser.add_argument('--files', type=argparse.FileType('rb'), required=True, nargs='+', help='Files to upload')
parser.add_argument('--folder', type=str, required=True)
parser.add_argument('--ready-folder', type=str)

groupId = "50e9a1cd-c3e3-481f-ad33-673c60eb7f6c"


class SharedFolder(object):

    def __init__(self, config_file):
        config = json.load(config_file)
        self.endpoint = config['endpoint']
        self.app = msal.ConfidentialClientApplication(
                config["client_id"], authority=config["authority"],
                client_credential=config["secret"],
        )
        result = self.app.acquire_token_silent(config["scope"], account=None)
        if not result:
            logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
            result = self.app.acquire_token_for_client(scopes=config["scope"])
        if "access_token" in result:
            self.access_token = result['access_token']
        else:
            raise Exception("Couldn't obtain access token. Ask IT (in particular Daniel Kuś) for help", result)

    def prepare_headers(self, headers):
        return dict(headers, **{'Authorization': 'Bearer ' + self.access_token})

    def create_folder(self, folder_name, parent_name=None):
        # https://docs.microsoft.com/en-us/graph/api/driveitem-post-children?view=graph-rest-1.0&tabs=http
        # POST /groups/{group-id}/drive/items/{parent-item-id}/children
        parent = "/General"
        if parent_name:
            parent = f"{parent}/{parent_name}"

        path = f"/groups/{groupId}/drive/root:{parent}:/children"
        data = json.dumps({"name": folder_name, "folder": {}})
        headers = self.prepare_headers({'Content-Type': 'application/json'})
        r = requests.post(
                self.endpoint + path,
                data=data,
                headers=headers
                )
        print(f"Request {path} -> {r.status_code} ({r.reason})")
        print(r.text)

    def upload_file(self, dir_path, file):
        # https://learn.microsoft.com/en-us/graph/api/driveitem-put-content?view=graph-rest-1.0&tabs=http
        # PUT /groups/{group-id}/drive/items/{parent-id}:/{filename}:/content
        filename = os.path.basename(file.name)
        path = f"/groups/{groupId}/drive/root:/General/{dir_path}/{filename}:/content"
        print(path)
        r = requests.put(
            self.endpoint + path,
            data=file.read(),
            headers=self.prepare_headers({'Content-Type': 'application/octet-stream'})
        )
        print(f"Request {path} -> {r.status_code} ({r.reason})")
        print(r.text)


args = parser.parse_args()
shared_folder = SharedFolder(args.config)

shared_folder.create_folder(args.folder)

if args.ready_folder:
    shared_folder.create_folder(args.ready_folder, parent_name=args.folder)

for file in args.files:
    shared_folder.upload_file(args.folder, file)