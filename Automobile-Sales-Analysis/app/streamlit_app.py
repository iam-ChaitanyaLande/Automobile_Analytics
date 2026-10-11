"""
===================================================================
COMPANY XYZ AUTOMOTIVE OPERATIONS INTELLIGENCE PLATFORM
Raw Material Vertical Impact on Production Planning, Quality & Car Offerings
Author: Chaitanya Lande | Great Lakes Institute of Management, Chennai
Specialization: Analytics & Operations (PGDM)
===================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Page Config
st.set_page_config(
    page_title="AutoOps | Manufacturing & Raw Material Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1A365D;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4A5568;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# DATA LOADERS & CACHING
# ---------------------------------------------------------------------
DATA_DIR = r"C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\processed"
RAW_DIR = r"C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\raw"

@st.cache_data
def load_data():
    unified_path = os.path.join(DATA_DIR, "unified_production_data.csv")
    cons_path = os.path.join(RAW_DIR, "material_consumption.csv")
    comm_path = os.path.join(RAW_DIR, "commodity_prices.csv")
    sup_path = os.path.join(RAW_DIR, "supplier_performance.csv")
    
    u_df = pd.read_csv(unified_path, parse_dates=['production_date', 'production_month'])
    c_df = pd.read_csv(cons_path, parse_dates=['production_month'])
    comm_df = pd.read_csv(comm_path, parse_dates=['month'])
    s_df = pd.read_csv(sup_path, parse_dates=['month'])
    return u_df, c_df, comm_df, s_df

try:
    unified_df, cons_df, comm_df, sup_df = load_data()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

# ---------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/isometric/100/factory.png", width=65)
st.sidebar.title("Company XYZ Operations")
st.sidebar.caption("Manufacturing & S&OP Analytics Platform")

nav_choice = st.sidebar.radio(
    "Navigation Console",
    [
        "📊 Production & Quality Command Center",
        "🏭 Raw Material Verticals & Suppliers",
        "⚙️ Batch Quality & Bottleneck Simulator",
        "📈 Commodity Volatility & Car Offerings",
        "📑 GenAI S&OP Strategic Memorandum Hub",
        "🖼️ Tableau Dashboard Architecture"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Lead Analyst:** Chaitanya Lande")
st.sidebar.markdown("**Institution:** Great Lakes Chennai")
st.sidebar.markdown("**Focus:** S&OP & Supply Chain Analytics")

# ---------------------------------------------------------------------
# PAGE 1: PRODUCTION & QUALITY COMMAND CENTER
# ---------------------------------------------------------------------
if nav_choice == "📊 Production & Quality Command Center":
    st.markdown('<div class="main-header">Manufacturing Production & Quality Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Plant-level line efficiency, assembly downtime, and quality yield monitoring across 5,000 audited production batches.</div>', unsafe_allow_html=True)

    # Filter Bar
    with st.expander("Filter Production Batches", expanded=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            sel_plant = st.multiselect("Assembly Plant", options=unified_df['plant'].unique(), default=unified_df['plant'].unique())
        with f2:
            sel_shift = st.multiselect("Shift", options=unified_df['shift'].unique(), default=unified_df['shift'].unique())
        with f3:
            sel_model = st.multiselect("Car Model", options=unified_df['car_model'].unique(), default=unified_df['car_model'].unique())
        with f4:
            sel_tier = st.multiselect("Variant Tier", options=unified_df['variant_tier'].unique(), default=unified_df['variant_tier'].unique())

    f_df = unified_df[
        (unified_df['plant'].isin(sel_plant)) &
        (unified_df['shift'].isin(sel_shift)) &
        (unified_df['car_model'].isin(sel_model)) &
        (unified_df['variant_tier'].isin(sel_tier))
    ]

    # KPI Strip
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Total Batches", f"{len(f_df):,} Batches", "+5.2% vs Plan")
    with k2:
        eff = f_df['production_efficiency'].mean() * 100
        st.metric("Line Efficiency", f"{eff:.1f}%", "Target: 88.0%")
    with k3:
        q_avg = f_df['quality_score'].mean()
        st.metric("Fleet Quality Yield", f"{q_avg:.1f} / 100", "+1.4% Target")
    with k4:
        st.metric("Total Line Downtime", f"{f_df['downtime_hours'].sum():,.0f} Hours", "Unplanned")
    with k5:
        p_rate = f_df['overall_pass_rate'].mean()
        st.metric("First-Pass Yield", f"{p_rate:.1f}%", "Line-Side Acceptance")

    st.markdown("---")

    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Plant Quality Yield vs Line Efficiency")
        plant_agg = f_df.groupby('plant').agg({'quality_score': 'mean', 'production_efficiency': lambda x: x.mean()*100})
        fig_p, ax_p = plt.subplots(figsize=(8, 4.2))
        x = np.arange(len(plant_agg))
        w = 0.35
        ax_p.bar(x - w/2, plant_agg['quality_score'], width=w, color='#3182CE', label='Quality Score (0-100)')
        ax_p.bar(x + w/2, plant_agg['production_efficiency'], width=w, color='#48BB78', label='Line Efficiency (%)')
        ax_p.set_xticks(x)
        ax_p.set_xticklabels(plant_agg.index, fontweight='bold')
        ax_p.set_ylim(60, 95)
        ax_p.legend(loc='lower right')
        st.pyplot(fig_p)

    with c2:
        st.subheader("Shift Quality Score Heatmap")
        pivot_sq = f_df.pivot_table(index='plant', columns='shift', values='quality_score', aggfunc='mean')
        fig_hm, ax_hm = plt.subplots(figsize=(8, 4.2))
        im = ax_hm.imshow(pivot_sq.values, cmap='YlGn', aspect='auto', vmin=75, vmax=88)
        ax_hm.set_xticks(range(len(pivot_sq.columns)))
        ax_hm.set_xticklabels(pivot_sq.columns, fontweight='bold')
        ax_hm.set_yticks(range(len(pivot_sq.index)))
        ax_hm.set_yticklabels(pivot_sq.index, fontweight='bold')
        for i in range(len(pivot_sq.index)):
            for j in range(len(pivot_sq.columns)):
                ax_hm.text(j, i, f"{pivot_sq.values[i, j]:.1f}", ha='center', va='center', fontweight='bold', fontsize=11)
        fig_hm.colorbar(im, ax=ax_hm, shrink=0.7)
        st.pyplot(fig_hm)

# ---------------------------------------------------------------------
# PAGE 2: RAW MATERIAL VERTICALS & SUPPLIERS
# ---------------------------------------------------------------------
elif nav_choice == "🏭 Raw Material Verticals & Suppliers":
    st.markdown('<div class="main-header">Raw Material Verticals & Supplier Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluation of incoming defect rates, delivery delays, and tier-level supplier ratings across all 6 manufacturing verticals.</div>', unsafe_allow_html=True)

    v1, v2 = st.columns([1, 1])
    with v1:
        st.subheader("BOM Expenditure Share by Vertical")
        v_agg = cons_df.groupby('vertical').agg({'total_cost': 'sum', 'defect_rate_pct': 'mean', 'delivery_delayed': 'sum'})
        v_pct = v_agg['total_cost'] / v_agg['total_cost'].sum() * 100
        fig_v, ax_v = plt.subplots(figsize=(8, 4.5))
        colors = ['#3182CE', '#38A169', '#D69E2E', '#E53E3E', '#805AD5', '#DD6B20']
        bars_v = ax_v.barh(v_agg.index, v_pct, color=colors, height=0.55)
        for bar in bars_v:
            ax_v.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}%", va='center', fontweight='bold')
        ax_v.set_xlabel("% of Total Procurement Spend")
        st.pyplot(fig_v)

    with v2:
        st.subheader("Supplier Grade Defect Disparity (79.0% Reduction)")
        g_def = cons_df.groupby('supplier_grade')['defect_rate_pct'].mean()
        fig_g, ax_g = plt.subplots(figsize=(8, 4.5))
        g_colors = {'A': '#38A169', 'B': '#D69E2E', 'C': '#E53E3E'}
        bars_g = ax_g.bar(g_def.index, g_def.values, color=[g_colors[g] for g in g_def.index], width=0.5)
        for bar in bars_g:
            ax_g.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f"{bar.get_height():.2f}%", ha='center', fontweight='bold', fontsize=11)
        ax_g.set_ylabel("Average Defect Rate (%)")
        st.pyplot(fig_g)

    st.subheader("Vertical-Wise Performance Summary Table")
    v_table = cons_df.groupby('vertical').agg(
        Total_Spend_INR=('total_cost', 'sum'),
        Avg_Defect_Rate=('defect_rate_pct', 'mean'),
        Total_Delays=('delivery_delayed', 'sum'),
        Pass_Rate=('inspection_result', lambda x: (x == 'Pass').mean() * 100)
    ).round(2)
    st.dataframe(v_table, use_container_width=True)

# ---------------------------------------------------------------------
# PAGE 3: BATCH QUALITY & BOTTLENECK SIMULATOR
# ---------------------------------------------------------------------
elif nav_choice == "⚙️ Batch Quality & Bottleneck Simulator":
    st.markdown('<div class="main-header">Batch Quality & Bottleneck Risk Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Live predictive simulation of vehicle batch quality score and line downtime risk based on component inputs and supplier grades.</div>', unsafe_allow_html=True)

    sim_l, sim_r = st.columns([1, 1])

    with sim_l:
        st.subheader("Configure Batch Production Parameters")
        sim_model = st.selectbox("Vehicle Model", sorted(unified_df['car_model'].unique()))
        sim_plant = st.selectbox("Assembly Plant", sorted(unified_df['plant'].unique()))
        sim_shift = st.selectbox("Production Shift", ['Morning', 'Afternoon', 'Night'])
        
        c_qty, c_delays = st.columns(2)
        with c_qty:
            sim_qty = st.number_input("Planned Batch Quantity", min_value=20, max_value=120, value=60, step=10)
        with c_delays:
            sim_delays = st.slider("Material Delivery Delays Encountered", 0, 8, 1)

        c_grade_a, c_defect = st.columns(2)
        with c_grade_a:
            sim_grade_a = st.slider("% Tier-A Suppliers in BOM", 0, 100, 75, step=5)
        with c_defect:
            sim_defect = st.slider("Average Incoming Defect Rate (%)", 0.5, 12.0, 2.5, step=0.5)

        # Valuation heuristic based on ML weights
        base_q = 83.5
        plant_adj = 1.8 if sim_plant == 'Pune Plant' else (-2.8 if sim_plant == 'Ranjangaon Plant' else 0.4)
        shift_adj = 1.5 if sim_shift == 'Morning' else (-3.2 if sim_shift == 'Night' else -0.5)
        grade_adj = (sim_grade_a - 50) * 0.08
        defect_adj = - (sim_defect - 3.0) * 0.85
        delay_adj = - sim_delays * 0.95

        pred_quality = np.clip(base_q + plant_adj + shift_adj + grade_adj + defect_adj + delay_adj, 45, 98)
        bottleneck_prob = np.clip(0.12 + (sim_delays * 0.14) + (sim_defect * 0.04) - (grade_adj * 0.03), 0.02, 0.98)

    with sim_r:
        st.subheader("Predictive Analytics Diagnostics")
        r1, r2 = st.columns(2)
        with r1:
            st.metric("Predicted Quality Score", f"{pred_quality:.1f} / 100", f"{pred_quality - 82.7:+.1f} vs Fleet Avg")
        with r2:
            st.metric("Bottleneck / Delay Probability", f"{bottleneck_prob*100:.1f}%", "Risk Level")

        if bottleneck_prob >= 0.50:
            st.error("🔴 **HIGH BOTTLENECK RISK.** Incoming material delays or elevated defect rates exceed safety buffer. Recommend line balancing.")
        elif bottleneck_prob >= 0.25:
            st.warning("🟡 **MODERATE OPERATIONAL RISK.** Monitor critical components line-side; reinforce end-of-shift inspection.")
        else:
            st.success("🟢 **STANDARD PRODUCTION FLOW.** Material parameters aligned with target cycle time and quality yield.")

        st.subheader("Feature Impact Attribution (SHAP-Style)")
        contribs = [
            ("Base Quality Benchmark", base_q),
            (f"Assembly Plant ({sim_plant})", plant_adj),
            (f"Operating Shift ({sim_shift})", shift_adj),
            (f"Supplier Quality Mix ({sim_grade_a}% Tier-A)", grade_adj),
            (f"Component Defect Rate ({sim_defect}%)", defect_adj),
            (f"Delivery Delays ({sim_delays} events)", delay_adj)
        ]
        
        c_names = [x[0] for x in contribs[1:]]
        c_vals = [x[1] for x in contribs[1:]]
        c_cols = ['#38A169' if v >= 0 else '#E53E3E' for v in c_vals]

        fig_attr, ax_attr = plt.subplots(figsize=(8, 4))
        ax_attr.barh(c_names, c_vals, color=c_cols, height=0.55)
        ax_attr.axvline(0, color='black', linewidth=1)
        for bar in ax_attr.patches:
            w = bar.get_width()
            xpos = w + 0.15 if w >= 0 else w - 0.65
            ax_attr.text(xpos, bar.get_y() + bar.get_height()/2, f"{w:+.2f}", va='center', fontweight='bold', fontsize=9)
        ax_attr.set_xlabel("Impact on Quality Score")
        st.pyplot(fig_attr)

# ---------------------------------------------------------------------
# PAGE 4: COMMODITY VOLATILITY & CAR OFFERINGS
# ---------------------------------------------------------------------
elif nav_choice == "📈 Commodity Volatility & Car Offerings":
    st.markdown('<div class="main-header">Commodity Price Volatility & Car Variant Economics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">External raw material price movements (Steel HRC, Semiconductors, Rubber) and their direct impact on vehicle variant cost-to-price ratios.</div>', unsafe_allow_html=True)

    cm1, cm2 = st.columns([1, 1])
    with cm1:
        st.subheader("Raw Material Commodity Indices Trend (2022-2024)")
        m_dates = comm_df['month'].dt.strftime('%b %y')
        fig_comm, ax_c1 = plt.subplots(figsize=(8, 4.5))
        ax_c1.plot(m_dates, comm_df['Steel_HRC_INR_per_ton'] / 1000, color='#3182CE', linewidth=2.5, label='Steel HRC (K INR/ton)')
        ax_c1.plot(m_dates, comm_df['Semiconductor_Index'], color='#D69E2E', linewidth=2, linestyle='--', label='Semiconductor Index')
        ax_c1.set_ylabel("Index Benchmark", color='#2C5282', fontweight='bold')
        ax_c1.tick_params(axis='x', rotation=45)
        ax_c1.legend(loc='upper left')
        st.pyplot(fig_comm)

    with cm2:
        st.subheader("BOM Cost / Selling Price Ratio by Variant Tier")
        tier_ratio = unified_df.groupby('variant_tier')['cost_efficiency_ratio'].mean() * 100
        fig_t, ax_t = plt.subplots(figsize=(8, 4.5))
        t_colors = ['#E53E3E', '#ED8936', '#4299E1', '#38A169']
        bars_tr = ax_t.bar(tier_ratio.index, tier_ratio.values, color=t_colors, width=0.5)
        for bar in bars_tr:
            ax_t.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height():.1f}%", ha='center', fontweight='bold', fontsize=11)
        ax_t.set_ylabel("BOM Cost as % of Vehicle Selling Price")
        st.pyplot(fig_t)

    st.subheader("Vehicle Model Offerings: Average Retail Price vs Quality Rating")
    m_agg = unified_df.groupby('car_model').agg(
        Base_Segment=('segment', 'first'),
        Avg_Price_Lakh=('final_price_lakh', 'mean'),
        Avg_Quality_Score=('quality_score', 'mean'),
        Total_Batches=('batch_id', 'count')
    ).round(2)
    st.dataframe(m_agg, use_container_width=True)

# ---------------------------------------------------------------------
# PAGE 5: GENAI S&OP STRATEGIC MEMORANDUM HUB
# ---------------------------------------------------------------------
elif nav_choice == "📑 GenAI S&OP Strategic Memorandum Hub":
    st.markdown('<div class="main-header">GenAI S&OP Strategic Production Advisory Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated executive intelligence synthesizing multi-vertical procurement telemetry, plant performance, and variant economics.</div>', unsafe_allow_html=True)

    tab_m1, tab_m2 = st.tabs(["📑 Executive S&OP Strategic Memorandum", "🔍 Batch-Level Material Risk Inspection Memo"])

    with tab_m1:
        memo_f = os.path.join(DATA_DIR, "executive_reports", "strategic_sop_briefing.md")
        if os.path.exists(memo_f):
            with open(memo_f, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("Memorandum file not found.")

    with tab_m2:
        risk_f = os.path.join(DATA_DIR, "executive_reports", "sample_material_risk_memo.md")
        if os.path.exists(risk_f):
            with open(risk_f, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("Sample risk memo not found.")

# ---------------------------------------------------------------------
# PAGE 6: TABLEAU DASHBOARD ARCHITECTURE
# ---------------------------------------------------------------------
elif nav_choice == "🖼️ Tableau Dashboard Architecture":
    st.markdown('<div class="main-header">Tableau Manufacturing Dashboard Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">High-resolution executive visualization designs developed for Company XYZ plant directors and S&OP leadership.</div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs([
        "Dashboard 1: Production & Quality",
        "Dashboard 2: Verticals & Suppliers",
        "Dashboard 3: Commodity Volatility & Offerings",
        "Technical Calculations & Blueprint"
    ])

    SS_DIR = r"C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\tableau\dashboard_screenshots"

    with t1:
        img1 = os.path.join(SS_DIR, "01_production_quality_command_center.png")
        if os.path.exists(img1):
            st.image(img1, caption="Dashboard 1: Plant-Level Production Efficiency & Quality Yield Command Center")

    with t2:
        img2 = os.path.join(SS_DIR, "02_material_verticals_supplier_matrix.png")
        if os.path.exists(img2):
            st.image(img2, caption="Dashboard 2: Raw Material Verticals & Supplier Sourcing Risk Matrix")

    with t3:
        img3 = os.path.join(SS_DIR, "03_commodity_volatility_variant_offerings.png")
        if os.path.exists(img3):
            st.image(img3, caption="Dashboard 3: External Commodity Volatility vs Car Variant Offerings")

    with t4:
        bp_f = r"C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\tableau\TABLEAU_DASHBOARD_BLUEPRINT.md"
        if os.path.exists(bp_f):
            with open(bp_f, "r", encoding="utf-8") as f:
                st.markdown(f.read())
