#!/usr/bin/env python3
"""Split a River1D horizontally concatenated stations.csv file into one CSV per station.

Usage:
    python split_stations.py stations.csv
    python split_stations.py stations.csv --outdir split_stations
    python split_stations.py stations.csv --encoding cp1252

The script detects the station header row by cells that start with "x =".
Each detected station block is written as station-1.csv, station-2.csv, ...
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, List


def read_csv(path: Path, encoding: str) -> List[List[str]]:
    with path.open("r", newline="", encoding=encoding) as f:
        return list(csv.reader(f))


def find_station_header_row(rows: List[List[str]]) -> int:
    """Return the first row containing station blocks like 'x = ... km'."""
    for i, row in enumerate(rows):
        if any(cell.strip().lower().startswith("x =") for cell in row):
            return i
    raise ValueError("Could not find a station header row containing cells that start with 'x ='.")


def find_station_starts(header_row: List[str]) -> List[int]:
    starts = [i for i, cell in enumerate(header_row) if cell.strip().lower().startswith("x =")]
    if not starts:
        raise ValueError("No station blocks found in the detected header row.")
    return starts


def infer_block_width(starts: List[int], header_row: List[str]) -> int:
    """Infer the number of columns in one station block, excluding blank separators."""
    if len(starts) > 1:
        # Usually station blocks are separated by one empty column, so the block width
        # is the spacing between starts minus that separator.
        spacings = [b - a for a, b in zip(starts, starts[1:])]
        return min(spacings) - 1

    # Single-station fallback: take columns until trailing blank columns begin.
    start = starts[0]
    end = len(header_row)
    while end > start and header_row[end - 1].strip() == "":
        end -= 1
    return end - start


def pad_and_slice(row: List[str], start: int, width: int) -> List[str]:
    """Return row[start:start+width], padding short rows with blanks."""
    stop = start + width
    if len(row) < stop:
        row = row + [""] * (stop - len(row))
    return row[start:stop]


def split_stations(input_csv: Path, outdir: Path, encoding: str = "cp1252", keep_preamble: bool = True) -> int:
    rows = read_csv(input_csv, encoding=encoding)
    header_idx = find_station_header_row(rows)
    header = rows[header_idx]
    starts = find_station_starts(header)
    width = infer_block_width(starts, header)

    if width <= 0:
        raise ValueError(f"Invalid inferred station block width: {width}")

    outdir.mkdir(parents=True, exist_ok=True)

    preamble = rows[:header_idx] if keep_preamble else []
    station_rows = rows[header_idx:]

    for station_number, start_col in enumerate(starts, start=1):
        outpath = outdir / f"station-{station_number}.csv"
        with outpath.open("w", newline="", encoding=encoding) as f:
            writer = csv.writer(f)
            if keep_preamble:
                writer.writerows(preamble)
            for row in station_rows:
                writer.writerow(pad_and_slice(row, start_col, width))

    return len(starts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Split a horizontally concatenated River1D stations.csv file.")
    parser.add_argument("input_csv", type=Path, help="Path to the combined stations.csv file")
    parser.add_argument("--outdir", type=Path, default=Path("station_files"), help="Directory for station-#.csv outputs")
    parser.add_argument("--encoding", default="cp1252", help="Input/output encoding; River1D CSVs with ° often use cp1252")
    parser.add_argument("--no-preamble", action="store_true", help="Do not copy the metadata rows above the station header")
    args = parser.parse_args()

    n = split_stations(
        input_csv=args.input_csv,
        outdir=args.outdir,
        encoding=args.encoding,
        keep_preamble=not args.no_preamble,
    )
    print(f"Wrote {n} station files to: {args.outdir.resolve()}")


if __name__ == "__main__":
    main()
