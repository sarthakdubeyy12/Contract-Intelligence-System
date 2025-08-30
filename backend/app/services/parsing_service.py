import fitz  # PyMuPDF
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text


def extract_contract_details(text: str) -> dict:
    """Extract structured contract details using NLP + regex."""
    doc = nlp(text)

    parties = []
    financials = []
    payment_terms = None
    sla = None

    # --- Parties (ORG + PERSON) ---
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON"]:
            if ent.text not in parties:
                parties.append(ent.text)

    # --- Financials (Currency + Amounts) ---
    money_regex = r"\$?\d+(?:,\d{3})*(?:\.\d{2})?"
    financials = re.findall(money_regex, text)

    # --- Payment Terms ---
    payment_regex = r"(payment(?: terms)?[:\s].{0,80})"
    match = re.search(payment_regex, text, re.IGNORECASE)
    if match:
        payment_terms = match.group(1)

    # --- SLA (Service Level Agreement terms) ---
    sla_regex = r"(SLA[:\s].{0,120})"
    match = re.search(sla_regex, text, re.IGNORECASE)
    if match:
        sla = match.group(1)

    return {
        "parties": parties,
        "financials": financials,
        "payment_terms": payment_terms,
        "sla": sla
    }


def parse_contract_pdf(pdf_path: str) -> dict:
    """Full pipeline: PDF → Text → Extracted Fields."""
    text = extract_text_from_pdf(pdf_path)
    extracted = extract_contract_details(text)
    return {
        "raw_text": text,
        "extracted": extracted
    }