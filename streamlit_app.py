"""HVAC Building public — Streamlit Community Cloud entrypoint."""
from pathlib import Path
import streamlit as st
import pandas as pd
from analysis_service import evaluate_building
from engine import ask_ai
from report_pdf import generate_report

st.set_page_config(page_title='HVAC Building · Diagnostic énergétique',page_icon='⚡',layout='wide')
st.markdown('<style>'+Path(__file__).with_name('streamlit_style.css').read_text(encoding='utf-8')+'</style>',unsafe_allow_html=True)

DEFAULTS = dict(name='',address='',building_type='bureaux',surface_m2=None,construction_year=None,
                electricity_kwh=0.0,gas_kwh=0.0,district_kwh=0.0,annual_energy_cost_eur=0.0,
                heating_type='unknown',cooling_type='unknown',ventilation_type='unknown',
                lighting_type='unknown',dhw_type='unknown',meter_separation=False,
                occupancy_hours_week=50.0,occupancy_days_year=250,
                heating_setpoint_c=None,cooling_setpoint_c=None,
                ventilation_schedule_hours_day=None,lighting_schedule_hours_day=None,dhw_gas_kwh=None)
EXAMPLE = dict(DEFAULTS,name='Bureaux · Exemple',surface_m2=1200.0,construction_year=2008,
               electricity_kwh=85000.0,gas_kwh=42000.0,annual_energy_cost_eur=21000.0,
               heating_type='electric',cooling_type='split',ventilation_type='simple_flux',
               lighting_type='fluorescent',dhw_type='gaz',meter_separation=True,
               heating_setpoint_c=22.0,cooling_setpoint_c=23.0,
               ventilation_schedule_hours_day=20.0,lighting_schedule_hours_day=13.0)
for field, value in DEFAULTS.items():
    if 'input_'+field not in st.session_state:
        st.session_state['input_'+field] = value
for key, value in [('analysis',None),('analysed_payload',None),('report_bytes',None),('chat',[]),('example_loaded',False)]:
    if key not in st.session_state:
        st.session_state[key] = value


def apply_example():
    for field, value in EXAMPLE.items():
        st.session_state['input_'+field] = value
    st.session_state.example_loaded = True


def clear():
    for field, value in DEFAULTS.items():
        st.session_state['input_'+field] = value
    st.session_state.analysis = None
    st.session_state.analysed_payload = None
    st.session_state.report_bytes = None
    st.session_state.chat = []
    st.session_state.example_loaded = False


def number(field, label, low=0.0, high=1e12, integer=False, **kwargs):
    return st.number_input(label, min_value=int(low) if integer else float(low),
                           max_value=int(high) if integer else float(high),
                           step=1 if integer else 0.1, key='input_'+field, **kwargs)


def select(field, label, options):
    return st.selectbox(label,list(options),format_func=options.get,key='input_'+field)


def fmt(value,digits=0):
    return f'{value:,.{digits}f}'.replace(',',' ').replace('.',',')


with st.sidebar:
    st.markdown('## ⚡ HVAC Building')
    st.caption('ENERGY INTELLIGENCE')
    st.divider()
    st.markdown('**Votre espace d’analyse**')
    st.caption('01 · Caractéristiques\n\n02 · Diagnostic\n\n03 · Assistant')
    st.divider()
    st.caption('Version publique. Chaque visiteur dispose de sa propre session. Aucune saisie n’est enregistrée dans un historique partagé.')
    st.button('Effacer ma session',key='reset',on_click=clear,width='stretch')
    st.caption('Moteur Python v06 conservé · Interface Streamlit')

st.markdown('''<div class="hero"><p class="eyebrow">COMPRENDRE. PRIORISER. AGIR.</p>
<h1>Votre bâtiment,<br>une énergie mieux maîtrisée.</h1>
<p>Transformez vos consommations en pistes d’action concrètes.</p></div>''',unsafe_allow_html=True)
st.caption('Pré-diagnostic indicatif · Données déclarées · Sans clé d’API')

