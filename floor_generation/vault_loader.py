# loads data from the vaults .json files and turns them into room objects
import json
import random

class VaultLoader():

    def __init__(self):
        self.vault_data = json.load(open("vault_data/vaults.json"))
        self.entry_vault_data = json.load(open("vault_data/entry_vaults.json"))
        self.last_vault_returned = None

    def get_entry_vault(self):
        choice = random.choice(self.entry_vault_data)
        while choice == self.last_vault_returned:
            choice = random.choice(self.entry_vault_data)
        self.last_vault_returned = choice
        return choice

    def get_vault(self):
        return random.choice(self.vault_data)