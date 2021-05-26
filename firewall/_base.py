import keyring

service_name = "opnsense_alias_updater"

class FirewallBase(object):
    _client_class = None
    def __init__(self, config):
        key = config["key"]
        private = keyring.get_password(service_name, key)
        self.client = self._client_class(
            key, private, config["base_url"], verify_cert=True
        )