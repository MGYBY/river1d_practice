#!/usr/bin/env python3

from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

INPUT_FILE = Path("./2041-2070/h-q_series_merged.txt")
OUTPUT_DIR = Path("./2041-2070/")
START_YEAR = 2041
END_YEAR = 2070
DISPLAY_YEAR = 2026
AVERAGE_FILE = OUTPUT_DIR / "daily_average_2041_2070.txt"


def read_rows(file_path: Path) -> list[tuple[int, str]]:
    """Read (day_index, discharge_text) rows from the merged file."""
    rows: list[tuple[int, str]] = []

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue

            day = int(parts[0])
            discharge = parts[1]
            rows.append((day, discharge))

    return rows


def split_into_year_blocks(rows: list[tuple[int, str]]) -> list[list[tuple[int, str]]]:
    """Split the merged time series into yearly blocks using the day reset."""
    if not rows:
        return []

    blocks: list[list[tuple[int, str]]] = []
    current_block: list[tuple[int, str]] = [rows[0]]

    for day, discharge in rows[1:]:
        previous_day = current_block[-1][0]

        if day < previous_day:
            blocks.append(current_block)
            current_block = []

        current_block.append((day, discharge))

    blocks.append(current_block)
    return blocks


def format_display_date(day_index: int, source_year: int) -> str:
    """Return the displayed date string MM/dd/yyyy with yyyy fixed as DISPLAY_YEAR."""
    source_date = date(source_year, 1, 1) + timedelta(days=day_index)
    # return f"{source_date:%m/%d}/{DISPLAY_YEAR}"
    return f"{DISPLAY_YEAR}-{source_date:%m-%d}"


def format_number(value: float) -> str:
    """Compact float formatting without unnecessary trailing zeros."""
    return format(value, ".15g")


def write_year_files(blocks: list[list[tuple[int, str]]], output_dir: Path) -> None:
    """Write yearly files 1991.txt ... 2020.txt."""
    years = list(range(START_YEAR, END_YEAR + 1))

    if len(blocks) != len(years):
        raise ValueError(
            f"Expected {len(years)} year blocks for {START_YEAR}-{END_YEAR}, "
            f"but found {len(blocks)} blocks."
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    for year, block in zip(years, blocks):
        out_file = output_dir / f"{year}.txt"

        with out_file.open("w", encoding="utf-8") as f:
            for day, discharge in block:
                display_date = format_display_date(day, year)
                f.write(f"{display_date} {discharge} {year}\n")


def build_daily_average(blocks: list[list[tuple[int, str]]]) -> list[tuple[str, float]]:
    """
    Build a 365-day daily-average series across all years.

    Feb 29 is ignored. Each remaining calendar day should have one value from each
    source year, so each average should use 30 values.
    """
    years = list(range(START_YEAR, END_YEAR + 1))

    if len(blocks) != len(years):
        raise ValueError(
            f"Expected {len(years)} year blocks for {START_YEAR}-{END_YEAR}, "
            f"but found {len(blocks)} blocks."
        )

    grouped: dict[tuple[int, int], list[float]] = defaultdict(list)

    for year, block in zip(years, blocks):
        for day, discharge in block:
            source_date = date(year, 1, 1) + timedelta(days=day)

            if source_date.month == 2 and source_date.day == 29:
                continue

            key = (source_date.month, source_date.day)
            grouped[key].append(float(discharge))

    average_rows: list[tuple[str, float]] = []
    display_day = date(DISPLAY_YEAR, 1, 1)

    for offset in range(365):
        current = display_day + timedelta(days=offset)
        key = (current.month, current.day)
        values = grouped.get(key, [])

        if len(values) != len(years):
            raise ValueError(
                f"Calendar day {current:%m/%d} has {len(values)} values, "
                f"expected {len(years)}."
            )

        average_rows.append((current.strftime("%Y-%m-%d"), sum(values) / len(values)))

    return average_rows


def write_daily_average_file(average_rows: list[tuple[str, float]], out_file: Path) -> None:
    """Write the 365-day average discharge file."""
    with out_file.open("w", encoding="utf-8") as f:
        for display_date, average_discharge in average_rows:
            f.write(f"{display_date} {format_number(average_discharge)}\n")


def main() -> None:
    rows = read_rows(INPUT_FILE)
    blocks = split_into_year_blocks(rows)

    write_year_files(blocks, OUTPUT_DIR)

    average_rows = build_daily_average(blocks)
    write_daily_average_file(average_rows, AVERAGE_FILE)

    print(f"Wrote {len(blocks)} yearly files to {OUTPUT_DIR}")
    print(f"Wrote daily average file: {AVERAGE_FILE}")


if __name__ == "__main__":
    main()
