"""Adaptation web des entrées ; le moteur Python d'origine reste inchangé."""
import math
from engine import (analyse_building, diagnose_building, build_recommendations,
                    estimate_savings, estimate_carbon)


def evaluate_building(payload):
    values = dict(payload)
    surface = values.pop('surface_m2', None)
    if surface is None or not math.isfinite(float(surface)) or float(surface) <= 0:
        raise ValueError('Renseignez une surface strictement positive.')
    energy = [values.pop(key, 0) for key in ('electricity_kwh', 'gas_kwh', 'district_kwh')]
    cost = values.pop('annual_energy_cost_eur', 0)
    if any(v is None or not math.isfinite(float(v)) or float(v) < 0 for v in [*energy, cost]):
        raise ValueError('Les consommations et dépenses doivent être positives ou nulles.')
    if values.get('dhw_gas_kwh') is not None and values['dhw_gas_kwh'] > energy[1]:
        raise ValueError('La part de gaz ECS ne peut pas dépasser la consommation totale de gaz.')
    values['name'] = str(values.get('name', '')).strip() or 'Mon bâtiment'
    values['heating_type'] = {'electrique':'electric', 'pac':'heat_pump'}.get(values.get('heating_type'), values.get('heating_type', 'unknown'))
    values.update(has_cooling=values.get('cooling_type') != 'none',
                  has_ventilation=values.get('ventilation_type') not in ('none', 'natural'),
                  has_dhw=values.get('dhw_type') != 'none')
    if not values['has_cooling']:
        values['cooling_setpoint_c'] = None
    if not values['has_ventilation']:
        values['ventilation_schedule_hours_day'] = None
    if not values['has_dhw']:
        values['dhw_gas_kwh'] = None
    data = analyse_building(surface, *energy, cost, **values)
    diagnosis = diagnose_building(data)
    recommendations = build_recommendations(data)
    return {'building':data, 'diagnosis':diagnosis, 'recommendations':recommendations,
            'savings':estimate_savings(data,recommendations), 'carbon':estimate_carbon(data)}
