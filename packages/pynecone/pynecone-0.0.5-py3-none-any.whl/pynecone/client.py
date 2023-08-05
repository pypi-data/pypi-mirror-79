import requests
from requests_toolbelt.utils import dump

from urllib.parse import urljoin


class Client:

    def __init__(self, api_base_url, token, get_token):
        self.api_base_url = api_base_url
        self.token = token
        self.get_token = get_token
        print(self.token)

    def get_endpoint_url(self, path):
        return urljoin(self.api_base_url, path)

    def get(self, path, params=None):
        headers = {}
        if self.token:
            headers = {"Authorization": "Bearer " + self.token}

        resp = requests.get(self.get_endpoint_url(path), headers=headers, params=params)

        if resp.status_code == requests.codes.ok:
            if resp.headers.get('content-type').startswith('application/json'):
                return resp.json()
            else:
                return resp.content
        elif resp.status_code == 401:
            self.token = self.get_token()
            return self.get(path, params)
        else:
            data = dump.dump_all(resp)
            print(data.decode('utf-8'))
            return None

    def post(self, path, params):
        token = self.token
        headers = {}
        if token:
            headers = {"Authorization": "Bearer " + token}

        resp = requests.post(self.get_endpoint_url(path), headers=headers, data=params)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            self.token = self.get_token()
            return self.post(path, params)
        else:
            data = dump.dump_all(resp)
            print(data.decode('utf-8'))
            return None

    def put(self, path, params):
        token = self.token
        headers = {}
        if token:
            headers = {"Authorization": "Bearer " + token}

        resp = requests.put(self.get_endpoint_url(path), headers=headers, data=params)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            self.token = self.get_token()
            return self.put(path, params)
        else:
            print(resp.status_code, resp.text)
            # data = dump.dump_all(resp)
            # print(data.decode('utf-8'))
            return None

    def put_file(self, path, file):
        token = self.token
        headers = {}
        if token:
            headers = {"Authorization": "Bearer " + token}

        resp = requests.put(self.get_endpoint_url(path), headers=headers, files=dict(file=file))

        if resp.status_code == requests.codes.ok:
            return resp.status_code
        elif resp.status_code == 401:
            self.token = self.get_token()
            return self.put_file(path, file)
        else:
            print(resp.status_code, resp.text)
            # data = dump.dump_all(resp)
            # print(data.decode('utf-8'))
            return None

    def delete(self, path, id):
        target = urljoin(path, id)
        token = self.token
        headers = {}
        if token:
            headers = {"Authorization": "Bearer " + token}

        resp = requests.delete(self.get_endpoint_url(target), headers=headers)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            self.token = self.get_token()
            return self.delete(path, id)
        else:
            data = dump.dump_all(resp)
            print(data.decode('utf-8'))
            return None



