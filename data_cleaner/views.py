from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import fetch_data, normalize_record, remove_duplicates
import requests
import os

API_BASE = os.getenv("LUMICORE_API", "https://fast-endpoint-production.up.railway.app")
CANDIDATE_ID = os.getenv("CANDIDATE_ID", "candidate-mohammedanas-abc123")


# ------------------------
# Fetch raw data
# ------------------------
@api_view(['GET'])
def get_raw_data(request, batch=1):
    data = fetch_data(batch)
    if data is None:
        return Response({"error": "Failed to fetch data"}, status=500)
    return Response(data)


# ------------------------
# Fetch cleaned/normalized data
# ------------------------
@api_view(['GET'])
def get_cleaned_data(request, batch=1):
    raw_response = fetch_data(batch)
    if not raw_response:
        return Response({"error": "Failed to fetch data"}, status=500)

    records = raw_response.get("records", [])
    cleaned = [normalize_record(r) for r in records]
    cleaned = remove_duplicates(cleaned)

    return Response(cleaned)



# ------------------------
# Submit cleaned data
# ------------------------
@api_view(['POST'])
def submit_cleaned_data(request):
    url = f"{API_BASE}/api/submit"
    payload = {
        "candidate_name": "Mohammed Anas",
        "batch_id": request.data.get("batch_id"),
        "cleaned_items": request.data.get("cleaned_items")
    }
    headers = {
        "Content-Type": "application/json",
        "X-Candidate-Id": CANDIDATE_ID
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return Response(response.json(), status=response.status_code)
    except requests.RequestException as e:
        return Response({"error": str(e)}, status=500)
