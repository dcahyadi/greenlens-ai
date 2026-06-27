"""GreenLens AI — Ingestion unit tests"""
import pytest
from ingestion.metadata import DOCUMENT_METADATA
from ingestion.indexer import get_splitter

REQUIRED_FIELDS = {"category", "language", "year", "regulation", "issuer", "status"}
VALID_CATEGORIES = {
    "carbon_market", "renewable_energy", "energy_transition",
    "environmental_law", "climate_commitment", "green_finance"
}
VALID_FOLDERS = {"carbon", "esdm", "jetp", "klhk", "ndc", "ojk"}


def test_all_docs_have_required_fields():
    for doc_key, meta in DOCUMENT_METADATA.items():
        missing = REQUIRED_FIELDS - set(meta.keys())
        assert not missing, f"Missing fields in {doc_key}: {missing}"


def test_all_categories_are_valid():
    for doc_key, meta in DOCUMENT_METADATA.items():
        assert meta["category"] in VALID_CATEGORIES, \
            f"Invalid category '{meta['category']}' in {doc_key}"


def test_all_years_are_reasonable():
    for doc_key, meta in DOCUMENT_METADATA.items():
        assert 2000 <= meta["year"] <= 2030, f"Suspicious year {meta['year']} in {doc_key}"


def test_all_doc_keys_have_valid_folder():
    for doc_key in DOCUMENT_METADATA:
        folder = doc_key.split("/")[0]
        assert folder in VALID_FOLDERS, f"Unknown folder '{folder}' in: {doc_key}"


def test_faq_uses_smaller_chunks():
    faq = get_splitter("ojk/tkbi-faq.pdf")
    reg = get_splitter("ndc/enhanced-ndc-2022-en.pdf")
    assert faq._chunk_size < reg._chunk_size


def test_factsheet_uses_smaller_chunks():
    fs = get_splitter("ojk/tkbi-fact-sheets.pdf")
    reg = get_splitter("carbon/perpres-98-2021-en.pdf")
    assert fs._chunk_size < reg._chunk_size


def test_metadata_count():
    # Ensure all expected documents are registered
    assert len(DOCUMENT_METADATA) >= 18, "Expected at least 18 documents in registry"
