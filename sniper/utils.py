from web3 import Web3
import time

def to_wei(amount: float, unit: str = 'ether') -> int:
    return Web3.to_wei(amount, unit)

def from_wei(amount: int, unit: str = 'ether') -> float:
    return float(Web3.from_wei(amount, unit))

def get_deadline(seconds: int = 60) -> int:
    return int(time.time()) + seconds

def apply_gas_multiplier(estimate: int, multiplier: float = 1.2) -> int:
    """Don't want to get stuck in mempool just for a few gwei"""
    return int(estimate * multiplier)
