Feature: Devolver herramienta
  As Ana Torres (arrendatario)
  I want to devolver la herramienta alquilada
  So that recuperar mi depósito y cerrar el alquiler

  Background:
    Given Ana tiene un alquiler activo con plazo hasta el 8 de noviembre
    And ha pagado un depósito de S/150

  Scenario: Devolución a tiempo
    Given Ana devuelve la herramienta el 7 de noviembre
    When sube 3 fotos del estado y confirma la devolución
    Then el sistema marca el estado como "Devuelto"
    And el depósito S/150 es liberado en 24 horas

  Scenario: Devolución con mora
    Given Ana devuelve la herramienta el 10 de noviembre
    When el sistema detecta 2 días de retraso
    Then aplica una mora de S/20
    And Ana recibe depósito neto de S/130

  Scenario: Daño reportado por Ana al recibir
    Given Ana recibe la lijadora con un rayón visible
    When sube una foto al momento de la entrega
    Then se crea un ticket automáticamente
    And Carlos (propietario) es notificado del reporte

  Scenario: Daño detectado por Carlos al devolver
    Given Ana devuelve la herramienta con un golpe
    When Carlos sube evidencia fotográfica
    Then se deduce S/80 del depósito
    And Ana recibe S/70 de reembolso