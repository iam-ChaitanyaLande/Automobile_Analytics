# Tableau Dashboard Architecture & Technical Specification
## Project: Automobile Raw Material Impact Analysis — Company XYZ
**Author:** Chaitanya Lande | Operations & Analytics Specialist  
**Data Sources:** `data/processed/unified_production_data.csv`, `data/raw/material_consumption.csv`, `data/raw/commodity_prices.csv`

---

## Suite Architecture Overview
This document specifies the exact layout, metric calculations, and visualization hierarchy for the 3-dashboard Tableau manufacturing intelligence suite developed for Company XYZ.

```
                    ┌─────────────────────────────────────────────────────┐
                    │     COMPANY XYZ MANUFACTURING CONTROL TOWER         │
                    └─────────────────────────────────────────────────────┘
                                               │
             ┌─────────────────────────────────┼────────────────────────────────┐
             │                                 │                                │
             ▼                                 ▼                                ▼
┌─────────────────────────┐       ┌─────────────────────────┐      ┌─────────────────────────┐
│       DASHBOARD 1       │       │       DASHBOARD 2       │      │       DASHBOARD 3       │
│  Production & Quality   │       │  Raw Material Verticals │      │    Commodity Prices     │
│     Command Center      │       │  & Supplier Performance │      │  & Variant Offerings    │
└─────────────────────────┘       └─────────────────────────┘      └─────────────────────────┘
```

---

## Dashboard 1: Manufacturing Production & Quality Command Center
### Objective:
Provide plant directors, shift managers, and operations leaders with real-time visibility into production efficiency, output volume, downtime root causes, and batch quality ratings.

### Layout & Visualizations (1920 × 1080):
1. **Top Executive KPI Bar:**
   * **Total Batches Produced:** `COUNTD([Batch Id])` (5,000 Batches)
   * **Average Line Efficiency:** `AVG([Production Efficiency]) * 100` (86.4%)
   * **Fleet-Wide Quality Yield:** `AVG([Quality Score])` (82.7 / 100)
   * **Total Unplanned Downtime:** `SUM([Downtime Hours])` (Hours lost across plants)
   * **Total Defect Count:** `SUM([Defect Count])` Units
2. **Plant Quality vs Efficiency Matrix (Dual-Axis Clustered Bar):**
   * **X-Axis:** `[Plant]` (Pune, Sanand, Ranjangaon)
   * **Primary Bar:** `AVG([Quality Score])`
   * **Secondary Bar:** `AVG([Production Efficiency])`
3. **Monthly Production Volume & Downtime Hours (Dual-Axis Area/Line):**
   * **X-Axis:** `MONTH([Production Date])`
   * **Area:** `SUM([Actual Qty])`
   * **Line (Red):** `SUM([Downtime Hours])`
4. **Shift Quality Degradation Heatmap:**
   * **Rows:** `[Plant]`
   * **Columns:** `[Shift]` (Morning, Afternoon, Night)
   * **Color Gradient:** `AVG([Quality Score])` (Green = High Quality, Red = Quality Risk)

### Tableau Calculated Fields:
```tableau
// 1. Efficiency Status Flag
IF [Production Efficiency] >= 0.90 THEN "High Performance"
ELSEIF [Production Efficiency] >= 0.80 THEN "Standard Operating Band"
ELSE "Bottleneck / Sub-Optimal"
END

// 2. High Downtime Incident Flag
IF [Downtime Hours] > 2.5 THEN 1 ELSE 0 END

// 3. Batch Quality Band
IF [Quality Score] >= 85 THEN "Grade I: Superior"
ELSEIF [Quality Score] >= 75 THEN "Grade II: Acceptable"
ELSE "Grade III: Rework / Defect Risk"
END
```

---

## Dashboard 2: Raw Material Verticals & Supplier Performance
### Objective:
Diagnose supplier defect rates, lead time variances, and delivery delays across all 6 manufacturing verticals to guide procurement SLAs and dual-sourcing strategies.

### Layout & Visualizations:
1. **Vertical Cost & Quality Bubble Matrix:**
   * **X-Axis:** `SUM([Total Cost])` (BOM Expenditure)
   * **Y-Axis:** `AVG([Defect Rate Pct])`
   * **Bubble Size:** `SUM([Delivery Delayed])`
   * **Labels:** 6 Verticals (Powertrain, Electrical & Electronics, Body & Structural, Suspension, Interior, Tyres)
2. **Supplier Grade Quality Benchmarking (Tornado / Diverging Bar):**
   * **Dimension:** `[Supplier Grade]` (A, B, C)
   * **Metrics:** Average Defect Rate % vs On-Time Delivery Rate %
   * **Annotation:** Grade A suppliers reduce defects by 79% relative to Grade C.
3. **Lead Time Variance vs Inspection Pass Rate (Scatter Plot with Reference Lines):**
   * **X-Axis:** `[Lead Time Variance Days]`
   * **Y-Axis:** `% Pass Inspection`
   * **Detail:** `[Supplier Name]`
4. **Top 10 Risk Component Watchlist:**
   * Table displaying highest defect rate materials with associated supplier names and replacement lead times.

### Tableau Calculated Fields:
```tableau
// 1. Critical Delay Flag
IF [Lead Time Variance Days] > 5 THEN "Severe Delay (>5 Days)"
ELSEIF [Lead Time Variance Days] > 0 THEN "Minor Delay"
ELSE "On-Time / Early"
END

// 2. Supplier Quality Index (LOD Expression)
{ FIXED [Supplier Name] : AVG([Defect Rate Pct]) }

// 3. First-Pass Yield %
SUM(IIF([Inspection Result] = 'Pass', 1, 0)) / COUNT([Inspection Result]) * 100
```

---

## Dashboard 3: Commodity Price Volatility & Car Variant Offering Impact
### Objective:
Correlate external commodity price indices (Steel HRC, Semiconductor Index, Natural Rubber) with raw material procurement costs and evaluate their margin compression impact across vehicle models and variant tiers.

### Layout & Visualizations:
1. **Commodity Price Index vs Material Cost Inflation (Dual-Axis Multi-Line Chart):**
   * **X-Axis:** `MONTH([Month])`
   * **Left Axis:** Steel HRC (INR/ton) & Semiconductor Index
   * **Right Axis:** Average Batch Material Cost (INR)
2. **Vehicle Variant Tier Margin Compression Index (Grouped Bar Chart):**
   * **X-Axis:** `[Car Model]` (Nexon, Harrier, Safari, Altroz, Punch, Tiago, Curvv)
   * **Color:** `[Variant Tier]` (Base, Mid, High, Top)
   * **Measure:** Cost-to-Price Ratio (%)
3. **Bill of Materials (BOM) Breakdown by Vehicle Segment (Stacked 100% Bar):**
   * **Dimension:** `[Segment]` (Hatchback, Micro SUV, Compact SUV, Mid SUV, Full SUV)
   * **Breakdown:** 6 Verticals
   * **Insight:** Demonstrates that Full SUVs carry 42% Powertrain and 28% Electronics cost, while Hatchbacks carry higher relative Body & Structural cost sensitivity.

### Tableau Calculated Fields:
```tableau
// 1. Material Cost to Retail Price Ratio
([Total Material Cost]) / ([Final Price Lakh] * 100000)

// 2. High Inflation Era Flag
IF [Steel Hrc Inr Per Ton] > 60000 OR [Semiconductor Index] > 115 THEN "Inflation Spike"
ELSE "Stable Market Period"
END

// 3. Variant Premium Spread
[Final Price Lakh] - { FIXED [Car Model] : MIN([Final Price Lakh]) }
```
