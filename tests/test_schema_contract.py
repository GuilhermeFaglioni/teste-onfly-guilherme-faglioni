"""Contrato do schema do relatório (docs/SCHEMA.md). Teste adicional — não editar sem escalonamento."""

import re

from helpers import run_cli

MONEY = re.compile(r"^-?\d+\.\d{2}$")
SUMMARY_INT = {
    "total_reservations",
    "confirmed_reservations",
    "cancelled_reservations",
    "no_show_reservations",
    "total_room_nights",
}
SUMMARY_MONEY = {"total_amount_brl", "average_nightly_rate_brl"}

ROWS = [
    {"reservation_id": "R-1", "hotel_id": "H01", "amount": "1000.00"},
    {"reservation_id": "R-2", "hotel_id": "H02", "currency": "USD", "amount": "10.00", "checkin_date": "2025-02-01",
     "checkout_date": "2025-02-03"},
    {"reservation_id": "R-3", "hotel_id": "H03", "status": "CANCELLED"},
    {"reservation_id": "R-4", "hotel_id": "H04", "status": "NO_SHOW"},
]


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def test_top_level_keys_and_version(tmp_path):
    report = run_cli(tmp_path, ROWS)
    assert set(report) == {"report_version", "generated_at", "summary", "by_month", "top_hotels"}
    assert report["report_version"] == "1.0"
    assert isinstance(report["generated_at"], str) and report["generated_at"].endswith("-03:00")


def test_summary_types(tmp_path):
    summary = run_cli(tmp_path, ROWS)["summary"]
    assert set(summary) == SUMMARY_INT | SUMMARY_MONEY
    assert all(_is_int(summary[key]) for key in SUMMARY_INT)
    assert all(isinstance(summary[key], str) and MONEY.match(summary[key]) for key in SUMMARY_MONEY)


def test_by_month_items(tmp_path):
    by_month = run_cli(tmp_path, ROWS)["by_month"]
    assert isinstance(by_month, list) and by_month
    for item in by_month:
        assert set(item) == {"month", "reservations", "room_nights", "total_brl"}
        assert re.match(r"^\d{4}-\d{2}$", item["month"])
        assert _is_int(item["reservations"]) and _is_int(item["room_nights"])
        assert MONEY.match(item["total_brl"])
    months = [item["month"] for item in by_month]
    assert months == sorted(months)


def test_top_hotels_items_and_limit(tmp_path):
    top = run_cli(tmp_path, ROWS, top=1)["top_hotels"]
    assert len(top) == 1
    for item in top:
        assert set(item) == {"hotel_id", "hotel_name", "room_nights", "total_brl"}
        assert isinstance(item["hotel_id"], str) and isinstance(item["hotel_name"], str)
        assert _is_int(item["room_nights"])
        assert MONEY.match(item["total_brl"])


def test_empty_nights_average_is_zero(tmp_path):
    summary = run_cli(tmp_path, [{"status": "CANCELLED"}])["summary"]
    assert summary["total_room_nights"] == 0
    assert summary["total_amount_brl"] == "0.00"
    assert summary["average_nightly_rate_brl"] == "0.00"
