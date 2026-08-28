from decimal import Decimal

import pytest

from estimator import break_even_sale_price, estimate_break_even, roi_percent


def test_estimate_with_explicit_rates():
    result = estimate_break_even(10, 50, "0.20", "0.50", 10, 5)
    assert result.expected_cards == Decimal("5.00")
    assert result.gross_revenue == Decimal("1.00")
    assert result.marketplace_fees == Decimal("0.05")
    assert result.net_revenue == Decimal("0.95")
    assert result.purchase_total == Decimal("0.55")
    assert result.profit == Decimal("0.40")
    assert roi_percent(result) == Decimal("72.7")
    assert break_even_sale_price(10, 50, "0.50", 10, 5) == Decimal("0.12")


@pytest.mark.parametrize("values", [(-1, 50, 1, 1), (10.5, 50, 1, 1), (10, 101, 1, 1), (10, 50, -1, 1)])
def test_invalid_inputs(values):
    with pytest.raises(ValueError):
        estimate_break_even(*values)


def test_break_even_is_unavailable_without_expected_cards():
    assert break_even_sale_price(10, 0, 1) is None
