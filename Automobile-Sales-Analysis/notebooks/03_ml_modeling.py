"""
===================================================================
NOTEBOOK 03: MACHINE LEARNING MODELING
===================================================================
Automobile Raw Material Impact Analysis
Author: Chaitanya Lande | Great Lakes PGDM (Analytics & Operations)
===================================================================

Models:
Part A: Regression — Predict Final Vehicle Quality Score from Material Inputs
Part B: Classification — Predict Production Efficiency Risk / Bottleneck
Part C: SHAP Explainability — Identify Primary Material & Operational Drivers
Part D: Time-Series Cross-Validation & Metric Comparison
===================================================================
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, roc_auc_score, classification_report
import xgboost as xgb
import shap

sys.stdout.reconfigure(encoding='utf-8')

PROC_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\processed'
CHART_DIR = os.path.join(PROC_DIR, 'ml_charts')
os.makedirs(CHART_DIR, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

print("=" * 70)
print("  PHASE 4: MACHINE LEARNING MODELING")
print("  Automobile Raw Material Impact Analysis")
print("=" * 70)

# Load data
unified = pd.read_csv(os.path.join(PROC_DIR, 'unified_production_data.csv'), parse_dates=['production_date', 'production_month'])
unified = unified.sort_values('production_date').reset_index(drop=True)
print(f"Loaded dataset: {len(unified):,} rows x {unified.shape[1]} columns")

# =====================================================================
# PART A: REGRESSION — PREDICTING BATCH QUALITY SCORE
# =====================================================================
print("\n--- Part A: Quality Score Prediction (Regression) ---")

# Feature selection
feature_cols = [
    'planned_qty', 'actual_qty', 'production_efficiency', 'downtime_hours',
    'total_material_cost', 'total_materials_used', 'avg_defect_rate', 'max_defect_rate',
    'avg_lead_variance', 'max_lead_variance', 'total_delays', 'total_fails', 'total_reworks',
    'overall_pass_rate', 'pct_grade_a_suppliers', 'pct_grade_c_suppliers',
    'unique_suppliers', 'material_cost_per_unit', 'cost_efficiency_ratio',
    'delay_risk_score', 'fail_rework_ratio',
    'Steel_HRC_INR_per_ton', 'Semiconductor_Index', 'Rubber_INR_per_kg', 'Crude_Oil_USD_per_barrel'
]

# Add vertical-specific columns if present
vert_cols = [c for c in unified.columns if any(c.startswith(p) for p in ['cost_', 'defect_', 'delays_', 'passrate_'])]
feature_cols.extend(vert_cols)
# Deduplicate feature_cols while preserving order
feature_cols = list(dict.fromkeys(feature_cols))

# Categorical features to encode
cat_cols = ['car_model', 'segment', 'variant_tier', 'plant', 'shift']
X_df = unified[feature_cols].copy()

for cat in cat_cols:
    dummies = pd.get_dummies(unified[cat], prefix=cat, drop_first=True)
    X_df = pd.concat([X_df, dummies], axis=1)

y_reg = unified['quality_score']

# Fill any remaining NaNs
X_df = X_df.fillna(0)

# Temporal train-test split (80% train, 20% test)
split_idx = int(len(X_df) * 0.8)
X_train, X_test = X_df.iloc[:split_idx], X_df.iloc[split_idx:]
y_train, y_test = y_reg.iloc[:split_idx], y_reg.iloc[split_idx:]

print(f"Train set: {len(X_train):,} batches | Test set: {len(X_test):,} batches | Features: {X_df.shape[1]}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
reg_models = {
    'Ridge': Ridge(alpha=1.0),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=6, random_state=42),
    'XGBoost': xgb.XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.08, random_state=42, n_jobs=-1)
}

reg_results = {}
for name, model in reg_models.items():
    if name == 'Ridge':
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    reg_results[name] = {'MAE': round(mae, 3), 'RMSE': round(rmse, 3), 'R2': round(r2, 4)}
    print(f"  {name:<20} MAE: {mae:.3f} | RMSE: {rmse:.3f} | R2: {r2:.4f}")

# Plot Regression Comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
models_list = list(reg_results.keys())
r2_vals = [reg_results[m]['R2'] for m in models_list]
mae_vals = [reg_results[m]['MAE'] for m in models_list]

axes[0].bar(models_list, r2_vals, color=['#CBD5E0', '#48BB78', '#38A169', '#3182CE'], width=0.55)
for i, v in enumerate(r2_vals):
    axes[0].text(i, v + 0.02, f"{v:.4f}", ha='center', fontweight='bold')
axes[0].set_title("Model Comparison: R-squared (Higher = Better)", fontsize=12, fontweight='bold')
axes[0].set_ylim(0, 1.1)

axes[1].bar(models_list, mae_vals, color=['#E53E3E', '#ED8936', '#D69E2E', '#3182CE'], width=0.55)
for i, v in enumerate(mae_vals):
    axes[1].text(i, v + 0.1, f"{v:.2f}", ha='center', fontweight='bold')
axes[1].set_title("Model Comparison: MAE (Lower = Better)", fontsize=12, fontweight='bold')

plt.tight_layout()
p_reg = os.path.join(CHART_DIR, '01_regression_comparison.png')
plt.savefig(p_reg, dpi=150, bbox_inches='tight')
plt.close()
print(f"[SAVED] {p_reg}")

# =====================================================================
# PART B: CLASSIFICATION — PREDICTING PRODUCTION BOTTLENECK / UNDERPERFORMANCE
# =====================================================================
print("\n--- Part B: Production Efficiency Bottleneck Classification ---")

y_clf = unified['is_underperforming']
y_train_c, y_test_c = y_clf.iloc[:split_idx], y_clf.iloc[split_idx:]

# Classification models
clf_models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
    'XGBoost': xgb.XGBClassifier(n_estimators=150, max_depth=5, learning_rate=0.08, random_state=42, n_jobs=-1)
}

clf_results = {}
for name, model in clf_models.items():
    if name == 'Logistic Regression':
        model.fit(X_train_scaled, y_train_c)
        probs = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train_c)
        probs = model.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test_c, probs)
    clf_results[name] = {'AUC': round(auc, 4)}
    print(f"  {name:<22} ROC-AUC: {auc:.4f}")

# Best XGBoost classifier report
best_clf = clf_models['XGBoost']
clf_preds = best_clf.predict(X_test)
print("\nXGBoost Classification Report:")
print(classification_report(y_test_c, clf_preds, target_names=['Normal Efficiency', 'Bottleneck Risk']))

# =====================================================================
# PART C: SHAP EXPLAINABILITY
# =====================================================================
print("\n--- Part C: SHAP Explainability ---")

best_reg = reg_models['XGBoost']
explainer = shap.TreeExplainer(best_reg)
sample_test = X_test.head(1000)
shap_values = explainer.shap_values(sample_test)

# Mean absolute SHAP values for top features
mean_shap = np.abs(shap_values).mean(axis=0)
shap_importance = pd.DataFrame({'feature': X_df.columns, 'mean_shap': mean_shap}).sort_values('mean_shap', ascending=False)

print("\nTop 10 Feature Drivers of Quality Score (SHAP):")
for _, r in shap_importance.head(10).iterrows():
    print(f"  {r['feature']:<35} : Mean |SHAP| = {r['mean_shap']:.4f}")

# Plot SHAP global importance
fig, ax = plt.subplots(figsize=(10, 6))
top_shap = shap_importance.head(12)
ax.barh(top_shap['feature'][::-1], top_shap['mean_shap'][::-1], color='#3182CE', height=0.6)
ax.set_xlabel("Mean |SHAP Value| (Impact on Quality Score)", fontsize=11)
ax.set_title("SHAP Global Feature Importance — Key Quality Drivers", fontsize=13, fontweight='bold')
plt.tight_layout()
p_shap = os.path.join(CHART_DIR, '02_shap_importance.png')
plt.savefig(p_shap, dpi=150, bbox_inches='tight')
plt.close()
print(f"[SAVED] {p_shap}")

# =====================================================================
# PART D: TIME-SERIES CROSS-VALIDATION
# =====================================================================
print("\n--- Part D: 5-Fold TimeSeriesSplit Cross-Validation ---")

tscv = TimeSeriesSplit(n_splits=5)
cv_scores = []

for fold, (train_idx, val_idx) in enumerate(tscv.split(X_df), 1):
    X_tr, X_val = X_df.iloc[train_idx], X_df.iloc[val_idx]
    y_tr, y_val = y_reg.iloc[train_idx], y_reg.iloc[val_idx]
    
    cv_model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.08, random_state=42, n_jobs=-1)
    cv_model.fit(X_tr, y_tr)
    cv_preds = cv_model.predict(X_val)
    
    fold_mae = mean_absolute_error(y_val, cv_preds)
    fold_r2 = r2_score(y_val, cv_preds)
    cv_scores.append({'fold': fold, 'MAE': fold_mae, 'R2': fold_r2})
    print(f"  Fold {fold}: MAE = {fold_mae:.3f} | R2 = {fold_r2:.4f}")

mean_mae = np.mean([s['MAE'] for s in cv_scores])
mean_r2 = np.mean([s['R2'] for s in cv_scores])
print(f"\nCV Summary: Mean MAE = {mean_mae:.3f} | Mean R2 = {mean_r2:.4f}")

# =====================================================================
# SAVE MODEL RESULTS
# =====================================================================
results_payload = {
    'regression': reg_results,
    'classification': clf_results,
    'cross_validation': {'mean_MAE': round(mean_mae, 3), 'mean_R2': round(mean_r2, 4)},
    'top_shap_features': shap_importance.head(10).to_dict(orient='records')
}

with open(os.path.join(PROC_DIR, 'model_results.json'), 'w') as f:
    json.dump(results_payload, f, indent=2)

print("\n" + "=" * 70)
print("  PHASE 4 COMPLETE - MACHINE LEARNING MODELING")
print("=" * 70)
