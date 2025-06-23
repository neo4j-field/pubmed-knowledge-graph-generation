
# 📚 User Stories – PubMed Knowledge Graph

This document outlines user stories related to the PubMed Knowledge Graph project, based on the Lead Data Scientist and Clinician personas at Solara Health.

---

## 👨‍🔬 Lead Data Scientist (Kansas-based)

### **User Story 1: Evidence-Backed Protocol Evaluation**
As a Lead Data Scientist, I want to aggregate clinical outcomes from PubMed articles into a graph structure, so that I can evaluate whether the protocols Solara currently uses are aligned with the most up-to-date and effective clinical practices.

### **User Story 2: Pattern Mining Across Studies**
As a Lead Data Scientist, I want to apply graph algorithms (e.g., similarity, centrality, influence) over the PubMed graph so I can identify treatment patterns or drug combinations that consistently correlate with positive outcomes.

### **User Story 3: Support Formulary Expansion Decisions**
As a Lead Data Scientist, I want to rank underused or emerging medications based on frequency of successful outcomes in similar populations, so I can make data-driven recommendations for expanding or refining our drug formulary.

### **User Story 4: LLM-Powered Summarization and Comparison**
As a Lead Data Scientist, I want to use an LLM orchestrated with LangGraph to automatically summarize evidence from literature and compare outcomes across protocols, so I can provide clinical stakeholders with clear, evidence-based comparisons.

---

## 🧑‍⚕️ Clinician (Virginia-based)

### **User Story 1: Protocol Review Based on Literature**
As a Clinician, I want to see how a given protocol compares to others in terms of outcomes reported in the clinical literature, so I can advocate for more effective, evidence-based approaches in our care models.

### **User Story 2: Identify Candidates for Protocol Refinement**
As a Clinician, I want to find protocols that are underperforming for certain patient segments and review what alternative protocols the literature suggests, so I can propose protocol refinements for our member population.

### **User Story 3: Explain Protocol Decisions with Evidence**
As a Clinician, I want to quickly retrieve PubMed-supported justifications for a particular protocol or formulary recommendation, so I can communicate the rationale clearly to patients and care managers.

### **User Story 4: Explore Outcomes for Similar Patients**
As a Clinician, I want to explore treatment outcomes reported in studies that match my patient’s condition and demographics, so I can personalize my care recommendations with supporting evidence.
