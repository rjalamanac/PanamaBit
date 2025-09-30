#!/usr/bin/env python3
"""
Demo Spark processing for ContractStore (conceptual)
"""

import os
from pyspark.sql import SparkSession
from pathlib import Path
from contract_utils import pdf_to_text, split_by_headings, extract_entities, CHUNK_WORD_SIZE

# -----------------------------
# CONFIG
# -----------------------------
PDF_FOLDER = os.getenv("PDF_FOLDER", "wasbs://<container>@<storage_account>.blob.core.windows.net/contracts/")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "./spark_output")

# -----------------------------
# SPARK SESSION
# -----------------------------
spark = SparkSession.builder \
    .appName("ContractStoreBuilder") \
    .config("spark.hadoop.fs.azure.account.key.<storage_account>.blob.core.windows.net",
            os.getenv("AZURE_STORAGE_KEY")) \
    .getOrCreate()

sc = spark.sparkContext

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def process_pdf(pdf_path: str):
    """Process a single PDF: OCR -> split -> extract metadata"""
    try:
        text = pdf_to_text(pdf_path)
        blocks = split_by_headings(text, ["Contrato", "Cláusula", "Artículo"])
        meta_list = []
        for i, block in enumerate(blocks):
            meta = {
                "doc_name": Path(pdf_path).name,
                "chunk_id": f"{Path(pdf_path).name}__{i}"
            }
            meta_list.append((block, meta))
        return meta_list
    except Exception as e:
        print(f"[WARN] Failed PDF {pdf_path}: {e}")
        return []

# -----------------------------
# DISTRIBUTED PROCESSING
# -----------------------------
# Step 1: Create an RDD of PDF paths
pdf_files = sc.parallelize([f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")])

# Step 2: Process each PDF in parallel
chunks_with_meta = pdf_files.flatMap(lambda f: process_pdf(os.path.join(PDF_FOLDER, f)))

# Step 3: Collect or save results (demo)
results = chunks_with_meta.collect()  # In prod, save to Parquet / Blob
print(f"[INFO] Processed {len(results)} chunks")

# -----------------------------
# STOP SPARK
# -----------------------------
spark.stop()
