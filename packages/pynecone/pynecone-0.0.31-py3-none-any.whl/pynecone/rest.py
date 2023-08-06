from abc import abstractmethod
from pynecone import Cmd
from .auth import Auth, AuthMode
from .cfg import Cfg

import requests
from requests_toolbelt.utils import dump

from urllib.parse import urljoin


class REST(Cmd):

    def run(self, args):
        return self.execute(args, self)

    @abstractmethod
    def execute(self, args, client):
        pass

    def get_config(self):
        return Cfg()

    def get_endpoint_url(self, path):
        return urljoin(self.get_config().api_base_url, path)

    def get_arguments(self):
        arguments = {'headers': None, 'cookies': None,
            'auth': None, 'timeout': self.get_config().get_timeout(), 'allow_redirects': True, 'proxies': None,
            'hooks': None, 'stream': None, 'verify': None, 'cert': None, 'json': None}

        auth = Auth(self.get_config())
        mode = auth.get_mode()

        if mode == AuthMode.CLIENT_KEY or mode == AuthMode.AUTH_URL:
            token = auth.retrieve_token()
            arguments['headers'] = {"Authorization": "Bearer " + token}
        elif mode == AuthMode.CLIENT_CERT:
            arguments['cert'] = (auth.client_cert, auth.client_cert_key)
            if auth.ca_bundle is not None:
                arguments['verify'] = auth.ca_bundle
        elif mode == AuthMode.BASIC:
            arguments['auth'] = auth.get_basic_token()

        return arguments

    def dump(self, response):
        data = dump.dump_all(response)
        print(data.decode('utf-8'))

    def get(self, path, params=None):

        resp = requests.get(self.get_endpoint_url(path),  params=params, **self.get_arguments())

        if self.get_config().get_debug():
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            if resp.headers.get('content-type').startswith('application/json'):
                return resp.json()
            else:
                return resp.content
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.get(path, params)
            else:
                print('Unauthorized')
        else:
            if not self.get_config().get_debug():
                self.dump(resp)
            return None

    def post(self, path, params=None, json=None):
        arguments = self.get_arguments()
        arguments['json'] = json
        resp = requests.post(self.get_endpoint_url(path), data=params, **arguments)

        if self.get_config().get_debug():
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.post(path, params)
            else:
                print('Unauthorized')
        else:
            if not self.get_config().get_debug():
                self.dump(resp)
            return None

    def put(self, path, params):

        resp = requests.put(self.get_endpoint_url(path), data=params, **self.get_arguments())

        if self.get_config().get_debug():
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.put(path, params)
            else:
                print('Unauthorized')
        else:
            print(resp.status_code, resp.text)
            if not self.get_config().get_debug():
                self.dump(resp)
            return None

    def put_file(self, path, file):

        resp = requests.put(self.get_endpoint_url(path), files=dict(file=file), **self.get_arguments())

        if self.get_config().get_debug():
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            return resp.status_code
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.put_file(path, file)
            else:
                print('Unauthorized')
        else:
            print(resp.status_code, resp.text)
            if not self.get_config().get_debug():
                self.dump(resp)
            return None

    def delete(self, path, id):
        target = urljoin(path, id)

        resp = requests.delete(self.get_endpoint_url(target), **self.get_arguments())

        if self.get_config().get_debug():
            self.dump(resp)

        if resp.status_code == requests.codes.ok:
            return resp.json()
        elif resp.status_code == 401:
            auth = Auth(self.get_config())
            mode = auth.get_mode()
            if mode == AuthMode.AUTH_URL:
                auth.login()
                return self.delete(path, id)
            else:
                print('Unauthorized')
        else:
            if not self.get_config().get_debug():
                self.dump(resp)
            return None

