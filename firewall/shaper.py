import ipaddress
from copy import copy
from pyopnsense import firewall_shaper
from ._base import FirewallBase, service_name

class FirewallShaper(FirewallBase):
    _client_class = firewall_shaper.FirewallShaperClient

    def apply(self):
        self.client.reconfigure()

    def delete(self, uuid):
        self.client.delete_item(uuid)

    def get_sequence_by_uuid(self, uuid):
        res = self.client.get_rule()
        return res["rule"]["sequence"]

    def get_current_sequence(self):
        res = self.client.get_rule()
        return res["rule"]["sequence"]
    
    def get_uuid_by_description(self, description):
        for row in self.client.search_rules(description)["rows"]:
            if row["description"] == description:
                return row["uuid"]
        return None
    
    def get_interface_id_by_name(self, name):
        res = self.client.get_rule()

        interfaces = res["rule"]["interface"]

        for interface_id in interfaces:
            if interfaces[interface_id]["value"] == name:
                return interface_id

        return None

    def get_target_id_by_name(self, name):
        res = self.client.get_rule()

        target = res["rule"]["target"]

        for target_id in target:
            if target[target_id]["value"] == name:
                return target_id

        return None

    def get_items_generated_by_updater(self):
        last_page = False
        rowCount = 100
        current = 1
        items = list()

        pattern = "%s " % service_name
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

   
    def save(self, data):
        data = copy(data)
        description = "{} {}".format(
            service_name,
            data.get("name", "")
        )
        
        uuid = self.get_uuid_by_description(description)
        
        interface = self.get_interface_id_by_name(data["interface"])
        source = data["source"]
        destination = data["destination"]
        target = self.get_target_id_by_name(data["target"])

        if uuid is not None:
            sequence = self.get_sequence_by_uuid(uuid)
            result = self.client.set_rule(uuid, sequence, interface, source, destination, target, description=description)
        else:
            sequence = self.get_current_sequence()
            result = self.client.add_rule(sequence, interface, source, destination, target, description=description)

        if result.get("result") != "saved":
            raise ValueError(result.get('validations'))
