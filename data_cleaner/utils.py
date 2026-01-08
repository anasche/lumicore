import requests
import time
from datetime import datetime
import re

API_BASE = "https://fast-endpoint-production.up.railway.app"
CANDIDATE_ID = "candidate-mohammed-anas-x7k2"

# ------------------------
# Field mappings (for reference)
# ------------------------
FIELD_MAPPING = {
    "doc_id": ["id", "documentId", "ref", "document_ref", "doc_number"],
    "type": ["docType", "category", "document_type", "doc_category"],
    "counterparty": ["vendorName", "supplier", "partyA", "vendor", "party_name"],
    "project": ["projectName", "project_name", "proj", "meta.project"],
    "expiry_date": ["expiry", "expiryDate", "end_date", "valid_till", "expires_on", "expiration"],
    "amount": ["value", "contractValue", "amount_aed", "total", "contract_amount"]
}

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%b %d %Y", "%d %b %Y", "%Y%m%d"]

# ------------------------
# Fetch data from LumiCore API with retry logic
# ------------------------
def fetch_data(batch=1, retries=3, delay=0.5):
    url = f"{API_BASE}/api/data?batch={batch}"
    headers = {"X-Candidate-Id": CANDIDATE_ID}
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        time.sleep(delay * (2 ** i))  # exponential backoff
    return None

# ------------------------
# Parse date to ISO format YYYY-MM-DD
# ------------------------
def parse_expiry_date(date_value):
    if not date_value:
        return None

    date_str = str(date_value).strip()

    # 1️⃣ ISO format: 2026-02-01
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return date_str

    # 2️⃣ Compact format: 20260201
    if re.match(r"^\d{8}$", date_str):
        try:
            return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
        except:
            return None

    # 3️⃣ DD/MM/YYYY (preferred)
    if "/" in date_str:
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            return None

    # 4️⃣ DD-MM-YYYY
    if "-" in date_str:
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
        except:
            return None

    # 5️⃣ Month name formats: "01 Feb 2026" or "Feb 01 2026"
    for fmt in ["%d %b %Y", "%b %d %Y"]:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except:
            continue

    return None

# ------------------------
# Clean amount field (remove AED, commas, spaces)
# ------------------------
def clean_amount(amount_value):
    if amount_value is None:
        return None
    if isinstance(amount_value, (int, float)):
        return int(amount_value)
    amount_str = str(amount_value)
    # Extract digits only
    digits = re.findall(r"\d+", amount_str)
    if digits:
        return int("".join(digits))
    return None

# ------------------------
# Normalize a single record
# ------------------------
def normalize_record(record):
    if not isinstance(record, dict):
        return None

    doc_id = (
        record.get("document_ref")
        or record.get("documentId")
        or record.get("ref")
        or record.get("doc_number")
    )
    record_type = (
        record.get("docType")
        or record.get("doc_category")
        or record.get("document_type")
        or record.get("category")
    )
    counterparty = (
        record.get("counterparty")
        or record.get("party_name")
        or record.get("partyA")
        or record.get("vendor")
        or record.get("supplier")
        or record.get("vendorName")
    )
    project = record.get("project") or record.get("meta", {}).get("project")
    
    # Parse date and amount using our helper functions
    expiry_date = parse_expiry_date(
        record.get("expiration")
        or record.get("end_date")
        or record.get("expires_on")
        or record.get("valid_till")
        or record.get("expiry")
    )
    amount = clean_amount(
        record.get("amount")
        or record.get("total")
        or record.get("value")
        or record.get("contract_amount")
    )

    return {
        "doc_id": doc_id,
        "type": record_type,
        "counterparty": counterparty,
        "project": project,
        "expiry_date": expiry_date,
        "amount": amount
    }

# ------------------------
# Remove duplicates by doc_id
# ------------------------
def remove_duplicates(records):
    seen = set()
    unique = []
    for rec in records:
        doc_id = rec.get("doc_id")
        if doc_id not in seen:
            seen.add(doc_id)
            unique.append(rec)
    return unique
