"""Regression checks for restored V5 workflows, with deterministic public API fixtures."""
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest
from engine import diagnose_building, build_recommendations, estimate_carbon, estimate_savings
from report_pdf import generate_report

APP = str(Path(__file__).with_name('streamlit_app.py'))


def button(app, label):
    return next(b for b in app.button if b.label == label)


class RestoredV5(unittest.TestCase):
    def app(self):
        app = AppTest.from_file(APP, default_timeout=15).run()
        self.assertFalse(app.exception)
        return app

    def page(self, app, name):
        app.sidebar.radio[0].set_value(name).run()
        self.assertFalse(app.exception)

    def test_navigation_and_full_manual_audit(self):
        app = self.app()
        self.assertEqual(app.sidebar.radio[0].options, ["Vue d'ensemble", 'Bâtiment', 'Audit énergétique', 'AI Advisor', 'Rapports & méthode'])
        button(app, "Ouvrir l'audit énergétique").click().run()
        self.assertEqual(app.sidebar.radio[0].value, 'Audit énergétique')
        values = {'Surface utile': 1200.0, 'Électricité': 85000.0, 'Gaz': 42000.0,
                  'Réseau de chaleur': 0.0, 'Dépenses': 21000.0}
        for widget in app.number_input:
            for prefix, value in values.items():
                if widget.label.startswith(prefix): widget.set_value(value)
        app.text_input(key='audit_usage').set_value('bureaux')
        app.text_input(key='audit_year').set_value('1998')
        app.text_input(key='audit_heating').set_value('electric')
        button(app, 'Calculer les indicateurs').click().run()
        self.assertFalse(app.exception)
        result = app.session_state['analysis']
        self.assertEqual(result['total_kwh'], 127000)
        self.assertAlmostEqual(result['intensity'], 105.833333333)
        self.page(app, 'AI Advisor')
        self.assertIn('Diagnostic technique détaillé', [s.value for s in app.subheader])
        app.text_area[0].set_value('Quels contrôles pour le chauffage ?').run()
        button(app, 'Générer une réponse').click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any('Assistant expert local' in c.value for c in app.caption))
        self.page(app, 'Rapports & méthode')
        self.assertEqual(len(app.get('download_button')), 2)
        recs = build_recommendations(result)
        pdf = generate_report(result, diagnose_building(result), recs,
                              estimate_carbon(result), estimate_savings(result, recs), None, None)
        self.assertTrue(pdf.startswith(b'%PDF'))
        self.page(app, "Vue d'ensemble")
        self.assertTrue(any('127 000' in m.value for m in app.metric))
        self.assertIsNone(self.app().session_state['analysis'])

    def test_address_dpe_confirmation_and_prefill(self):
        app = self.app()
        button(app, 'Ouvrir le module bâtiment').click().run()
        self.assertEqual(app.sidebar.radio[0].value, 'Bâtiment')
        location = {'address': '10 rue de la Paix 75002 Paris', 'ban_id': 'test', 'lat': 48.0, 'lon': 2.0}
        row = {'Surface_habitable_logement': 68, 'Etiquette_DPE': 'D', 'Etiquette_GES': 'B',
               'Adresse_brute': location['address'], 'Année_construction': 1990,
               'Type_énergie_principale_chauffage': 'gaz', 'Type_ventilation': 'simple flux', 'N°DPE': 'test-dpe'}
        app.text_input[0].set_value(location['address'])
        with patch('building_enrichment.geocode', return_value=[location]):
            button(app, "Rechercher l'adresse").click().run()
        with patch('building_enrichment.search_dpe', side_effect=[[row], []]), patch('building_enrichment.search_bdnb', return_value=([], None)):
            button(app, 'Identifier les bâtiments et rechercher les DPE').click().run()
        self.assertFalse(app.exception)
        self.assertTrue(button(app, 'Préremplir la fiche depuis ce DPE').disabled)
        app.checkbox(key='confirm_dpe').check().run()
        button(app, 'Préremplir la fiche depuis ce DPE').click().run()
        self.assertEqual(app.session_state['prefill']['surface_m2'], 68)
        self.page(app, 'Audit énergétique')
        self.assertEqual(app.number_input(key='audit_surface').value, 68)
        self.assertEqual(app.text_input(key='audit_heating').value, 'gaz')
        self.assertEqual(app.text_input(key='audit_year').value, '1990')
        self.assertEqual(app.text_input(key='audit_ventilation').value, 'simple flux')

    def test_api_failure_and_empty_analysis(self):
        app = self.app()
        self.page(app, 'Bâtiment')
        app.text_input[0].set_value('adresse test')
        with patch('building_enrichment.geocode', side_effect=ConnectionError):
            button(app, "Rechercher l'adresse").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.error)
        self.page(app, 'Audit énergétique')
        button(app, 'Calculer les indicateurs').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state['analysis']['total_kwh'], 0)
        self.page(app, 'AI Advisor')
        self.assertFalse(app.exception)
        self.page(app, 'Rapports & méthode')
        self.assertFalse(app.exception)


if __name__ == '__main__':
    unittest.main()
