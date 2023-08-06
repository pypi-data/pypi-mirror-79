"""
    Here is the actual code for the client
"""
import json

import requests

from requests.auth import HTTPBasicAuth

from direct_debit.classes import UserInfo


class FailedRequestException(Exception):
    pass


class DirectDebitClient:
    def __init__(self, production, user_code, password):
        subdomain = "dos" if production else "dos-dr"
        self.base_url = f'https://{subdomain}.directdebit.co.za:31143/v2/'
        self.auth = HTTPBasicAuth(user_code, password)

    def whoami(self):
        resp = requests.get(self.base_url + 'whoami', auth=self.auth)

        if resp.status_code != 200:
            error = f"whoami request failed with code {resp.status_code}"
            message = resp.json().get("message")
            if message is not None:
                error += ": " + message
            else:
                error += "."

            raise FailedRequestException(error)

        data = resp.json()
        return UserInfo(data.get("user_code"), data.get("email"))