with st.container(border=True):
    left,right=st.columns([3,1],vertical_alignment='center')
    left.subheader('01 · Parlons de votre bâtiment')
    right.button('Essayer un exemple',key='example',on_click=apply_example,width='stretch')
    if st.session_state.example_loaded:
        st.caption('Exemple fictif chargé. Vous pouvez modifier toutes les valeurs avant analyse.')
    tab_building,tab_equipment,tab_energy=st.tabs(['Bâtiment','Équipements','Consommations'])
    with tab_building:
        a,b=st.columns(2)
        with a:
            st.text_input('Nom du bâtiment',key='input_name',max_chars=150,placeholder='Ex. : Bureaux Suresnes')
            number('surface_m2','Surface de référence (m²) *',low=0.1,high=10000000,placeholder='À renseigner')
            number('occupancy_hours_week','Occupation (h / semaine)',high=168)
        with b:
            select('building_type','Usage principal',{'bureaux':'Bureaux','enseignement':'Enseignement','commerce':'Commerce','residentiel':'Résidentiel'})
            number('construction_year','Année de construction (facultatif)',low=1700,high=2100,integer=True,placeholder='Inconnue')
            number('occupancy_days_year','Occupation (jours / an)',high=366,integer=True)
        st.text_input('Adresse (facultatif)',key='input_address',max_chars=300,placeholder='Adresse déclarée du bâtiment')
        st.caption('L’adresse est déclarative. Cette version ne lance pas de recherche automatique de DPE.')
    with tab_equipment:
        a,b=st.columns(2)
        with a:
            select('heating_type','Chauffage',{'unknown':'À préciser','electric':'Électrique direct','gaz':'Chaudière gaz','heat_pump':'Pompe à chaleur','district':'Réseau de chaleur'})
            select('ventilation_type','Ventilation',{'unknown':'À préciser','simple_flux':'VMC simple flux','double_flux':'VMC double flux','natural':'Naturelle','none':'Aucune déclarée'})
            select('dhw_type','Eau chaude sanitaire',{'unknown':'À préciser','gaz':'Gaz','electrique':'Électrique','heat_pump':'Thermodynamique','none':'Aucune'})
            number('heating_setpoint_c','Consigne de chauffage (°C, facultatif)',low=5,high=35,placeholder='Inconnue')
            number('ventilation_schedule_hours_day','Ventilation (h / jour, facultatif)',high=24,placeholder='Inconnue',disabled=st.session_state.input_ventilation_type in ('none','natural'))
        with b:
            select('cooling_type','Climatisation',{'unknown':'À préciser','split':'Climatisation indépendante / split','central':'Production centralisée','none':'Aucune'})
            select('lighting_type','Éclairage',{'unknown':'À préciser','fluorescent':'Fluorescent','LED':'LED'})
            number('cooling_setpoint_c','Consigne de climatisation (°C, facultatif)',low=10,high=40,placeholder='Inconnue',disabled=st.session_state.input_cooling_type=='none')
            number('lighting_schedule_hours_day','Éclairage (h / jour, facultatif)',high=24,placeholder='Inconnue')
    with tab_energy:
        st.caption('Consommations facturées sur une même période de 12 mois. Indiquez 0 pour une énergie non utilisée.')
        a,b=st.columns(2)
        with a:
            number('electricity_kwh','Électricité (kWh / an)')
            number('district_kwh','Réseau de chaleur (kWh / an)')
            number('dhw_gas_kwh','Dont gaz ECS (kWh / an, si mesuré)',placeholder='Laisser vide si inconnu',disabled=st.session_state.input_dhw_type=='none')
        with b:
            number('gas_kwh','Gaz (kWh / an)')
            number('annual_energy_cost_eur','Dépenses énergétiques (€ / an)')
            st.checkbox('Compteurs séparés par énergie',key='input_meter_separation')
        st.caption('Des compteurs par énergie ne permettent pas d’isoler chaque usage CVC.')
    payload={field:st.session_state['input_'+field] for field in DEFAULTS}
    if st.button('Analyser mon bâtiment',key='analyse',type='primary',width='stretch'):
        try:
            with st.spinner('Analyse du bâtiment…'):
                result=evaluate_building(payload)
                pdf=generate_report(result['building'],result['diagnosis'],result['recommendations'],result['carbon'],result['savings'])
            st.session_state.analysis=result
            st.session_state.analysed_payload=dict(payload)
            st.session_state.report_bytes=pdf
            st.session_state.chat=[]
        except (ValueError,TypeError) as error:
            st.error(str(error))

result=st.session_state.analysis
stale=result is not None and payload!=st.session_state.analysed_payload
st.subheader('02 · Votre pré-diagnostic')
if result is None:
    st.info('Renseignez votre bâtiment ou chargez l’exemple, puis lancez l’analyse.')
