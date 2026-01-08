LUMICORE BACKEND – DATA CLEANING API

This project is a Django REST Framework–based backend service that fetches raw data from an external LumiCore API, normalizes and cleans the data, removes duplicates, and submits the cleaned data back to the API.

FEATURES

• Fetch raw data from an external API
• Normalize inconsistent field names
• Standardize date formats
• Clean currency and amount values
• Remove duplicate records
• Submit cleaned data securely
• Centralized environment configuration
• Retry logic with exponential backoff

TECH STACK

• Python 3.10+
• Django
• Django REST Framework
• Requests
• dotenv / OS environment variables

SETUP INSTRUCTIONS

Clone the repository

git clone https://github.com/your-username/lumicore-backend.git

cd lumicore-backend

Create and activate a virtual environment

python -m venv venv

macOS / Linux:
source venv/bin/activate

Windows:
venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Environment variables setup

Create a .env file in the project root directory.

Run the server

python manage.py runserver

The server will start at:
http://127.0.0.1:8000/

ENVIRONMENT VARIABLES

All environment variables are centralized in:
lumicore_backend/env.py

Example .env file:

External API

BASE_API=https://fast-endpoint-production.up.railway.app

CANDIDATE_ID=candidate-your-id-here

ENVIRONMENT VARIABLE DESCRIPTION

BASE_API
→ Base URL of the LumiCore external API

CANDIDATE_ID
→ Unique candidate identifier (Required)

NOTE:
CANDIDATE_ID is mandatory. The application will fail if it is missing.

API ENDPOINTS

Get Raw Data

GET /api/raw-data/?batch=1

Returns the raw response from the external API.

Get Cleaned Data

GET /api/cleaned-data/?batch=1

Returns:
• Normalized fields
• Standardized date formats
• Cleaned numeric values
• Duplicate-free records

Submit Cleaned Data

POST /api/submit/

Request Body:

{
"batch_id": 1
}

Note:
The backend re-fetches and cleans data before submission to ensure data integrity.

DATA CLEANING & NORMALIZATION LOGIC

Normalized Fields Mapping:

doc_id
→ id, documentId, ref, doc_number

type
→ docType, category, document_type

counterparty
→ vendorName, supplier, partyA

project
→ project, meta.project

expiry_date
→ expiry, end_date, expires_on

amount
→ value, total, contract_amount

DATE HANDLING

Supported date formats:
• YYYY-MM-DD
• DD/MM/YYYY
• DD-MM-YYYY
• YYYYMMDD
• 01 Feb 2026
• Feb 01 2026

All dates are converted to the standard format:
YYYY-MM-DD

AMOUNT HANDLING

• Removes currency symbols (AED, commas, spaces)
• Extracts numeric values only
• Converts values to integers

DUPLICATE REMOVAL

• Records are deduplicated using doc_id
• The first occurrence of a record is preserved

RELIABILITY & ERROR HANDLING

• API calls use retry logic with exponential backoff
• Timeout protection for external API requests
• Graceful error handling and responses
• Backend acts as the single source of truth (no blind frontend trust)

DESIGN APPROACH

• Clear separation of concerns

views.py: API endpoints

utils.py: business logic

env.py: configuration

• Config-driven architecture
• Backend-controlled data validation
• Production-ready error handling
• Clean, readable, maintainable, and testable code
