# Vérification de la restauration V5

Base : `HVAC_Building_v05_Partage.zip`, archive partagée par le propriétaire. Les 15 modules métier déjà déployés sont conservés sans modification. Leur contenu correspond à la V5, hors fins de lignes et ligne vide finale.

## Résultats

- `python tests_smoke.py` : OK, 15 recommandations, intensité 105,83, émissions 13,95 tCO2e/an.
- `python tests_enrichment.py` : OK.
- `python tests_streamlit.py` : 3 groupes de tests, OK sous Python 3.12.14, Streamlit 1.64.0 et pandas 2.3.3.
- Navigation rapide et latérale entre les cinq rubriques restaurées.
- Audit de 1 200 m² avec 85 000 kWh électriques, 42 000 kWh gaz et 21 000 € : 127 000 kWh/an, 105,8 kWh/m²/an.
- Diagnostic technique détaillé et conseiller local : réponse affichée.
- PDF réel généré ; les deux téléchargements PDF et CSV sont présents.
- Parcours adresse → candidats DPE → confirmation → préremplissage : testé avec données contrôlées.
- Recherche réelle dans l’interface de test : IGN a retourné l’adresse publique « 10 Rue de la Paix 75002 Paris » ; ADEME a retourné des DPE candidats. Aucun DPE voisin n’a été confirmé comme correspondant à cette adresse.
- Panne du géocodage : message explicite, audit manuel disponible.
- Consommations nulles : aucun plantage ; indicateurs et pages de diagnostic/rapport accessibles.
- Sessions indépendantes : pas de reprise des données de l’autre visiteur.
- Contrôle visuel sur ordinateur et à largeurs CSS 454 et 340 px : aucun débordement horizontal global, formulaire utilisable et menu latéral ouvrable. Ce contrôle utilise le zoom du navigateur ; il ne constitue pas un test sur un iPhone physique.

Les dépendances du correctif Python 3.14 sont conservées. Le runtime applicatif local est Python 3.12 ; le fonctionnement sur Community Cloud nécessite la vérification du site déployé.

## Écart limité à l’interface

Les formulaires, options, cinq rubriques, calculs, résultats et exports viennent de la V5. Changements : CSS clair responsive, thème clair, application correcte de la navigation rapide, suppression d’un titre « Priorité » en double, restauration du dossier `services/` manquant dans le dépôt initial. Le moteur et les connecteurs restaurés ne reçoivent aucune nouvelle règle métier.
