# worker/contract_parser.py
import pdfplumber
import re

def parse_contract(contract_path: str, contract_name: str) -> dict:
    """
    Extracts structured info from a contract PDF.
    Returns dict with confidence scores.
    """
    text = ""
    with pdfplumber.open(contract_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    result = {
        "contract_name": contract_name,
        "contract_id": re.search(r"Contract ID:\s*(.*)", text).group(1).strip() if re.search(r"Contract ID:", text) else None,
        "effective_date": re.search(r"Effective Date:\s*(.*)", text).group(1).strip() if re.search(r"Effective Date:", text) else None,
        "term": re.search(r"Contract Term:\s*(.*)", text).group(1).strip() if re.search(r"Contract Term:", text) else None,
        "service_provider": re.search(r"Service Provider:\s*(.*)", text).group(1).strip() if re.search(r"Service Provider:", text) else None,
        "customer": re.search(r"Customer:\s*(.*)", text).group(1).strip() if re.search(r"Customer:", text) else None,
        "total_value": re.search(r"Total Annual Value:\s*\$?([\d,\.]+)", text).group(1).strip() if re.search(r"Total Annual Value:", text) else None,
        "payment_terms": re.search(r"Payment Terms:\s*(.*)", text).group(1).strip() if re.search(r"Payment Terms:", text) else None,
    }

    result_with_confidence = {
        field: {"value": val, "confidence": 0.9 if val else 0.0} 
        for field, val in result.items()
    }

    return result_with_confidence
    