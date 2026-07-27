import time
from web3 import Web3
from sniper.abi import ERC20_ABI, ROUTER_ABI

class TokenScanner:
    def __init__(self, w3, router_addr, wbnb_addr):
        self.w3 = w3
        self.router_address = router_addr
        self.router = w3.eth.contract(address=Web3.to_checksum_address(router_addr), abi=ROUTER_ABI)
        self.wbnb = Web3.to_checksum_address(wbnb_addr)

    def check_token(self, token_addr, account):
        token = self.w3.eth.contract(address=Web3.to_checksum_address(token_addr), abi=ERC20_ABI)
        
        # TODO: check if liquidity is locked on unicrypt/pinksafe
        
        try:
            # simulate buying 0.1 bnb worth
            amount_in = Web3.to_wei(0.1, 'ether')
            path = [self.wbnb, token.address]
            
            # print(f"simulating for {token_addr}") # debug

            # test buy
            self.router.functions.swapExactETHForTokens(
                0,
                path,
                account.address,
                int(time.time()) + 60
            ).call({'from': account.address, 'value': amount_in})
            
            return True
        except Exception as e:
            if 'transfer helper' in str(e).lower():
                return False
            return False

    def get_tax(self, token_addr):
        # check decimals first so we don't look like idiots
        pass
