#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

INPUT_FILE = Path("./1991-2020/1991-2020.txt")
OUTPUT_DIR = Path("./1991-2020/")
ENCODING = "ISO-8859-1"
# Use a synthetic Nov-Oct display year pair so winter is contiguous on the x-axis.
# 2027-2028 is chosen so Feb 29 remains a valid calendar date in leap-water-years.
DISPLAY_START_YEAR = 2027
AVERAGE_FILE = OUTPUT_DIR / "average_1991_2020_water_year.csv"

NUMERIC_HEADERS = [
    "Stage (m)",
    "Discharge (cms)",
    "Ice Velocity (m/s)",
    "Water Temperature (°C)",
    "Frazil Concentration (%)",
    "Ice Concentration (%)",
    "Anchor Ice Thickness (m)",
    "Frazil Slush Thickness (m)",
    "Solid Ice Thickness (m)",
    "Border Ice Fraction",
    "Border Ice Width (m)",
    "Air Temperature (°C)",
    "Maximum Border Ice Thickness (m)",
    "ave border thickness",
    "Water Depth (m)",
    "Water Velocity (m/s)",
    "Water Surface Width (m)",
]

YEARLY_HEADER = [
    "Time (hrs)",
    "Datetime",
    "Time",
    "Real Year",
    *NUMERIC_HEADERS,
]

AVERAGE_HEADER = [
    "Time (hrs)",
    "Datetime",
    "Time",
    *NUMERIC_HEADERS,
]


@dataclass(frozen=True)
class Record:
    source_dt: datetime
    time_str: str
    numeric_text: list[str]
    numeric_values: list[float]


@dataclass(frozen=True)
class WaterYearRecord:
    water_year: int
    display_dt: datetime
    time_str: str
    numeric_text: list[str]
    numeric_values: list[float]


def format_float(value: float) -> str:
    return format(value, ".15g")


def read_records(file_path: Path) -> list[Record]:
    records: list[Record] = []

    with file_path.open("r", encoding=ENCODING) as f:
        header = f.readline()
        if not header:
            raise ValueError(f"Input file is empty: {file_path}")

        for line in f:
            stripped = line.strip()
            if not stripped:
                continue

            parts = stripped.split()
            if len(parts) < 20:
                continue

            date_str = parts[1]
            time_str = parts[2]
            source_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
            numeric_text = parts[3:]
            numeric_values = [float(x) for x in numeric_text]

            if len(numeric_text) != len(NUMERIC_HEADERS):
                raise ValueError(
                    f"Expected {len(NUMERIC_HEADERS)} numeric columns after date/time, "
                    f"but found {len(numeric_text)} in line:\n{line}"
                )

            records.append(
                Record(
                    source_dt=source_dt,
                    time_str=time_str,
                    numeric_text=numeric_text,
                    numeric_values=numeric_values,
                )
            )

    if not records:
        raise ValueError("No data rows were found in the input file.")

    return records


def water_year_of(dt: datetime) -> int:
    """Return the water-year label year, defined by the year containing November."""
    return dt.year if dt.month >= 11 else dt.year - 1


