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
