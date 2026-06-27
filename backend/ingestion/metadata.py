"""Document metadata registry — used to tag every chunk during ingestion."""

DOCUMENT_METADATA: dict[str, dict] = {
    "carbon/perpres-98-2021-en.pdf": {
        "category": "carbon_market", "language": "en", "year": 2021,
        "regulation": "Perpres 98/2021", "issuer": "President of Indonesia", "status": "active",
        "topics": ["carbon_pricing", "carbon_trading", "ndc_implementation"],
    },
    "carbon/perpres-98-2021-id.pdf": {
        "category": "carbon_market", "language": "id", "year": 2021,
        "regulation": "Perpres 98/2021", "issuer": "President of Indonesia", "status": "active",
        "topics": ["carbon_pricing", "carbon_trading", "ndc_implementation"],
    },
    "carbon/perpres-110-2025-id.pdf": {
        "category": "carbon_market", "language": "id", "year": 2025,
        "regulation": "Perpres 110/2025", "issuer": "President of Indonesia", "status": "active",
        "topics": ["carbon_pricing", "grk_control", "ndc_implementation"],
    },
    "carbon/pojk-14-2023-id-carbon-trading.pdf": {
        "category": "carbon_market", "language": "id", "year": 2023,
        "regulation": "POJK 14/2023", "issuer": "OJK", "status": "active",
        "topics": ["carbon_exchange", "carbon_trading", "idx_carbon"],
    },
    "esdm/permen-esdm-2-2024.pdf": {
        "category": "renewable_energy", "language": "id", "year": 2024,
        "regulation": "Permen ESDM 2/2024", "issuer": "Ministry of Energy and Mineral Resources", "status": "active",
        "topics": ["plts_atap", "rooftop_solar", "net_metering"],
    },
    "esdm/perpres-112-2022.pdf": {
        "category": "renewable_energy", "language": "id", "year": 2022,
        "regulation": "Perpres 112/2022", "issuer": "President of Indonesia", "status": "active",
        "topics": ["renewable_energy", "ebt_acceleration", "coal_phaseout"],
    },
    "jetp/jetp-cipp-2023.pdf": {
        "category": "energy_transition", "language": "en", "year": 2023,
        "regulation": "JETP CIPP 2023", "issuer": "JETP Secretariat", "status": "active",
        "topics": ["jetp", "investment_plan", "coal_retirement", "renewable_energy"],
    },
    "jetp/jetp-progress-report-2025-en.pdf": {
        "category": "energy_transition", "language": "en", "year": 2025,
        "regulation": "JETP Progress Report 2025", "issuer": "JETP Secretariat", "status": "active",
        "topics": ["jetp", "implementation_status", "financing", "milestones"],
    },
    "jetp/jetp-progress-report-2025-id.pdf": {
        "category": "energy_transition", "language": "id", "year": 2025,
        "regulation": "JETP Progress Report 2025", "issuer": "JETP Secretariat", "status": "active",
        "topics": ["jetp", "implementation_status", "financing", "milestones"],
    },
    "klhk/permen-LHK-4-2021.pdf": {
        "category": "environmental_law", "language": "id", "year": 2021,
        "regulation": "PermenLHK 4/2021", "issuer": "Ministry of Environment and Forestry", "status": "active",
        "topics": ["amdal", "ukl_upl", "sppl", "environmental_permit"],
    },
    "klhk/permen-LHK-21-2022.pdf": {
        "category": "environmental_law", "language": "id", "year": 2022,
        "regulation": "PermenLHK 21/2022", "issuer": "Ministry of Environment and Forestry", "status": "active",
        "topics": ["carbon_nek", "carbon_trading", "nek_implementation"],
    },
    "klhk/pp-22-2021.pdf": {
        "category": "environmental_law", "language": "id", "year": 2021,
        "regulation": "PP 22/2021", "issuer": "Government of Indonesia", "status": "active",
        "topics": ["amdal", "environmental_protection", "environmental_permit"],
    },
    "ndc/enhanced-ndc-2022-en.pdf": {
        "category": "climate_commitment", "language": "en", "year": 2022,
        "regulation": "Enhanced NDC 2022", "issuer": "Government of Indonesia / UNFCCC", "status": "active",
        "topics": ["ndc", "emission_reduction", "mitigation", "adaptation"],
    },
    "ndc/updated-ndc-2021-en.pdf": {
        "category": "climate_commitment", "language": "en", "year": 2021,
        "regulation": "Updated NDC 2021", "issuer": "Government of Indonesia / UNFCCC", "status": "superseded",
        "topics": ["ndc", "emission_reduction", "mitigation", "adaptation"],
    },
    "ojk/tkbi-ver3-2026-en.pdf": {
        "category": "green_finance", "language": "en", "year": 2026,
        "regulation": "TKBI Version 3 2026", "issuer": "OJK", "status": "active",
        "topics": ["green_taxonomy", "sustainable_finance", "green_bonds", "esg"],
    },
    "ojk/tkbi-ver3-2026-id.pdf": {
        "category": "green_finance", "language": "id", "year": 2026,
        "regulation": "TKBI Version 3 2026", "issuer": "OJK", "status": "active",
        "topics": ["green_taxonomy", "sustainable_finance", "green_bonds", "esg"],
    },
    "ojk/tkbi-fact-sheets.pdf": {
        "category": "green_finance", "language": "en", "year": 2026,
        "regulation": "TKBI Fact Sheets", "issuer": "OJK", "status": "active",
        "topics": ["green_taxonomy", "summary", "quick_reference"],
    },
    "ojk/tkbi-faq.pdf": {
        "category": "green_finance", "language": "en", "year": 2026,
        "regulation": "TKBI FAQ", "issuer": "OJK", "status": "active",
        "topics": ["green_taxonomy", "faq", "practical_guidance"],
    },
}
