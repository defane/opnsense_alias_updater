import yaml
import requests
import ipaddress
import networkx as nx
from copy import copy


class NetworkFile(object):
    _path = "networks.yml"

    def __init__(self):
        with open(self._path, 'r') as stream:
            try:
                self.data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                exit(-1)

    def save(self):
        with open(self._path, 'w') as stream:
            yaml.dump(self.data, stream)

    def sort(self):
        G = nx.DiGraph()

        for alias in self.data["networks"]:
            for dep in alias["content"]:
                if self.has_dependency(dep):
                    G.add_edge(alias["name"], dep)

        sorted_networks = list(reversed(list(nx.topological_sort(G))))
        self.data["networks"] = sorted(
            self.data["networks"],
            key=lambda k: (
                sorted_networks.index(k['name'])
                if k['name'] in sorted_networks else 0
            )
        )

    def update(self):
        for alias in self.data["networks"]:
            if "update_url" not in alias:
                continue

            res = requests.get(alias["update_url"])
            if res.status_code == 200:
                alias["content"] = res.content.decode('utf-8').split('\n')

    @staticmethod
    def clean_alias(alias):
        output = copy(alias)

        if "update_url" in output:
            del output["update_url"]

        return output

    @staticmethod
    def contains_exclusively_ip_cidr(alias):
        for content in alias["content"]:
            try:
                ipaddress.ip_address(content)
                continue
            except ValueError:
                pass
            try:
                ipaddress.ip_network(content)
                continue
            except ValueError:
                pass
            return False
        return True

    @staticmethod
    def has_dependency(content):
        if "http://" == content[:7] or "https://" == content[:8]:
            return False
        try:
            ipaddress.ip_address(content)
            return False
        except ValueError:
            pass
        try:
            ipaddress.ip_network(content)
            return False
        except ValueError:
            pass
        return True
