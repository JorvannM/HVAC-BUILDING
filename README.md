# HVAC Building — V5 restaurée

Application Streamlit basée sur `HVAC_Building_v05_Partage.zip`, la V5 partagée par son propriétaire. Les cinq rubriques et leurs fonctionnalités sont rétablies :

- Vue d’ensemble : synthèse et navigation rapide.
- Bâtiment : géocodage IGN, recherche de DPE ADEME, sélection et confirmation du diagnostic, préremplissage traçable.
- Audit énergétique : caractéristiques du bâtiment, consommations et dépenses, indicateurs et graphiques.
- AI Advisor : diagnostic technique détaillé, recommandations, émissions, économies indicatives et conseiller local.
- Rapports & méthode : exports PDF et CSV, données et méthode.

Le moteur Python déjà déployé est conservé. La présentation est claire et responsive. Les corrections techniques se limitent à la navigation rapide, au rétablissement du dossier `services/` manquant et à un titre de priorité affiché en double.

## Lancement

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Streamlit Community Cloud : dépôt `JorvannM/HVAC-BUILDING`, branche `main`, fichier `streamlit_app.py`. Les dépendances compatibles avec le déploiement Python 3.14 sont conservées.

## Vérification

```bash
python tests_smoke.py
python tests_enrichment.py
python tests_streamlit.py
```

Les services publics sont externes. Une indisponibilité ne bloque pas la saisie manuelle. Le connecteur BDNB reste celui de la V5 : configuration par `HVAC_BDNB_SEARCH_URL`. Les DPE candidats nécessitent une confirmation du périmètre. Le conseiller local fonctionne sans clé API.

Les données saisies restent propres à la session du visiteur. L’application est un outil de préanalyse ; les hypothèses et limites d’origine sont conservées.
