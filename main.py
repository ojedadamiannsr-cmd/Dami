#!/usr/bin/env python3
"""
main.py - Interfaz CLI del Market Report Generator
Uso: python main.py --archivo datos.xlsx [opciones]
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

from modules.reader import ExcelReader
from modules.calculator import MetricsCalculator
from modules.charts import ChartGenerator
from modules.pdf_generator import PDFGenerator
from modules.excel_exporter import ExcelExporter
from config import OUTPUTS, LOGGING

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOGGING["level"]),
    format=LOGGING["format"]
)
logger = logging.getLogger(__name__)


def main():
    """Función principal de CLI."""
    parser = argparse.ArgumentParser(
        description="🚗 Market Report Generator - Generador de reportes automotrices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Generar PDF y Excel
  python main.py --archivo datos.xlsx
  
  # Solo PDF
  python main.py --archivo datos.xlsx --solo-pdf
  
  # Solo Excel
  python main.py --archivo datos.xlsx --solo-excel
  
  # Salida personalizada
  python main.py --archivo datos.xlsx --salida ./mis_reportes/
  
  # Con período personalizado
  python main.py --archivo datos.xlsx --periodo "JUN'26"
        """
    )
    
    parser.add_argument(
        "--archivo", "-a",
        required=True,
        help="Ruta del archivo Excel de entrada (requerido)"
    )
    
    parser.add_argument(
        "--salida", "-o",
        default=OUTPUTS["pdf"],
        help=f"Directorio de salida (default: {OUTPUTS['pdf']})"
    )
    
    parser.add_argument(
        "--periodo", "-p",
        default=None,
        help="Período del reporte (ej: MAY'26). Si no se especifica, se toma del Excel"
    )
    
    parser.add_argument(
        "--solo-pdf",
        action="store_true",
        help="Generar solo PDF (sin Excel)"
    )
    
    parser.add_argument(
        "--solo-excel",
        action="store_true",
        help="Generar solo Excel (sin PDF)"
    )
    
    parser.add_argument(
        "--sin-graficos",
        action="store_true",
        help="Generar sin gráficos (más rápido)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar más detalles durante la ejecución"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Crear directorio de salida si no existe
        Path(args.salida).mkdir(parents=True, exist_ok=True)
        
        logger.info("🚀 Iniciando Market Report Generator")
        logger.info(f"📁 Archivo: {args.archivo}")
        
        # 1. Leer Excel
        logger.info("📖 Leyendo archivo Excel...")
        reader = ExcelReader(args.archivo)
        data = reader.read_all_sheets()
        
        # Extraer período del Excel si no se especificó
        periodo = args.periodo
        if not periodo and "Dashboard" in data:
            periodo = data["Dashboard"].iloc[0]["Período"] if len(data["Dashboard"]) > 0 else "N/A"
        
        logger.info(f"📅 Período: {periodo}")
        
        # 2. Procesar mercado
        if "Market Data" in data and "Seasonality" in data:
            logger.info("🧮 Calculando métricas...")
            market_processed = MetricsCalculator.process_market_data(
                data["Market Data"],
                data["Seasonality"]
            )
            logger.info("✓ Métricas calculadas")
        else:
            logger.warning("⚠️  No se encontraron hojas Market Data o Seasonality")
            market_processed = data.get("Market Data", None)
        
        # 3. Generar gráficos
        charts_dir = Path(OUTPUTS["charts"])
        charts_dir.mkdir(parents=True, exist_ok=True)
        chart_paths = {}
        
        if not args.sin_graficos and market_processed is not None:
            logger.info("📊 Generando gráficos...")
            chart_gen = ChartGenerator(str(charts_dir))
            
            try:
                # Gráficos del mercado
                if "Mes Actual" in market_processed.columns and "Mes PY" in market_processed.columns:
                    top_10 = market_processed.nlargest(10, "Mes Actual")
                    chart_paths["monthly_vs_py"] = chart_gen.generate_monthly_vs_py_chart(
                        top_10["Marca"].tolist(),
                        top_10["Mes Actual"].tolist(),
                        top_10["Mes PY"].tolist()
                    )
                
                # Pie chart
                if "Market Share %" in market_processed.columns:
                    top_5 = market_processed.nlargest(5, "Market Share %")
                    chart_paths["market_share"] = chart_gen.generate_market_share_pie(
                        top_5["Marca"].tolist(),
                        top_5["Market Share %"].tolist()
                    )
                
                # Growth chart
                if "vs PY %" in market_processed.columns:
                    top_10 = market_processed.nlargest(10, "Mes Actual")
                    chart_paths["growth"] = chart_gen.generate_growth_chart(
                        top_10["Marca"].tolist(),
                        top_10["vs PY %"].tolist()
                    )
                
                logger.info(f"✓ {len(chart_paths)} gráficos generados")
            except Exception as e:
                logger.warning(f"⚠️  Error generando gráficos: {str(e)}")
        
        # 4. Generar PDF
        if not args.solo_excel:
            logger.info("📄 Generando PDF...")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            pdf_path = Path(args.salida) / f"Market_Report_{timestamp}.pdf"
            
            pdf_gen = PDFGenerator(str(pdf_path))
            try:
                pdf_gen.generate_pdf(
                    periodo=periodo or "N/A",
                    market_df=market_processed if market_processed is not None else None,
                    segment_df=data.get("Segments", None),
                    regional_df=data.get("Regional", None),
                    chart_paths=chart_paths
                )
                logger.info(f"✅ PDF generado: {pdf_path}")
            except Exception as e:
                logger.error(f"❌ Error generando PDF: {str(e)}")
                raise
        
        # 5. Generar Excel
        if not args.solo_pdf and market_processed is not None:
            logger.info("📊 Generando Excel...")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            excel_path = Path(args.salida) / f"Market_Report_{timestamp}_Comentarios.xlsx"
            
            excel_exp = ExcelExporter(str(excel_path))
            try:
                # Resumen
                summary = {
                    "periodo": periodo or "N/A",
                    "total_market": market_processed["Mes Actual"].sum() if "Mes Actual" in market_processed.columns else 0,
                    "total_ytd": market_processed["YTD"].sum() if "YTD" in market_processed.columns else 0,
                    "market_growth": market_processed["vs PY %"].mean() if "vs PY %" in market_processed.columns else 0,
                    "ytd_growth": market_processed["YTD vs PY %"].mean() if "YTD vs PY %" in market_processed.columns else 0,
                    "num_brands": len(market_processed),
                }
                
                excel_exp.add_summary_sheet(summary)
                excel_exp.add_market_data_sheet(market_processed)
                
                if "Segments" in data and data["Segments"] is not None:
                    excel_exp.add_segment_data_sheet(data["Segments"])
                
                excel_exp.add_comments_sheet(market_processed)
                excel_exp.save()
                logger.info(f"✅ Excel generado: {excel_path}")
            except Exception as e:
                logger.error(f"❌ Error generando Excel: {str(e)}")
                raise
        
        # Resumen final
        logger.info("=" * 60)
        logger.info("✅ ¡REPORTES GENERADOS EXITOSAMENTE!")
        logger.info(f"📁 Ubicación: {Path(args.salida).absolute()}")
        logger.info("=" * 60)
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"❌ Archivo no encontrado: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
