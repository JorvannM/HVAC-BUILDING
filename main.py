"""API Web HVAC Building v06, basée sur le moteur v05."""
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from engine import analyse_building, diagnose_building, build_recommendations, estimate_savings, estimate_carbon, ask_ai

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="HVAC Building Web", version="0.6.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

class BuildingRequest(BaseModel):
    name: str = "Bâtiment de référence"
    building_type: str = "bureaux"
    surface_m2: float = Field(default=1200, gt=0)
    electricity_kwh: float = Field(default=85000, ge=0)
    gas_kwh: float = Field(default=42000, ge=0)
    district_kwh: float = Field(default=0, ge=0)
    annual_energy_cost_eur: float = Field(default=21000, ge=0)
    heating_type: str = "electrique"
    cooling_type: str = "split"
    ventilation_type: str = "simple_flux"
    lighting_type: str = "fluorescent"
    dhw_type: str = "gaz"
    meter_separation: bool = True

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=3000)
    building: BuildingRequest

def evaluate(building: BuildingRequest):
    v = building.model_dump()
    data = analyse_building(v.pop("surface_m2"),v.pop("electricity_kwh"),v.pop("gas_kwh"),v.pop("district_kwh"),v.pop("annual_energy_cost_eur"),**v)
    diagnosis = diagnose_building(data)
    recommendations = build_recommendations(data)
    return data, diagnosis, recommendations

@app.get("/")
def index():
    return FileResponse(ROOT / "templates" / "index.html")

@app.get("/api/health")
def health():
    return {"status":"ok","version":"0.6.0"}

@app.post("/api/diagnostic")
def diagnostic(building: BuildingRequest):
    try:
        data, diagnosis, recommendations = evaluate(building)
        return {"building":data,"diagnosis":diagnosis,"recommendations":recommendations,"savings":estimate_savings(data,recommendations),"carbon":estimate_carbon(data)}
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc

@app.post("/api/assistant")
def assistant(payload: ChatRequest):
    try:
        data, _, recommendations = evaluate(payload.building)
        answer, source = ask_ai(payload.question,data,recommendations)
        return {"answer":answer,"source":source}
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422,detail=str(exc)) from exc
