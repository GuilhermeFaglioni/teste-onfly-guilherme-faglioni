"""Testes da SPEC-001: só CONFIRMED é faturável."""

import pytest
from helpers import run_cli

from onfly_report.services.status_policy import is_billable


@pytest.mark.parametrize(
    ("status", "expected"),
    [("CONFIRMED", True), ("NO_SHOW", False), ("CANCELLED", False), ("PENDING", False)],
    ids=["CONFIRMED", "NO_SHOW", "CANCELLED", "PENDING"],
)
def test_is_billable(status, expected):
    """Apenas CONFIRMED é faturável; demais status (inclusive desconhecidos) não."""
    assert is_billable(status) is expected


def test_no_show_counted_but_not_billed(tmp_path):
    """NO_SHOW entra na contagem, mas não em noites nem valores."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CONFIRMED", "amount": "100.00"},
            {
                "reservation_id": "R-2",
                "status": "NO_SHOW",
                "amount": "70.00",
                "checkout_date": "2025-01-13",
            },
        ],
    )
    summary = report["summary"]
    assert summary["no_show_reservations"] == 1
    assert summary["total_room_nights"] == 1
    assert summary["total_amount_brl"] == "100.00"
