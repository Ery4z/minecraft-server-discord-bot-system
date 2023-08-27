import requests
import json

# Constants
BASE_URL = 'https://iaas.us-phoenix-1.oraclecloud.com'


class OracleConnector:
    def __init__(self, auth_token, subnet_id):
        self.auth_token = auth_token
        self.subnet_id = subnet_id

    def set_firewall_rules(self, ips):
        """
        Create firewall rules to allow a list of IPs (or all IPs) to a subnet for port 25565.
        """
        for ip in ips:
            source_cidr = f'{ip}/32' if ip != '0.0.0.0' else '0.0.0.0/0'
            url = f'{BASE_URL}/n/{self.subnet_id}/securityRules'
            payload = {
                'direction': 'INGRESS',
                'source': source_cidr,
                'protocol': 'tcp',
                'destinationPortRange': {
                    'min': 25565,
                    'max': 25565
                }
            }
            response = requests.post(url, headers=AUTH_HEADER, data=json.dumps(payload))
            if response.status_code != 200:
                print(f"Failed to set rule for IP: {ip}")
                response.raise_for_status()

    def get_firewall_rule_ids_by_port(self):
        """
        Retrieve the IDs of firewall rules based on the port 25565.
        """
        url = f'{BASE_URL}/n/{self.subnet_id}/securityRules'
        response = requests.get(url, headers=AUTH_HEADER)
        if response.status_code == 200:
            rules = response.json()
            rule_ids = [rule['id'] for rule in rules if rule.get('destinationPortRange') and rule['destinationPortRange']['min'] == 25565 and rule['destinationPortRange']['max'] == 25565]
            return rule_ids
        else:
            response.raise_for_status()

    def get_firewall_rules_by_port(self):
        """
        Retrieve the firewall rules based on the port 25565.
        """
        url = f'{BASE_URL}/n/{self.subnet_id}/securityRules'
        response = requests.get(url, headers=AUTH_HEADER)
        if response.status_code == 200:
            rules = response.json()
            relevant_rules = [rule for rule in rules if rule.get('destinationPortRange') 
                            and rule['destinationPortRange']['min'] == 25565 
                            and rule['destinationPortRange']['max'] == 25565]
            return relevant_rules
        else:
            response.raise_for_status()

    def is_ip_in_rules(self, target_ips='0.0.0.0/32'):
        """
        Check if the target IP is a source in any of the firewall rules for port 25565.
        """
        rules = self.get_firewall_rules_by_port()
        for rule in rules:
            if rule['source'] == target_ip:
                return True
        return False

    def get_allowed_ips(self):
        rules = self.get_firewall_rules_by_port()
        allowed = []
        for rule in rules:
            allowed.append(rule['source'])
        return allowed

    def delete_firewall_rules_by_port(self):
        """
        Delete firewall rules for port 25565.
        """
        rule_ids = self.get_firewall_rule_ids_by_port()
        for rule_id in rule_ids:
            url = f'{BASE_URL}/n/securityRules/{rule_id}'
            response = requests.delete(url, headers=AUTH_HEADER)
            if response.status_code != 200:
                print(f"Failed to delete rule with ID: {rule_id}")
                response.raise_for_status()

    def check_firewall_rules_by_port(self):
        """
        Check if any firewall rules for port 25565 exist in a subnet.
        """
        rule_ids = self.get_firewall_rule_ids_by_port()
        return bool(rule_ids)


    def set_allowed_ips(self, ips=[]):
        self.delete_firewall_rules_by_port()
        self.set_firewall_rules( ips)
        allowed = self.get_allowed_ips()
        for ip in ips:
            if not ip.contains('/'):
                ip = ((ip + '/32') if ip != '0.0.0.0' else (ip + '/0'))
            if not ip in allowed:
                return False
        return True

    def set_allow_all(self):
        self.delete_firewall_rules_by_port()
        self.set_firewall_rules( ['0.0.0.0'])
        return is_ip_in_rules( '0.0.0.0')


# Usage
# set_firewall_rules('YOUR_SUBNET_ID', ips=['1.2.3.4', '5.6.7.8'])  # Allow IPs 1.2.3.4 and 5.6.7.8 to access port 25565
# delete_firewall_rules_by_port('YOUR_SUBNET_ID')
# are_rules_present = check_firewall_rules_by_port('YOUR_SUBNET_ID')