# Red Social de Herramientas - BDD  
## Historia de Uso: *Devolver Herramienta*

---

### **Descripción del Proyecto**

Este repositorio implementa **pruebas BDD (Behavior-Driven Development)** utilizando **Behave** en Python para la **historia de uso "Devolver herramienta"** en una red social de alquiler de herramientas.

Se enfoca en **Ana Torres (arrendataria)** y sus interacciones con el sistema al devolver una herramienta, incluyendo:
- Devolución a tiempo
- Mora por retraso
- Reporte de daño inicial
- Daño detectado al devolver

---

### **Estructura del Proyecto**

red_social_herramientas_bdd/

├── features/

│   ├── devolver_herramienta.feature          # Escenarios en Gherkin

│   └── steps/

│  ----           └── devolver_herramienta_steps.py     # Implementación en Python

└── README.md


---

### **Feature: Devolver Herramienta**

```gherkin
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
```
