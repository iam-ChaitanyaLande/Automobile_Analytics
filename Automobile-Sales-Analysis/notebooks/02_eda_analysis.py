"""
===================================================================
NOTEBOOK 02: EXPLORATORY DATA ANALYSIS
===================================================================
Automobile Raw Material Impact Analysis
Author: Chaitanya Lande | Great Lakes PGDM (Analytics & Operations)
===================================================================

Core analyses:
1. Vertical-wise cost distribution & quality impact
2. Supplier grade impact on defect rates & production quality
3. Commodity price volatility vs production cost trends
4. Delay propagation: which verticals cause most downtime
5. Quality score decomposition by plant, shift, and vertical
6. Statistical hypothesis testing (ANOVA, Chi-Square, Correlation)
===================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats

sys.stdout.reconfigure(encoding='utf-8')

PROC_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\processed'
RAW_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\raw'
CHART_DIR = os.path.join(PROC_DIR, 'eda_charts')
os.makedirs(CHART_DIR, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

print("=" * 70)
print("  PHASE 3: EXPLORATORY DATA ANALYSIS")
print("  Automobile Raw Material Impact Analysis")
print("=" * 70)

# Load data
unified = pd.read_csv(os.path.join(PROC_DIR, 'unified_production_data.csv'), parse_dates=['production_date', 'production_month'])
cons_df = pd.read_csv(os.path.join(RAW_DIR, 'material_consumption.csv'), parse_dates=['production_month'])
mat_df = pd.read_csv(os.path.join(RAW_DIR, 'raw_materials_master.csv'))
commodity_df = pd.read_csv(os.path.join(RAW_DIR, 'commodity_prices.csv'), parse_dates=['month'])
supplier_df = pd.read_csv(os.path.join(RAW_DIR, 'supplier_performance.csv'), parse_dates=['month'])

print(f"Loaded unified dataset: {len(unified):,} batches x {unified.shape[1]} columns")

# =====================================================================
# ANALYSIS 1: VERTICAL-WISE COST, QUALITY & DELAY PROFILE
# =====================================================================
print("\n--- Analysis 1: Vertical-wise Cost, Quality & Delay Profile ---")

fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle("Manufacturing Vertical Impact Profile", fontsize=18, fontweight='bold', y=0.98)

# 1a. Total Cost Distribution by Vertical
vert_cost = cons_df.groupby('vertical')['total_cost'].sum().sort_values(ascending=False)
colors_v = ['#3182CE', '#38A169', '#D69E2E', '#E53E3E', '#805AD5', '#DD6B20']
axes[0, 0].barh(vert_cost.index, vert_cost.values / 1e6, color=colors_v, height=0.55)
for i, (v, c) in enumerate(zip(vert_cost.index, vert_cost.values)):
    axes[0, 0].text(c/1e6 + 0.5, i, f"{c/1e6:.1f}M", va='center', fontweight='bold', fontsize=10)
axes[0, 0].set_xlabel("Total Material Cost (INR Millions)", fontsize=11)
axes[0, 0].set_title("Total BOM Cost by Vertical", fontsize=13, fontweight='bold')

# 1b. Average Defect Rate by Vertical
vert_defect = cons_df.groupby('vertical')['defect_rate_pct'].mean().sort_values(ascending=False)
bars_d = axes[0, 1].bar(range(len(vert_defect)), vert_defect.values, color=colors_v, width=0.6)
axes[0, 1].set_xticks(range(len(vert_defect)))
axes[0, 1].set_xticklabels(vert_defect.index, rotation=25, ha='right', fontsize=9)
for bar in bars_d:
    axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f"{bar.get_height():.2f}%", ha='center', fontweight='bold', fontsize=9)
axes[0, 1].set_ylabel("Average Defect Rate (%)", fontsize=11)
axes[0, 1].set_title("Incoming Material Defect Rate by Vertical", fontsize=13, fontweight='bold')

# 1c. Delay Count by Vertical
vert_delay = cons_df.groupby('vertical')['delivery_delayed'].sum().sort_values(ascending=False)
delay_pct = (cons_df.groupby('vertical')['delivery_delayed'].mean() * 100)
axes[1, 0].barh(vert_delay.index, vert_delay.values, color=colors_v, height=0.55)
for i, (v, d) in enumerate(zip(vert_delay.index, vert_delay.values)):
    pct = delay_pct[v]
    axes[1, 0].text(d + 30, i, f"{d:,} ({pct:.1f}%)", va='center', fontweight='bold', fontsize=10)
axes[1, 0].set_xlabel("Total Delayed Deliveries", fontsize=11)
axes[1, 0].set_title("Supply Chain Delays by Vertical", fontsize=13, fontweight='bold')

# 1d. Inspection Pass Rate by Vertical
vert_pass = cons_df.groupby('vertical')['inspection_result'].apply(lambda x: (x == 'Pass').mean() * 100).sort_values()
bars_p = axes[1, 1].barh(vert_pass.index, vert_pass.values, color=['#E53E3E' if v < 85 else '#38A169' for v in vert_pass.values], height=0.55)
axes[1, 1].axvline(85, color='gray', linestyle=':', label='85% Target')
for bar in bars_p:
    axes[1, 1].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}%", va='center', fontweight='bold', fontsize=10)
axes[1, 1].set_xlabel("Inspection Pass Rate (%)", fontsize=11)
axes[1, 1].set_title("First-Pass Quality Rate by Vertical", fontsize=13, fontweight='bold')
axes[1, 1].legend()

plt.tight_layout()
path1 = os.path.join(CHART_DIR, '01_vertical_profile.png')
plt.savefig(path1, dpi=150, bbox_inches='tight')
plt.close()
print(f"[SAVED] {path1}")

# Print vertical summary
print("\nVertical Impact Summary:")
print(f"{'Vertical':<30} {'Cost Share':>10} {'Defect Rate':>12} {'Delay Rate':>12} {'Pass Rate':>10}")
print("-" * 75)
total_cost = cons_df['total_cost'].sum()
for v in vert_cost.index:
    v_data = cons_df[cons_df['vertical'] == v]
    cost_share = v_data['total_cost'].sum() / total_cost * 100
    defect = v_data['defect_rate_pct'].mean()
    delay = v_data['delivery_delayed'].mean() * 100
    pass_r = (v_data['inspection_result'] == 'Pass').mean() * 100
    print(f"  {v:<28} {cost_share:>8.1f}% {defect:>10.2f}% {delay:>10.1f}% {pass_r:>8.1f}%")

# =====================================================================
# ANALYSIS 2: SUPPLIER GRADE IMPACT
# =====================================================================
print("\n--- Analysis 2: Supplier Grade Impact on Quality & Delivery ---")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Supplier Grade Impact: Quality, Delivery & Cost", fontsize=16, fontweight='bold')

grade_colors = {'A': '#38A169', 'B': '#D69E2E', 'C': '#E53E3E'}

# 2a. Defect Rate by Supplier Grade
grade_defect = cons_df.groupby('supplier_grade')['defect_rate_pct'].mean()
for grade in ['A', 'B', 'C']:
    if grade in grade_defect.index:
        axes[0].bar(grade, grade_defect[grade], color=grade_colors[grade], width=0.5)
        axes[0].text(grade, grade_defect[grade] + 0.1, f"{grade_defect[grade]:.2f}%", ha='center', fontweight='bold', fontsize=12)
axes[0].set_title("Avg Defect Rate by Supplier Grade", fontsize=13, fontweight='bold')
axes[0].set_ylabel("Defect Rate (%)")

# 2b. On-Time Delivery Rate
grade_otd = supplier_df.groupby('supplier_grade')['on_time_delivery_rate'].mean() * 100
for grade in ['A', 'B', 'C']:
    if grade in grade_otd.index:
        axes[1].bar(grade, grade_otd[grade], color=grade_colors[grade], width=0.5)
        axes[1].text(grade, grade_otd[grade] + 0.5, f"{grade_otd[grade]:.1f}%", ha='center', fontweight='bold', fontsize=12)
axes[1].set_title("Avg On-Time Delivery Rate", fontsize=13, fontweight='bold')
axes[1].set_ylabel("OTD Rate (%)")
axes[1].axhline(90, color='red', linestyle='--', label='90% Target')
axes[1].legend()

# 2c. Quality Incidents
grade_incidents = supplier_df.groupby('supplier_grade')['quality_incidents'].mean()
for grade in ['A', 'B', 'C']:
    if grade in grade_incidents.index:
        axes[2].bar(grade, grade_incidents[grade], color=grade_colors[grade], width=0.5)
        axes[2].text(grade, grade_incidents[grade] + 0.05, f"{grade_incidents[grade]:.2f}", ha='center', fontweight='bold', fontsize=12)
axes[2].set_title("Avg Monthly Quality Incidents", fontsize=13, fontweight='bold')
axes[2].set_ylabel("Incidents per Month")

plt.tight_layout()
path2 = os.path.join(CHART_DIR, '02_supplier_grade_impact.png')
plt.savefig(path2, dpi=150, bbox_inches='tight')
plt.close()
print(f"[SAVED] {path2}")

# =====================================================================
# ANALYSIS 3: COMMODITY PRICE VOLATILITY VS PRODUCTION COSTS
# =====================================================================
print("\n--- Analysis 3: Commodity Volatility vs Production Cost Trends ---")

fig, axes = plt.subplots(2, 1, figsize=(18, 10))

monthly_cost = unified.groupby('production_month')['total_material_cost'].mean()
monthly_quality = unified.groupby('production_month')['quality_score'].mean()

# 3a. Steel Price vs Avg Material Cost
ax1 = axes[0]
months_str = commodity_df['month'].dt.strftime('%b %y')
ax1.plot(months_str, commodity_df['Steel_HRC_INR_per_ton'] / 1000, 'b-s', linewidth=2, label='Steel HRC (INR K/ton)')
ax1.plot(months_str, commodity_df['Semiconductor_Index'], 'r-o', linewidth=2, label='Semiconductor Index')
ax1.set_ylabel("Commodity Index Value", fontsize=11, color='#2C5282')
ax1.tick_params(axis='x', rotation=45)
ax1_twin = ax1.twinx()
ax1_twin.plot(months_str[:len(monthly_cost)], monthly_cost.values[:len(months_str)], 'g-^', linewidth=2.5, label='Avg Batch Material Cost (INR)')
ax1_twin.set_ylabel("Avg Material Cost per Batch (INR)", color='green', fontsize=11)
ax1_twin.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax1.set_title("Commodity Price Indices vs Average Production Material Cost (2022-2024)", fontsize=14, fontweight='bold')

# 3b. Steel Price vs Quality Score
ax2 = axes[1]
ax2.plot(months_str, commodity_df['Steel_HRC_INR_per_ton'] / 1000, 'b-s', linewidth=2, label='Steel HRC (INR K/ton)')
ax2_twin = ax2.twinx()
ax2_twin.plot(months_str[:len(monthly_quality)], monthly_quality.values[:len(months_str)], 'm-o', linewidth=2.5, label='Avg Quality Score')
ax2_twin.set_ylabel("Avg Quality Score (0-100)", color='purple', fontsize=11)
ax2.set_ylabel("Steel HRC (INR K/ton)", color='#2C5282', fontsize=11)
ax2.tick_params(axis='x', rotation=45)
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax2.set_title("Does Commodity Inflation Correlate with Quality Outcomes?", fontsize=14, fontweight='bold')

plt.tight_layout()
path3 = os.path.join(CHART_DIR, '03_commodity_vs_production.png')
plt.savefig(path3, dpi=150, bbox_inches='tight')
plt.close()
print(f"[SAVED] {path3}")

# =====================================================================
# ANALYSIS 4: DELAY PROPAGATION & DOWNTIME ANALYSIS
# =====================================================================
print("\n--- Analysis 4: Delay Propagation & Production Downtime ---")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 4a. Downtime vs Delay Count
axes[0].scatter(unified['total_delays'], unified['downtime_hours'], alpha=0.3, s=20, color='#E53E3E')
# Fit and plot trend
z = np.polyfit(unified['total_delays'], unified['downtime_hours'], 1)
p = np.poly1d(z)
x_trend = np.linspace(unified['total_delays'].min(), unified['total_delays'].max(), 50)
axes[0].plot(x_trend, p(x_trend), 'k--', linewidth=2, label=f'Trend: {z[0]:.2f}x + {z[1]:.2f}')
axes[0].set_xlabel("Number of Delayed Material Deliveries", fontsize=11)
axes[0].set_ylabel("Production Downtime (Hours)", fontsize=11)
axes[0].set_title("Material Delays Drive Production Downtime", fontsize=13, fontweight='bold')
axes[0].legend()

# Correlation
corr, pval = stats.pearsonr(unified['total_delays'], unified['downtime_hours'])
axes[0].text(0.05, 0.95, f"r = {corr:.3f}, p = {pval:.2e}", transform=axes[0].transAxes, fontsize=10, va='top', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 4b. Quality Score by Delay Risk Categories
unified['delay_risk_cat'] = pd.cut(unified['total_delays'], bins=[-1, 1, 3, 5, 100], labels=['Low (0-1)', 'Moderate (2-3)', 'High (4-5)', 'Critical (>5)'])
delay_quality = unified.groupby('delay_risk_cat', observed=True)['quality_score'].mean()
cat_colors = ['#38A169', '#D69E2E', '#DD6B20', '#E53E3E']
bars_dq = axes[1].bar(range(len(delay_quality)), delay_quality.values, color=cat_colors[:len(delay_quality)], width=0.55)
axes[1].set_xticks(range(len(delay_quality)))
axes[1].set_xticklabels(delay_quality.index, fontsize=10)
for bar in bars_dq:
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height():.1f}", ha='center', fontweight='bold', fontsize=11)
axes[1].set_ylabel("Avg Quality Score", fontsize=11)
axes[1].set_title("Quality Score Degrades with Material Delivery Delays", fontsize=13, fontweight='bold')

plt.tight_layout()
path4 = os.path.join(CHART_DIR, '04_delay_propagation.png')
plt.savefig(path4, dpi=150, bbox_inches='tight')
plt.close()
print(f"[SAVED] {path4}")

# =====================================================================
# ANALYSIS 5: PRODUCTION QUALITY BY PLANT, SHIFT, MODEL
# =====================================================================
print("\n--- Analysis 5: Quality Decomposition (Plant / Shift / Model) ---")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Production Quality Decomposition", fontsize=16, fontweight='bold')

# 5a. Quality by Plant
plant_q = unified.groupby('plant')['quality_score'].agg(['mean', 'std']).sort_values('mean', ascending=False)
axes[0].bar(plant_q.index, plant_q['mean'], yerr=plant_q['std'], color=['#3182CE', '#38A169', '#E53E3E'], width=0.5, capsize=5)
for i, (plant, row) in enumerate(plant_q.iterrows()):
    axes[0].text(i, row['mean'] + row['std'] + 0.5, f"{row['mean']:.1f}", ha='center', fontweight='bold')
axes[0].set_title("Quality Score by Plant", fontsize=13, fontweight='bold')
axes[0].set_ylabel("Avg Quality Score")

# 5b. Quality by Shift
shift_q = unified.groupby('shift')['quality_score'].agg(['mean', 'std']).sort_values('mean', ascending=False)
shift_colors = {'Morning': '#38A169', 'Afternoon': '#D69E2E', 'Night': '#E53E3E'}
axes[1].bar(shift_q.index, shift_q['mean'], yerr=shift_q['std'], color=[shift_colors.get(s, 'gray') for s in shift_q.index], width=0.5, capsize=5)
for i, (shift, row) in enumerate(shift_q.iterrows()):
    axes[1].text(i, row['mean'] + row['std'] + 0.5, f"{row['mean']:.1f}", ha='center', fontweight='bold')
axes[1].set_title("Quality Score by Shift", fontsize=13, fontweight='bold')
axes[1].set_ylabel("Avg Quality Score")

# 5c. Quality by Car Model
model_q = unified.groupby('car_model')['quality_score'].mean().sort_values(ascending=False)
axes[2].barh(model_q.index, model_q.values, color='#4A5568', height=0.55)
for i, (model, q) in enumerate(zip(model_q.index, model_q.values)):
    axes[2].text(q + 0.3, i, f"{q:.1f}", va='center', fontweight='bold', fontsize=10)
axes[2].set_title("Quality Score by Car Model", fontsize=13, fontweight='bold')
axes[2].set_xlabel("Avg Quality Score")

plt.tight_layout()
path5 = os.path.join(CHART_DIR, '05_quality_decomposition.png')
plt.savefig(path5, dpi=150, bbox_inches='tight')
plt.close()
print(f"[SAVED] {path5}")

# =====================================================================
# ANALYSIS 6: STATISTICAL HYPOTHESIS TESTING
# =====================================================================
print("\n--- Analysis 6: Statistical Hypothesis Testing ---")

# Test 1: ANOVA — Quality Score across Plants
print("\n[Test 1] One-Way ANOVA: Quality Score ~ Plant")
plant_groups = [g['quality_score'].values for _, g in unified.groupby('plant')]
f_stat, p_val = stats.f_oneway(*plant_groups)
print(f"  F-statistic = {f_stat:.4f}, p-value = {p_val:.2e}")
print(f"  Result: {'Significant' if p_val < 0.05 else 'Not Significant'} at alpha=0.05")

# Test 2: ANOVA — Quality Score across Shifts
print("\n[Test 2] One-Way ANOVA: Quality Score ~ Shift")
shift_groups = [g['quality_score'].values for _, g in unified.groupby('shift')]
f_stat, p_val = stats.f_oneway(*shift_groups)
print(f"  F-statistic = {f_stat:.4f}, p-value = {p_val:.2e}")
print(f"  Result: {'Significant' if p_val < 0.05 else 'Not Significant'} at alpha=0.05")

# Test 3: T-Test — Grade A vs Grade C supplier defect rates
print("\n[Test 3] Independent T-Test: Defect Rate (Grade A vs Grade C Suppliers)")
grade_a_defects = cons_df[cons_df['supplier_grade'] == 'A']['defect_rate_pct']
grade_c_defects = cons_df[cons_df['supplier_grade'] == 'C']['defect_rate_pct']
t_stat, p_val = stats.ttest_ind(grade_a_defects, grade_c_defects, equal_var=False)
print(f"  Grade A Mean Defect: {grade_a_defects.mean():.3f}% | Grade C Mean Defect: {grade_c_defects.mean():.3f}%")
print(f"  t-statistic = {t_stat:.4f}, p-value = {p_val:.2e}")
print(f"  Reduction: Grade A delivers {((grade_c_defects.mean() - grade_a_defects.mean()) / grade_c_defects.mean() * 100):.1f}% fewer defects")

# Test 4: Pearson Correlation — Delays vs Quality Score
print("\n[Test 4] Pearson Correlation: Total Delays vs Quality Score")
corr, p_val = stats.pearsonr(unified['total_delays'], unified['quality_score'])
print(f"  Correlation = {corr:.4f}, p-value = {p_val:.2e}")
print(f"  Result: {'Significant negative correlation' if corr < 0 and p_val < 0.05 else 'Weak or no correlation'}")

# Test 5: Chi-Square — Supplier Grade vs Inspection Result
print("\n[Test 5] Chi-Square: Supplier Grade vs Inspection Outcome")
ct = pd.crosstab(cons_df['supplier_grade'], cons_df['inspection_result'])
chi2, p_val, dof, expected = stats.chi2_contingency(ct)
print(f"  Chi-square = {chi2:.2f}, p-value = {p_val:.2e}, DoF = {dof}")
print(f"  Result: {'Significant association' if p_val < 0.05 else 'No significant association'}")

print("\n" + "=" * 70)
print("  PHASE 3 COMPLETE - EXPLORATORY DATA ANALYSIS")
print("=" * 70)
print(f"  5 analytical chart panels saved to {CHART_DIR}")
print(f"  5 statistical hypothesis tests completed")
