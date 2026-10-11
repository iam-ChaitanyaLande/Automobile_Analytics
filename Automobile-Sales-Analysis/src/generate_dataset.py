"""
===================================================================
DATASET GENERATOR: Automobile Manufacturing Raw Material Analysis
===================================================================
Generates realistic synthetic datasets simulating an automobile OEM's
raw material procurement, production batch, and quality tracking system
across 6 manufacturing verticals.

Datasets produced:
1. raw_materials_master.csv     - 200 materials across 6 verticals
2. production_batches.csv       - 5,000 production batch records
3. material_consumption.csv     - ~60,000 material usage records
4. supplier_performance.csv     - Monthly supplier KPIs (36 months)
5. commodity_prices.csv         - Monthly commodity price indices
===================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')
np.random.seed(42)

OUTPUT_DIR = r'C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis\data\raw'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("  GENERATING AUTOMOBILE MANUFACTURING DATASETS")
print("  6 Verticals | 200 Materials | 5,000 Production Batches")
print("=" * 70)

# =====================================================================
# 1. RAW MATERIALS MASTER
# =====================================================================
print("\n--- 1. Generating Raw Materials Master ---")

verticals = {
    'Body & Structural': {
        'materials': ['CR Steel Sheet', 'HR Steel Sheet', 'Galvanized Steel', 'Aluminum Sheet 6xxx',
                      'Aluminum Extrusion', 'High-Strength Steel', 'Stamping Die Steel',
                      'Zinc Coating Material', 'Structural Adhesive', 'Spot Weld Wire',
                      'Body Sealant', 'Underbody Coating', 'Anti-Rust Primer',
                      'Roof Panel Steel', 'Door Panel Aluminum', 'Fender Steel Sheet',
                      'Bumper Reinforcement Bar', 'Pillar Steel Tube', 'Floor Pan Steel',
                      'Cross Member Steel', 'Rocker Panel Steel', 'Hood Aluminum Sheet',
                      'Trunk Lid Steel', 'Wheel Arch Liner', 'Splash Guard Material',
                      'Paint Primer Coat', 'Base Coat Paint', 'Clear Coat Paint',
                      'E-Coat Material', 'Body Filler Putty'],
        'cost_range': (80, 950),
        'lead_time_range': (7, 28),
        'criticality': 'High'
    },
    'Powertrain': {
        'materials': ['Engine Block Casting', 'Cylinder Head Casting', 'Crankshaft Forging',
                      'Camshaft Forging', 'Piston Assembly', 'Connecting Rod',
                      'Timing Chain Assembly', 'Turbocharger Unit', 'Exhaust Manifold',
                      'Catalytic Converter', 'Transmission Housing', 'Gear Set Assembly',
                      'Clutch Plate Assembly', 'Flywheel Assembly', 'CV Joint Assembly',
                      'Drive Shaft', 'Differential Assembly', 'Oil Pump Assembly',
                      'Water Pump Assembly', 'Fuel Injector Set', 'Throttle Body',
                      'Intake Manifold', 'Oil Filter Housing', 'Engine Mount Bracket',
                      'Exhaust Pipe Assembly', 'Muffler Assembly', 'O2 Sensor',
                      'Knock Sensor', 'Coolant Thermostat', 'Radiator Assembly',
                      'Intercooler Unit', 'EGR Valve Assembly', 'Fuel Rail Assembly',
                      'Engine Gasket Kit', 'Valve Spring Set'],
        'cost_range': (120, 2800),
        'lead_time_range': (14, 45),
        'criticality': 'Critical'
    },
    'Interior': {
        'materials': ['Dashboard Module', 'Instrument Cluster Housing', 'Steering Wheel Assembly',
                      'Seat Foam Padding', 'Seat Cover Fabric', 'Seat Cover Leather',
                      'Door Trim Panel', 'Center Console Assembly', 'Gear Knob Assembly',
                      'Headliner Fabric', 'Carpet Floor Mat', 'Sun Visor Assembly',
                      'Rearview Mirror Housing', 'Glove Box Assembly', 'Air Vent Module',
                      'Cup Holder Insert', 'Arm Rest Assembly', 'Seat Belt Webbing',
                      'Seat Belt Buckle', 'Airbag Module', 'Pedal Assembly',
                      'Handbrake Lever', 'Door Handle Inner', 'Window Regulator',
                      'Door Lock Actuator', 'Trunk Carpet Liner', 'Pillar Trim Cover',
                      'Boot Board Assembly', 'Acoustic Insulation Mat', 'NVH Damping Sheet'],
        'cost_range': (15, 650),
        'lead_time_range': (5, 21),
        'criticality': 'Medium'
    },
    'Electrical & Electronics': {
        'materials': ['Main Wiring Harness', 'Engine Bay Harness', 'Body Control Module',
                      'Engine Control Unit (ECU)', 'Transmission Control Module',
                      'ABS Control Unit', 'Airbag Control Module', 'Infotainment Head Unit',
                      'Instrument Cluster Display', 'Rear Camera Module', 'Front Radar Sensor',
                      'Ultrasonic Parking Sensor Set', 'Headlamp LED Module', 'Tail Lamp Assembly',
                      'Fog Lamp Assembly', 'Turn Signal Module', 'Horn Assembly',
                      'Starter Motor', 'Alternator Assembly', 'Battery (12V)',
                      'Fuse Box Assembly', 'Relay Module Set', 'Power Window Motor',
                      'Wiper Motor Assembly', 'Blower Motor HVAC', 'Compressor Clutch',
                      'GPS Antenna Module', 'Bluetooth Module', 'USB Port Assembly',
                      'Keyless Entry Module', 'Immobilizer Unit', 'TPMS Sensor Set',
                      'Rain Sensor Module', 'Light Sensor Module', 'Antenna Assembly'],
        'cost_range': (25, 1800),
        'lead_time_range': (10, 60),
        'criticality': 'Critical'
    },
    'Suspension & Chassis': {
        'materials': ['Front Coil Spring Set', 'Rear Coil Spring Set', 'Front Shock Absorber',
                      'Rear Shock Absorber', 'Front Stabilizer Bar', 'Rear Stabilizer Bar',
                      'Lower Control Arm', 'Upper Control Arm', 'Steering Rack Assembly',
                      'Tie Rod End Set', 'Ball Joint Set', 'Front Wheel Hub Bearing',
                      'Rear Wheel Hub Bearing', 'Brake Disc Front', 'Brake Disc Rear',
                      'Brake Pad Set Front', 'Brake Pad Set Rear', 'Brake Caliper Front',
                      'Brake Caliper Rear', 'Brake Master Cylinder', 'ABS Wheel Speed Sensor',
                      'Subframe Assembly', 'Steering Column Assembly', 'Power Steering Pump',
                      'Steering Fluid Reservoir', 'Chassis Cross Brace', 'Engine Cradle',
                      'Leaf Spring Assembly', 'Torsion Bar', 'Strut Mount Bearing'],
        'cost_range': (30, 850),
        'lead_time_range': (7, 25),
        'criticality': 'High'
    },
    'Tyres & Rubber': {
        'materials': ['Front Tyre 205/55R16', 'Rear Tyre 205/55R16', 'Front Tyre 225/45R17',
                      'Rear Tyre 225/45R17', 'Spare Tyre Assembly', 'Alloy Wheel 16inch',
                      'Alloy Wheel 17inch', 'Steel Wheel 15inch', 'Wheel Nut Set',
                      'Valve Stem Set', 'Door Seal Rubber', 'Window Seal Rubber',
                      'Trunk Seal Rubber', 'Hood Seal Rubber', 'Engine Mount Rubber',
                      'Exhaust Hanger Rubber', 'Suspension Bush Set', 'Stabilizer Link Bush',
                      'Steering Rack Boot', 'CV Boot Set', 'Radiator Hose Upper',
                      'Radiator Hose Lower', 'Heater Hose Set', 'Fuel Line Hose',
                      'Brake Hose Set', 'Vacuum Hose Set', 'Windshield Wiper Blade Set',
                      'Weatherstrip Door Set', 'Grommet Assortment Kit', 'Vibration Damper Pad'],
        'cost_range': (10, 480),
        'lead_time_range': (5, 18),
        'criticality': 'Medium'
    }
}

# Generate suppliers
suppliers = [
    ('Tata Steel', 'India', 'A'), ('JSW Steel', 'India', 'A'), ('SAIL', 'India', 'B'),
    ('Hindalco', 'India', 'A'), ('Novelis India', 'India', 'B'),
    ('Bharat Forge', 'India', 'A'), ('Mahle India', 'India', 'B'), ('Bosch India', 'India', 'A'),
    ('Denso India', 'India', 'A'), ('Continental India', 'India', 'B'),
    ('Motherson Sumi', 'India', 'A'), ('Minda Industries', 'India', 'B'),
    ('Valeo India', 'India', 'B'), ('ZF India', 'India', 'A'),
    ('Endurance Tech', 'India', 'A'), ('Sundaram Clayton', 'India', 'B'),
    ('Apollo Tyres', 'India', 'A'), ('MRF Ltd', 'India', 'A'),
    ('CEAT Tyres', 'India', 'B'), ('JK Tyre', 'India', 'B'),
    ('Samvardhana Motherson', 'India', 'A'), ('Sona BLW', 'India', 'A'),
    ('Rane Holdings', 'India', 'B'), ('Wheels India', 'India', 'B'),
    ('Lumax Industries', 'India', 'B'), ('Subros Ltd', 'India', 'C'),
    ('Jamna Auto', 'India', 'B'), ('Gabriel India', 'India', 'B'),
    ('Fiem Industries', 'India', 'C'), ('Pricol Ltd', 'India', 'C'),
    ('Nippon Steel Import', 'Japan', 'A'), ('POSCO Import', 'South Korea', 'A'),
    ('Schaeffler India', 'Germany', 'A'), ('SKF India', 'Sweden', 'A'),
    ('Delphi India', 'USA', 'B'), ('Magna India', 'Canada', 'B'),
    ('Hyundai Mobis', 'South Korea', 'A'), ('Aisin India', 'Japan', 'A'),
    ('NGK India', 'Japan', 'A'), ('Yazaki India', 'Japan', 'B'),
]

# Vertical-to-supplier mapping
vertical_supplier_map = {
    'Body & Structural': ['Tata Steel', 'JSW Steel', 'SAIL', 'Hindalco', 'Novelis India', 'Nippon Steel Import', 'POSCO Import'],
    'Powertrain': ['Bharat Forge', 'Mahle India', 'Bosch India', 'Denso India', 'Aisin India', 'NGK India', 'Sona BLW'],
    'Interior': ['Motherson Sumi', 'Samvardhana Motherson', 'Valeo India', 'Minda Industries', 'Lumax Industries', 'Pricol Ltd', 'Subros Ltd'],
    'Electrical & Electronics': ['Bosch India', 'Denso India', 'Continental India', 'Motherson Sumi', 'Yazaki India', 'Delphi India', 'Hyundai Mobis', 'Fiem Industries'],
    'Suspension & Chassis': ['ZF India', 'Endurance Tech', 'Sundaram Clayton', 'Rane Holdings', 'Gabriel India', 'Schaeffler India', 'SKF India'],
    'Tyres & Rubber': ['Apollo Tyres', 'MRF Ltd', 'CEAT Tyres', 'JK Tyre', 'Wheels India', 'Jamna Auto']
}

supplier_dict = {s[0]: {'region': s[1], 'grade': s[2]} for s in suppliers}

materials_records = []
mat_id = 1000
for vertical, config in verticals.items():
    avail_suppliers = vertical_supplier_map[vertical]
    for mat_name in config['materials']:
        supplier = np.random.choice(avail_suppliers)
        sup_info = supplier_dict[supplier]
        base_cost = np.random.uniform(*config['cost_range'])
        base_lead = np.random.randint(*config['lead_time_range'])
        
        # Grade affects cost and quality
        grade_factor = {'A': 1.0, 'B': 0.88, 'C': 0.75}[sup_info['grade']]
        quality_score = np.clip(np.random.normal(85 * grade_factor + 10, 8), 40, 100)
        
        materials_records.append({
            'material_id': f'MAT-{mat_id}',
            'material_name': mat_name,
            'vertical': vertical,
            'criticality': config['criticality'],
            'supplier_name': supplier,
            'supplier_region': sup_info['region'],
            'supplier_grade': sup_info['grade'],
            'unit_cost_inr': round(base_cost, 2),
            'base_lead_time_days': base_lead,
            'incoming_quality_score': round(quality_score, 1),
            'moq': np.random.choice([50, 100, 200, 500, 1000]),
            'safety_stock_days': np.random.choice([3, 5, 7, 10, 14])
        })
        mat_id += 1

mat_df = pd.DataFrame(materials_records)
mat_df.to_csv(os.path.join(OUTPUT_DIR, 'raw_materials_master.csv'), index=False)
print(f"  Raw Materials Master: {len(mat_df)} materials across {mat_df['vertical'].nunique()} verticals")

# =====================================================================
# 2. COMMODITY PRICE INDICES (36 months)
# =====================================================================
print("\n--- 2. Generating Commodity Price Indices ---")

months = pd.date_range('2022-01-01', '2024-12-31', freq='MS')
commodities = {
    'Steel_HRC_INR_per_ton': {'base': 55000, 'volatility': 0.06},
    'Aluminum_INR_per_ton': {'base': 210000, 'volatility': 0.05},
    'Copper_INR_per_ton': {'base': 720000, 'volatility': 0.07},
    'Rubber_INR_per_kg': {'base': 165, 'volatility': 0.08},
    'Crude_Oil_USD_per_barrel': {'base': 82, 'volatility': 0.10},
    'Plastic_Resin_INR_per_ton': {'base': 95000, 'volatility': 0.04},
    'Semiconductor_Index': {'base': 100, 'volatility': 0.12}
}

commodity_records = []
for month in months:
    record = {'month': month}
    for commodity, params in commodities.items():
        t = (month - months[0]).days / 365.0
        trend = 1.0 + 0.03 * t  # mild inflation trend
        seasonal = 1.0 + 0.02 * np.sin(2 * np.pi * month.month / 12)
        shock = np.random.normal(0, params['volatility'])
        price = params['base'] * trend * seasonal * (1 + shock)
        record[commodity] = round(price, 2)
    commodity_records.append(record)

commodity_df = pd.DataFrame(commodity_records)
commodity_df.to_csv(os.path.join(OUTPUT_DIR, 'commodity_prices.csv'), index=False)
print(f"  Commodity Prices: {len(commodity_df)} months x {len(commodities)} indices")

# =====================================================================
# 3. PRODUCTION BATCHES
# =====================================================================
print("\n--- 3. Generating Production Batches ---")

car_models = {
    'Nexon': {'segment': 'Compact SUV', 'base_price_lakh': 8.5, 'variants': ['Smart', 'Pure', 'Creative', 'Fearless']},
    'Harrier': {'segment': 'Mid SUV', 'base_price_lakh': 15.5, 'variants': ['Smart', 'Pure', 'Adventure', 'Accomplished']},
    'Safari': {'segment': 'Full SUV', 'base_price_lakh': 16.2, 'variants': ['Smart', 'Pure', 'Adventure', 'Accomplished Plus']},
    'Altroz': {'segment': 'Hatchback', 'base_price_lakh': 6.8, 'variants': ['XE', 'XM', 'XZ', 'XZ+']},
    'Punch': {'segment': 'Micro SUV', 'base_price_lakh': 6.0, 'variants': ['Pure', 'Adventure', 'Accomplished', 'Creative']},
    'Tiago': {'segment': 'Hatchback', 'base_price_lakh': 5.5, 'variants': ['XE', 'XM', 'XT', 'XZ+']},
    'Curvv': {'segment': 'SUV Coupe', 'base_price_lakh': 10.5, 'variants': ['Smart', 'Pure', 'Creative', 'Accomplished']},
}

plants = ['Pune Plant', 'Sanand Plant', 'Ranjangaon Plant']
shifts = ['Morning', 'Afternoon', 'Night']

production_dates = pd.date_range('2022-01-03', '2024-12-28', freq='B')  # business days

batch_records = []
batch_id = 5000
for i in range(5000):
    prod_date = np.random.choice(production_dates)
    model_name = np.random.choice(list(car_models.keys()), p=[0.22, 0.15, 0.12, 0.15, 0.18, 0.10, 0.08])
    model_config = car_models[model_name]
    variant = np.random.choice(model_config['variants'])
    plant = np.random.choice(plants, p=[0.45, 0.35, 0.20])
    shift = np.random.choice(shifts, p=[0.40, 0.35, 0.25])
    
    planned_qty = np.random.choice([40, 50, 60, 80, 100])
    
    # Production efficiency affected by month (seasonal), shift, plant
    base_eff = 0.88
    shift_factor = {'Morning': 0.04, 'Afternoon': 0.01, 'Night': -0.03}[shift]
    plant_factor = {'Pune Plant': 0.03, 'Sanand Plant': 0.01, 'Ranjangaon Plant': -0.02}[plant]
    seasonal_factor = 0.02 * np.sin(2 * np.pi * pd.Timestamp(prod_date).month / 12)
    noise = np.random.normal(0, 0.05)
    efficiency = np.clip(base_eff + shift_factor + plant_factor + seasonal_factor + noise, 0.55, 0.99)
    
    actual_qty = max(int(planned_qty * efficiency), int(planned_qty * 0.5))
    downtime_hours = max(0, np.random.exponential(1.5) * (1 - efficiency) * 10)
    
    # Quality score affected by plant, shift, and randomness
    base_quality = 82
    quality_noise = np.random.normal(0, 6)
    quality_score = np.clip(base_quality + plant_factor * 80 + shift_factor * 50 + quality_noise, 45, 100)
    
    # Defect count
    defect_count = max(0, int(np.random.poisson(max(0.5, (100 - quality_score) / 15))))
    
    # Rework needed
    rework_units = min(defect_count, int(actual_qty * 0.1))
    
    # Calculate variant price impact
    variant_idx = model_config['variants'].index(variant)
    variant_premium = variant_idx * 1.2  # higher variant = more premium
    final_price_lakh = model_config['base_price_lakh'] + variant_premium
    
    batch_records.append({
        'batch_id': f'BATCH-{batch_id}',
        'production_date': prod_date,
        'car_model': model_name,
        'segment': model_config['segment'],
        'variant': variant,
        'plant': plant,
        'shift': shift,
        'planned_qty': planned_qty,
        'actual_qty': actual_qty,
        'production_efficiency': round(efficiency, 4),
        'downtime_hours': round(downtime_hours, 2),
        'quality_score': round(quality_score, 1),
        'defect_count': defect_count,
        'rework_units': rework_units,
        'final_price_lakh': round(final_price_lakh, 2),
        'production_month': pd.Timestamp(prod_date).to_period('M').to_timestamp()
    })
    batch_id += 1

batch_df = pd.DataFrame(batch_records)
batch_df.to_csv(os.path.join(OUTPUT_DIR, 'production_batches.csv'), index=False)
print(f"  Production Batches: {len(batch_df)} batches | {batch_df['car_model'].nunique()} models | {batch_df['plant'].nunique()} plants")

# =====================================================================
# 4. MATERIAL CONSUMPTION RECORDS
# =====================================================================
print("\n--- 4. Generating Material Consumption Records ---")

consumption_records = []
cons_id = 10000

for _, batch in batch_df.iterrows():
    # Each batch uses ~12 materials from various verticals
    n_materials = np.random.randint(10, 16)
    
    # Ensure representation from each vertical
    selected_mats = []
    for vertical in verticals.keys():
        v_mats = mat_df[mat_df['vertical'] == vertical]
        n_from_v = max(1, int(n_materials * len(v_mats) / len(mat_df)))
        chosen = v_mats.sample(min(n_from_v, len(v_mats)), random_state=cons_id)
        selected_mats.append(chosen)
    
    all_selected = pd.concat(selected_mats).head(n_materials)
    
    for _, mat in all_selected.iterrows():
        qty_used = batch['actual_qty'] * np.random.uniform(0.8, 2.5)
        
        # Cost fluctuation based on commodity prices
        month_idx = min(len(commodity_df)-1, max(0, (pd.Timestamp(batch['production_date']) - pd.Timestamp('2022-01-01')).days // 30))
        cost_factor = 1.0
        if 'Steel' in mat['material_name'] or mat['vertical'] == 'Body & Structural':
            cost_factor = commodity_df.iloc[month_idx]['Steel_HRC_INR_per_ton'] / 55000
        elif mat['vertical'] == 'Electrical & Electronics':
            cost_factor = commodity_df.iloc[month_idx]['Semiconductor_Index'] / 100
        elif mat['vertical'] == 'Tyres & Rubber':
            cost_factor = commodity_df.iloc[month_idx]['Rubber_INR_per_kg'] / 165
        
        actual_cost = mat['unit_cost_inr'] * cost_factor * np.random.uniform(0.95, 1.08)
        
        # Lead time variance
        actual_lead = max(1, mat['base_lead_time_days'] + np.random.randint(-5, 10))
        lead_variance = actual_lead - mat['base_lead_time_days']
        delayed = lead_variance > 3
        
        # Defect rate influenced by supplier grade
        grade_defect = {'A': 0.02, 'B': 0.05, 'C': 0.10}[mat['supplier_grade']]
        defect_rate = np.clip(np.random.exponential(grade_defect), 0, 0.30)
        
        inspection = 'Pass'
        if defect_rate > 0.08:
            inspection = np.random.choice(['Fail', 'Rework'], p=[0.4, 0.6])
        elif defect_rate > 0.04:
            inspection = np.random.choice(['Pass', 'Rework'], p=[0.7, 0.3])
        
        consumption_records.append({
            'consumption_id': f'CONS-{cons_id}',
            'batch_id': batch['batch_id'],
            'material_id': mat['material_id'],
            'vertical': mat['vertical'],
            'supplier_name': mat['supplier_name'],
            'supplier_grade': mat['supplier_grade'],
            'quantity_used': round(qty_used, 1),
            'unit_cost_actual': round(actual_cost, 2),
            'total_cost': round(qty_used * actual_cost, 2),
            'actual_lead_time_days': actual_lead,
            'lead_time_variance_days': lead_variance,
            'delivery_delayed': delayed,
            'defect_rate_pct': round(defect_rate * 100, 2),
            'inspection_result': inspection,
            'production_month': batch['production_month']
        })
        cons_id += 1

cons_df = pd.DataFrame(consumption_records)
cons_df.to_csv(os.path.join(OUTPUT_DIR, 'material_consumption.csv'), index=False)
print(f"  Material Consumption: {len(cons_df):,} records")

# =====================================================================
# 5. SUPPLIER PERFORMANCE (MONTHLY KPIs)
# =====================================================================
print("\n--- 5. Generating Supplier Performance KPIs ---")

supplier_records = []
unique_suppliers = mat_df['supplier_name'].unique()

for month in months:
    for supplier in unique_suppliers:
        sup_info = supplier_dict.get(supplier, {'region': 'India', 'grade': 'B'})
        grade_base = {'A': 0.94, 'B': 0.85, 'C': 0.74}[sup_info['grade']]
        
        otd_rate = np.clip(grade_base + np.random.normal(0, 0.05), 0.50, 1.00)
        rejection_rate = np.clip(np.random.exponential(0.10 - grade_base * 0.08) * 100, 0.1, 18.0)
        cost_variance = np.random.normal(0, 3.5)  # % variance from contracted price
        response_time_hours = max(1, np.random.exponential(48 / grade_base * 0.5))
        quality_incidents = max(0, np.random.poisson(max(0.2, 3 * (1 - grade_base))))
        
        supplier_records.append({
            'supplier_name': supplier,
            'supplier_grade': sup_info['grade'],
            'month': month,
            'on_time_delivery_rate': round(otd_rate, 4),
            'rejection_rate_pct': round(rejection_rate, 2),
            'cost_variance_pct': round(cost_variance, 2),
            'avg_response_time_hours': round(response_time_hours, 1),
            'quality_incidents': quality_incidents
        })

supplier_perf_df = pd.DataFrame(supplier_records)
supplier_perf_df.to_csv(os.path.join(OUTPUT_DIR, 'supplier_performance.csv'), index=False)
print(f"  Supplier Performance: {len(supplier_perf_df):,} records ({len(unique_suppliers)} suppliers x {len(months)} months)")

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "=" * 70)
print("  DATASET GENERATION COMPLETE")
print("=" * 70)
print(f"  1. raw_materials_master.csv    : {len(mat_df):>7,} rows")
print(f"  2. commodity_prices.csv        : {len(commodity_df):>7,} rows")
print(f"  3. production_batches.csv      : {len(batch_df):>7,} rows")
print(f"  4. material_consumption.csv    : {len(cons_df):>7,} rows")
print(f"  5. supplier_performance.csv    : {len(supplier_perf_df):>7,} rows")
print(f"  Total records generated        : {len(mat_df)+len(commodity_df)+len(batch_df)+len(cons_df)+len(supplier_perf_df):>7,}")
print(f"  Output directory: {OUTPUT_DIR}")
