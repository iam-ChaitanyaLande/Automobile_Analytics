"""
===================================================================
TABLEAU DASHBOARD MOCKUP RENDERER — COMPANY XYZ
===================================================================
Automobile Raw Material Impact Analysis
Author: Chaitanya Lande | Great Lakes PGDM (Analytics & Operations)
===================================================================

Renders high-resolution dashboard simulation screenshots for Company XYZ:
1. Production & Quality Command Center
2. Raw Material Verticals & Supplier Performance
3. Commodity Price Volatility & Car Variant Offering Impact
===================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as mticker

sys.stdout.reconfigure(encoding='utf-8')

PROC_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\processed'
RAW_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\raw'
SCREENSHOT_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\tableau\dashboard_screenshots'
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

unified = pd.read_csv(os.path.join(PROC_DIR, 'unified_production_data.csv'), parse_dates=['production_date', 'production_month'])
cons_df = pd.read_csv(os.path.join(RAW_DIR, 'material_consumption.csv'), parse_dates=['production_month'])
commodity_df = pd.read_csv(os.path.join(RAW_DIR, 'commodity_prices.csv'), parse_dates=['month'])
supplier_df = pd.read_csv(os.path.join(RAW_DIR, 'supplier_performance.csv'), parse_dates=['month'])

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

# =====================================================================
# DASHBOARD 1: PRODUCTION & QUALITY COMMAND CENTER
# =====================================================================
print("Rendering Dashboard 1: Production & Quality Command Center...")
fig = plt.figure(figsize=(20, 11), facecolor='#F8F9FA')

fig.text(0.04, 0.955, "MANUFACTURING PRODUCTION & QUALITY COMMAND CENTER | COMPANY XYZ", 
         fontsize=18, fontweight='bold', color='#1A202C')
fig.text(0.04, 0.932, "Plant-Level Line Efficiency, Unplanned Downtime, and Batch Quality Yield Monitoring (5,000 Batches)", 
         fontsize=11, color='#718096')

# KPI Cards Strip
kpi_cards = [
    ("TOTAL BATCHES", f"{len(unified):,} Batches", "Audited Records", "#2B6CB0"),
    ("AVG LINE EFFICIENCY", f"{unified['production_efficiency'].mean()*100:.1f}%", "Target: 88.0%", "#2F855A"),
    ("FLEET QUALITY SCORE", f"{unified['quality_score'].mean():.1f} / 100", "Acceptance Band", "#3182CE"),
    ("TOTAL DOWNTIME", f"{unified['downtime_hours'].sum():,.0f} Hours", "Unplanned Stoppages", "#C53030"),
    ("FIRST-PASS YIELD", f"{unified['overall_pass_rate'].mean():.1f}%", "Line-Side Acceptance", "#805AD5")
]

card_xs = [0.04, 0.23, 0.42, 0.61, 0.80]
for (title, val, sub, col), x in zip(kpi_cards, card_xs):
    rect = patches.FancyBboxPatch((x, 0.82), 0.165, 0.085, boxstyle="round,pad=0.01", 
                                  transform=fig.transFigure, facecolor='white', 
                                  edgecolor='#E2E8F0', linewidth=1.5)
    fig.patches.append(rect)
    fig.text(x + 0.012, 0.88, title, fontsize=9, fontweight='bold', color='#A0AEC0', transform=fig.transFigure)
    fig.text(x + 0.012, 0.842, val, fontsize=17, fontweight='bold', color=col, transform=fig.transFigure)
    fig.text(x + 0.012, 0.825, sub, fontsize=8.5, color='#718096', transform=fig.transFigure)

gs1 = fig.add_gridspec(2, 2, top=0.79, bottom=0.06, left=0.04, right=0.96, hspace=0.32, wspace=0.22)

# Chart 1.1: Quality vs Efficiency by Plant
ax1_1 = fig.add_subplot(gs1[0, 0])
plant_stats = unified.groupby('plant').agg({'quality_score': 'mean', 'production_efficiency': lambda x: x.mean()*100})
x_p = np.arange(len(plant_stats))
w = 0.35
ax1_1.bar(x_p - w/2, plant_stats['quality_score'], width=w, color='#3182CE', label='Quality Score (0-100)')
ax1_1.bar(x_p + w/2, plant_stats['production_efficiency'], width=w, color='#48BB78', label='Line Efficiency (%)')
ax1_1.set_xticks(x_p)
ax1_1.set_xticklabels(plant_stats.index, fontsize=10.5, fontweight='bold')
ax1_1.set_title("Plant Performance Benchmarking: Quality Score vs Efficiency", fontsize=12.5, fontweight='bold')
ax1_1.set_ylim(60, 95)
ax1_1.legend(loc='lower right')

# Chart 1.2: Shift Quality Heatmap
ax1_2 = fig.add_subplot(gs1[0, 1])
shift_plant_q = unified.pivot_table(index='plant', columns='shift', values='quality_score', aggfunc='mean')
im = ax1_2.imshow(shift_plant_q.values, cmap='YlGn', aspect='auto', vmin=75, vmax=88)
ax1_2.set_xticks(range(len(shift_plant_q.columns)))
ax1_2.set_xticklabels(shift_plant_q.columns, fontsize=10.5, fontweight='bold')
ax1_2.set_yticks(range(len(shift_plant_q.index)))
ax1_2.set_yticklabels(shift_plant_q.index, fontsize=10.5, fontweight='bold')
for i in range(len(shift_plant_q.index)):
    for j in range(len(shift_plant_q.columns)):
        ax1_2.text(j, i, f"{shift_plant_q.values[i, j]:.1f}", ha='center', va='center', fontweight='bold', fontsize=12)
ax1_2.set_title("Quality Score Heatmap by Plant & Shift (Night Shift Dip Confirmed)", fontsize=12.5, fontweight='bold')
fig.colorbar(im, ax=ax1_2, shrink=0.7, label='Quality Score')

# Chart 1.3: Monthly Production Volume & Downtime
ax1_3 = fig.add_subplot(gs1[1, 0])
monthly_b = unified.groupby(pd.Grouper(key='production_date', freq='ME')).agg({'actual_qty': 'sum', 'downtime_hours': 'sum'})
m_dates = monthly_b.index.strftime('%b %y')
ax1_3.bar(m_dates, monthly_b['actual_qty'], color='#CBD5E0', width=0.6, label='Produced Units')
ax1_3.set_ylabel("Total Units Produced", color='#4A5568', fontsize=10)
ax1_3.tick_params(axis='x', rotation=45)
ax1_3_twin = ax1_3.twinx()
ax1_3_twin.plot(m_dates, monthly_b['downtime_hours'], color='#E53E3E', linewidth=2.5, marker='o', label='Downtime Hours')
ax1_3_twin.set_ylabel("Downtime (Hours)", color='#C53030', fontsize=10)
ax1_3.set_title("Monthly Output Volume vs Assembly Downtime Hours", fontsize=12.5, fontweight='bold')

# Chart 1.4: Defect Count Distribution by Vehicle Model
ax1_4 = fig.add_subplot(gs1[1, 1])
model_def = unified.groupby('car_model')['defect_count'].mean().sort_values(ascending=False)
bars_md = ax1_4.barh(model_def.index, model_def.values, color='#DD6B20', height=0.55)
for bar in bars_md:
    ax1_4.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.2f} / batch", va='center', fontweight='bold', fontsize=9.5)
ax1_4.set_title("Average Defect Count per Batch by Vehicle Model", fontsize=12.5, fontweight='bold')
ax1_4.set_xlabel("Average Defects per Batch")

path1 = os.path.join(SCREENSHOT_DIR, '01_production_quality_command_center.png')
plt.savefig(path1, dpi=160, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print(f"[SAVED] {path1}")


# =====================================================================
# DASHBOARD 2: RAW MATERIAL VERTICALS & SUPPLIER PERFORMANCE
# =====================================================================
print("\nRendering Dashboard 2: Raw Material Verticals & Supplier Performance...")
fig2 = plt.figure(figsize=(20, 11), facecolor='#F8F9FA')

fig2.text(0.04, 0.955, "RAW MATERIAL VERTICALS & SUPPLIER RISK MATRIX | SOURCING CONTROL TOWER", 
          fontsize=18, fontweight='bold', color='#1A202C')
fig2.text(0.04, 0.932, "Incoming Component Defect Rates, Delivery Delays, and Tier-A/B/C Supplier Benchmarks", 
          fontsize=11, color='#718096')

gs2 = fig2.add_gridspec(2, 2, top=0.90, bottom=0.07, left=0.04, right=0.96, hspace=0.30, wspace=0.20)

# Chart 2.1: Vertical Cost Share vs Defect Rate
ax2_1 = fig2.add_subplot(gs2[0, 0])
v_metrics = cons_df.groupby('vertical').agg({'total_cost': 'sum', 'defect_rate_pct': 'mean', 'delivery_delayed': 'sum'})
v_cost_pct = v_metrics['total_cost'] / v_metrics['total_cost'].sum() * 100
colors_v = ['#3182CE', '#38A169', '#D69E2E', '#E53E3E', '#805AD5', '#DD6B20']
bars_v = ax2_1.barh(v_metrics.index, v_cost_pct, color=colors_v, height=0.55)
for bar, d in zip(bars_v, v_metrics['defect_rate_pct']):
    ax2_1.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}% (Defect: {d:.2f}%)", va='center', fontweight='bold', fontsize=9.5)
ax2_1.set_title("BOM Cost Share by Vertical (with Defect Rate Benchmark)", fontsize=13, fontweight='bold')
ax2_1.set_xlabel("% of Total Material Cost")

# Chart 2.2: Supplier Grade Defect Comparison
ax2_2 = fig2.add_subplot(gs2[0, 1])
grade_d = cons_df.groupby('supplier_grade')['defect_rate_pct'].mean()
colors_g = {'A': '#38A169', 'B': '#D69E2E', 'C': '#E53E3E'}
bars_g = ax2_2.bar(grade_d.index, grade_d.values, color=[colors_g[g] for g in grade_d.index], width=0.5)
for bar in bars_g:
    ax2_2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f"{bar.get_height():.2f}%", ha='center', fontweight='bold', fontsize=12)
ax2_2.set_title("Supplier Grade Defect Rate Disparity (Grade A: -79% Defects)", fontsize=13, fontweight='bold')
ax2_2.set_ylabel("Average Defect Rate (%)")

# Chart 2.3: Delay Count by Vertical
ax2_3 = fig2.add_subplot(gs2[1, 0])
delays_v = cons_df.groupby('vertical')['delivery_delayed'].sum().sort_values(ascending=False)
ax2_3.bar(delays_v.index, delays_v.values, color='#4A5568', width=0.55)
ax2_3.tick_params(axis='x', rotation=25)
for i, v in enumerate(delays_v.values):
    ax2_3.text(i, v + 40, f"{v:,}", ha='center', fontweight='bold', fontsize=9.5)
ax2_3.set_title("Delayed Material Shipments Count by Vertical", fontsize=13, fontweight='bold')
ax2_3.set_ylabel("Number of Delayed Deliveries")

# Chart 2.4: Inspection Pass Rate vs Lead Time Variance
ax2_4 = fig2.add_subplot(gs2[1, 1])
lead_pass = cons_df.groupby(pd.cut(cons_df['lead_time_variance_days'], bins=[-10, 0, 3, 6, 20], labels=['Early/On-Time', '1-3 Days Delay', '4-6 Days Delay', '>6 Days Delay']))['inspection_result'].apply(lambda x: (x == 'Pass').mean() * 100)
bars_lp = ax2_4.bar(lead_pass.index, lead_pass.values, color=['#38A169', '#48BB78', '#ED8936', '#E53E3E'], width=0.55)
for bar in bars_lp:
    ax2_4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f"{bar.get_height():.1f}%", ha='center', fontweight='bold', fontsize=10.5)
ax2_4.set_title("Delivery Lead Time Variance vs First-Pass Quality Rate", fontsize=13, fontweight='bold')
ax2_4.set_ylabel("% Pass Inspection")
ax2_4.set_ylim(60, 100)

path2 = os.path.join(SCREENSHOT_DIR, '02_material_verticals_supplier_matrix.png')
plt.savefig(path2, dpi=160, facecolor=fig2.get_facecolor(), bbox_inches='tight')
plt.close()
print(f"[SAVED] {path2}")


# =====================================================================
# DASHBOARD 3: COMMODITY PRICE VOLATILITY & VARIANT OFFERINGS
# =====================================================================
print("\nRendering Dashboard 3: Commodity Price Volatility & Car Variant Offering Impact...")
fig3 = plt.figure(figsize=(20, 11), facecolor='#F8F9FA')

fig3.text(0.04, 0.955, "COMMODITY PRICE VOLATILITY & CAR VARIANT OFFERINGS | ECONOMIC IMPACT", 
          fontsize=18, fontweight='bold', color='#1A202C')
fig3.text(0.04, 0.932, "Raw Material Price Transmissions (Steel HRC, Semiconductors) and Variant Margin Elasticity", 
          fontsize=11, color='#718096')

gs3 = fig3.add_gridspec(2, 2, top=0.90, bottom=0.07, left=0.04, right=0.96, hspace=0.30, wspace=0.20)

# Chart 3.1: Steel & Semiconductor vs Material Cost
ax3_1 = fig3.add_subplot(gs3[0, :])
m_str = commodity_df['month'].dt.strftime('%b %y')
ax3_1.plot(m_str, commodity_df['Steel_HRC_INR_per_ton'] / 1000, color='#3182CE', linewidth=2.5, marker='s', label='Steel HRC (INR K/ton)')
ax3_1.plot(m_str, commodity_df['Semiconductor_Index'], color='#D69E2E', linewidth=2, linestyle='--', label='Semiconductor Cost Index')
ax3_1.set_ylabel("Commodity Benchmark", color='#2C5282', fontsize=11, fontweight='bold')
ax3_1.tick_params(axis='x', rotation=45)

ax3_1_twin = ax3_1.twinx()
monthly_mcost = unified.groupby(pd.Grouper(key='production_date', freq='ME'))['total_material_cost'].mean()
ax3_1_twin.plot(m_str[:len(monthly_mcost)], monthly_mcost.values[:len(m_str)], color='#E53E3E', linewidth=3, marker='o', label='Avg Batch Material Cost (INR)')
ax3_1_twin.set_ylabel("Avg Material Cost per Batch (INR)", color='#9B2C2C', fontsize=11, fontweight='bold')
ax3_1_twin.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))

l1, lb1 = ax3_1.get_legend_handles_labels()
l2, lb2 = ax3_1_twin.get_legend_handles_labels()
ax3_1.legend(l1 + l2, lb1 + lb2, loc='upper left', frameon=True)
ax3_1.set_title("Commodity Price Swings vs Actual Material Procurement Expenditure", fontsize=13, fontweight='bold')

# Chart 3.2: Variant Tier Cost-to-Price Ratio
ax3_2 = fig3.add_subplot(gs3[1, 0])
tier_cost_ratio = unified.groupby('variant_tier')['cost_efficiency_ratio'].mean() * 100
colors_tier = ['#E53E3E', '#ED8936', '#4299E1', '#38A169']
bars_t = ax3_2.bar(tier_cost_ratio.index, tier_cost_ratio.values, color=colors_tier, width=0.55)
for bar in bars_t:
    ax3_2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height():.1f}%", ha='center', fontweight='bold', fontsize=10.5)
ax3_2.set_title("BOM Cost as % of Vehicle Selling Price by Variant Tier", fontsize=13, fontweight='bold')
ax3_2.set_ylabel("BOM Cost / Selling Price (%)")
ax3_2.set_xlabel("Variant Tier")

# Chart 3.3: Car Model Price vs Quality Scatter
ax3_3 = fig3.add_subplot(gs3[1, 1])
model_stats = unified.groupby('car_model').agg({'final_price_lakh': 'mean', 'quality_score': 'mean', 'planned_qty': 'sum'})
scatter = ax3_3.scatter(model_stats['final_price_lakh'], model_stats['quality_score'], 
                        s=model_stats['planned_qty']/50, c=model_stats['final_price_lakh'], 
                        cmap='Blues', alpha=0.9, edgecolors='black', linewidth=1.5)
for model, row in model_stats.iterrows():
    ax3_3.annotate(model, (row['final_price_lakh'] + 0.25, row['quality_score'] - 0.2), fontsize=10, fontweight='bold')
ax3_3.set_title("Vehicle Model Offerings: Retail Price vs Quality Rating (Bubble = Volume)", fontsize=13, fontweight='bold')
ax3_3.set_xlabel("Average Retail Price (Lakh INR)")
ax3_3.set_ylabel("Batch Quality Score")

path3 = os.path.join(SCREENSHOT_DIR, '03_commodity_volatility_variant_offerings.png')
plt.savefig(path3, dpi=160, facecolor=fig3.get_facecolor(), bbox_inches='tight')
plt.close()
print(f"[SAVED] {path3}")

print("\n" + "=" * 70)
print("  PHASE 6 COMPLETE - ALL 3 TABLEAU DASHBOARDS RENDERED & SAVED")
print("=" * 70)
