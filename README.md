# HVAC Building — Streamlit Community Cloud

Version Streamlit adaptée du moteur Python de la version finale v06. Le propriétaire a autorisé une mise en ligne **publique**. Cette version est prête pour Streamlit Community Cloud. Le déploiement doit être activé dans le compte Streamlit du propriétaire ; aucune URL de production n’est encore vérifiée.

## Déployer depuis le téléphone ou l’ordinateur

1. Extraire le ZIP.
2. Dans un dépôt GitHub, déposer le **contenu** du dossier, avec `streamlit_app.py` et `requirements.txt` à la racine. Conserver les sous-dossiers `data/` et `.streamlit/`. Ne pas déposer seulement le ZIP.
3. Se connecter sur https://share.streamlit.io/ et choisir « Create app », puis l’application existante depuis GitHub.
4. Choisir le dépôt et sa branche. Le fichier de démarrage est **`streamlit_app.py`**.
5. Dans les paramètres avancés, choisir **Python 3.12**. Aucun secret ni clé d’API n’est nécessaire.
6. Déployer et vérifier l’application. Pour la rendre publique, si nécessaire, ouvrir Settings → Sharing et sélectionner « This app is public and searchable ».

Documentation officielle :
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app

Le code et les données techniques d’exemple peuvent être publics. Ne pas ajouter de factures, mots de passe ou données client dans le dépôt. Les informations saisies dans l’interface sont conservées uniquement dans la session du visiteur : aucun fichier de données utilisateur ni historique partagé n’est écrit par l’application. Il n’existe pas de base de données utilisateur.

## Lancer localement

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Sur Windows, l’activation d’un environnement virtuel n’est pas requise si vous appelez directement son interpréteur : `.venv\Scripts\python.exe -m streamlit run streamlit_app.py`.

## Ce qui fonctionne

- Saisie typée des caractéristiques, équipements, horaires et consommations annuelles.
- Chargement d’un exemple explicitement fictif et effacement de la session.
- Calcul réel avec le moteur Python d’origine : énergie, intensité, dépenses, carbone, économies indicatives, alertes et recommandations.
- Absence de climatisation prise en compte ; consignes et horaires réellement transmis aux modules de diagnostic.
- Recommandations filtrées par poste et assistant local à règles métier.
- Rapport PDF téléchargeable.
- Résultats signalés comme obsolètes après modification ; assistant et téléchargement bloqués jusqu’au recalcul.

Les facteurs d’émission et les règles restent ceux de la version finale d’origine, sans actualisation automatique. L’adresse est déclarative ; cette version n’interroge pas les services de recherche DPE. Aucun appel à une IA distante et aucune clé OpenAI ne sont nécessaires. L’interface Streamlit remplace ici l’interface FastAPI ; la version FastAPI privée précédente reste une livraison distincte.

## Vérifications

```bash
python tests_smoke.py
python tests_streamlit.py
```

Test de fumée du moteur réussi. Trois groupes de parcours Streamlit réussis : exemple, diagnostic, PDF, assistant ; modifications, blocage des résultats obsolètes et absence de climatisation ; erreurs de saisie, zéro consommation, effacement et isolation de deux sessions.

Voir `VERIFICATION.md` pour les limites des contrôles. Les empreintes des modules conservés sont dans `SOURCE_PROVENANCE.json`.

## Dépôt GitHub

Dépôt : `JorvannM/HVAC-BUILDING` ; branche : `main` ; point d’entrée Streamlit : `streamlit_app.py`. Le style propre à Streamlit se trouve dans `streamlit_style.css`. Les fichiers des anciennes interfaces sont conservés ; `app.py` et `main.py` ne sont pas le point d’entrée à sélectionner pour ce déploiement. Les dépendances requests et openai sont conservées pour compatibilité avec ces fichiers hérités.
