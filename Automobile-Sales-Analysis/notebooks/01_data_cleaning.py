"""
===================================================================
NOTEBOOK 01: DATA CLEANING & FEATURE ENGINEERING
===================================================================
Automobile Raw Material Impact Analysis
Author: Chaitanya Lande | Great Lakes PGDM (Analytics & Operations)
===================================================================

Cleans, validates, and engineers features from the 5 raw datasets to
produce a unified analytical dataset suitable for ML modeling and
Tableau dashboarding. Core engineering focus:

1. Validate data types, handle missing/outlier values
2. Aggregate material consumption to batch-level vertical metrics
3. Merge commodity price data with temporal production records
4. Create production KPI features (vertical delay score, weighted
   quality index, cost volatility exposure, etc.)
===================================================================
"""

import os
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\raw'
PROC_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\processed'
os.makedirs(PROC_DIR, exist_ok=True)

print("=" * 70)
print("  PHASE 2: DATA CLEANING & FEATURE ENGINEERING")
print("  Automobile Raw Material Impact Analysis")
print("=" * 70)

# =====================================================================
# 1. LOAD ALL DATASETS
# =====================================================================
print("\n--- Step 1: Loading Raw Datasets ---")

mat_df = pd.read_csv(os.path.join(RAW_DIR, 'raw_materials_master.csv'))
batch_df = pd.read_csv(os.path.join(RAW_DIR, 'production_batches.csv'), parse_dates=['production_date', 'production_month'])
cons_df = pd.read_csv(os.path.join(RAW_DIR, 'material_consumption.csv'), parse_dates=['production_month'])
supplier_df = pd.read_csv(os.path.join(RAW_DIR, 'supplier_performance.csv'), parse_dates=['month'])
commodity_df = pd.read_csv(os.path.join(RAW_DIR, 'commodity_prices.csv'), parse_dates=['month'])

print(f"  Materials Master  : {len(mat_df):>7,} rows x {mat_df.shape[1]} cols")
print(f"  Production Batches: {len(batch_df):>7,} rows x {batch_df.shape[1]} cols")
print(f"  Consumption       : {len(cons_df):>7,} rows x {cons_df.shape[1]} cols")
print(f"  Supplier Perf     : {len(supplier_df):>7,} rows x {supplier_df.shape[1]} cols")
print(f"  Commodity Prices  : {len(commodity_df):>7,} rows x {commodity_df.shape[1]} cols")

# =====================================================================
# 2. DATA VALIDATION & CLEANING
# =====================================================================
print("\n--- Step 2: Data Validation & Cleaning ---")

# 2a. Check for missing values
for name, frame in [('Materials', mat_df), ('Batches', batch_df), ('Consumption', cons_df), ('Supplier', supplier_df)]:
    missing = frame.isnull().sum()
    missing_cols = missing[missing > 0]
    if len(missing_cols) > 0:
        print(f"  [{name}] Missing values found:")
        for col, cnt in missing_cols.items():
            print(f"    - {col}: {cnt} ({cnt/len(frame)*100:.1f}%)")
    else:
        print(f"  [{name}] No missing values found.")

# 2b. Validate ranges
print("\n  Validating value ranges...")
invalid_eff = (batch_df['production_efficiency'] < 0) | (batch_df['production_efficiency'] > 1)
print(f"  - Invalid efficiency values: {invalid_eff.sum()}")
batch_df.loc[invalid_eff, 'production_efficiency'] = batch_df['production_efficiency'].median()

invalid_quality = (batch_df['quality_score'] < 0) | (batch_df['quality_score'] > 100)
print(f"  - Invalid quality scores: {invalid_quality.sum()}")
batch_df.loc[invalid_quality, 'quality_score'] = batch_df['quality_score'].median()

negative_defect = cons_df['defect_rate_pct'] < 0
print(f"  - Negative defect rates: {negative_defect.sum()}")
cons_df.loc[negative_defect, 'defect_rate_pct'] = 0

# 2c. Standardize text fields
mat_df['vertical'] = mat_df['vertical'].str.strip()
mat_df['supplier_grade'] = mat_df['supplier_grade'].str.upper()
cons_df['inspection_result'] = cons_df['inspection_result'].str.strip().str.title()

print("  Text fields standardized.")

# =====================================================================
# 3. BATCH-LEVEL VERTICAL AGGREGATION
# =====================================================================
print("\n--- Step 3: Aggregating Consumption to Batch-Level Vertical Metrics ---")

# 3a. Per-batch, per-vertical aggregations
vertical_agg = cons_df.groupby(['batch_id', 'vertical']).agg(
    vertical_material_count=('material_id', 'nunique'),
    vertical_total_cost=('total_cost', 'sum'),
    vertical_avg_defect_rate=('defect_rate_pct', 'mean'),
    vertical_max_lead_variance=('lead_time_variance_days', 'max'),
    vertical_avg_lead_variance=('lead_time_variance_days', 'mean'),
    vertical_delay_count=('delivery_delayed', 'sum'),
    vertical_fail_count=('inspection_result', lambda x: (x == 'Fail').sum()),
    vertical_rework_count=('inspection_result', lambda x: (x == 'Rework').sum()),
    vertical_pass_rate=('inspection_result', lambda x: (x == 'Pass').mean() * 100)
).reset_index()

