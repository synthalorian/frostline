"""Offline planting windows from a bundled frost-date table."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CITIES_PATH = ROOT / "data" / "cities.csv"
CROPS_PATH = ROOT / "data" / "crops.csv"
REFERENCE_YEAR = 2026
NO_FROST = "no frost date on file"


def load_rows(path: Path, key: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows[row[key].casefold()] = row
    return rows


def month_day(value: str) -> date:
    month, day = value.split("-")
    return date(REFERENCE_YEAR, int(month), int(day))


def format_month_day(value: date) -> str:
    return f"{value.month:02d}-{value.day:02d}"


def no_frost(city_row: dict[str, str]) -> bool:
    return city_row["last_spring"] == "00-00" and city_row["first_fall"] == "00-00"


def window_lines(city_row: dict[str, str], crop_row: dict[str, str]) -> str:
    last_spring = month_day(city_row["last_spring"])
    sow = last_spring - timedelta(days=int(crop_row["sow_days_before_last_frost"]))
    transplant = last_spring + timedelta(
        days=int(crop_row["transplant_days_after_last_frost"])
    )
    return "\n".join(
        [
            f"city: {city_row['city']}",
            f"crop: {crop_row['crop']}",
            f"sow: {format_month_day(sow)}",
            f"transplant: {format_month_day(transplant)}",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="frostline")
    sub = parser.add_subparsers(dest="command", required=True)
    window = sub.add_parser("window")
    window.add_argument("--city", required=True)
    window.add_argument("--crop", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cities = load_rows(CITIES_PATH, "city")
    crops = load_rows(CROPS_PATH, "crop")
    city_row = cities.get(args.city.casefold())
    if city_row is None:
        print(f"unknown city: {args.city}", file=sys.stderr)
        return 2
    crop_row = crops.get(args.crop.casefold())
    if crop_row is None:
        print(f"unknown crop: {args.crop}", file=sys.stderr)
        return 2
    if no_frost(city_row):
        print(NO_FROST)
        return 0
    print(window_lines(city_row, crop_row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
