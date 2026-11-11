"""Planting-window contract from SPEC.md."""

import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CITIES = """\
city,last_spring,first_fall
Richmond,04-15,10-26
Minneapolis,05-15,09-30
Atlanta,03-24,11-08
Portland,04-03,11-15
Phoenix,01-15,12-15
Denver,05-05,10-07
Chicago,04-20,10-21
Miami,00-00,00-00
Seattle,03-24,11-11
Austin,03-01,11-28
Boston,04-08,11-07
Nashville,04-06,10-31
Dallas,03-18,11-20
Detroit,04-26,10-20
Kansas City,04-15,10-20
San Francisco,01-15,12-15
Albuquerque,04-16,10-28
Fargo,05-15,09-24
Honolulu,00-00,00-00
Anchorage,05-18,09-15
"""

CROPS = """\
crop,sow_days_before_last_frost,transplant_days_after_last_frost
tomato,42,0
lettuce,14,-14
beans,0,7
basil,28,7
"""


def run(*args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, "-m", "frostline", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


class DataTests(unittest.TestCase):
    def test_cities_csv_matches_spec(self):
        self.assertEqual((ROOT / "data" / "cities.csv").read_text(encoding="utf-8"), CITIES)

    def test_crops_csv_matches_spec(self):
        self.assertEqual((ROOT / "data" / "crops.csv").read_text(encoding="utf-8"), CROPS)


class WindowTests(unittest.TestCase):
    def test_richmond_tomato(self):
        result = run("window", "--city", "Richmond", "--crop", "tomato")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout,
            "city: Richmond\ncrop: tomato\nsow: 03-04\ntransplant: 04-15\n",
        )

    def test_richmond_lettuce_transplant(self):
        result = run("window", "--city", "Richmond", "--crop", "lettuce")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout,
            "city: Richmond\ncrop: lettuce\nsow: 04-01\ntransplant: 04-01\n",
        )

    def test_miami_no_frost(self):
        result = run("window", "--city", "Miami", "--crop", "tomato")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "no frost date on file\n")
        self.assertEqual(result.stderr, "")

    def test_unknown_city_exits_2(self):
        result = run("window", "--city", "Atlantis", "--crop", "tomato")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("unknown city", result.stderr)
        self.assertIn("Atlantis", result.stderr)

    def test_unknown_crop_exits_2(self):
        result = run("window", "--city", "Richmond", "--crop", "mango")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("unknown crop", result.stderr)

    def test_case_insensitive_match(self):
        result = run("window", "--city", "richmond", "--crop", "TOMATO")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout,
            "city: Richmond\ncrop: tomato\nsow: 03-04\ntransplant: 04-15\n",
        )

    def test_negative_transplant_and_year_wrap(self):
        result = run("window", "--city", "Phoenix", "--crop", "basil")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout,
            "city: Phoenix\ncrop: basil\nsow: 12-18\ntransplant: 01-22\n",
        )

    def test_honolulu_no_frost(self):
        result = run("window", "--city", "Honolulu", "--crop", "beans")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "no frost date on file\n")

    def test_data_path_independent_of_cwd(self):
        result = subprocess.run(
            [sys.executable, "-m", "frostline", "window", "--city", "Denver", "--crop", "beans"],
            cwd=ROOT / "tests",
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PYTHONPATH": str(ROOT)},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "city: Denver\ncrop: beans\nsow: 05-05\ntransplant: 05-12\n",
        )


if __name__ == "__main__":
    unittest.main()
