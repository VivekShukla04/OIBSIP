# Task 3 - Data Cleaning

**Oasis Infobyte | Data Analytics | Level 1**
Author: [Vivek Shukla](https://github.com/VivekShukla04) &nbsp;|&nbsp; Repository: [VivekShukla04/OIBSIP](https://github.com/VivekShukla04/OIBSIP)

---

## 1. Objective

Demonstrate professional data-cleaning skills by taking a **genuinely messy public dataset**,
auditing its quality systematically, and producing a **trustworthy, analysis-ready** version -
without ever destroying the original data.

1. Load the raw file exactly as stored and produce a **data-quality report** quantifying every
   problem.
2. Clean each problem with a **justified** strategy, never a blind fill.
3. Detect outliers with **two** methods and decide, per column, whether to **retain, cap or
   remove** - recording the reason.
4. Present a **before vs. after** quality summary.
5. Save `cleaned_data.csv` while **proving** the raw file is untouched.

## 2. Dataset Information

| Item | Value |
|---|---|
| Dataset | **Adult (Census Income)** |
| Source | UCI Machine Learning Repository, dataset ID 2 |
| Source URL | <https://archive.ics.uci.edu/dataset/2/adult> |
| Download archive | <https://archive.ics.uci.edu/static/public/2/adult.zip> |
| Local raw file | `data/adult.data` (unmodified, exactly as published by UCI) |
| Documentation | `data/adult.names` (official UCI variable description) |
| Citation | Becker, B. & Kohavi, R. (1996). *Adult*. UCI Machine Learning Repository. |
| Period | 1994 US Census / Current Population Survey |
| Raw rows / columns | 32,561 / 15 |
| Licence | CC BY 4.0 (UCI Machine Learning Repository) |

### Why this dataset

It is a genuinely messy, real-world, officially published dataset - not a toy file. It contains
every problem a cleaning project should demonstrate: a sentinel character used for missing
values, leading whitespace on every categorical value, exact duplicate rows, numbers stored as
text, a known top-coding artefact, a documented typo and a redundant feature - plus several
outliers that are *legitimate* and must not be deleted.

### Note on dates

This dataset contains **no date column**, so the "inconsistent date format" problem cannot occur
here and has **not** been simulated. The formatting standardisation that *does* apply to this
file is demonstrated on text: leading whitespace, inconsistent capitalisation conventions,
sentinel values and a documented typo.

## 3. Project Structure

```
DataAnalytics-L1-CleaningData/
├── Cleaning_Data.ipynb      # the cleaning (executed, all outputs embedded)
├── cleaned_data.csv         # the deliverable: 32,537 rows x 23 columns
├── README.md                # this file
├── requirements.txt         # pinned dependencies
├── data/
│   ├── adult.data           # raw, never modified (SHA-256 verified in the notebook)
│   └── adult.names          # official UCI variable documentation
└── outputs/                 # 5 PNG charts + 8 result CSVs
```

## 4. How to Run

```bash
cd DataAnalytics-L1-CleaningData
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter lab Cleaning_Data.ipynb
```

Running the notebook regenerates `cleaned_data.csv` and every file in `outputs/`. The raw dataset
is opened read-only; the notebook records its SHA-256 before any work and re-verifies it at the
end, asserting that the file is byte-for-byte unchanged.

## 5. Data Quality Report - Before

| Issue | Location | Count | Severity |
|---|---|---|---|
| `' ?'` used as the missing-value sentinel | workclass, occupation, native-country | **4,262 cells** (2,399 rows, 7.37%) | High |
| Leading space on every categorical value | all 9 categorical columns | **104 distinct labels** | High |
| 6 columns hold numbers but are stored as text | age, fnlwgt, education-num, capital-gain, capital-loss, hours-per-week | 6 of 15 | High |
| Exact duplicate rows | whole file | **24** | Medium |
| `capital-gain == 99999` (top-coded placeholder) | capital-gain | **159** | High |
| Misspelled category `Holand-Netherlands` | native-country | 1 | Medium |
| Redundant 1:1 pair `education` / `education-num` | both | 16 levels | Low |
| Age 17, below working age | age | 395 rows under 18 | Medium |
| Extreme work weeks (to 99 h) | hours-per-week | 341 rows >= 80 h | Medium |

`Postal Code`-style noise is absent here, and `sex` has exactly two clean values after trimming -
reported honestly rather than padded with invented mappings.

## 6. Cleaning Applied

1. **Sentinel to real missing value** - `^\s*\?\s*$` becomes a genuine `NaN` so missing values are
   countable and imputable instead of being a category that looks like text.
2. **Whitespace trimming and internal collapsing** on all 9 categorical columns.
3. **Mode imputation with a flag** for `workclass`, `occupation` and `native-country`:

   | Column | Missing | Strategy | Why |
   |---|---|---|---|
   | `workclass` | 1,836 (5.64%) | mode `Private` + flag | descriptive label, not a measurement; deleting 5.6% of rows over a job title is disproportionate |
   | `occupation` | 1,843 (5.66%) | mode `Prof-specialty` + flag | same reasoning |
   | `native-country` | 583 (1.79%) | mode `United-States` + flag | only 1.79% missing and the file is 89.59% United-States |
   | numeric columns | 0 | **no imputation** | nothing is missing; imputing would be inventing data |

   Mean/median were rejected because these columns are nominal and have no numeric scale;
   forward fill was rejected because row order in a survey extract carries no meaning; zero-fill
   was rejected because `0` is a *real* value in `capital-gain` and would be actively misleading.
4. **Duplicate removal** - 24 exact duplicates dropped. Every removed row had an identical twin
   that remains, so no information is lost.
5. **Typo correction** - `Holand-Netherlands` -> `Netherlands` (1 row), logged in
   `outputs/typo_corrections.csv`.
6. **Type correction** - the 6 numeric columns cast to `int64` via `pd.to_numeric(errors="coerce")`,
   so any unconvertible value would be reported rather than silently poisoning the column.
   Categorical columns are cast to `category`.

## 7. Outlier Decisions

Two methods were run so the weakness of each becomes visible.

| Column | IQR outliers | Z-score outliers | Decision | Reasoning |
|---|---|---|---|---|
| `age` | 142 (age 79+) | 120 | **Retained + flagged** | Real census respondents. Winsorising would destroy genuine information. Flagged `age_is_minor` (395) and `age_over_79` (120). |
| `hours-per-week` | **9,002 (27.67%)** | 440 | **Retained + flagged** | IQR flags over a quarter of the file, which proves the rule is inapplicable rather than that the data is wrong. 341 rows >= 80 h flagged `hours_extreme`. |
| `capital-gain` | 2,712 (all non-zero) | 215 | **Capped to 41,310 + flagged** | 99,999 is a known top-code placeholder meaning "at or above the recording ceiling". It is 2.4x the largest genuine gain and sits 13.4 sd out. |
| `capital-loss` | 1,519 (all non-zero) | 1,470 | **Retained** | Same zero-inflation; max 4,356 is plausible. |
| `fnlwgt` | 993 | 346 | **Retained** | A survey sampling weight, not a measurement. Extreme weights are by design; capping them would bias every statistic. |
| **Rows deleted for outliers** | - | - | **0** | Detection is a diagnostic, not a licence to delete. |

**Why IQR fails here:** `capital-gain` and `capital-loss` have Q1 = Q3 = 0, so the IQR is 0 and the
bounds collapse to `[0, 0]`, flagging *every* non-zero value. On `hours-per-week` the distribution
is heavily left-skewed, which IQR's symmetry assumption does not handle.

**Effect of the cap:** `capital-gain` mean 1,077.65 -> 791.65 (**-26.5%**), standard deviation
7,385.29 -> 3,819.67 (**-48.3%**), and the distribution becomes visible at all on a chart. 159 rows
of 32,537 (0.49%) changed.

## 8. Before vs. After

| Metric | Before | After |
|---|---|---|
| Row count | 32,561 | **32,537** (24 duplicates removed) |
| Column count | 15 | **23** (8 flag/derived columns added) |
| Missing cells | 4,262 | **0** |
| Duplicate rows | 24 | **0** |
| Padded text values (distinct) | 104 | **0** |
| `'?'` sentinel values | 4,262 | **0** |
| Numeric columns stored as text | 6 | **0** |
| Top-coded placeholders (99,999) | 159 | **0** |
| Documented typos | 1 | **0** |
| Rows deleted as outliers | 0 | **0** |

The cleaned dataset is **larger** than the raw one: 8 columns were added and none removed -
`workclass_was_missing`, `occupation_was_missing`, `native-country_was_missing`,
`capital_gain_topcoded`, `age_is_minor`, `age_over_79`, `hours_extreme` and the derived
`income_above_50k`. Cleaning here means adding information about the data's reliability, not
discarding inconvenient rows.

## 9. Deliverable

`cleaned_data.csv` - 32,537 rows x 23 columns, verified by reading it back from disk in the
notebook. The raw dataset is proven unchanged by a SHA-256 comparison taken before and after the
run.

## 10. Outputs

**Charts** (`outputs/`, 5 PNG): missing values before cleaning, numeric distributions, IQR vs.
Z-score disagreement, `capital-gain` before/after the cap, before/after quality metrics.

**Tables** (`outputs/`, 8 CSV): `suspicious_values_report.csv`, `numeric_range_report_before.csv`,
`imputation_log.csv`, `dtype_corrections.csv`, `typo_corrections.csv`, `outlier_detection.csv`,
`capital_gain_cap_comparison.csv`, `before_after_quality_summary.csv`.

## 11. Conclusions

1. **The mess is structural, not cosmetic.** All 15 columns arrive as text - 6 holding nothing but
   numbers - all 9 categorical columns carry a leading space, and 4,262 cells use `' ?'` as a
   missing-value sentinel. `' Male'` and `'Male'` are different strings, and `' ?'` becomes a 42nd
   country.
2. **Duplicates were safe to remove; outliers were not.** 24 exact duplicates went with zero
   information loss. **Zero** rows were deleted for being extreme - ages 79-90, 80-hour weeks and
   extreme survey weights are all real.
3. **Two outlier methods, two different answers, and both can be wrong.** IQR flags 9,002 rows
   (27.67%) of `hours-per-week` and all 2,712 non-zero `capital-gain` values; the Z-score puts 159
   rows 13.4 sd out. A statistical rule cannot decide what is an error - domain knowledge must.
4. **One genuine error was found and corrected.** The 99,999 top-code in `capital-gain`, capped to
   the largest genuine value, cut the column mean 26.5% and its standard deviation 48.3%.
5. **Every imputation is traceable.** Mode fill, never zero, and each one recorded in a
   `*_was_missing` flag column.
6. **The clean result is larger than the raw result**, not smaller.
7. **The raw dataset is byte-for-byte unchanged**, so the cleaning is fully repeatable and fully
   reversible.

## 12. Limitations

1. **No date column exists**, so date-format normalisation could not be demonstrated and was not
   faked.
2. **`fnlwgt` was deliberately left untouched.** A dataset cleaned for analysis must keep the
   survey weight or every statistic will be biased.
3. **`education` and `education-num` are perfectly collinear** (16 levels, verified 1:1). Both were
   kept for interpretability, but any model must use only one.
4. **The mode imputation is a guess** - the safest available for a nominal category, and auditable
   via the flag columns, but `workclass == 'Private'` is an assumption for 1,836 individuals.
5. **Capping assumes 99,999 is a ceiling.** Obtaining uncensored source data would be better; the
   flag column identifies the 159 affected rows for that purpose.
6. **Only `adult.data` was used** (32,561 rows), not `adult.test` (16,281 rows), which has a
   different structure.
7. **The 1994 data is over 30 years old** and reflects US labour-market conditions of that decade.
   The cleaning techniques transfer; the demographic conclusions do not.
