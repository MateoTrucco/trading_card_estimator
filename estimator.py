"""Configurable trading-card break-even estimates.

This module intentionally avoids assuming a particular platform's current drop,
fee or tax rules. Users provide every rate explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

_CENT = Decimal("0.01")


@dataclass(frozen=True, slots=True)
class Estimate:
    expected_cards: Decimal
    gross_revenue: Decimal
    marketplace_fees: Decimal
    net_revenue: Decimal
    purchase_total: Decimal
    profit: Decimal


def _decimal(value: object, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def estimate_break_even(
    total_cards: object,
    drop_rate_percent: object,
    average_sale_price: object,
    game_price: object,
    purchase_tax_percent: object = 0,
    marketplace_fee_percent: object = 0,
) -> Estimate:
    """Return an expected-value estimate using explicit user-provided rates."""
    cards = _decimal(total_cards, "total_cards")
    drop_rate = _decimal(drop_rate_percent, "drop_rate_percent")
    sale_price = _decimal(average_sale_price, "average_sale_price")
    price = _decimal(game_price, "game_price")
    purchase_tax = _decimal(purchase_tax_percent, "purchase_tax_percent")
    marketplace_fee = _decimal(marketplace_fee_percent, "marketplace_fee_percent")

    if cards < 0 or cards != cards.to_integral_value():
        raise ValueError("total_cards must be a non-negative integer")
    if sale_price < 0 or price < 0:
        raise ValueError("prices cannot be negative")
    for field, value in (("drop rate", drop_rate), ("purchase tax", purchase_tax), ("marketplace fee", marketplace_fee)):
        if value < 0 or value > 100:
            raise ValueError(f"{field} must be between 0 and 100")

    expected_cards = cards * drop_rate / Decimal("100")
    gross = expected_cards * sale_price
    fees = gross * marketplace_fee / Decimal("100")
    net = gross - fees
    purchase_total = price * (Decimal("1") + purchase_tax / Decimal("100"))
    profit = net - purchase_total

    money = lambda value: value.quantize(_CENT, rounding=ROUND_HALF_UP)
    return Estimate(
        expected_cards=expected_cards.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        gross_revenue=money(gross),
        marketplace_fees=money(fees),
        net_revenue=money(net),
        purchase_total=money(purchase_total),
        profit=money(profit),
    )
