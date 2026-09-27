# Oasis Infobyte Data Analytics - Level 1

**Internship:** Oasis Infobyte &nbsp;|&nbsp; **Track:** Data Analytics &nbsp;|&nbsp; **Level:** 1
**Author:** [Vivek Shukla](https://github.com/VivekShukla04)

Three complete, executed and self-documenting Jupyter notebooks. Every figure quoted in a
notebook or a README is produced by the code in that notebook - no number is typed in by hand,
and no field is fabricated to fill a gap in the source data.

| # | Project | Notebook | Status |
|---|---|---|---|
| 1 | EDA on Retail Sales | [`DataAnalytics-L1-EDARetailSales/`](DataAnalytics-L1-EDARetailSales/) | 87 cells, 0 errors, 14 charts, 11 CSVs |
| 2 | Customer Segmentation (RFM + K-Means) | [`DataAnalytics-L1-CustomerSegmentation/`](DataAnalytics-L1-CustomerSegmentation/) | 79 cells, 0 errors, 11 charts, 8 CSVs |
| 3 | Data Cleaning | [`DataAnalytics-L1-CleaningData/`](DataAnalytics-L1-CleaningData/) | 63 cells, 0 errors, 5 charts, 8 CSVs |

All three notebooks were executed top-to-bottom with **zero error outputs**, and every chart is
embedded in the committed notebook as well as written to `outputs/`.

## Quick Start

Each project is self-contained. Clone, then:

```bash
cd <project-folder>
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter lab <notebook>.ipynb
```

To reproduce everything from a clean checkout, the notebooks can also be re-executed headlessly:

```bash
python -m jupyter nbconvert --to notebook --execute --inplace <notebook>.ipynb
```

Verified with **Python 3.12**.

## Repository Structure

```
OIBSIP/
├── README.md
├── .gitignore
├── data/                                  # (reserved; each project keeps its own data/)
├── outputs/                               # (reserved; each project keeps its own outputs/)
├── DataAnalytics-L1-EDARetailSales/
│   ├── EDA_Retail_Sales.ipynb
│   ├── README.md
│   ├── requirements.txt
│   ├── data/global_super_store_orders.tsv
│   └── outputs/                          # 14 PNG + 11 CSV
├── DataAnalytics-L1-CustomerSegmentation/
│   ├── Customer_Segmentation.ipynb
│   ├── download_data.py
│   ├── README.md
│   ├── requirements.txt
│   ├── data/online_retail.csv.gz
│   └── outputs/                          # 11 PNG + 8 CSV
└── DataAnalytics-L1-CleaningData/
    ├── Cleaning_Data.ipynb
    ├── cleaned_data.csv                  # deliverable: 32,537 x 23
    ├── README.md
    ├── requirements.txt
    ├── data/adult.data, adult.names
    └── outputs/                          # 5 PNG + 8 CSV
```

## Datasets

All three are public, officially published datasets, committed alongside the analysis so the
work is reproducible offline.

| Project | Dataset | Source | Licence |
|---|---|---|---|
| 1 | Global Superstore Orders (1,000-line public sample) | [`plotly/datasets`](https://github.com/plotly/datasets) | Public sample data |
| 2 | Online Retail (UK giftware retailer) | [UCI, dataset 352](https://archive.ics.uci.edu/dataset/352/online+retail) | CC BY 4.0 |
| 3 | Adult / Census Income | [UCI, dataset 2](https://archive.ics.uci.edu/dataset/2/adult) | CC BY 4.0 |

### Citations

* **Global Superstore** - public sample distributed via the `plotly/datasets` repository.
* **Online Retail** - Chen, D. (2012). *Data mining for the online retail industry*.
  UCI Machine Learning Repository. <https://doi.org/10.24432/C5BW31>
* **Adult** - Becker, B. & Kohavi, R. (1996). *Adult*. UCI Machine Learning Repository.
  <https://doi.org/10.24432/C5X7KH>

## What each project demonstrates

### 1. EDA on Retail Sales
Converts 1,000 order lines covering 2011-2014 into 8 evidence-linked business recommendations.
The headline finding is a **profitability cliff at 20% discount**: margin is +25.37% at no
discount and +10.18% at 11-20%, then -15.85% at 21-30% and **-59.58% beyond 30%**. The 21%+ bands
are 22.8% of order lines but destroy **68% of net profit**.

It also corrects a natural but wrong reading of the data: 2014's margin collapse from 16.14% to
8.01% is **not** caused by deeper average discounting (the mean discount was flat at ~15%) but by
margin inversions in big-ticket sub-categories.

### 2. Customer Segmentation
Cleans 541,909 raw transactions down to 391,148 usable order lines across 4,333 customers, builds
RFM features, and applies K-Means to find **five segments** - from 321 Champions holding 51.41% of
revenue down to 1,177 Dormant customers holding 3.67%.

The project is explicit that `log1p` preprocessing, not the algorithm, produced the usable result:
on raw features K-Means produces a 4,309-vs-24 split, and after the transform the smallest cluster
at k=5 holds 321 customers. It also states plainly that **k=5 is a judgement call** (silhouette
peaks at k=2, and at k=4 among k>=3) rather than presenting it as a discovered optimum, and
validates the segments against an independent quintile RFM scoring.

### 3. Data Cleaning
Audits the UCI Adult dataset and turns a genuinely messy file into a trustworthy one: 4,262
missing cells to 0, 24 duplicates to 0, 6 text-encoded numeric columns to proper integers, 1 typo
corrected.

The core lesson is restraint. IQR and Z-score detection **disagree sharply** (IQR flags 27.67% of
`hours-per-week` and every non-zero `capital-gain`, because Q1 = Q3 = 0), so **zero rows are
deleted for being extreme**. Only the one genuine error is corrected - the 159 top-coded
`capital-gain` values of 99,999, capped to the largest genuine value, which cut the column mean
26.5% and standard deviation 48.3%. Everything else is retained and **flagged**, so the cleaned
dataset has 8 more columns than the raw one. The raw file's SHA-256 is recorded before the run and
re-verified at the end, proving it was never modified.

## Principles applied throughout

* **No fabricated data.** Where a field or a date column does not exist, the gap is documented
  rather than filled. Project 1 has no `Age`/`Gender`; Project 3 has no dates.
* **Every number is computed.** All figures in the notebooks and READMEs are emitted by the code
  and written to `outputs/*.csv`.
* **Corrections are reported, not hidden.** Capped values, imputed values and removed duplicates
  all produce log files and flag columns.
* **Extreme is not the same as wrong.** Statistical rules flag candidates; domain knowledge decides.
* **The raw data is never modified.** Project 3 proves this with a hash; Projects 1 and 2 clean
  in-memory copies and write new files.
* **Limitations are stated** in every project, including where a dataset cannot support a
  requested analysis.

## Requirements

Each project pins its own dependencies in `requirements.txt`; the versions below are the ones
every notebook was executed and verified against.

| Package | Version |
|---|---|
| Python | 3.12 |
| pandas | 3.0.6 |
| numpy | 2.5.3 |
| matplotlib | 3.11.2 |
| seaborn | 0.13.2 |
| scikit-learn | 1.9.1 |
| jupyter | 1.1.1 |
| ipykernel | 7.3.0 |
| openpyxl | 3.1.5 (Project 2, used by `download_data.py`) |

## Licence

The analysis code and notebooks in this repository are provided for educational and portfolio
purposes as part of the Oasis Infobyte Data Analytics internship. The datasets remain under their
original licences, listed in the table above and in each project's README.
