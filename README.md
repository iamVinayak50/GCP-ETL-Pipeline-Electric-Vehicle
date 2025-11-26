# 🚗🔋 EV Telemetry Real-Time Data Platform (GCP End-to-End Project)

A complete real-time EV (Electric Vehicle) telemetry data pipeline built on **Google Cloud Platform** using:

- Pub/Sub (real-time ingestion)  
- Dataflow (stream processing)  
- BigQuery (Bronze → Silver → Gold)  
- Dataform (transformations, SQL automation)  
- Cloud Monitoring (data quality & pipeline alerts)  
- Tableau (dashboards and visualizations)  

This project simulates a real-world scenario where an automotive company wants to **monitor EV performance, battery health, GPS movement, and system alerts** in real time.

---

# 🧩 **1. Business Goal**

The business needs **real-time visibility** into electric vehicle performance:

- Monitor motor temperature, battery SOC/SOH  
- Track vehicle location and speed  
- Detect charging patterns  
- Identify faults or overheating  
- Generate operational dashboards  
- Enable long-term analytics & forecasting  

This platform provides **clean, governed, high-quality data** for both real-time dashboards and analytics.

---

# ⚙️ **2. Architecture Overview**


### **Key Components**
| Layer | Purpose |
|-------|---------|
| **Pub/Sub** | Ingest raw real-time telemetry |
| **Dataflow** | Validations, cleaning, type casting |
| **BigQuery Bronze** | Raw partitioned storage layer |
| **Dataform** | SQL transformations (Silver/Gold) |
| **BigQuery Silver** | Clean, validated, deduplicated data |
| **BigQuery Gold** | Aggregated business metrics |
| **Tableau** | Dashboards for fleet performance |

---

# 📥 **3. Data Ingestion — Pub/Sub**

Telemetry fields received from EV:

- `vin`
- `vehicle_model`
- `timestamp`
- `gps_lat`, `gps_lon`
- `speed_kmph`
- `odometer_km`
- `state_of_charge_percent`
- `state_of_health_percent`
- `motor_temp_c`
- `charging_state`
- `charging_power_kw`

A Pub/Sub subscription triggers Dataflow streaming pipeline.

---

# 🔄 **4. Real-Time Processing — Dataflow**

Dataflow performs:

- JSON parsing  
- Schema validation  
- Missing field handling  
- Numeric type conversion  
- Range validations  
- Dropping invalid messages  
- Adding ingestion timestamp  
- Writing to **Bronze BigQuery table**

### **Bronze Table**
