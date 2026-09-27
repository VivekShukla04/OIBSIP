#!/usr/bin/env python3
"""
download_data.py
================
Downloads the **UCI Online Retail** dataset used in this project and places it in `data/`.

Dataset : UCI Online Retail
Source  : https://archive.ics.uci.edu/dataset/352/online+retail
Archive : https://archive.ics.uci.edu/static/public/352/online+retail.zip
Citation: Chen, D. (2012). Data mining for the online retail industry.
          University of Southampton. UCI Machine Learning Repository.

What this script does
---------------------
1. Downloads `online+retail.zip` from the official UCI archive.
2. Extracts the original workbook `Online Retail.xlsx` into `data/`.
3. Also writes a **lossless CSV export** of that same worksheet as
   `data/online_retail.csv.gz` (a gzip-compressed CSV, ~7.6 MB instead of ~45 MB).
   A CSV export changes only the *file format* - no value, row or column is altered.
   The committed `.csv.gz` is produced by this script, which allows the notebook to run
   without a 45 MB binary file in Git.

Usage
-----
    python download_data.py

The notebook (`Customer_Segmentation.ipynb`) calls `main()` automatically if no data
file is found locally, so running this script manually is optional.
"""

from __future__ import annotations

import gzip
import io
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

DATASET_NAME = "UCI Online Retail"
ARCHIVE_URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
DATASET_PAGE = "https://archive.ics.uci.edu/dataset/352/online+retail"
ORIGINAL_WORKBOOK = "Online Retail.xlsx"
CSV_NAME = "online_retail.csv.gz"
TIMEOUT_SECONDS = 180


def project_dir() -> Path:
    """Return the folder that contains this script."""
    return Path(__file__).resolve().parent


def data_dir() -> Path:
    """Create and return the `data/` folder of the project."""
    folder = project_dir() / "data"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def download_archive(destination: Path) -> Path:
    """Download the UCI zip archive to `destination` and return its path."""
    if destination.exists() and destination.stat().st_size > 0:
        print(f"[skip]   Archive already present: {destination.name}")
        return destination

    print(f"[get]    Downloading {DATASET_NAME} from UCI ...")
    print(f"[url]    {ARCHIVE_URL}")
    with urllib.request.urlopen(ARCHIVE_URL, timeout=TIMEOUT_SECONDS) as response:
        payload = response.read()
    destination.write_bytes(payload)
    print(f"[ok]     Downloaded {len(payload) / 1_000_000:.1f} MB -> {destination.name}")
    return destination


def extract_workbook(archive: Path, target_dir: Path) -> Path:
    """Extract the original `Online Retail.xlsx` workbook into `target_dir`."""
    workbook = target_dir / ORIGINAL_WORKBOOK
    if workbook.exists():
        print(f"[skip]   Workbook already present: {workbook.name}")
        return workbook

    with zipfile.ZipFile(archive) as zf:
        if ORIGINAL_WORKBOOK not in zf.namelist():
            raise FileNotFoundError(
                f"'{ORIGINAL_WORKBOOK}' not found inside the archive. Members: {zf.namelist()}"
            )
        with zf.open(ORIGINAL_WORKBOOK) as source, workbook.open("wb") as target:
            shutil.copyfileobj(source, target)

    size_mb = workbook.stat().st_size / 1_000_000
    print(f"[ok]     Extracted {ORIGINAL_WORKBOOK} ({size_mb:.1f} MB)")
    return workbook


def export_csv_gz(workbook: Path, target_dir: Path) -> Path:
    """Write a gzip-compressed, lossless CSV export of the workbook's single sheet."""
    import pandas as pd

    csv_gz = target_dir / CSV_NAME
    print(f"[read]   Reading {workbook.name} with pandas (this takes ~1 minute) ...")
    frame = pd.read_excel(workbook, engine="openpyxl", sheet_name=0)

    buffer = io.BytesIO()
    frame.to_csv(buffer, index=False)
    with gzip.open(csv_gz, "wb", compresslevel=9) as target:
        target.write(buffer.getvalue())

    print(
        f"[ok]     Wrote {csv_gz.name}: {len(frame):,} rows x {frame.shape[1]} columns "
        f"({csv_gz.stat().st_size / 1_000_000:.1f} MB gzipped)"
    )
    return csv_gz


def main() -> Path:
    """Run the full download/extract/export pipeline and return the CSV path."""
    print("=" * 78)
    print(f"  {DATASET_NAME} - dataset downloader")
    print("=" * 78)

    target_dir = data_dir()
    archive = target_dir / "online_retail.zip"

    download_archive(archive)
    workbook = extract_workbook(archive, target_dir)
    csv_gz = export_csv_gz(workbook, target_dir)

    print("-" * 78)
    print(f"  Dataset page : {DATASET_PAGE}")
    print(f"  Archive      : {ARCHIVE_URL}")
    print(f"  CSV export   : {csv_gz}")
    print("  Done.")
    print("=" * 78)
    return csv_gz


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - CLI entry point, report clearly
        print(f"\nERROR: could not download the dataset.\n{type(exc).__name__}: {exc}\n", file=sys.stderr)
        print(
            "Manual alternative - download and place the file in data/:\n"
            f"  1. Open {DATASET_PAGE}\n"
            "  2. Download the data archive\n"
            "  3. Extract it and copy the file into the 'data' folder of this project\n"
            "  4. Re-run the notebook",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