print(f"  Vertical-level aggregations: {len(vertical_agg):,} records")

# 3b. Pivot verticals into columns for each batch
# Key metrics per vertical: cost, defect rate, delay count, pass rate
pivoted_cost = vertical_agg.pivot_table(index='batch_id', columns='vertical', values='vertical_total_cost', fill_value=0)
pivoted_cost.columns = [f'cost_{v.lower().replace(" & ", "_").replace(" ", "_")}' for v in pivoted_cost.columns]

pivoted_defect = vertical_agg.pivot_table(index='batch_id', columns='vertical', values='vertical_avg_defect_rate', fill_value=0)
pivoted_defect.columns = [f'defect_{v.lower().replace(" & ", "_").replace(" ", "_")}' for v in pivoted_defect.columns]

pivoted_delay = vertical_agg.pivot_table(index='batch_id', columns='vertical', values='vertical_delay_count', fill_value=0)
pivoted_delay.columns = [f'delays_{v.lower().replace(" & ", "_").replace(" ", "_")}' for v in pivoted_delay.columns]

pivoted_pass = vertical_agg.pivot_table(index='batch_id', columns='vertical', values='vertical_pass_rate', fill_value=100)
pivoted_pass.columns = [f'passrate_{v.lower().replace(" & ", "_").replace(" ", "_")}' for v in pivoted_pass.columns]

print(f"  Pivoted features: {pivoted_cost.shape[1]} cost + {pivoted_defect.shape[1]} defect + {pivoted_delay.shape[1]} delay + {pivoted_pass.shape[1]} pass rate")

# 3c. Overall batch-level consumption aggregations
batch_cons_agg = cons_df.groupby('batch_id').agg(
    total_material_cost=('total_cost', 'sum'),
    total_materials_used=('material_id', 'nunique'),
    avg_defect_rate=('defect_rate_pct', 'mean'),
    max_defect_rate=('defect_rate_pct', 'max'),
    avg_lead_variance=('lead_time_variance_days', 'mean'),
    max_lead_variance=('lead_time_variance_days', 'max'),
    total_delays=('delivery_delayed', 'sum'),
    total_fails=('inspection_result', lambda x: (x == 'Fail').sum()),
    total_reworks=('inspection_result', lambda x: (x == 'Rework').sum()),
    overall_pass_rate=('inspection_result', lambda x: (x == 'Pass').mean() * 100),
    pct_grade_a_suppliers=('supplier_grade', lambda x: (x == 'A').mean() * 100),
    pct_grade_c_suppliers=('supplier_grade', lambda x: (x == 'C').mean() * 100),
    unique_suppliers=('supplier_name', 'nunique'),
    unique_verticals=('vertical', 'nunique')
).reset_index()

print(f"  Batch-level aggregations: {len(batch_cons_agg):,} batches x {batch_cons_agg.shape[1]-1} features")

# =====================================================================
# 4. MERGE INTO UNIFIED ANALYTICAL DATASET
# =====================================================================
print("\n--- Step 4: Merging into Unified Analytical Dataset ---")

# Start with batch data
unified = batch_df.copy()

# Merge batch-level consumption aggregations
unified = unified.merge(batch_cons_agg, on='batch_id', how='left')

# Merge pivoted vertical features
for pivot_df in [pivoted_cost, pivoted_defect, pivoted_delay, pivoted_pass]:
    unified = unified.merge(pivot_df, on='batch_id', how='left')

# Merge commodity prices (monthly)
unified = unified.merge(commodity_df, left_on='production_month', right_on='month', how='left', suffixes=('', '_commodity'))
if 'month' in unified.columns:
    unified.drop(columns=['month'], inplace=True)

print(f"  Unified dataset: {len(unified):,} rows x {unified.shape[1]} columns")

# =====================================================================
# 5. FEATURE ENGINEERING
# =====================================================================
print("\n--- Step 5: Engineering Production & Operations Features ---")

# 5a. Production Efficiency Metrics
unified['efficiency_gap'] = unified['planned_qty'] - unified['actual_qty']
unified['efficiency_loss_pct'] = (unified['efficiency_gap'] / unified['planned_qty']) * 100
unified['is_underperforming'] = (unified['production_efficiency'] < 0.85).astype(int)

# 5b. Quality Risk Features
unified['quality_grade'] = pd.cut(unified['quality_score'], bins=[0, 60, 75, 85, 100], labels=['Critical', 'Below_Target', 'Acceptable', 'Excellent'])
unified['high_defect_batch'] = (unified['avg_defect_rate'] > unified['avg_defect_rate'].quantile(0.75)).astype(int)
unified['fail_rework_ratio'] = (unified['total_fails'] + unified['total_reworks']) / unified['total_materials_used']

