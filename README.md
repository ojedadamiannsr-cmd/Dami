# Market Report Generator

## 🚗 Generador Profesional de Reportes Automotrices

Una aplicación completa en Python para generar reportes profesionales de mercado automotriz desde archivos Excel. Genera PDF de 3-4 páginas con gráficos, análisis y Excel con columna de comentarios.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

---

## ✨ Características

✅ **Lectura flexible de Excel** - 5 hojas soportadas (Dashboard, Seasonality, Market Data, Segments, Regional)
✅ **Cálculos automáticos** - 9 métricas (variación %, market share, SAAR, etc.)
✅ **Gráficos profesionales** - 5 tipos (Bar, Line, Pie charts)
✅ **PDF multi-página** - Formato profesional Carta (8.5x11")
✅ **Excel con comentarios** - Estructura espejo + columna vacía para análisis
✅ **CLI & GUI** - Interfaz de línea de comandos e interfaz gráfica
✅ **Validación de datos** - Verifica estructura y columnas
✅ **Logging completo** - Seguimiento detallado de procesos
✅ **100% documentado** - Guías, ejemplos y developer docs

---

## 📦 Instalación

### Opción 1: Script automático (recomendado)

```bash
git clone https://github.com/ojedadamiannsr-cmd/Dami.git
cd Dami
bash setup.sh
```

### Opción 2: Manual

```bash
git clone https://github.com/ojedadamiannsr-cmd/Dami.git
cd Dami
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Uso Rápido

### 1. Generar datos de ejemplo
```bash
python examples/sample_data.py
```

### 2. Generar reporte (CLI)
```bash
# Ambos (PDF + Excel)
python main.py --archivo examples/TEMPLATE_Market_Report.xlsx

# Solo PDF
python main.py --archivo datos.xlsx --solo-pdf

# Solo Excel
python main.py --archivo datos.xlsx --solo-excel

# Sin gráficos (más rápido)
python main.py --archivo datos.xlsx --sin-graficos
```

### 3. O usar GUI
```bash
python gui.py
```

---

## 📊 Estructura de Entrada (Excel)

El archivo debe tener estas 5 hojas:

### **Dashboard**
| Período | Mes actual | YTD actual | YTD año anterior | SAAR | Forecast anual |
|---------|-----------|-----------|-----------------|------|-----------------|
| MAY'26  | 3942      | 11071     | 10500           | 45415 | 38400          |

### **Seasonality**
| Mes | Índice |
|-----|--------|
| Jan | 1.0718 |
| Feb | 0.9238 |
| ... | ...    |

### **Market Data** (Requerido)
| Marca  | Mes Actual | Mes PY | YTD  | YTD PY |
|--------|-----------|--------|------|--------|
| TOYOTA | 680       | 648    | 1850 | 1790   |
| JAC    | 520       | 478    | 1420 | 1305   |

### **Segments** (Opcional)
| Segmento | Ventas | Ventas PY | YTD  | YTD PY |
|----------|--------|-----------|------|--------|
| SEDANES  | 1200   | 1138      | 3400 | 3291   |

### **Regional** (Opcional)
| Región  | Marca  | Ventas | Share |
|---------|--------|--------|-------|
| Central | TOYOTA | 1144   | 41%   |

---

## 📄 Estructura de Salida

### PDF (3-4 páginas)
- **Página 1:** Portada corporativa (Rojo Toyota #C41E3A)
- **Página 2:** Market Data con Top 10 + gráficos
- **Página 3:** Segmentos (tarjetas visuales + tabla)
- **Página 4:** Regional (si hay datos)

### Excel
- **Hoja Resumen:** Métricas principales
- **Hoja Market Data:** Todos los datos procesados
- **Hoja Comentarios:** Columna vacía para análisis
- **Formato profesional:** Estilos, bordes, colores

---

## 🔧 Opciones CLI

```bash
python main.py --help

Opciones:
  --archivo FILE, -a FILE       Archivo Excel (requerido)
  --salida DIR, -o DIR          Directorio de salida [reports/]
  --periodo STR, -p STR         Período (ej: MAY'26)
  --solo-pdf                    Solo generar PDF
  --solo-excel                  Solo generar Excel
  --sin-graficos                Omitir gráficos
  --verbose, -v                 Mostrar debug info
```

---

## 🎨 Personalización

### Cambiar colores corporativos
Editar `config.py`:
```python
COLORS = {
    "primary_red": "#C41E3A",    # Tu color
    "light_gray": "#F5F5F5",
    ...
}
```

### Cambiar tamaño de página
```python
PAGE = {
    "width": 11,      # A4
    "height": 8.5,
}
```

### Agregar nuevas métricas
Ver `DEVELOPMENT.md` para guía completa.

---

## 📁 Estructura del Proyecto

```
Dami/
├── main.py                      # CLI principal
├── gui.py                       # Interfaz gráfica
├── config.py                    # Configuración
├── requirements.txt             # Dependencias
├── setup.sh                     # Script instalación
│
├── modules/                     # Núcleo
│   ├── reader.py               # Lectura Excel
│   ├── calculator.py           # Cálculos
│   ├── formatter.py            # Formateo
│   ├── charts.py               # Gráficos
│   ├── pdf_generator.py        # Generación PDF
│   └── excel_exporter.py       # Exportación Excel
│
├── tests/                       # Tests
│   └── test_calculator.py      # Tests unitarios
│
├── examples/                    # Ejemplos
│   └── sample_data.py          # Generador de datos
│
└── reports/                     # Salida (auto-creado)
    ├── *.pdf
    └── *.xlsx
```

---

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Con cobertura
python -m pytest tests/ --cov=modules

# Test específico
python -m pytest tests/test_calculator.py::TestMetricsCalculator::test_percentage_change
```

---

## 📚 Documentación

- **`QUICKSTART.md`** - Inicio en 3 pasos
- **`DEVELOPMENT.md`** - Guía técnica para developers
- **`README.md`** - Esta documentación

---

## 🐛 Solucionar Problemas

### "Archivo no encontrado"
```bash
# Usa rutas absolutas o relativas correctas
python main.py --archivo ./examples/TEMPLATE_Market_Report.xlsx
```

### "Hojas no encontradas"
Asegúrate que el Excel tiene:
- Dashboard
- Seasonality  
- Market Data

Las otras son opcionales.

### "Columnas faltantes"
Verifica nombres exactos (case-sensitive):
- `Marca`, `Mes Actual`, `Mes PY`, `YTD`, `YTD PY`

### "PDF muy pesado"
```bash
python main.py --archivo datos.xlsx --sin-graficos
```

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Reporte completo
```bash
python main.py --archivo ventas_mayo.xlsx --periodo "MAY'26"
```
Genera `Market_Report_2026-05-16_120530.pdf` + `Market_Report_2026-05-16_120530_Comentarios.xlsx`

### Ejemplo 2: Solo análisis
```bash
python main.py --archivo ventas_mayo.xlsx --solo-excel
```

### Ejemplo 3: Rápido (sin gráficos)
```bash
python main.py --archivo ventas_mayo.xlsx --sin-graficos
```

### Ejemplo 4: GUI
```bash
python gui.py
```

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

Ver `DEVELOPMENT.md` para más detalles.

---

## 📝 Licencia

MIT License - ver `LICENSE` para detalles

---

## 👨‍💻 Autor

**ojedadamiannsr-cmd**
- GitHub: [@ojedadamiannsr-cmd](https://github.com/ojedadamiannsr-cmd)

---

## 🙏 Agradecimientos

- Inspiración: Venezuelan Automotive Market Report
- Librerías: pandas, openpyxl, reportlab, matplotlib

---

## 📈 Roadmap

### v1.0 (Actual)
✅ CLI completo
✅ GUI con Tkinter
✅ PDF multi-página
✅ Excel con comentarios

### v1.1 (Próximo)
🔄 Gráficos mejorados
🔄 Validación avanzada
🔄 Manejo de errores robusto

### v2.0 (Futuro)
🔄 PowerPoint support
🔄 Cloud storage
🔄 Histórico de reportes

---

## 📞 Soporte

Para reportar bugs o sugerencias, abre un [Issue](https://github.com/ojedadamiannsr-cmd/Dami/issues) en GitHub.

---

**¡Disfruta generando reportes profesionales! 🚀**
