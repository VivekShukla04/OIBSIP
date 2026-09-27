# Task 1 - Exploratory Data Analysis on Retail Sales Data

**Oasis Infobyte | Data Analytics | Level 1**
Author: [Vivek Shukla](https://github.com/VivekShukla04) &nbsp;|&nbsp; Repository: [VivekShukla04/OIBSIP](https://github.com/VivekShukla04/OIBSIP)

---

## 1. Objective

Perform a thorough **Exploratory Data Analysis (EDA)** on a retail sales transaction dataset in
order to:

1. Understand the structure, quality and basic statistics of the data.
2. Understand how **revenue and profit behave over time**.
3. Understand **which products and categories** drive sales and which destroy value.
4. Understand **customer behaviour** (segments, markets, repeat purchasing).
5. Quantify relationships between numeric variables.
6. Convert the findings into **actionable, data-backed business recommendations**.

## 2. Dataset Information

| Item | Value |
|---|---|
| Dataset | Global Superstore Orders (public sample) |
| Source repository | `plotly/datasets` |
| Source URL | <https://raw.githubusercontent.com/plotly/datasets/master/global_super_store_orders.tsv> |
| Repository URL | <https://github.com/plotly/datasets> |
| File used | `data/global_super_store_orders.tsv` - the **public 1,000-line sample** |
| Format | Tab-separated values (`.tsv`) |
| Grain | One row = one **order line item** |
| Period covered | 01 Jan 2011 - 30 Dec 2014 |
| Rows / columns | 1,000 / 24 |

### Notes on the data (nothing is invented)

* This is a **real, published dataset**. No field has been created, simulated or estimated.
* The file stores numbers with the **European decimal comma** (`45,06`, `-3.701,89`), so `Sales`,
  `Discount`, `Profit` and `Shipping Cost` arrive as *text* and **must** be converted before any
  statistic or chart is correct. Skipping that step produces silently wrong results.
* The dataset contains **no `Age` and no `Gender` column**. Because fabricating demographic fields
  is not acceptable, the customer section uses the attributes that genuinely exist: `Segment`,
  `Market`, `Region`, `City`, `Country` and `Ship Mode`.

## 3. Project Structure

```
DataAnalytics-L1-EDARetailSales/
├── EDA_Retail_Sales.ipynb      # the analysis (executed, all outputs embedded)
├── README.md                   # this file
├── requirements.txt            # pinned dependencies
├── data/
│   └── global_super_store_orders.tsv
└── outputs/                    # 14 PNG charts + 11 summary CSVs
```

## 4. How to Run

```bash
cd DataAnalytics-L1-EDARetailSales
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter lab EDA_Retail_Sales.ipynb
```

The notebook resolves its own folder, so it runs from the project directory, the repository root,
or any subdirectory. Every chart and CSV is regenerated on execution.

## 5. Analysis Performed

| # | Section | Content |
|---|---|---|
| 1 | Setup and data loading | Portable path resolution, TSV load, first look |
| 2 | Dataset information | Source, shape, grain, and the decimal-comma problem |
| 3 | Data inspection | Shape, dtypes, head/tail, duplicates |
| 4 | Missing values | Per-column missing counts and chart |
| 5 | Variable types | Categorical vs. numeric inventory |
| 6 | Data cleaning | Decimal-comma conversion, date parsing, derived features |
| 7 | Descriptive statistics | mean / median / mode / std / min / max / skew |
| 8 | Distribution analysis | Sales, Profit, Discount, Quantity histograms |
| 9 | Yearly analysis | Revenue, profit, margin and volume by year |
| 10 | Monthly analysis | Monthly trend with 3-month moving average |
| 11 | Quarterly analysis | Quarterly revenue vs. margin |
| 12 | Customer segmentation | Consumer / Corporate / Home Office |
| 13 | Market analysis | Revenue, profit and margin by market |
| 14 | Repeat vs. one-time customers | Order frequency distribution and value per order |
| 15 | Product analysis - top 10 by quantity | Volume leaders |
| 16 | Product analysis - top 10 by revenue | Value leaders |
| 17 | Category analysis | Revenue, profit, margin, shares by category |
| 18 | Sub-category analysis | Every sub-category ranked by margin |
| 19 | Correlation analysis | Correlation heatmap of 7 numeric variables |
| 20 | Discount threshold analysis | Margin by discount band |
| 21 | Loss-making analysis | Which lines lose money and why |
| 22 | Key figures | Single consolidated figures table |
| 23 | Conclusions | 12 numbered findings |
| 24 | Recommendations | 8 prioritised, evidence-linked actions |
| 25 | Limitations | What this data cannot support |

## 6. Key Figures

Every figure below is produced by the notebook and written to `outputs/key_figures.csv`.

| Metric | Value |
|---|---|
| Order lines analysed | 1,000 |
| Distinct orders | 979 |
| Distinct customers | 654 |
| Distinct products | 827 |
| Period | 01 Jan 2011 - 30 Dec 2014 |
| Total revenue | 243,960.06 |
| Total profit | 28,009.23 |
| Overall margin | 11.48% |
| Loss-making lines | 255 (25.5%) worth -20,722.57 |
| Profit from the other 745 lines | +48,731.80 |
| Orders per customer | 1.50 |
| Repeat-customer rate | 35.0% |
| Lines discounted > 20% | 228 (22.8%) worth -19,036.19 |
| Correlation, Sales ~ Shipping Cost | +0.878 |
| Correlation, Discount ~ Profit | -0.332 |
| Exact duplicate rows | 0 |

## 7. Main Findings

1. **2014 is volume growth hiding a profitability collapse.** Order lines grew 176 -> 326 and
   revenue peaked at 72,872, yet margin fell from 16.14% to **8.01%** and profit per order line
   dropped **57.2%**. The mean discount was *flat* (14.97% -> 15.03%), so this is **not** a
   headline-discount problem - it is a margin inversion in big-ticket sub-categories (Appliances
   28.71% -> -8.62%, Chairs 23.25% -> -5.69%, Copiers 20.63% -> -3.94%) with average unit price
   falling 78.92 -> 66.09.

2. **There is a hard profitability cliff at 20% discount.** Margin is +25.37% at no discount and
   +10.18% at 11-20%, then turns negative: -15.85% at 21-30% and **-59.58% beyond 30%**. The
   21%+ bands are only 228 order lines but destroy 19,036 - **68% of net profit**.

3. **One quarter of order lines sell at a loss.** 255 lines destroy -20,722.57 against
   +48,731.80 from the rest. **81.2% of them are discounted past 20%** against a 22.8% base rate -
   a 3.6x over-representation. The problem is portfolio-wide: 28.0% of Technology lines, 26.8% of
   Furniture, 24.4% of Office Supplies.

4. **Volume and value sit in completely different places.** Office Supplies is 62.0% of order
   lines but 18.9% of profit (6.90% margin); Technology is 18.6% of lines but 42.6% of profit
   (14.72%). The volume-leading product (Stockwell Paper Clips, 22 units) is 73x cheaper per unit
   than the revenue-leading Motorola Smart Phone.

5. **Segment profitability is the opposite of segment size.** Consumer supplies 53.6% of order
   lines and 52.6% of revenue but has the **worst** margin (9.24%). Corporate has the **best**
   margin (14.46%) on 24.5% of revenue. Home Office earns the most per customer (436.68).
   Prioritising by order count would push effort towards the least profitable segment.

6. **The US is revenue-heavy and margin-poor, but improving.** 16.7% of revenue at a 1.40%
   margin, against 10.52% in EMEA and 35.52% in Canada; market revenue and market margin are
   negatively related (r = -0.50). US margin by year: -7.91%, 9.09%, 1.52%, **20.03%** (2014).

7. **Shipping cost is proportional; speed buys nothing.** Sales ~ Shipping Cost = +0.88, so
   shipping must be modelled as a share of order value. Delivery Days correlates -0.01 with Sales,
   0.00 with Profit and -0.01 with Discount. Unit Price (0.82) drives order value far more than
   Quantity (0.31).

8. **Retention is the largest untouched pool.** 65.0% of customers (425 of 654) never order
   again. A repeat customer generates 2.79x the total revenue of a one-time customer, but only
   1.12x per individual order - the gap is about frequency, not basket size.

## 8. Recommendations

All eight are tied to a measured number; see section 15 of the notebook.

1. **Enforce a 20% discount ceiling** and re-price the 31%+ band (recovers up to ~33% of profit).
2. **Exit or restructure Binders** (-2,089, -14.98%), which destroys 39% of the Office Supplies
   category's profit.
3. **Re-price US delivery economics** - worth ~3,710 on current US revenue, though the US is
   already self-correcting.
4. **Shift commercial effort from Office Supplies to Technology and Corporate.**
5. **Run a retention programme on the 425 one-time customers**, using the profitable 1-10%
   discount band.
6. **Model shipping as a percentage of order value** and stop paying for speed.
7. **Protect the low-discount assortment** (0% band: +25.37% margin; 1-10%: highest profit per
   line at +73.39).
8. **Review the big-ticket lines that inverted in 2014** - the discount cap will not fix a margin
   inversion on a full-price order.

## 9. Outputs

**Charts** (`outputs/`, 14 PNG): missing-values overview, distributions, revenue vs. profit by
year, monthly trend, quarterly revenue and margin, customer segments, market revenue and profit,
top 10 by quantity, top 10 by revenue, category revenue and margin, sub-category margin,
correlation heatmap, discount-threshold effect, loss-making analysis.

**Tables** (`outputs/`, 11 CSV): `key_figures.csv`, `yearly_summary.csv`, `monthly_summary.csv`,
`quarterly_summary.csv`, `customer_segment_summary.csv`, `market_summary.csv`,
`category_summary.csv`, `subcategory_margin.csv`, `top10_products_by_quantity.csv`,
`top10_products_by_revenue.csv`, `discount_band_analysis.csv`.

## 10. Limitations

* The file is the **public 1,000-line sample** of the Global Superstore dataset, so absolute
  currency totals are sample-level. The *patterns* are the point.
* No `Age` or `Gender` fields exist, so age-group and gender analysis is impossible from this
  source and has deliberately not been faked.
* The dataset does not state its currency unit, so figures are reported as "currency units".
* No acquisition cost, marketing-spend or inventory data, so recommendation impact cannot be
  converted into a guaranteed ROI.
* Correlation is not causation; the discount finding is a strong association with a plausible
  mechanism, but a causal claim would need an experiment.
* The market revenue/margin relationship (r = -0.50) rests on only 7 markets.
* The 2014 sub-category margin inversions rest on 19-37 order lines each, so they should be
  confirmed against the full dataset before being used to set pricing.
