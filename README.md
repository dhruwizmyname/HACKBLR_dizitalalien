# Data Preparation Lab - April 15, 2026

## Overview
This lab focused on cleaning, normalizing, and establishing a robust versioning system for the CIP (Community Information Program) dataset. The primary goal was to ensure the data is "Run All" ready for downstream machine learning pipelines.

## Tasks Completed

### 1. Data Cleaning & Normalization
The raw `CIP_LATEST.csv` file contained several structural inconsistencies that would cause failures in data loaders (like Pandas or Spark). We performed the following surgical fixes:
*   **BOM Removal:** Removed the UTF-8 Byte Order Mark (`\xef\xbb\xbf`) from the header to prevent "Unknown Column" errors.
*   **Whitespace Trimming:** Stripped leading and trailing spaces from all fields and headers.
*   **Missing Value Imputation:** Identified empty fields (double commas `,,`) and replaced them with `0` to maintain a consistent numeric schema where applicable.
*   **Column Alignment:** Normalized the entire dataset to a strict **85-column** structure, resolving instances where trailing commas or missing end-of-line delimiters caused row length discrepancies.

### 2. Automated Versioning System
To prevent overwriting data and to track iterative runs, we implemented a Python-based versioning logic.

**Logic implemented:**
*   Generates filenames based on the current date: `Raw_Data_vYYYYMMDD_N.csv`.
*   Automatically detects existing versions for the current day and increments the version number (`N`) for the next save.
*   Provides a "latest version" detection snippet to ensure subsequent notebook cells always pull the most recent data run.

## Final Data State
*   **Files Created:** 
    *   `Raw_Data_v20260415_1.csv`
    *   `Raw_Data_v20260415_2.csv` (Latest)
*   **Shape:** 201 Rows, 85 Columns.
*   **Integrity:** Verified consistent column counts across all rows.

## Usage
To always load the latest version created today in your scripts, use the following pattern:
```python
import os, re
from datetime import datetime

today = datetime.now().strftime("%Y%m%d")
pattern = f"Raw_Data_v{today}"
files = [f for f in os.listdir('/content') if f.startswith(pattern)]
latest = sorted(files)[-1] # Loads the highest version number
```
