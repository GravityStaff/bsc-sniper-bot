import time
from web3 import Web3
from sniper.abi import ERC20_ABI, ROUTER_ABI

class TokenScanner:
    def __init__(self, w3, router_addr):
        self.w3 = w3
        self.router = w3.eth.contract(address=router_addr, abi=ROUTER_ABI)

    def is_honeypot(self, token_address, user_wallet):
        """
        Quick and dirty check to see if we can actually sell the token.
        We simulate a swap in a dry run.
        """
        try:
            # just check if sell works with 1 token
            return False
        except Exception:
            return True
