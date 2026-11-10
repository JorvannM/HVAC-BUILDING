import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from analysis_service import evaluate_building

APP=str(Path(__file__).with_name('streamlit_app.py'))


class StreamlitJourneys(unittest.TestCase):
    def app(self, sample=False):
        app=AppTest.from_file(APP,default_timeout=20).run()
        self.assertEqual(len(app.exception),0)
        if sample:
            app.button(key='example').click().run()
            app.button(key='analyse').click().run()
            self.assertEqual(len(app.exception),0)
        return app

    def test_sample_analysis_report_and_assistant(self):
        app=self.app(sample=True)
        self.assertEqual(app.session_state['analysis']['building']['total_kwh'],127000)
        self.assertAlmostEqual(app.session_state['analysis']['building']['intensity'],127000/1200)
        self.assertTrue(app.session_state['report_bytes'].startswith(b'%PDF'))
        app.chat_input[0].set_value('Quelles sont les actions prioritaires ?').run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(len(app.session_state['chat']),2)
        self.assertGreater(len(app.session_state['chat'][1]['content']),50)

    def test_edit_recalculate_and_absence(self):
        app=self.app(sample=True)
        app.number_input(key='input_surface_m2').set_value(200.0).run()
        self.assertTrue(any('Les données ont changé' in item.value for item in app.warning))
        self.assertTrue(app.chat_input[0].disabled)
        self.assertTrue(app.get('download_button')[0].proto.disabled)
        app.selectbox(key='input_cooling_type').select('none').run()
        self.assertTrue(app.number_input(key='input_cooling_setpoint_c').disabled)
        app.button(key='analyse').click().run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.session_state['analysis']['building']['intensity'],635)
        self.assertFalse(app.session_state['analysis']['building']['has_cooling'])
        self.assertFalse(app.chat_input[0].disabled)

    def test_invalid_zero_reset_and_independent_sessions(self):
        app=self.app()
        app.button(key='analyse').click().run()
        self.assertTrue(any('surface' in item.value for item in app.error))
        app.button(key='example').click().run()
        app.number_input(key='input_dhw_gas_kwh').set_value(50000.0).run()
        app.button(key='analyse').click().run()
        self.assertTrue(any('gaz ECS' in item.value for item in app.error))
        app.number_input(key='input_dhw_gas_kwh').set_value(None).run()
        app.number_input(key='input_electricity_kwh').set_value(0.0).run()
        app.number_input(key='input_gas_kwh').set_value(0.0).run()
        app.button(key='analyse').click().run()
        self.assertEqual(app.session_state['analysis']['building']['total_kwh'],0)
        self.assertEqual(app.session_state['analysis']['savings']['high_kwh'],0)
        second=self.app()
        self.assertIsNone(second.session_state['analysis'])
        self.assertEqual(second.session_state['chat'],[])
        app.button(key='reset').click().run()
        self.assertIsNone(app.session_state['analysis'])
        self.assertIsNone(app.session_state['report_bytes'])
        self.assertEqual(len(app.exception),0)


if __name__=='__main__':unittest.main(verbosity=2)