def display_datetime_for_water_year(dt: datetime) -> datetime:
    """
    Map all water years to a synthetic Nov-Oct display year pair so that
    Nov-Dec and Jan-Feb plot continuously on the same axis.
    """
    display_year = DISPLAY_START_YEAR if dt.month >= 11 else DISPLAY_START_YEAR + 1
    return datetime(display_year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def elapsed_hours_in_water_year(display_dt: datetime) -> int:
    start = datetime(DISPLAY_START_YEAR, 11, 1, 0, 0, 0)
    return int((display_dt - start).total_seconds() // 3600)


def build_water_year_records(records: list[Record]) -> list[WaterYearRecord]:
    source_years = sorted({rec.source_dt.year for rec in records})
    min_year = min(source_years)
    max_year = max(source_years)

    water_records: list[WaterYearRecord] = []
    for rec in records:
        wy = water_year_of(rec.source_dt)
        # Keep only complete Nov-Oct windows inside the source period:
        # 1991-1992, 1992-1993, ..., 2019-2020 for a 1991-2020 source file.
        if wy < min_year or wy + 1 > max_year:
            continue

        water_records.append(
            WaterYearRecord(
                water_year=wy,
                display_dt=display_datetime_for_water_year(rec.source_dt),
                time_str=rec.time_str,
                numeric_text=rec.numeric_text,
                numeric_values=rec.numeric_values,
            )
        )

    if not water_records:
        raise ValueError("No complete November-to-October water years were found.")

    return water_records


def write_water_year_csvs(water_records: list[WaterYearRecord], output_dir: Path) -> list[int]:
    output_dir.mkdir(parents=True, exist_ok=True)

    grouped: dict[int, list[WaterYearRecord]] = defaultdict(list)
    for rec in water_records:
        grouped[rec.water_year].append(rec)

    start_years = sorted(grouped.keys())

    for start_year in start_years:
        rows = sorted(grouped[start_year], key=lambda r: r.display_dt)
        out_file = output_dir / f"{start_year}-{start_year + 1}.csv"

        with out_file.open("w", encoding=ENCODING, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(YEARLY_HEADER)

            for rec in rows:
                writer.writerow(
                    [
                        elapsed_hours_in_water_year(rec.display_dt),
                        rec.display_dt.strftime("%Y-%m-%d"),
                        rec.display_dt.strftime("%H:%M:%S"),
                        start_year,
                        *rec.numeric_text,
                    ]
                )

    return start_years


def write_average_csv(water_records: list[WaterYearRecord], out_file: Path) -> None:
    grouped: dict[tuple[int, int, int, int, int], list[list[float]]] = defaultdict(list)

    for rec in water_records:
        key = (
            rec.display_dt.month,
            rec.display_dt.day,
            rec.display_dt.hour,
            rec.display_dt.minute,
            rec.display_dt.second,
        )
        grouped[key].append(rec.numeric_values)

    sorted_keys = sorted(
        grouped.keys(),
        key=lambda k: datetime(
            DISPLAY_START_YEAR if k[0] >= 11 else DISPLAY_START_YEAR + 1,
            k[0],
            k[1],
            k[2],
            k[3],
            k[4],
        ),
    )

    with out_file.open("w", encoding=ENCODING, newline="") as f:
        writer = csv.writer(f)
        writer.writerow(AVERAGE_HEADER)

        for month, day, hour, minute, second in sorted_keys:
            display_year = DISPLAY_START_YEAR if month >= 11 else DISPLAY_START_YEAR + 1
            ref_dt = datetime(display_year, month, day, hour, minute, second)
            elapsed_hours = elapsed_hours_in_water_year(ref_dt)
            values_by_record = grouped[(month, day, hour, minute, second)]

            averaged = []
            for col_idx in range(len(NUMERIC_HEADERS)):
                col_values = [row[col_idx] for row in values_by_record]
                averaged.append(sum(col_values) / len(col_values))

            writer.writerow(
                [
                    elapsed_hours,
                    ref_dt.strftime("%Y-%m-%d"),
                    ref_dt.strftime("%H:%M:%S"),
                    *[format_float(v) for v in averaged],
                ]
            )


def main() -> None:
    records = read_records(INPUT_FILE)
    water_records = build_water_year_records(records)
    start_years = write_water_year_csvs(water_records, OUTPUT_DIR)
    write_average_csv(water_records, AVERAGE_FILE)

    print(f"Wrote {len(start_years)} water-year CSV files to {OUTPUT_DIR.resolve()}")
    print("Water years:", ", ".join(f"{y}-{y + 1}" for y in start_years))
    print(f"Wrote average CSV file: {AVERAGE_FILE.resolve()}")


if __name__ == "__main__":
    main()
