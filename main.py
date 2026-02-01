# ================================
# Contract Generator Service
# Tech: Python + FastAPI
# Run: uvicorn main:app --host 0.0.0.0 --port 4000
# ================================

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from docx import Document
from datetime import datetime
import os
import uuid
from num2words import num2words




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
CLAUSE_DIR = os.path.join(BASE_DIR, "clauses")

os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI(title="Contract Generator", version="1.0")
CURRENCIES = {
    "USD": {"symbol": "$", "name": "US Dollars", "rate": 1},
    "EUR": {"symbol": "€", "name": "Euros", "rate": 1.08},
    "GBP": {"symbol": "£", "name": "Pounds Sterling", "rate": 1.27},
    "AED": {"symbol": "AED ", "name": "UAE Dirhams", "rate": 0.27},
    "SAR": {"symbol": "SAR ", "name": "Saudi Riyals", "rate": 0.27}
}


# ------------------------------
# Utility Functions
# ------------------------------

def load_clause(name: str) -> str:
    path = os.path.join(CLAUSE_DIR, f"{name}.txt")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_contract(data: dict) -> str:
    doc = Document(os.path.join(TEMPLATE_DIR, "master_contract.docx"))

    services_block = ""
    for service in data["services"]:
        services_block += load_clause(service) + "\n\n"

    replacements = {
    "{{CLIENT_NAME}}": data["client_name"],
    "{{COUNTRY}}": data["country"],
    "{{EFFECTIVE_DATE}}": data["date"],
    "{{FEES_AMOUNT}}": data["fees"],
    "{{FEES_IN_WORDS}}": data["fees_words"],
    "{{CURRENCY_SYMBOL}}": data["currency_symbol"],
    "{{CURRENCY_NAME}}": data["currency_name"],
    "{{USD_EQUIVALENT}}": data["usd_equivalent"],
    "{{CONTRACT_DURATION}}": data["contract_duration"],
    "{{SERVICES_BLOCK}}": services_block
    }


    for p in doc.paragraphs:
        for key, value in replacements.items():
            if key in p.text:
                p.text = p.text.replace(key, value)

    file_id = str(uuid.uuid4())
    file_path = os.path.join(OUTPUT_DIR, f"contract_{file_id}.docx")
    doc.save(file_path)
    return file_path

# ------------------------------
# Web UI
# ------------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<html>
<head>
<title>Contract Generator</title>
</head>
<body style="font-family:Arial;max-width:900px;margin:auto">
<h2>International Contract Generator</h2>

<form method="post" action="/generate">

<label>Client Name</label><br>
<input name="client_name" required style="width:100%"><br><br>

<label>Country</label><br>
<select name="country">
  <option>USA</option>
  <option>UK</option>
  <option>UAE</option>
  <option>KSA</option>
  <option>Bahrain</option>
</select><br><br>

<label>Contract Duration</label><br>
<select name="duration">
  <option>6 Months</option>
  <option>12 Months</option>
  <option>24 Months</option>
  <option>36 Months</option>
</select><br><br>

<label>Fee Amount</label><br>
<input name="fees" placeholder="2000" required><br><br>

<label>Currency</label><br>
<select name="currency">
  <option value="USD">USD – US Dollar</option>
  <option value="EUR">EUR – Euro</option>
  <option value="GBP">GBP – Pound</option>
  <option value="AED">AED – Dirham</option>
  <option value="SAR">SAR – Riyal</option>
</select><br><br>

<label>Services</label><br>
<input type="checkbox" name="services" value="finance"> Finance & Accounting<br>
<input type="checkbox" name="services" value="it"> IT / Software<br>
<input type="checkbox" name="services" value="hr"> HR & Payroll<br>
<input type="checkbox" name="services" value="business"> Business Consulting<br><br>

<button type="submit" style="padding:10px 20px;font-size:16px">
Generate Contract
</button>

</form>
</body>
</html>
"""


# ------------------------------
# Generate Contract
# ------------------------------

@app.post("/generate")
def generate(
    client_name: str = Form(...),
    country: str = Form(...),
    fees: str = Form(...),
    currency: str = Form("USD"),
    duration: str = Form("12 Months"),
    services: list[str] = Form([])
):
    amount = float(fees.replace(",", ""))
    currency_data = CURRENCIES[currency]

    usd_equivalent = round(amount * currency_data["rate"], 2)

    fees_in_words = num2words(amount, to="currency", currency=currency).title()

    data = {
        "client_name": client_name,
        "country": country,
        "fees": f"{amount:,.2f}",
        "fees_words": fees_in_words,
        "currency_symbol": currency_data["symbol"],
        "currency_name": currency_data["name"],
        "usd_equivalent": f"{usd_equivalent:,.2f}",
        "contract_duration": duration,
        "date": datetime.today().strftime("%d %B %Y"),
        "services": services
    }

    file_path = generate_contract(data)
    return FileResponse(file_path, filename="Service_Agreement.docx")

