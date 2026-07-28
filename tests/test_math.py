import pytest
from sniper.utils import calculate_slippage, get_price_impact

def test_basic_slippage():
    assert calculate_slippage(1000, 10) == 900
    assert calculate_slippage(1000, 0.5) == 995

def test_impact_calc():
    # if pool is 100 bnb and we swap 1, impact should be roughly 1%
    res = get_price_impact(1, 100)
    assert res == 1.0

def test_insane_slippage():
    with pytest.raises(ValueError):
        calculate_slippage(100, 101)
