from decimal import Decimal

from onfly_report.services.currency_converter import convert_to_brl


def test_usd_multiplies():
    assert convert_to_brl(Decimal("100"), "USD", {"USD": Decimal("5.42")}) == Decimal("542.00")


def test_brl_identity():
    assert convert_to_brl(Decimal("100"), "BRL", {"BRL": Decimal("1")}) == Decimal("100.00")


def test_exact_decimal():
    result = convert_to_brl(Decimal("0.10"), "USD", {"USD": Decimal("5.420001")})
    assert isinstance(result, Decimal)
    assert result == Decimal("0.10") * Decimal("5.420001")
