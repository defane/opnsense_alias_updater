from copy import copy
from ._base import FirewallBase, service_name
from pyopnsense import firewall_alias

class FirewallAlias(FirewallBase):
    _client_class = firewall_alias.FirewallAliasClient

    def get_uuid(self, name):
        for row in self.client.search_item(name)["rows"]:
            if row["name"] == name:
                return row["uuid"]
        return None

    def save(self, alias_data):
        data = copy(alias_data)
        data["description"] = "[{}] {}".format(
            service_name,
            data.get("description", "")
        )

        uuid = self.get_uuid(data["name"])

        if uuid is not None:
            data["id"] = uuid
            result = self.client.set_item(**data)
        else:
            result = self.client.add_item(**data)

        if result.get("result") != "saved":
            raise ValueError(result.get('validations'))

    def get_items_generated_by_updater(self):
        last_page = False
        rowCount = 100
        current = 1
        items = list()

        pattern = "[%s]" % service_name
        pattern_lenght = len(pattern)

        while not last_page:
            rows = self.client.search_item(
                current=current, rowCount=rowCount
            )['rows']

            if len(rows) == rowCount:
                current = current + 1
            else:
                last_page = True

            for row in rows:
                if row["description"][:pattern_lenght] == pattern:
                    items.append(row)
        return items

    def delete(self, uuid):
        self.client.delete_item(uuid)

    def apply(self):
        self.client.reconfigure()
