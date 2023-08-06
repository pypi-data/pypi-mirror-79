class Config:

    def __init__(self,  api_base_url, auth_url, callback_url, client_id, client_key, client_secret, token_url, debug=False):
        self.api_base_url = api_base_url
        self.auth_url = auth_url
        self.callback_url = callback_url
        self.client_id = client_id
        self.client_key = client_key
        self.client_secret = client_secret
        self.token_url = token_url
        self.debug = debug;

    def get_client_id(self):
        return self.client_id

    def get_client_key(self):
        return self.client_key

    def get_client_secret(self):
        return self.client_secret

    def get_callback_url(self):
        return self.callback_url

    def get_auth_url(self):
        return self.auth_url

    def get_api_base_url(self):
        return self.api_base_url

    def get_token_url(self):
        return self.token_url

    def get_debug(self):
        return self.debug
