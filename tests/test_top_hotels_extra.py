"""Testes adicionais do ranking top_hotels (SPEC-004)."""

from helpers import run_cli


def _ids(report):
    return [hotel["hotel_id"] for hotel in report["top_hotels"]]


def test_tie_breaks_by_hotel_id_asc(tmp_path):
    """Empate em total_brl desempata por hotel_id ascendente, após os maiores."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H02", "amount": "500.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "amount": "500.00"},
            {"reservation_id": "R-3", "hotel_id": "H03", "amount": "100.00"},
        ],
    )
    assert _ids(report) == ["H01", "H02", "H03"]


def test_limit_keeps_highest(tmp_path):
    """--top 1 mantém apenas o hotel de maior total."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "amount": "200.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "amount": "900.00"},
            {"reservation_id": "R-3", "hotel_id": "H03", "amount": "100.00"},
        ],
        top=1,
    )
    assert _ids(report) == ["H02"]
    assert report["top_hotels"][0]["total_brl"] == "900.00"


def test_fewer_hotels_than_top(tmp_path):
    """Com menos hotéis que --top, retorna todos."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "amount": "200.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "amount": "300.00"},
        ],
        top=5,
    )
    assert _ids(report) == ["H02", "H01"]
