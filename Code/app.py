import os
import pdfplumber
import pandas as pd
import streamlit as st
import networkx as nx
import streamlit.components.v1 as components
from pyvis.network import Network
import chromadb
from chromadb.utils import embedding_functions

st.set_page_config(page_title="AUTOSAR HLD AI Assistant", page_icon="🚗", layout="wide")
st.title("🚗 AUTOSAR HLD Architecture Analysis Assistant")
st.caption("TechPulse FY-26 Capstone | Case Study 1: AUTOSAR Document AI")

@st.cache_resource
def get_vector_store():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return chroma_client.get_or_create_collection(name="autosar_hld", embedding_function=emb_fn)

collection = get_vector_store()

def process_pdf(pdf_path):
    chunks, tables_data = [], []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                chunks.append({"id": f"page_{page_num}", "text": text, "metadata": {"page": page_num, "source": os.path.basename(pdf_path)}})
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                tables_data.append({"page": page_num, "df": df})
    return chunks, tables_data

with st.sidebar:
    st.header("📄 Document Ingestion")
    uploaded_file = st.file_uploader("Upload AUTOSAR HLD (PDF)", type=["pdf"])
    if uploaded_file:
        save_path = os.path.join("../Input_Data", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        if st.button("Index Document"):
            chunks, tables = process_pdf(save_path)
            collection.add(
                ids=[c["id"] for c in chunks],
                documents=[c["text"] for c in chunks],
                metadatas=[c["metadata"] for c in chunks]
            )
            st.session_state["tables"] = tables
            st.success(f"Indexed {len(chunks)} pages successfully!")

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📊 Signal Matrix", "🕸️ Graph", "🛡️ Health Audit"])

with tab1:
    query = st.text_input("Ask a question about components or signals:")
    if query:
        results = collection.query(query_texts=[query], n_results=2)
        if results and results["documents"]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                st.info(f"**Citation:** {meta['source']} (Page {meta['page']})")
                st.write(doc)

with tab2:
    if "tables" in st.session_state:
        for t in st.session_state["tables"]:
            st.write(f"**Table from Page {t['page']}**")
            st.dataframe(t["df"], use_container_width=True)

with tab3:
    if "tables" in st.session_state:
        G = nx.DiGraph()
        for t in st.session_state["tables"]:
            df = t["df"]
            if "Source SWC" in df.columns and "Target SWC" in df.columns:
                for _, row in df.iterrows():
                    if row["Source SWC"] and row["Target SWC"]:
                        G.add_edge(row["Source SWC"], row["Target SWC"], title=row.get("Signal Name", ""))
        net = Network(height="400px", width="100%", directed=True)
        net.from_nx(G)
        net.save_graph("graph.html")
        with open("graph.html", "r") as f:
            components.html(f.read(), height=450)

with tab4:
    if st.button("Run Architecture Audit"):
        issues = []
        if "tables" in st.session_state:
            for t in st.session_state["tables"]:
                for idx, row in t["df"].iterrows():
                    if row.get("Target SWC") == "UNMAPPED":
                        issues.append({
                            "Severity": "HIGH",
                            "Type": "Orphaned Signal",
                            "Description": f"Signal '{row.get('Signal Name')}' has no target consumer.",
                            "Page": t["page"]
                        })
            st.error(f"Found {len(issues)} Defect(s):")
            st.table(pd.DataFrame(issues))
