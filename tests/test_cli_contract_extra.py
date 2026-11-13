"""Testes de contrato da CLI e de exatidão (SPEC-006)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from helpers import run_cli

import onfly_report.cli as cli

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RATES = PROJECT_ROOT / "data" / "taxas_cambio.csv"
SAMPLE = PROJECT_ROOT / "data" / "exemplo-validacao.csv"


def _run(args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "onfly_report", *args],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_exit_0_and_output_created(tmp_path):
    output = tmp_path / "out" / "report.json"
    proc = _run(["--input", str(SAMPLE), "--rates", str(RATES), "--output", str(output)])
    assert proc.returncode == 0, proc.stderr
    assert output.is_file()
    json.loads(output.read_text(encoding="utf-8"))


def test_exit_2_missing_input(tmp_path):
    proc = _run(
        [
            "--input", str(tmp_path / "nao-existe.csv"),
            "--rates", str(RATES),
            "--output", str(tmp_path / "report.json"),
        ]
    )
    assert proc.returncode == 2


@pytest.mark.parametrize("top", ["0", "-1", "abc"])
def test_exit_2_invalid_top(tmp_path, top):
    proc = _run(
        [
            "--input", str(SAMPLE),
            "--rates", str(RATES),
            "--output", str(tmp_path / "report.json"),
            "--top", top,
        ]
    )
    assert proc.returncode == 2


def test_exit_1_unexpected_error(tmp_path, monkeypatch):
    class Boom:
        def __init__(self, *args, **kwargs):
            pass

        def build(self):
            raise RuntimeError("falha inesperada")

    monkeypatch.setattr(cli, "ReportBuilder", Boom)
    code = cli.main(
        ["--input", str(SAMPLE), "--rates", str(RATES), "--output", str(tmp_path / "r.json")]
    )
    assert code == 1


def test_half_up_and_sum_before_round(tmp_path):
    rows = [
        {"reservation_id": f"R-{i}", "hotel_id": "H01", "amount": "0.335"}
        for i in range(3)
    ]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_amount_brl"] == "1.01"


def test_by_month_uses_checkin_month(tmp_path):
    rows = [{"checkin_date": "2025-01-31", "checkout_date": "2025-02-02"}]
    report = run_cli(tmp_path, rows)
    assert [m["month"] for m in report["by_month"]] == ["2025-01"]
    assert report["by_month"][0]["room_nights"] == 2


def test_validation_sample_matches_readme(tmp_path):
    output = tmp_path / "exemplo.json"
    proc = _run(["--input", str(SAMPLE), "--rates", str(RATES), "--output", str(output)])
    assert proc.returncode == 0, proc.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["summary"] == {
        "total_reservations": 12,
        "confirmed_reservations": 9,
        "cancelled_reservations": 2,
        "no_show_reservations": 1,
        "total_room_nights": 28,
        "total_amount_brl": "7566.00",
        "average_nightly_rate_brl": "270.21",
    }
    assert report["by_month"] == [
        {"month": "2025-01", "reservations": 8, "room_nights": 25, "total_brl": "6684.00"},
        {"month": "2025-02", "reservations": 1, "room_nights": 3, "total_brl": "882.00"},
    ]
    assert report["top_hotels"] == [
        {"hotel_id": "H01", "hotel_name": "Hotel Aurora Paulista", "room_nights": 3, "total_brl": "1200.00"},
        {"hotel_id": "H02", "hotel_name": "Hotel Mirante", "room_nights": 2, "total_brl": "1084.00"},
        {"hotel_id": "H12", "hotel_name": "Hotel Miami Beach", "room_nights": 1, "total_brl": "1000.00"},
        {"hotel_id": "H10", "hotel_name": "Hotel Madrid, Gran Vía", "room_nights": 4, "total_brl": "900.00"},
        {"hotel_id": "H09", "hotel_name": "Hotel Lisboa, Centro", "room_nights": 3, "total_brl": "882.00"},
    ]
