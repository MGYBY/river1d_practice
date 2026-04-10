#!/usr/bin/env python3

from __future__ import annotations

import calendar
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

INPUT_FILE = Path("./2071-2100/h-q_series_merged.txt")
OUTPUT_DIR = Path("./2071-2100/")
START_YEAR = 2071
END_YEAR = 2100
DISPLAY_YEAR = 2026
AVERAGE_FILE = OUTPUT_DIR / "daily_average_2041_2070.txt"

Row = tuple[int, str]
YearRecord = tuple[str, str]

YEARS = list(range(START_YEAR, END_YEAR + 1))
YEAR_LENGTHS = {year: (366 if calendar.isleap(year) else 365) for year in YEARS}
TOTAL_DAYS = sum(YEAR_LENGTHS.values())


def read_rows(file_path: Path) -> list[Row]:
    """Read (day_index, discharge_text) rows from the merged file."""
    rows: list[Row] = []

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue

            day_index = int(parts[0])
            discharge = parts[1]
            rows.append((day_index, discharge))

    if not rows:
        raise ValueError(f"No valid rows found in {file_path}")

    return rows


def build_year_boundaries() -> list[tuple[int, int, int]]:
    """
    Return [(year, start_offset, end_offset), ...] with end_offset exclusive.

    Offsets are counted from the first day in the file after normalization.
    """
    boundaries: list[tuple[int, int, int]] = []
    start_offset = 0

    for year in YEARS:
        end_offset = start_offset + YEAR_LENGTHS[year]
        boundaries.append((year, start_offset, end_offset))
        start_offset = end_offset

    return boundaries


def split_offset_to_year(offset: int, boundaries: list[tuple[int, int, int]]) -> tuple[int, int]:
    """Map a normalized day offset to (source_year, day_in_year)."""
    for year, start_offset, end_offset in boundaries:
        if start_offset <= offset < end_offset:
            return year, offset - start_offset

    raise ValueError(f"Day offset {offset} is outside the configured year range.")


def make_display_date(source_year: int, day_in_year: int) -> str:
    """
    Build the displayed date string using the source month/day and a fixed DISPLAY_YEAR.

    This intentionally formats the string manually so that leap-day labels like
    2026-02-29 are preserved as text even though 2026 is not a leap year.
    """
    source_date = date(source_year, 1, 1) + timedelta(days=day_in_year)
    return f"{DISPLAY_YEAR}-{source_date:%m-%d}"


def build_records_by_year(rows: list[Row]) -> dict[int, list[YearRecord]]:
    """
    Split the merged series into yearly blocks.

    Assumptions for the source file:
    - the first column is a monotonically increasing day count across the full period
    - leap years are included according to the actual Gregorian calendar
    - the first day index can start from 0, 1, or any other integer as long as it is continuous
    """
    if len(rows) != TOTAL_DAYS:
        raise ValueError(
            f"Expected {TOTAL_DAYS} daily rows for {START_YEAR}-{END_YEAR} "
            f"with leap years included, but found {len(rows)} rows."
        )

    first_day = rows[0][0]
    boundaries = build_year_boundaries()
    records_by_year: dict[int, list[YearRecord]] = {year: [] for year in YEARS}

    for i, (day_index, discharge) in enumerate(rows):
        offset = day_index - first_day

        if offset != i:
            raise ValueError(
                f"Day index is not continuous at row {i + 1}: "
                f"expected {first_day + i}, found {day_index}."
            )

        source_year, day_in_year = split_offset_to_year(offset, boundaries)
        display_date = make_display_date(source_year, day_in_year)
        records_by_year[source_year].append((display_date, discharge))

    for year in YEARS:
        expected_len = YEAR_LENGTHS[year]
        actual_len = len(records_by_year[year])
        if actual_len != expected_len:
            raise ValueError(
                f"Year {year} has {actual_len} rows; expected {expected_len}."
            )

    return records_by_year


def format_number(value: float) -> str:
    """Compact float formatting without unnecessary trailing zeros."""
    return format(value, ".15g")


def write_year_files(records_by_year: dict[int, list[YearRecord]], output_dir: Path) -> None:
    """Write yearly files such as 2041.txt ... 2070.txt."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for year in YEARS:
        out_file = output_dir / f"{year}.txt"
        with out_file.open("w", encoding="utf-8") as f:
            for display_date, discharge in records_by_year[year]:
                f.write(f"{display_date} {discharge} {year}\n")


def build_daily_average(rows: list[Row]) -> list[tuple[str, float]]:
    """
    Build a calendar-day average series across all years.

    The output has 366 rows in leap-calendar order. For 02-29, only leap years
    contribute values.
    """
    first_day = rows[0][0]
    boundaries = build_year_boundaries()
    grouped: dict[tuple[int, int], list[float]] = defaultdict(list)

    for i, (day_index, discharge) in enumerate(rows):
        offset = day_index - first_day
        if offset != i:
            raise ValueError(
                f"Day index is not continuous at row {i + 1}: "
                f"expected {first_day + i}, found {day_index}."
            )

        source_year, day_in_year = split_offset_to_year(offset, boundaries)
        source_date = date(source_year, 1, 1) + timedelta(days=day_in_year)
        grouped[(source_date.month, source_date.day)].append(float(discharge))

    average_rows: list[tuple[str, float]] = []
    leap_template = date(2024, 1, 1)  # leap year only used to generate month/day order

    for offset in range(366):
        template_date = leap_template + timedelta(days=offset)
        key = (template_date.month, template_date.day)
        values = grouped.get(key, [])

        if not values:
            raise ValueError(
                f"Calendar day {template_date:%m-%d} has no values in the source data."
            )

        display_date = f"{DISPLAY_YEAR}-{template_date:%m-%d}"
        average_rows.append((display_date, sum(values) / len(values)))

    return average_rows


def write_daily_average_file(average_rows: list[tuple[str, float]], out_file: Path) -> None:
    """Write the calendar-day average discharge file."""
    with out_file.open("w", encoding="utf-8") as f:
        for display_date, average_discharge in average_rows:
            f.write(f"{display_date} {format_number(average_discharge)}\n")


def main() -> None:
    rows = read_rows(INPUT_FILE)
    records_by_year = build_records_by_year(rows)

    write_year_files(records_by_year, OUTPUT_DIR)

    average_rows = build_daily_average(rows)
    write_daily_average_file(average_rows, AVERAGE_FILE)

    print(f"Wrote {len(YEARS)} yearly files to {OUTPUT_DIR}")
    print(f"Wrote daily average file: {AVERAGE_FILE}")


if __name__ == "__main__":
    main()
