
# 🔗 Solara Health Graph Integration: Structured and Unstructured Data

## 📁 Purpose

This document describes the structure and purpose of the **Cypher scripts** and **CSV data files** used to build a unified graph model that integrates:
- **Structured patient journey data** from Solara Health
- **Unstructured evidence from PubMed articles**

The goal is to **identify correlations and clinical insights** across both domains—linking Solara members to evidence-supported protocols, treatments, comorbidities, and outcomes.

---

## 📦 Files Overview

### 🧮 CSV File: `extended_patient_journey.csv`
This file contains synthetic patient journey data representing member demographics, diagnoses, procedures, treatments, lab results, and outcomes.

| Column | Description |
|--------|-------------|
| `member_id` | Unique patient ID |
| `age`, `sex`, `zip_code` | Demographic attributes |
| `diagnosis`, `diagnosis_code` | Primary diagnosis (e.g., T2D or HTN) |
| `procedure_code`, `procedure_name` | Procedure performed (e.g., HbA1c Test) |
| `medications` | List of medications given during the visit |
| `visit_date` | Date of visit |
| `lab_test`, `lab_loinc`, `lab_value` | Lab test details (e.g., A1C) |
| `outcome` | Outcome based on lab result (e.g., Controlled/Not Controlled) |

---

### 🕸 Cypher Files

#### `demo_load_patient_journey.cypher`
- Creates a basic subset of members and their associated nodes (conditions, drugs, procedures, labs, demographics).
- Designed for quick local testing and visualization.

#### `load_extended_journey_csv.cypher`
- Uses `LOAD CSV` to import all rows from `extended_patient_journey.csv`.
- Builds relationships between members and clinical entities:
  - `(:Member)-[:TAKES]->(:Drug)`
  - `(:Member)-[:HAS_DIAGNOSIS]->(:Condition)`
  - `(:Member)-[:UNDERWENT]->(:Procedure)`
  - `(:Member)-[:HAS_LAB]->(:LabResult)`
  - `(:Member)-[:ACHIEVES]->(:Outcome)`
  - `(:Member)-[:HAS_DEMO]->(:Demographic)`

---

## 🔍 Reasoning: Linking to PubMed Evidence

### Why This Graph Structure?

This model enables:
- **Patient similarity analysis** using shared structure (e.g., same drugs, labs, demographics)
- **Cross-domain mapping** of Solara members to PubMed study subjects

### Example Use Case

1. A Solara member has Type 2 Diabetes and is taking Metformin and GLP-1.
2. Their graph profile includes:
   - `(:Member)-[:HAS_DIAGNOSIS]->(:Condition {name: 'Type 2 Diabetes'})`
   - `(:Member)-[:TAKES]->(:Drug {name: 'GLP-1'})`
3. A PubMed article describes a cohort with the same profile and observes cardiovascular benefits.
4. Using graph similarity algorithms, Solara identifies this match and flags it for:
   - **Protocol confirmation or refinement**
   - **Formulary expansion consideration**
   - **Risk awareness (e.g., side effects reported)**

---

## 🌉 Outcome

This integrated graph approach allows Solara Health to:
- Detect best-performing protocols outside their current system
- Match members to evidence in the literature based on full clinical context—not just diagnosis codes
- Suggest new therapies or protocol modifications using defensible, data-backed evidence

