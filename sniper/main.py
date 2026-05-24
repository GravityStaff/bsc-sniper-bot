import os
import time
import signal
import sys
from dotenv import load_dotenv
from web3 import Web3

from sniper.core import SniperEngine
from sniper.scanner import MempoolScanner
from sniper.wallet import WalletManager

def main():
    load_dotenv()
    
    w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
    if not w3.is_connected():
        print("can't connect to bsc node")
        return

    wallet = WalletManager(w3, os.getenv("PRIVATE_KEY"))
    engine = SniperEngine(w3, wallet)
    scanner = MempoolScanner(w3)

    print(f"starting sniper on {wallet.address}")
    
    try:
        for pair in scanner.stream_new_pairs():
            print(f"new pair detected: {pair}")
            engine.process_pair(pair)
    except KeyboardInterrupt:
        print("shutting down")

if __name__ == "__main__":
    main()
