# Vérifications — 10 novembre 2026

- Test de fumée du moteur d’origine : réussi.
- Trois groupes de tests Streamlit AppTest : réussis. Ils couvrent le diagnostic à partir de l’exemple, la création PDF, l’assistant local, le recalcul, les résultats obsolètes, l’absence de climatisation, la saisie invalide, le cas sans consommation, l’effacement et l’isolation de deux sessions.
- Navigateur Chromium : exemple chargé puis analysé ; indicateurs observés : 127 000 kWh/an, 105,8 kWh/m²/an, 13,95 tCO₂e/an et 21 000 €/an.
- Affichage observé sur ordinateur (1 363 px) et aux largeurs CSS de 454 et 340 px par zoom du navigateur, sans débordement horizontal du document. Aucun test sur téléphone physique ni Safari iOS.
- Les 18 fichiers d’origine listés dans SOURCE_PROVENANCE.json sont conservés à l’identique.

Le diagnostic dépend des règles et facteurs du moteur d’origine ; il n’est pas un DPE ni un audit réglementaire. Aucune vérification extérieure de ces hypothèses n’a été ajoutée.

Le déploiement distant n’a pas encore été exécuté. Le site Streamlit Community Cloud affiche la page de connexion ; le propriétaire doit activer le déploiement depuis son compte Streamlit. Le dépôt de destination est JorvannM/HVAC-BUILDING, branche main. Les modules métier présents dans ce dépôt ont été comparés aux modules testés : les 15 fichiers du moteur et du rapport sont identiques.
