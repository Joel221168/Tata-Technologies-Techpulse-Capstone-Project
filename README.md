# 🚗 AUTOSAR HLD Architecture Analysis Assistant
> **TechPulse FY-26 Capstone Project | Case Study 1**  
> **Student:** Joel Emmanuel (PRN: 123B1D022) | **Institute:** PCCOE, Pune  

An end-to-end Document AI and GraphRAG platform engineered to analyze multi-page AUTOSAR High-Level Design (HLD) specifications. The system combines layout-aware PDF ingestion, dense vector search with grounded page citations, interactive software component topology graphs, and deterministic architectural health auditing.

---

## 🌟 Key Features

* **🔍 Layout-Aware Grounded RAG (Tab 1):** Extracts narrative paragraphs without losing page context. Answers architectural queries with explicit source page attribution (e.g., `Citation: AUTOSAR_EMS_HLD_v1.0.pdf (Page 2)`).
* **📊 Signal Matrix Parsing & Export (Tab 2):** Bypasses unstructured token chunking to preserve signal mapping tables, offering live data grid rendering and one-click CSV export.
* **🕸️ GraphRAG Component Topology (Tab 3):** Transforms tabular component-to-component mappings into an interactive 2D directed network graph (`NetworkX` + `Pyvis`) for visual signal path tracing.
* **🛡️ Architecture Health Audit (Tab 4):** Employs a deterministic rule engine to automatically flag orphaned signals (`Target SWC == 'UNMAPPED'`) with zero false positives or LLM hallucinations.
* **🔒 100% Private & Local Execution:** Powered by locally hosted embedding models (`all-MiniLM-L6-v2`) and local vector storage (`ChromaDB`) with zero cloud API dependencies.

---

## 🏗️ System Architecture
