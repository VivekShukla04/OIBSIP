# Task 2 - Customer Segmentation Analysis

**Oasis Infobyte | Data Analytics | Level 1**
Author: [Vivek Shukla](https://github.com/VivekShukla04) &nbsp;|&nbsp; Repository: [VivekShukla04/OIBSIP](https://github.com/VivekShukla04/OIBSIP)

---

## 1. Objective

Perform **RFM (Recency, Frequency, Monetary)** analysis on a real transactional retail dataset
and apply **K-Means clustering** to discover customer segments, then validate and interpret them.

1. Clean a genuinely messy transactional dataset and document every decision.
2. Engineer RFM features per customer.
3. Choose *k* using the elbow method, silhouette analysis and cluster-balance checks.
4. Profile, name and size each segment.
5. Validate the clusters against an independent method (classical quintile RFM scoring).
6. Attach a concrete marketing action to each segment.

## 2. Dataset Information

| Item | Value |
|---|---|
| Dataset | Online Retail (UK giftware retailer) |
| Source | UCI Machine Learning Repository, dataset ID 352 |
| Source URL | <https://archive.ics.uci.edu/dataset/352/online+retail> |
| Local file | `data/online_retail.csv.gz` |
| Origin | `Online Retail.xlsx` from the UCI archive, exported to a **lossless** gzipped CSV |
| Raw rows | 541,909 |
| Period | Dec 2010 - Dec 2011 (snapshot 2011-12-10) |
| Licence | CC BY 4.0 (UCI Machine Learning Repository) |

> The committed file is a byte-faithful CSV export of the original workbook (all 541,909 rows and
> all original columns), gzip-compressed. No value was edited, rounded or dropped. It is
> committed rather than downloaded at run time so the analysis is reproducible offline and
> immune to upstream URL changes.

## 3. Project Structure

```
DataAnalytics-L1-CustomerSegmentation/
├── Customer_Segmentation.ipynb   # the analysis (executed, all outputs embedded)
├── download_data.py              # re-downloads the dataset from UCI and exports the CSV
├── README.md                     # this file
├── requirements.txt              # pinned dependencies
├── data/
│   └── online_retail.csv.gz
└── outputs/                      # 11 PNG charts + 8 result CSVs
```

## 4. How to Run

```bash
cd DataAnalytics-L1-CustomerSegmentation
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Optional: re-download the dataset from UCI (overwrites data/online_retail.csv.gz)
python download_data.py

jupyter lab Customer_Segmentation.ipynb
```

## 5. Data Cleaning

Six documented steps, each with a reason and a logged row count.

| # | Step | Rows removed | Share |
|---|---|---|---|
| 1 | Guest checkouts (`CustomerID` missing) | 135,080 | 24.93% |
| 2 | Cancellation / credit-note invoices (`InvoiceNo` starts with `C`) | 8,905 | 2.19% |
| 3 | Non-product lines (`UnitPrice <= 0`) | 40 | 0.01% |
| 4 | Administrative stock codes (`POST`, `BANK CHARGES`, `AMAZONFEE`, ...) | 1,547 | 0.39% |
| 5 | Exact duplicate rows | 5,187 | 1.31% |
| 6 | Impossible / extreme quantities (`<= 0`, `> 10,000`) | 2 | 0.00% |
| | **Total** | **150,761** | **27.8%** |

Result: **391,148** order lines, **18,400** invoices, **4,333** customers, **3,658** distinct
products, **8,491,574.44** total revenue.

**Why cancellations are removed rather than converted to negative sales:** a credit note is the
*reversal* of an earlier purchase. Keeping both would net to zero and destroy the real purchasing
history, while treating the credit note as a sale would understate customer value. For RFM-style
behavioural analysis the defensible choice is to model genuine purchases only.

## 6. Method

### 6.1 RFM features

* **Recency** - days since the customer's last purchase (snapshot 2011-12-10).
* **Frequency** - number of distinct invoices.
* **Monetary** - total spend.
* Plus **Avg Basket Value**, **Total Items**, **Distinct Products** and **Active Months** for
  profiling.

### 6.2 Preprocessing (the decisive step)

Frequency and Monetary are extremely right-skewed (skewness **11.95** and **20.92**); the top
customer has 206 invoices and 279,138.02 of spend, **142x** the base average of 1,959.74. Feeding
raw values into a distance-based algorithm makes K-Means split "the few giants" from everyone
else instead of finding segments. Both features are therefore transformed with `log1p` and then
`StandardScaler`-scaled, so a single Euclidean distance is meaningful.

The notebook demonstrates the failure mode rather than asserting it: on raw features K-Means
produces a 4,309-vs-24 split at k=2 and a smallest cluster of just **3** customers at k=5, versus
**321** after the transform.

### 6.3 Choosing k = 5

Stated honestly: **no single metric selects k = 5.**

* Silhouette peaks at **k = 2** (0.4331) and, among k >= 3, at **k = 4** (0.3382). Moving to k=5
  costs only 0.02 of separation quality.
* Inertia shows **diminishing returns rather than a sharp elbow**: 25.0% / 19.1% / 16.4% / 13.4% /
  10.7% reduction per added cluster for k=3..7. Supporting evidence, not proof.
* **Business usefulness decides it.** At k=4 the "recent loyal" and "lapsing high-value"
  populations merge, hiding the most recoverable revenue in the database.
* The smallest cluster at k=5 still holds **321** customers (7.4%), so nothing is degenerate.

## 7. Segments

| Cluster | Segment | Customers | Share of customers | Share of revenue | Recency (days) | Frequency | Monetary | Active months |
|---|---|---|---|---|---|---|---|---|
| 2 | **Champions** | 321 | 7.41% | **51.41%** | 11.33 | 21.22 | 13,600.93 | 9.75 |
| 4 | **Loyal Customers** | 975 | 22.50% | 25.22% | 19.46 | 5.86 | 2,196.35 | 4.66 |
| 1 | **At-Risk High-Value** | 1,028 | 23.72% | 15.95% | 106.96 | 3.03 | 1,317.34 | 2.66 |
| 5 | **Recent Occasional Buyers** | 832 | 19.20% | 3.75% | 26.95 | 1.63 | 382.92 | 1.52 |
| 3 | **Dormant Low-Value** | 1,177 | 27.16% | 3.67% | 209.57 | 1.19 | 264.58 | 1.15 |

A note on the name **At-Risk High-Value**: its 1,317.34 average spend is only **0.67x** the
overall customer average of 1,959.74, so "high-value" is *relative to the other lapsed
customers* - 5.0x the Dormant segment and 3.4x the Recent Occasional segment. It is the
best-paying population that is going quiet, which is what makes it the priority, but it should not
be read as a high-spend segment in absolute terms.

## 8. Validation

Cross-tabulating the K-Means labels against classical quintile RFM scores (an independent
method) gives strong agreement:

* **306 of 321** K-Means Champions are also quintile Champions.
* **1,023 of 1,177** K-Means Dormant customers are quintile Dormant, and **zero** fall in the top
  quintile.
* The only systematic disagreement is the Loyal group, split by the quintile rule across Champions
  (629), Loyal (335) and Recent (11) - a 20% forced-size rule cannot express "good on both
  dimensions".

Disagreement is expected: quintiles force every segment to hold exactly 20% of customers while
K-Means lets segment sizes differ.

## 9. Key Findings

1. **The cleaning stage matters most.** 27.8% of raw rows are unusable for customer analysis;
   135,080 are guest checkouts with no customer ID.
2. **Feature engineering, not the algorithm, decided the outcome.** `log1p` is the difference
   between a useless split and a usable segmentation.
3. **k = 5 is a judgement call**, documented as such in section 6.3 rather than presented as a
   discovered fact.
4. **Revenue is extremely concentrated.** 321 Champions (7.41% of customers) generate 51.41% of
   revenue; the 1,177 Dormant customers (27.16%, the largest group by headcount) generate 3.67%.
5. **The biggest opportunity is the At-Risk segment** - 15.95% of revenue gone quiet for a mean
   of 107 days, the one group where spend can be recovered rather than created.
6. **Frequency, not basket size, is the lever.** Champions are active in 9.75 of 12 months versus
   1.15-1.52 for the occasional and dormant groups.
7. **The segments survive an independent check** against quintile RFM scoring.

## 10. Recommended Actions

| Segment | Objective | Key actions |
|---|---|---|
| Champions | Protect and grow | Named account manager, early access, loyalty points over discounts, referral programme; alert if Recency exceeds 30 days |
| Loyal Customers | Convert to Champions | Cross-sell higher-margin categories, replenishment reminders, spend-threshold vouchers, loyalty programme invite |
| At-Risk High-Value | Win back before dormancy | Win-back campaign at 60-90 days of inactivity, personalised reactivation referencing real past purchases, modest incentive not blanket discount |
| Recent Occasional Buyers | Build frequency | Second-purchase incentive, onboarding series, cross-sell adjacent categories |
| Dormant Low-Value | Low-cost reactivation only | Broad low-cost email; do not spend high-value incentives or retention-manager time here |

## 11. Outputs

**Charts** (`outputs/`, 11 PNG): missing values, RFM distributions, effect of the log transform,
elbow and silhouette curves, cluster balance raw vs. log, three cluster scatter plots, cluster
size vs. revenue share, recency/frequency by cluster, K-Means vs. RFM validation heatmap.

**Tables** (`outputs/`, 8 CSV): `cleaning_log.csv`, `k_selection_metrics.csv`,
`cluster_profile.csv`, `cluster_profile_full.csv`, `cluster_centroids_log_space.csv`,
`customer_segments.csv`, `segment_summary.csv`, `kmeans_vs_rfm_crosstab.csv`.

## 12. Limitations

1. **The data is a 2010-2011 snapshot** of a UK giftware retailer, so results may not transfer to
   other sectors or to the current market.
2. **27.8% of the data could not be used.** The 135,080 guest checkouts are real revenue that is
   invisible here, so the true customer base is larger than 4,333.
3. **Only three features were clustered.** RFM says nothing about *what* is bought, the channel,
   or acquisition source. 89.19% of clean order lines ship to the United Kingdom, so geographic
   segmentation would add little.
4. **K-Means assumes spherical, similarly sized clusters.** The silhouette of 0.3167 confirms
   overlap; customers near a boundary genuinely belong to two segments.
5. **Five clusters is a modelling choice, not a discovered truth.** k=4, k=5 and k=6 are all
   defensible from the diagnostics.
6. **The extreme tail was transformed, not removed.** The log transform limits the influence of
   the wholesale customers but does not eliminate it, and they sit inside the Champions cluster.
7. **No causal or predictive claim is made.** A campaign targeting the At-Risk segment must be
   A/B tested.
8. **Recency is measured against a 2011-12-10 snapshot**, not today.
