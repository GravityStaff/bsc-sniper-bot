from eth_account import Account
from sniper.abi import ERC20_ABI

class WalletManager:
    def __init__(self, w3, private_key):
        self.w3 = w3
        self.account = Account.from_key(private_key)
        self.address = self.account.address

    def get_eth_balance(self):
        return self.w3.eth.get_balance(self.address)

    def sign_and_send(self, tx):
        tx['nonce'] = self.w3.eth.get_transaction_count(self.address)
        signed = self.w3.eth.account.sign_transaction(tx, self.account.key)
        return self.w3.eth.send_raw_transaction(signed.rawTransaction)
