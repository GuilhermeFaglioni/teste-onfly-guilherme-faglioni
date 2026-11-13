"""SPEC-005: o repositório deve ler todas as linhas do CSV."""

from __future__ import annotations

from pathlib import Path

from helpers import run_cli

from onfly_report.repositories.csv_reservation_repository import CsvReservationRepository

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_reads_more_than_200_rows(tmp_path: Path) -> None:
    rows = [{"reservation_id": f"R-{i}"} for i in range(250)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_reservations"] == 250


def test_real_dataset_count() -> None:
    rows = CsvReservationRepository(PROJECT_ROOT / "data" / "reservas_hoteis.csv").read()
    assert len(rows) == 300