# 5c. Supply Chain Delay Risk
unified['any_critical_delay'] = (unified['max_lead_variance'] > 5).astype(int)
unified['delay_intensity'] = unified['total_delays'] / unified['total_materials_used']
unified['delay_risk_score'] = (unified['avg_lead_variance'] * 0.4 + unified['max_lead_variance'] * 0.3 + unified['delay_intensity'] * 100 * 0.3)

# 5d. Cost Structure Features
unified['material_cost_per_unit'] = unified['total_material_cost'] / unified['actual_qty']
unified['cost_efficiency_ratio'] = unified['total_material_cost'] / (unified['final_price_lakh'] * 100000 * unified['actual_qty'])

# 5e. Commodity Volatility Features (rolling std over prior 3 months)
for col in ['Steel_HRC_INR_per_ton', 'Semiconductor_Index', 'Rubber_INR_per_kg', 'Crude_Oil_USD_per_barrel']:
    if col in commodity_df.columns:
        vol_series = commodity_df.set_index('month')[col].rolling(3, min_periods=1).std()
        vol_map = vol_series.to_dict()
        unified[f'{col}_volatility'] = unified['production_month'].map(vol_map)

# 5f. Temporal Features
unified['production_quarter'] = unified['production_date'].dt.quarter
unified['production_year'] = unified['production_date'].dt.year
unified['production_dow'] = unified['production_date'].dt.dayofweek
unified['is_month_end_batch'] = (unified['production_date'].dt.day > 20).astype(int)

# 5g. Variant Tier
variant_tier_map = {}
for model, config in {
    'Nexon': ['Smart', 'Pure', 'Creative', 'Fearless'],
    'Harrier': ['Smart', 'Pure', 'Adventure', 'Accomplished'],
    'Safari': ['Smart', 'Pure', 'Adventure', 'Accomplished Plus'],
    'Altroz': ['XE', 'XM', 'XZ', 'XZ+'],
    'Punch': ['Pure', 'Adventure', 'Accomplished', 'Creative'],
    'Tiago': ['XE', 'XM', 'XT', 'XZ+'],
    'Curvv': ['Smart', 'Pure', 'Creative', 'Accomplished']
}.items():
    for i, v in enumerate(config):
        variant_tier_map[(model, v)] = ['Base', 'Mid', 'High', 'Top'][i]

unified['variant_tier'] = unified.apply(lambda r: variant_tier_map.get((r['car_model'], r['variant']), 'Mid'), axis=1)

# Fill any remaining NaN values from merges
numeric_cols = unified.select_dtypes(include=[np.number]).columns
unified[numeric_cols] = unified[numeric_cols].fillna(0)

feature_count = unified.shape[1] - batch_df.shape[1]
print(f"  Engineered {feature_count} new features")
print(f"  Final unified dataset: {len(unified):,} rows x {unified.shape[1]} columns")

# =====================================================================
# 6. SAVE OUTPUTS
# =====================================================================
print("\n--- Step 6: Saving Processed Data ---")

unified.to_csv(os.path.join(PROC_DIR, 'unified_production_data.csv'), index=False)
print(f"  [SAVED] unified_production_data.csv ({len(unified):,} rows x {unified.shape[1]} cols)")

vertical_agg.to_csv(os.path.join(PROC_DIR, 'vertical_aggregations.csv'), index=False)
print(f"  [SAVED] vertical_aggregations.csv ({len(vertical_agg):,} rows)")

# Save cleaning audit
audit = {
    'total_records_processed': len(cons_df),
    'batches_processed': len(unified),
    'features_engineered': feature_count,
    'invalid_efficiency_fixed': int(invalid_eff.sum()),
    'invalid_quality_fixed': int(invalid_quality.sum()),
    'negative_defects_fixed': int(negative_defect.sum()),
    'final_columns': unified.shape[1]
}
pd.DataFrame([audit]).to_csv(os.path.join(PROC_DIR, 'cleaning_audit_log.csv'), index=False)
print(f"  [SAVED] cleaning_audit_log.csv")

print("\n" + "=" * 70)
print("  PHASE 2 COMPLETE - DATA CLEANING & FEATURE ENGINEERING")
print("=" * 70)
print(f"  Unified dataset: {len(unified):,} rows x {unified.shape[1]} columns")
print(f"  Key engineered features:")
print(f"    - Vertical-level costs, defect rates, delays, pass rates (24 features)")
print(f"    - Quality grade bucketing & fail/rework ratios")
print(f"    - Delay risk score (composite weighted metric)")
print(f"    - Material cost per unit & cost efficiency ratio")
print(f"    - Commodity volatility features (rolling 3-month std)")
print(f"    - Variant tier classification (Base/Mid/High/Top)")
