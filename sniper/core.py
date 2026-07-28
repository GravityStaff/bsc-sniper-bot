import logging
from sniper.abi import PANCAKE_ROUTER_ABI, ERC20_ABI
from sniper.utils import get_deadline, apply_gas_multiplier

logger = logging.getLogger(__name__)

class Sniper:
    """Main logic for sniping. It's a bit of a mess because of rapid changes during launches."""
    def __init__(self, w3, wallet, router_addr, wbnb_addr):
        self.w3 = w3
        self.wallet = wallet
        self.router_address = self.w3.to_checksum_address(router_addr)
        self.wbnb = self.w3.to_checksum_address(wbnb_addr)
        self.router = self.w3.eth.contract(address=self.router_address, abi=PANCAKE_ROUTER_ABI)

    def get_token_decimals(self, token_addr):
        contract = self.w3.eth.contract(address=token_addr, abi=ERC20_ABI)
        return contract.functions.decimals().call()

    def buy_token(self, token_address, amount_in_eth, slippage=0, gas_price=None):
        # print(f"Attempting buy for {token_address}")
        token_address = self.w3.to_checksum_address(token_address)
        
        path = [self.wbnb, token_address]
        
        if not gas_price:
            gas_price = self.w3.eth.gas_price

        # we don't use estimate_gas here because it fails if liquidity isn't added yet
        # and we want the tx to hit exactly when it is
        tx_params = {
            'from': self.wallet.address,
            'value': amount_in_eth,
            'gas': 300000,
            'gasPrice': apply_gas_multiplier(gas_price, 1.1),
            'nonce': self.w3.eth.get_transaction_count(self.wallet.address)
        }

        try:
            func = self.router.functions.swapExactETHForTokens(
                slippage, 
                path,
                self.wallet.address,
                get_deadline(300)
            )
            
            tx = func.build_transaction(tx_params)
            tx_hash = self.wallet.sign_and_send(tx)
            logger.info(f"Buy sent: {tx_hash.hex()}")
            return tx_hash
        except Exception as e:
            logger.error(f"Failed to build buy tx: {e}")
            return None

    def watch_logs(self, factory_address, callback):
        """
        Poll for new PairCreated events. 
        Web3 py filter is sometimes slow, but let's stick to it for now.
        """
        # TODO: switch to websocket subscription for faster mempool access
        event_signature_hash = self.w3.keccak(text="PairCreated(address,address,address,uint256)").hex()
        
        filter_params = {
            "address": factory_address,
            "topics": [event_signature_hash]
        }

        while True:
            try:
                logs = self.w3.eth.get_logs(filter_params)
                for log in logs:
                    # extracting token from log topics
                    # topic 0 is event sig, 1 is token0, 2 is token1
                    t0 = "0x" + log['topics'][1].hex()[-40:]
                    t1 = "0x" + log['topics'][2].hex()[-40:]
                    
                    target = t1 if t0.lower() == self.wbnb.lower() else t0
                    callback(target)
            except Exception as e:
                logger.warning(f"log fetch error: {e}")
            
            import time
            time.sleep(0.5) # don't spam node too hard
