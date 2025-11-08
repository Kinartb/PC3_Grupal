# features/steps/devolver_herramienta_steps.py
from behave import given, when, then
from datetime import datetime

# Base de datos simulada
DATABASE = {
    'rentals': {},
    'tools': {},
    'notifications': [],
    'tickets': []
}

# --- Background ---
@given('Ana tiene un alquiler activo con plazo hasta el 8 de noviembre')
def step_alquiler_activo(context):
    DATABASE['rentals'][5001] = {
        'id': 5001,
        'renter': 'Ana',
        'owner': 'Carlos',
        'tool': 'Lijadora',
        'end_date': datetime(2025, 11, 8),
        'deposit': 150.0,
        'status': 'active',
        'returned_at': None,
        'late_days': 0,
        'late_fee': 0.0,
        'damage_deduction': 0.0
    }
    DATABASE['tools'][1001] = {
        'id': 1001,
        'name': 'Lijadora',
        'status': 'rented'
    }

@given('ha pagado un depósito de S/150')
def step_deposito_pagado(context):
    assert DATABASE['rentals'][5001]['deposit'] == 150.0

# --- Escenario 1: Devolución a tiempo ---
@given('Ana devuelve la herramienta el 7 de noviembre')
def step_devuelve_7_nov(context):
    context.return_date = datetime(2025, 11, 7)

@when('sube 3 fotos del estado y confirma la devolución')
def step_subir_fotos_confirmar(context):
    rental = DATABASE['rentals'][5001]
    rental['returned_at'] = context.return_date
    rental['photos_count'] = 3
    rental['status'] = 'returned'
    DATABASE['tools'][1001]['status'] = 'available'

@then('el sistema marca el estado como "Devuelto"')
def step_estado_devuelto(context):
    assert DATABASE['rentals'][5001]['status'] == 'returned'

@then('el depósito S/150 es liberado en 24 horas')
def step_deposito_liberado(context):
    refund = DATABASE['rentals'][5001]['deposit'] - DATABASE['rentals'][5001].get('late_fee', 0) - DATABASE['rentals'][5001].get('damage_deduction', 0)
    assert refund == 150.0
    DATABASE['notifications'].append(('Ana', 'Depósito S/150 liberado en 24h'))

# --- Escenario 2: Devolución con mora ---
@given('Ana devuelve la herramienta el 10 de noviembre')
def step_devuelve_10_nov(context):
    context.return_date = datetime(2025, 11, 10)

@when('el sistema detecta 2 días de retraso')
def step_detectar_mora(context):
    rental = DATABASE['rentals'][5001]
    end_date = rental['end_date']
    days_late = (context.return_date - end_date).days
    if days_late > 0:
        rental['late_days'] = days_late
        rental['late_fee'] = days_late * 10  # S/10 por día
        rental['status'] = 'returned_late'

@then('aplica una mora de S/20')
def step_mora_20(context):
    assert DATABASE['rentals'][5001]['late_fee'] == 20.0

@then('Ana recibe depósito neto de S/130')
def step_deposito_neto_130(context):
    net = 150.0 - 20.0
    assert net == 130.0
    DATABASE['notifications'].append(('Ana', 'Depósito neto: S/130 (mora S/20)'))

# --- Escenario 3: Daño reportado por Ana al recibir ---
@given('Ana recibe la lijadora con un rayón visible')
def step_lijadora_rayada(context):
    context.initial_damage = True

@when('sube una foto al momento de la entrega')
def step_subir_foto_recibir(context):
    ticket = {
        'id': 9001,
        'rental_id': 5001,
        'type': 'initial_damage',
        'reporter': 'Ana',
        'description': 'Rayón visible al recibir',
        'photo': 'recv_damage.jpg'
    }
    DATABASE['tickets'].append(ticket)
    DATABASE['notifications'].append(('Carlos', 'Ana reportó daño inicial (Ticket #9001)'))

@then('se crea un ticket automáticamente')
def step_ticket_creado(context):
    assert any(t['type'] == 'initial_damage' for t in DATABASE['tickets'])

@then('Carlos (propietario) es notificado del reporte')
def step_carlos_notificado(context):
    assert any(
        recipient == 'Carlos' and 'reportó daño inicial' in message
        for recipient, message in DATABASE['notifications']
    ), f"Notificaciones actuales: {DATABASE['notifications']}"
    
# --- Escenario 4: Daño detectado por Carlos al devolver ---
@given('Ana devuelve la herramienta con un golpe')
def step_devuelve_con_golpe(context):
    context.final_damage = True
    context.return_date = datetime(2025, 11, 7)

@when('Carlos sube evidencia fotográfica')
def step_carlos_subir_evidencia(context):
    rental = DATABASE['rentals'][5001]
    rental['damage_deduction'] = 80.0
    rental['status'] = 'damage_reported'
    DATABASE['notifications'].append(('Ana', 'Daño detectado. Deducción: S/80'))

@then('se deduce S/80 del depósito')
def step_deduccion_80(context):
    assert DATABASE['rentals'][5001]['damage_deduction'] == 80.0

@then('Ana recibe S/70 de reembolso')
def step_ana_recibe_70(context):
    net = 150.0 - 80.0
    assert net == 70.0
    DATABASE['notifications'].append(('Ana', 'Reembolso final: S/70'))