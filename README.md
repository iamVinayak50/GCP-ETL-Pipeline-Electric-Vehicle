# 🚗 EV Real-Time Telemetry Data Pipeline (High-Level Overview)

This project demonstrates an end-to-end **real-time data engineering pipeline** on Google Cloud Platform (GCP) for processing Electric Vehicle (EV) telemetry data.  
The goal is to show how EV data can be collected, processed, cleaned, stored, transformed, and visualized in real time.

---

## 🔎 1. Business Need (Why this project?)

Modern Electric Vehicles continuously generate telemetry such as:
- GPS location  
- Battery status (SOC/SOH)  
- Speed & odometer  
- Motor temperature  
- Charging activity  

The business needs to:
- Monitor vehicle health  
- Improve battery performance  
- Detect issues early (overheating, low SOC, faults)  
- Analyze driving patterns  
- Create dashboards for operations teams  

This project provides a **real-time platform** to support these analytics.

---

## 📡 2. High-Level Architecture


### Component Overview
- **Pub/Sub**: Receives live telemetry events.
- **Dataflow (Streaming)**: Cleans, validates, and processes each message.
- **BigQuery Bronze**: Stores raw but structured events.
- **Dataform (Silver)**: Cleans, deduplicates, and standardizes data.
- **Dataform (Gold)**: Creates aggregated tables for dashboards.
- **Tableau**: Visualizes battery performance, charging, model metrics, etc.

---

## 🛠️ 3. Pipeline Summary

### **1. Ingestion (Pub/Sub)**
The EV backend publishes real-time messages to a Pub/Sub topic.

### **2. Processing (Dataflow Streaming)**
Dataflow performs:
- JSON parsing  
- Field validation  
- Type conversions  
- Dropping invalid data  
- Writing valid rows into BigQuery  

### **3. Storage (BigQuery Bronze Layer)**
Raw structured data is stored in a partitioned BigQuery table.

### **4. Transformation (Dataform)**
Dataform manages SQL transformations:
- **Silver layer**: cleansed & validated data  
- **Gold layer**: aggregated metrics for dashboards  

### **5. Dashboarding (Tableau)**
Final “Gold” tables are used in Tableau dashboards for:
- Vehicle performance  
- Battery health  
- Charging behavior  
- Model-level insights  

---

## 📊 4. What the Dashboard Shows

- Battery SOC trends  
- SOH degradation  
- Charging vs driving patterns  
- Motor temperature distribution  
- Model-level summary metrics  
- Fleet status overview  

---

## 🔍 5. Monitoring & Data Quality (High Level)

The project includes:
- Validation rules in Dataflow  
- Basic checks in Silver (GPS range, SOC 0–100, temp limits)  
- Cloud Monitoring alerts (pipeline failures, subscription lag)  
- BigQuery partitioning for performance and governance  

---

## ✔️ 6. Key Skills Demonstrated

- Real-time streaming pipelines  
- BigQuery modeling (Bronze → Silver → Gold)  
- Dataform workflow automation  
- Data quality governance  
- Dashboarding using Tableau  
- End-to-end GCP data engineering architecture  

---

## 📦 7. Technology Stack

- **Google Pub/Sub**  
- **Apache Beam / Dataflow**  
- **BigQuery**  
- **Dataform**  
- **Python**  
- **Tableau Desktop**  

---

## 🎯 Summary

This project is a complete, interview-ready real-time data engineering solution showing how EV telemetry moves from ingestion → processing → storage → transformation → visualization on GCP.

