from abc import abstractmethod
from pynecone import Command
from .authenticator import Authenticator
from .client import Client


class RESTCommand(Command):

    def run(self, args):
        return self.execute(args, Client(self.get_config().get_api_base_url(), self.get_token(), self.get_token))

    def get_token(self):
        authenticator = Authenticator(self.get_config().get_client_id(),
                                      self.get_config().get_callback_url(),
                                      self.get_config().get_auth_url(),
                                      self.get_config().get_token_url())

        client_key = self.get_config().get_client_key()
        client_secret = self.get_config().get_client_secret()

        if client_key is not None and client_secret is not None:
            token = authenticator.get_api_token(client_key, client_secret)
        else:
            token = authenticator.login()

        return token

    @abstractmethod
    def execute(self, args, client):
        pass

    @abstractmethod
    def get_config(self):
        pass

