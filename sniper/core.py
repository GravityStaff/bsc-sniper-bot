import time
from sniper.abi import PANCAKE_ROUTER_ABI
from sniper.utils import get_deadline

class Sniper:
    def __init__(self, w3, wallet, router_addr):
        self.w3 = w3
        self.wallet = wallet
        self.router = self.w3.eth.contract(address=router_addr, abi=PANCAKE_ROUTER_ABI)

    def buy_token(self, token_address, amount_in_wei):
        path = [self.w3.to_checksum_address("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"), 
                self.w3.to_checksum_address(token_address)]
        
        tx = self.router.functions.swapExactETHForTokens(
            0, # danger: zero slippage for speed
            path,
            self.wallet.address,
            get_deadline()
        ).build_transaction({
            'from': self.wallet.address,
            'value': amount_in_wei,
            'gas': 250000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        return self.wallet.sign_and_send(tx)
