# loads data from the vaults .json files and turns them into room objects
import json
import random

class VaultLoader():

    def __init__(self):
        # right now this is just loading some default test vault data
        # it might be a good idea to enable using multiple files,
        # or having seperate VaultLoader instances for different area types?
        self.vault_data = json.load(open("vault_data/vaults.json"))
        self.entry_vault_data = json.load(open("vault_data/entry_vaults.json"))
        # keeping track of the last vault returned so that we don't have
        # duplicates - might be better if it was like, a list of the X most
        # recently used vaults
        self.last_vault_returned = None

    def get_entry_vault(self):
        choice = random.choice(self.entry_vault_data)
        while choice == self.last_vault_returned:
            choice = random.choice(self.entry_vault_data)
        self.last_vault_returned = choice
        return choice

    # oh we're keeping track of which vaults we use...
    # but not referencing them here at all. lol. lmao. hmbol.
    def get_vault(self):
        return random.choice(self.vault_data)