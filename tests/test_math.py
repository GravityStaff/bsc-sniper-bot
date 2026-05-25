from sniper.utils import calculate_slippage

def test_basic_slippage():
    amount = 1000
    pct = 10
    # 10% of 1000 is 100, so 900 min
    assert calculate_slippage(amount, pct) == 900

