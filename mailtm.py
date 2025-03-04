"""A Simple Client for Mail.tm Provider"""
# @Author: CypherpunkSamurai
# @License: APACHE 2.0
import random
import string
import requests


class MailTMClient:
    def __init__(self):
        self.base_url = "https://api.mail.tm"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "random",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self.token = None

    def get_domains(self):
        """Get available domains"""
        response = self.session.get(f"{self.base_url}/domains")
        response.raise_for_status()
        return response.json()

    def create_account(self, address, password):
        """Create a new account"""
        data = {
            "address": address,
            "password": password
        }
        response = self.session.post(
            f"{self.base_url}/accounts",
            json=data
        )
        response.raise_for_status()
        return response.json()

    def generate_random_account(self, password=None):
        """Generate a random account using available domains

        Returns:
            tuple: (account_data, password)
        """
        domains = self.get_domains()

        if not domains:
            raise ValueError("No domains available")

        domain = domains[0]['domain']
        username = ''.join(random.choices(
            string.ascii_lowercase + string.digits,
            k=10
        ))
        address = f"{username}@{domain}"

        if password is None:
            password = ''.join(random.choices(
                string.ascii_letters + string.digits + '!@#$%^&*',
                k=12
            ))

        account = self.create_account(address, password)
        return account, password

    def get_token(self, address, password):
        """Get authentication token and set session headers"""
        data = {
            "address": address,
            "password": password
        }
        response = self.session.post(
            f"{self.base_url}/token",
            json=data
        )
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data.get("token")

        if self.token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

        return token_data

    def get_me(self):
        """Get current account information"""
        response = self.session.get(f"{self.base_url}/me")
        response.raise_for_status()
        return response.json()

    def _get_messages(self):
        """Get all messages for the current account"""
        response = self.session.get(f"{self.base_url}/messages")
        response.raise_for_status()
        return response.json()

    def get_message_count(self):
        """Get the total number of messages"""
        messages = self._get_messages()
        if isinstance(messages, dict) and 'hydra:totalItems' in messages:
            return messages['hydra:totalItems']
        elif isinstance(messages, list):
            return len(messages)
        return 0

    def get_message_list(self):
        """Get the list of messages without hydra wrapper"""
        messages = self._get_messages()
        if isinstance(messages, dict) and 'hydra:member' in messages:
            return messages['hydra:member']
        elif isinstance(messages, list):
            return messages
        return []

    def get_message(self, message_id):
        """Get a specific message by ID"""
        response = self.session.get(
            f"{self.base_url}/messages/{message_id}"
        )
        response.raise_for_status()
        return response.json()

    def mark_as_seen(self, message_id):
        """Mark a message as seen"""
        data = {"seen": True}
        response = self.session.patch(
            f"{self.base_url}/messages/{message_id}",
            json=data
        )
        response.raise_for_status()
        return response.json()
