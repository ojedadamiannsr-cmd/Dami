# DEVELOPMENT.md
# 📝 Guía de Desarrollo

## Estructura del Proyecto

```
Dami/
├── main.py                    # CLI principal
├── gui.py                     # Interfaz gráfica
├── config.py                  # Configuración centralizada
├── requirements.txt           # Dependencias
├── setup.sh                   # Script de instalación
├── README.md                  # Documentación
├── QUICKSTART.md              # Inicio rápido
├── DEVELOPMENT.md             # Esta guía
│
├── modules/                   # Núcleo de la aplicación
│   ├── __init__.py
│   ├── reader.py              # Lectura de Excel
│   ├── calculator.py          # Cálculos y métricas
│   ├── formatter.py           # Formateo de datos
│   ├── charts.py              # Generación de gráficos
│   ├── pdf_generator.py       # Generación de PDF
│   └── excel_exporter.py      # Exportación a Excel
│
├── tests/                     # Tests unitarios
│   ├── __init__.py
│   └── test_calculator.py
│
├── examples/                  # Ejemplos y plantillas
│   ├── __init__.py
│   ├── sample_data.py         # Generador de datos
│   └── TEMPLATE_Market_Report.xlsx  # Plantilla
│
└── reports/                   # Salida (generado)
    ├── Market_Report_*.pdf
    └── Market_Report_*_Comentarios.xlsx
```

## Flujo de Datos

```
Excel Input
    ↓
ExcelReader (modules/reader.py)
    ↓
MetricsCalculator (modules/calculator.py)
    ├── Variaciones %
    ├── Market Share
    ├── SAAR
    └── Forecast Delta
    ↓
ChartGenerator (modules/charts.py)
    ├── Bar Charts
    ├── Line Charts
    ├── Pie Charts
    └── Growth Charts
    ↓
├─→ PDFGenerator (modules/pdf_generator.py) → PDF Output
└─→ ExcelExporter (modules/excel_exporter.py) → Excel Output
```

## Módulos Principales

### 1. **reader.py** - ExcelReader
Lee datos desde archivos Excel con múltiples hojas.

```python
reader = ExcelReader('datos.xlsx')
market_df = reader.get_market_data()
seasonality_df = reader.get_seasonality_data()
```

**Métodos:**
- `read_all_sheets()` - Lee todas las hojas
- `read_sheet(name)` - Lee hoja específica
- `get_market_data()`, `get_segments_data()`, etc.
- `validate_structure()` - Valida estructura mínima

### 2. **calculator.py** - MetricsCalculator
Calcula automáticamente todas las métricas.

```python
# Variación porcentual
var = MetricsCalculator.calculate_percentage_change(current, previous)

# Market share
share = MetricsCalculator.calculate_market_share(sales, total)

# SAAR
saar = MetricsCalculator.calculate_saar(monthly_sales, seasonality_index)

# Procesar DataFrame
df = MetricsCalculator.process_market_data(market_df, seasonality_df)
```

### 3. **formatter.py** - Formatter
Formatea datos para presentación.

```python
# Moneda
Formatter.format_currency(1000.5) → "1,000"

# Porcentaje
Formatter.format_percentage(5.5) → "+5.5%"

# Color según variación
color = Formatter.get_color_for_percentage(-2.5) → "#F44336"
```

### 4. **charts.py** - ChartGenerator
Genera gráficos profesionales con matplotlib.

```python
gen = ChartGenerator('temp/charts')

# Bar chart mes vs PY
gen.generate_monthly_vs_py_chart(brands, current, previous)

# Pie chart market share
gen.generate_market_share_pie(brands, shares)

# Growth chart
gen.generate_growth_chart(brands, growth_pct)
```

### 5. **pdf_generator.py** - PDFGenerator
Genera PDF con ReportLab.

```python
pdf = PDFGenerator('reporte.pdf')
pdf.generate_pdf(
    periodo='MAY\'26',
    market_df=market_df,
    segment_df=segment_df,
    chart_paths=chart_paths
)
```

### 6. **excel_exporter.py** - ExcelExporter
Exporta a Excel con openpyxl.

```python
excel = ExcelExporter('reporte.xlsx')
excel.add_summary_sheet(summary)
excel.add_market_data_sheet(market_df)
excel.add_comments_sheet(market_df)
excel.save()
```

## Desarrollo Local

### Crear rama de desarrollo
```bash
git checkout -b feature/nueva-caracteristica
```

### Agregar nuevas métricas
1. Crear método en `calculator.py`:
```python
@staticmethod
def calculate_nueva_metrica(valor1, valor2):
    """Calcula nueva métrica."""
    return (valor1 / valor2) * 100
```

2. Agregar test en `tests/test_calculator.py`

3. Integrar en `process_market_data()`

### Agregar nuevo tipo de gráfico
1. Crear método en `charts.py`:
```python
def generate_nuevo_grafico(self, datos):
    """Genera nuevo gráfico."""
    fig, ax = plt.subplots()
    # ... código del gráfico
    plt.savefig(filepath)
    return str(filepath)
```

2. Llamar desde `pdf_generator.py`

## Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Con cobertura
python -m pytest tests/ --cov=modules

# Test específico
python -m pytest tests/test_calculator.py::TestMetricsCalculator::test_percentage_change
```

### Agregar nuevo test
```python
# tests/test_nuevo.py
import unittest
from modules.nuevo_modulo import NuevaClase

class TestNuevaClase(unittest.TestCase):
    def test_nuevo_metodo(self):
        resultado = NuevaClase.nuevo_metodo()
        self.assertEqual(resultado, valor_esperado)
```

## Configuración

### Cambiar colores corporativos
Editar `config.py`:
```python
COLORS = {
    "primary_red": "#NUEVO_COLOR",
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

## Logging

La aplicación usa logging estándar de Python.

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Mensaje de información")
logger.warning("Mensaje de advertencia")
logger.error("Mensaje de error")
logger.debug("Mensaje de debug")
```

## Performance

### Optimizaciones implementadas
- Lectura eficiente de Excel con pandas
- Cálculos vectorizados con numpy
- Generación de gráficos en thread separado (GUI)
- Caché de estilos PDF

### Mejoras futuras
- Procesamiento paralelo de múltiples reportes
- Caché de gráficos
- Compresión de PDF
- Almacenamiento en cloud

## Issues Comunes

### "Archivo muy pesado"
- Limitar número de marcas mostradas en gráficos
- Reducir resolución DPI de gráficos

### "Memoria insuficiente"
- Procesar por lotes
- Usar dtype apropiados en pandas

### "PDF tarda mucho"
- Reducir número de páginas
- Usar gráficos más simples

## Versionado

Formato semántico: `MAJOR.MINOR.PATCH`

- v1.0.0 - MVP con CLI
- v1.1.0 - GUI agregada
- v2.0.0 - Cloud storage

## Documentación del Código

Usar docstrings con formato Google:

```python
def mi_funcion(param1: str, param2: int) -> dict:
    """
    Descripción breve de la función.
    
    Descripción más larga si es necesario.
    
    Args:
        param1: Descripción del param1
        param2: Descripción del param2
        
    Returns:
        Descripción del retorno
        
    Raises:
        ValueError: Cuándo se lanza esta excepción
    """
```

## Contribuir

1. Fork el proyecto
2. Crear rama con tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

**Última actualización**: 2026-05-16
