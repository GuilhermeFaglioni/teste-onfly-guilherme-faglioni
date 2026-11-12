"""Testes extras da SPEC-002: noites pela diferença de datas."""

from datetime import date

from onfly_report.services.stay_calculator import calculate_room_nights


def test_same_month():
    assert calculate_room_nights(date(2024, 1, 10), date(2024, 1, 13), 1) == 3


def test_month_boundary():
    assert calculate_room_nights(date(2024, 1, 30), date(2024, 2, 2), 1) == 3


def test_year_boundary():
    assert calculate_room_nights(date(2024, 12, 31), date(2025, 1, 2), 1) == 2


def test_multiple_rooms_across_month():
    assert calculate_room_nights(date(2024, 1, 30), date(2024, 2, 2), 2) == 6


def test_leap_february():
    assert calculate_room_nights(date(2024, 2, 28), date(2024, 3, 1), 1) == 2
