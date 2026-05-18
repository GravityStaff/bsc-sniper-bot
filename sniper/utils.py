from web3 import Web3

def to_wei(amount: float, unit: str = 'ether') -> int:
    return Web3.to_wei(amount, unit)

def from_wei(amount: int, unit: str = 'ether') -> float:
    return float(Web3.from_wei(amount, unit))

def get_deadline(seconds: int = 120) -> int:
    import time
    return int(time.time()) + seconds
