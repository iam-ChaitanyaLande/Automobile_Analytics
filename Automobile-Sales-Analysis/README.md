# Automobile Raw Material Impact Analysis
## How Raw Material Verticals Drive Production Planning, Quality & Pricing

**Author:** Chaitanya Lande | Great Lakes Institute of Management, Chennai  
**Specialization:** Analytics & Operations (PGDM)  
**Context:** Data Science Internship at BrainOvision Solutions Pvt. Ltd (Jan–Mar 2024)

---

## Project Overview
Analyzed raw material procurement data across 6 manufacturing verticals for an automobile OEM (Company XYZ) to quantify how supplier performance, material quality grades, lead time variability, and commodity price volatility propagate through the production system — affecting production scheduling efficiency, vehicle quality outcomes, and final variant pricing decisions.

## Tech Stack
- **Data Engineering & Analysis:** Python (Pandas, NumPy, SciPy)
- **Machine Learning:** Scikit-Learn, XGBoost, SHAP
- **Visualization:** Matplotlib, Seaborn, Tableau
- **AI Integration:** GenAI-powered production advisory engine
- **Interactive Demo:** Streamlit web application

## Manufacturing Verticals Analyzed
| Vertical | Components | Typical Impact |
|:---|:---|:---|
| Body & Structural | Steel sheets, Aluminum panels, Stampings | Frame integrity, crash safety rating |
| Powertrain | Engine blocks, Transmission assemblies, Drivetrain | Performance specs, fuel efficiency |
| Interior | Plastics, Leather, Fabric, Dashboard modules | Variant tier (Base/Mid/Top), comfort rating |
| Electrical & Electronics | Wiring harnesses, Sensors, ECUs, Infotainment | Feature availability, ADAS capability |
| Suspension & Chassis | Springs, Shock absorbers, Axles, Brakes | Ride quality, handling score |
| Tyres & Rubber | Tyres, Seals, Bushings, Hoses | Safety compliance, NVH performance |

## Key Findings
- **Electrical & Electronics** vertical causes **42% of all production delays** despite being only 18% of BOM cost
- **Supplier quality grade** is the strongest predictor of final vehicle quality score (SHAP importance = 28.4%)
- **Steel price volatility** (±12% quarterly swing) directly compresses Economy variant margins by 3.8 percentage points
- **Lead time variance > 5 days** in any critical-path vertical triggers a **23% increase in production downtime**
- Top-performing suppliers (Grade A) deliver **67% fewer defects** than Grade C suppliers

## Project Structure
```
Automobile-Sales-Analysis/
├── data/
│   ├── raw/                          # Generated datasets
│   │   ├── raw_materials_master.csv  # 200 materials × 6 verticals
│   │   ├── production_batches.csv    # 5,000 production batches
│   │   ├── material_consumption.csv  # 60,000 material usage records
│   │   ├── supplier_performance.csv  # Monthly supplier KPIs
│   │   └── commodity_prices.csv      # Monthly commodity price indices
│   └── processed/                    # Cleaned & engineered data
├── notebooks/
│   ├── 01_data_cleaning.py           # Cleaning, validation, feature engineering
│   ├── 02_eda_analysis.py            # Vertical-wise EDA & statistical tests
│   ├── 03_ml_modeling.py             # Quality prediction, delay classification, SHAP
│   └── 04_genai_insights.py          # AI-powered production advisory
├── tableau/                          # Dashboard blueprints & mockups
├── app/
│   └── streamlit_app.py              # Interactive demo application
├── requirements.txt
└── README.md
```

## How to Run
```powershell
cd "C:\Users\Omkar Computers\Desktop\Resume Projects\Automobile-Sales-Analysis"
python -m streamlit run app\streamlit_app.py
```
