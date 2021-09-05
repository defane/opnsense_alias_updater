import yaml

service_name = "opnsense_alias_updater"
with open("keys.yml", 'r') as stream:
    try:
        keys = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(-1)

class FirewallBase(object):
    _client_class = None
    def __init__(self, config):

        res = list(filter(lambda x: x['name'] == config['name'], keys['keys']))

        if len(res) != 1:
            raise ValueError("unknown firwarall %s" % config['name'])

        res = res[0]

        key = res['key']
        private = res['secret']

        self.client = self._client_class(
            key, private, config["base_url"], verify_cert=True
        )