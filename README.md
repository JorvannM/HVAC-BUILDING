# HVAC Building — v0.6

**Application de pré-diagnostic énergétique des bâtiments**, avec moteur Python modulaire et interface web FastAPI / HTML / CSS / JavaScript.

## Fonctionnalités

- Saisie des caractéristiques du bâtiment et de ses consommations énergétiques
- Analyse des usages : chauffage, refroidissement, ventilation, éclairage et eau chaude sanitaire
- Indicateurs énergétiques, estimation indicative des émissions carbone et pistes d'économies
- Recommandations de pré-diagnostic et assistant local de questions-réponses
- Interface web et documentation interactive de l'API

## Technologies

Python, FastAPI, Pydantic, Uvicorn, HTML, CSS, JavaScript. Une interface historique Streamlit est également conservée.

## Installation — interface web (Windows PowerShell)

Prérequis : Python 3.10+ (version recommandée ; non vérifiée sur toutes les versions).

```powershell
git clone https://github.com/VOTRE-UTILISATEUR/HVAC-Building.git
cd HVAC-Building
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-web.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Ouvrir **http://127.0.0.1:8000**.

Sans Git, télécharger le ZIP du dépôt, l'extraire puis exécuter les commandes à partir de `py -m venv .venv`.

## API

| Méthode | Route | Usage |
|---|---|---|
| GET | `/` | Interface web |
| GET | `/api/health` | Vérification du service |
| POST | `/api/diagnostic` | Pré-diagnostic énergétique |
| POST | `/api/assistant` | Assistant local |
| GET | `/docs` | Documentation interactive FastAPI |

## Interface Streamlit historique (optionnelle)

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Cette interface historique conserve des parcours de recherche d'adresse, de rapprochement DPE et de rapport PDF. Ils **ne sont pas encore migrés** vers l'interface FastAPI. Certaines intégrations de données publiques nécessitent un accès réseau ou une configuration et ne sont pas garanties.

## Tests

```powershell
.\.venv\Scripts\python.exe tests_smoke.py
.\.venv\Scripts\python.exe tests_enrichment.py
```

## Structure

- `main.py` : serveur web FastAPI
- `templates/` et `static/` : interface HTML/CSS/JavaScript
- `engine.py` et modules métiers : calculs, contrôles, recommandations
- `assistant_local.py` : assistant local
- `data/` : paramètres et règles de pré-diagnostic
- `app.py` : interface historique Streamlit
- `services/` : services d'enrichissement externe

## Limites et avertissement

**Les résultats sont indicatifs : ce projet n'est ni un DPE, ni un audit énergétique réglementaire.** Les données d'entrée doivent être vérifiées ; les facteurs d'émission et hypothèses d'économies doivent être adaptés au contexte et à l'année d'étude. Les économies par poste ne doivent pas être additionnées automatiquement. Ne pas publier de données personnelles ou de clés API.

## État de validation

Le code a passé une vérification de syntaxe Python et le test `tests_smoke.py` lors de la préparation de cette archive. Le fonctionnement complet du serveur web et les intégrations externes n'ont pas été testés ici.

## Documentation complémentaire

Voir `README_WEB.md`, `README_FINAL.md` et `README_IDENTIFICATION.md`.
