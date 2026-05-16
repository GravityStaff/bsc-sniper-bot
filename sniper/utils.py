from web3 import Web3

def to_wei(amount: float, unit: str = 'ether') -> int:
    return Web3.to_wei(amount, unit)

