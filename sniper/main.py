import os
import time
import signal
import sys
import logging
from dotenv import load_dotenv
from web3 import Web3
from colorama import Fore, Style, init

from sniper.core import SniperEngine
from sniper.scanner import MempoolScanner
from sniper.wallet import WalletManager

# just global setup for terminal colors
init(autoreset=True)

def handle_exit(sig, frame):
    print(f"\n{Fore.YELLOW}caught exit signal, cleaning up...")
    sys.exit(0)

def main():
    """
    entry point for the bot. loads config, sets up web3 connection,
    and starts the main block/mempool polling loop.
    """
    load_dotenv()
    signal.signal(signal.SIGINT, handle_exit)

    rpc_url = os.getenv("RPC_URL")
    if not rpc_url:
        print(f"{Fore.RED}error: RPC_URL not set in .env")
        return

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print(f"{Fore.RED}failed to connect to {rpc_url}")
        return

    # print(f"debug: chain id is {w3.eth.chain_id}") # moved to logs
    
    wallet = WalletManager(w3, os.getenv("PRIVATE_KEY"))
    engine = SniperEngine(w3, wallet)
    scanner = MempoolScanner(w3)

    print(f"{Fore.CYAN}--- BSC SNIPER STARTED ---")
    print(f"{Fore.GREEN}wallet: {wallet.address}")
    print(f"{Fore.GREEN}balance: {w3.from_wei(wallet.get_balance(), 'ether')} BNB")
    
    # we poll because standard websockets on public nodes are trash
    # and drop connection every 5 minutes
    while True:
        try:
            for pair_data in scanner.scan():
                if not pair_data:
                    continue
                
                token_addr = pair_data['token']
                print(f"{Fore.MAGENTA}found potential target: {token_addr}")
                
                # TODO: add rug check here before committing buy
                success = engine.execute_buy(
                    token_addr, 
                    float(os.getenv("AMOUNT_TO_SPEND", 0.05))
                )
                
                if success:
                    print(f"{Fore.GREEN}buy order sent!")
                else:
                    print(f"{Fore.RED}buy failed or skipped")
            
            time.sleep(0.1) # tiny sleep to not burn cpu
            
        except Exception as e:
            print(f"{Fore.RED}loop error: {e}")
            time.sleep(1) # cool down on error

if __name__ == "__main__":
    main()
