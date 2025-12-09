from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from systems.trim.models import TrimJobInput, TrimJobResult
from systems.trim.pricing_engine import price_job

app = FastAPI(title="Residential Trim API")

@app.get("/api/trim/ping")
def ping():
    return {"status": "ok"}

@app.post("/api/trim/quote", response_model=TrimJobResult)
def quote(job_input: TrimJobInput):
    return price_job(job_input)

@app.get("/", response_class=HTMLResponse)
def index():
    # Resolve template path relative to this file's location for robustness
    BASE_DIR = Path(__file__).resolve().parent
    template_path = BASE_DIR / "templates" / "trim_frontend.html"
    html = template_path.read_text(encoding="utf-8")
    return HTMLResponse(content=html)