else:
    if stale:
        st.warning('Les données ont changé. Relancez le diagnostic pour actualiser les résultats, l’export et l’assistant.')
    data=result['building'];diagnosis=result['diagnosis'];savings=result['savings'];carbon=result['carbon']
    st.text(f"{data['name']} · {fmt(data['surface_m2'])} m² · Données déclarées sur 12 mois")
    cols=st.columns(4)
    for column,label,value in zip(cols,['Énergie (kWh / an)','Intensité (kWh / m² / an)','Émissions (t CO₂e / an)','Dépenses (€ / an)'],
                                  [fmt(data['total_kwh']),fmt(data['intensity'],1),fmt(carbon['total_tonnes'],2),fmt(data['annual_cost'])]):
        column.metric(label,value,border=True)
    a,b=st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown('#### Chaque énergie, sa part')
            chart=pd.DataFrame({'Énergie':['Électricité','Gaz','Réseau de chaleur'],'kWh/an':[data['electricity_kwh'],data['gas_kwh'],data['district_kwh']]}).set_index('Énergie')
            st.bar_chart(chart,color='#65e0ba',height=230)
            st.caption('Répartition par énergie, sans estimation des consommations par usage.')
    with b:
        with st.container(border=True):
            st.markdown('#### Potentiel à étudier')
            if data['total_kwh']:
                st.metric('Fourchette indicative',f"{fmt(savings['low_pct'])}–{fmt(savings['high_pct'])} %")
                st.write(f"{fmt(savings['low_kwh'])} à {fmt(savings['high_kwh'])} kWh / an")
                st.write(f"Soit {fmt(savings['low_eur'])} à {fmt(savings['high_eur'])} € / an, aux prix déclarés.")
            else:
                st.write('Potentiel non estimable sans consommation renseignée.')
            st.caption(savings.get('warning','Les économies ne sont pas garanties.'))
    with st.expander(f"Points de vigilance · {len(diagnosis['alerts'])} alertes",expanded=True):
        for warning in data['validation']['warnings']:
            st.warning(warning)
        for alert in diagnosis['alerts']:
            labels={'Heating':'Chauffage','Cooling':'Climatisation','Lighting':'Éclairage','Hot Water':'Eau chaude sanitaire','Operation':'Exploitation'}
            st.warning(labels.get(alert['title'],alert['title'])+' — '+alert['detail'])
        if not diagnosis['alerts']:
            st.info('Aucune alerte détectée. Cela ne prouve pas l’absence de défaut.')
    for finding in diagnosis.get('detailed_diagnostics',[]):
        with st.expander(finding['category']+' · '+finding['title']):
            st.write(finding['cause']);st.info(finding['evidence'])
            st.markdown('**Contrôles à effectuer**')
            for check in finding['checks']:st.write('• '+check)
            st.caption('Confiance : '+finding['confidence'])
    st.markdown('#### Votre plan d’actions')
    recommendations=result['recommendations']
    category=st.selectbox('Filtrer les recommandations',['Tous']+sorted({action['category'] for action in recommendations}),key='category')
    for action in recommendations:
        if category!='Tous' and action['category']!=category:continue
        with st.container(border=True):
            st.caption(action['category'].upper())
            st.markdown('**'+action['title']+'**')
            st.write(action['basis']);st.caption(action['savings_note'])
    st.caption(carbon['warning']+' Facteurs d’émission de la version finale d’origine, sans mise à jour automatique.')
    st.download_button('Télécharger le rapport PDF',data=st.session_state.report_bytes,
                       file_name='HVAC_Building_Diagnostic.pdf',mime='application/pdf',
                       key='download_pdf',disabled=stale,on_click='ignore',width='stretch')

st.subheader('03 · Un éclairage sur vos résultats')
st.caption('Assistant local à règles métier, fondé sur les données de votre dernier diagnostic.')
if not result:st.info('Lancez d’abord un diagnostic pour interroger l’assistant.')
for message in st.session_state.chat:
    with st.chat_message(message['role']):
        if message['role']=='user':st.text(message['content'])
        else:st.markdown(message['content'])
question=st.chat_input('Quelles sont les actions prioritaires ?',key='question',disabled=result is None or stale,max_chars=3000)
if question:
    answer,source=ask_ai(question,result['building'],result['recommendations'])
    st.session_state.chat.extend([{'role':'user','content':question},{'role':'assistant','content':answer}])
    st.rerun()
st.divider()
st.caption('HVAC Building · Pré-diagnostic indicatif, sans valeur de DPE ou d’audit réglementaire. Les recommandations nécessitent une validation technique. Les données restent dans la session du visiteur et ne sont pas sauvegardées automatiquement.')
