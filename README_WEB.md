# HVAC Building v06 Web

Migration de l’interface Streamlit vers FastAPI + HTML/CSS/JavaScript. Les fichiers Python du moteur v05 sont conservés. L’application Streamlit originale (`app.py`) reste disponible.

## Démarrage sous Windows (PowerShell)

```powershell
cd "$HOME\Desktop\HVAC_Building_v06_Web"
python -m pip install -r requirements-web.txt
python -m uvicorn main:app --reload
```

Ouvrir http://127.0.0.1:8000

## API
- `GET /api/health` : état
- `POST /api/diagnostic` : moteur v05
- `POST /api/assistant` : assistant local v05
- `GET /docs` : documentation interactive FastAPI

## Périmètre de cette version
La nouvelle interface propose le diagnostic et l’assistant local. Les fonctionnalités Streamlit de géocodage, enrichissement externe, sélection DPE et export PDF restent dans l’ancienne interface et ne sont pas encore migrées. Les estimations sont indicatives et ne constituent pas un audit réglementaire.
