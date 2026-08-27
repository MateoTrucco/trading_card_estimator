from decimal import Decimal

import pytest

from estimator import estimate_break_even


def test_estimate_with_explicit_rates():
    result = estimate_break_even(10, 50, "0.20", "0.50", 10, 5)
    assert result.expected_cards == Decimal("5.00")
    assert result.gross_revenue == Decimal("1.00")
    assert result.marketplace_fees == Decimal("0.05")
    assert result.net_revenue == Decimal("0.95")
    assert result.purchase_total == Decimal("0.55")
    assert result.profit == Decimal("0.40")


@pytest.mark.parametrize("values", [(-1, 50, 1, 1), (10.5, 50, 1, 1), (10, 101, 1, 1), (10, 50, -1, 1)])
def test_invalid_inputs(values):
    with pytest.raises(ValueError):
        estimate_break_even(*values)
