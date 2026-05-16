#!/usr/bin/env python3
"""
gui.py - Interfaz Gráfica (GUI) del Market Report Generator
Usa Tkinter para interfaz amigable sin CLI
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from threading import Thread
import logging

from modules.reader import ExcelReader
from modules.calculator import MetricsCalculator
from modules.charts import ChartGenerator
from modules.pdf_generator import PDFGenerator
from modules.excel_exporter import ExcelExporter
from config import OUTPUTS

logger = logging.getLogger(__name__)


class MarketReportGUI:
    """Interfaz gráfica para Market Report Generator."""
    
    def __init__(self, root):
        """Inicializa la GUI."""
        self.root = root
        self.root.title("🚗 Market Report Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.selected_file = tk.StringVar()
        self.periodo = tk.StringVar()
        self.gen_pdf = tk.BooleanVar(value=True)
        self.gen_excel = tk.BooleanVar(value=True)
        self.gen_charts = tk.BooleanVar(value=True)
        
        self._create_widgets()
        self._center_window()
    
    def _create_widgets(self):
        """Crea widgets de la interfaz."""
        # Título
        title = tk.Label(
            self.root,
            text="Market Report Generator",
            font=("Arial", 18, "bold"),
            fg="#C41E3A"
        )
        title.pack(pady=15)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Selección de archivo
        ttk.Label(main_frame, text="Archivo Excel:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(file_frame, textvariable=self.selected_file, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Examinar", command=self._browse_file).pack(side=tk.LEFT, padx=5)
        
        # Período
        ttk.Label(main_frame, text="Período (ej: MAY'26):", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15, 0))
        ttk.Entry(main_frame, textvariable=self.periodo, width=30).pack(anchor=tk.W, pady=5)
        
        # Opciones
        ttk.Label(main_frame, text="Opciones:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15, 5))
        
        ttk.Checkbutton(main_frame, text="Generar PDF", variable=self.gen_pdf).pack(anchor=tk.W)
        ttk.Checkbutton(main_frame, text="Generar Excel con comentarios", variable=self.gen_excel).pack(anchor=tk.W)
        ttk.Checkbutton(main_frame, text="Incluir gráficos", variable=self.gen_charts).pack(anchor=tk.W)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Generar Reporte", command=self._generate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salir", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(15, 0))
        
        # Log
        ttk.Label(main_frame, text="Registro:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15, 5))
        
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=6, width=60, yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
    
    def _center_window(self):
        """Centra la ventana en pantalla."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def _browse_file(self):
        """Selecciona archivo Excel."""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file.set(filename)
            self._log(f"✓ Archivo seleccionado: {Path(filename).name}")
    
    def _log(self, message):
        """Agrega mensaje al log."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def _generate(self):
        """Genera reporte."""
        if not self.selected_file.get():
            messagebox.showerror("Error", "Por favor selecciona un archivo Excel")
            return
        
        if not self.gen_pdf.get() and not self.gen_excel.get():
            messagebox.showerror("Error", "Selecciona al menos PDF o Excel")
            return
        
        # Ejecutar en thread para no bloquear GUI
        thread = Thread(target=self._generate_thread)
        thread.start()
    
    def _generate_thread(self):
        """Hilo para generar reporte."""
        try:
            self.log_text.delete(1.0, tk.END)
            self.progress.start()
            self._log("🚀 Iniciando generación de reporte...")
            
            archivo = self.selected_file.get()
            
            # Leer Excel
            self._log("📖 Leyendo Excel...")
            reader = ExcelReader(archivo)
            data = reader.read_all_sheets()
            
            # Período
            periodo = self.periodo.get() or "N/A"
            if not self.periodo.get() and "Dashboard" in data and len(data["Dashboard"]) > 0:
                periodo = data["Dashboard"].iloc[0]["Período"]
            
            self._log(f"📅 Período: {periodo}")
            
            # Procesar datos
            self._log("🧮 Calculando métricas...")
            market_processed = MetricsCalculator.process_market_data(
                data.get("Market Data"),
                data.get("Seasonality")
            )
            
            # Gráficos
            chart_paths = {}
            if self.gen_charts.get():
                self._log("📊 Generando gráficos...")
                charts_dir = Path(OUTPUTS["charts"])
                charts_dir.mkdir(parents=True, exist_ok=True)
                chart_gen = ChartGenerator(str(charts_dir))
                
                try:
                    if "Mes Actual" in market_processed.columns:
                        top_10 = market_processed.nlargest(10, "Mes Actual")
                        chart_paths["monthly_vs_py"] = chart_gen.generate_monthly_vs_py_chart(
                            top_10["Marca"].tolist(),
                            top_10["Mes Actual"].tolist(),
                            top_10["Mes PY"].tolist()
                        )
                    
                    if "Market Share %" in market_processed.columns:
                        top_5 = market_processed.nlargest(5, "Market Share %")
                        chart_paths["market_share"] = chart_gen.generate_market_share_pie(
                            top_5["Marca"].tolist(),
                            top_5["Market Share %"].tolist()
                        )
                except Exception as e:
                    self._log(f"⚠️  Error en gráficos: {str(e)}")
            
            # PDF
            if self.gen_pdf.get():
                self._log("📄 Generando PDF...")
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                pdf_path = Path(OUTPUTS["pdf"]) / f"Market_Report_{timestamp}.pdf"
                
                Path(OUTPUTS["pdf"]).mkdir(parents=True, exist_ok=True)
                
                pdf_gen = PDFGenerator(str(pdf_path))
                pdf_gen.generate_pdf(
                    periodo=periodo,
                    market_df=market_processed,
                    segment_df=data.get("Segments"),
                    regional_df=data.get("Regional"),
                    chart_paths=chart_paths
                )
                self._log(f"✅ PDF: {pdf_path.name}")
            
            # Excel
            if self.gen_excel.get():
                self._log("📊 Generando Excel...")
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                excel_path = Path(OUTPUTS["excel"]) / f"Market_Report_{timestamp}_Comentarios.xlsx"
                
                Path(OUTPUTS["excel"]).mkdir(parents=True, exist_ok=True)
                
                excel_exp = ExcelExporter(str(excel_path))
                excel_exp.add_summary_sheet({
                    "periodo": periodo,
                    "total_market": market_processed["Mes Actual"].sum(),
                    "num_brands": len(market_processed),
                })
                excel_exp.add_market_data_sheet(market_processed)
                excel_exp.add_comments_sheet(market_processed)
                excel_exp.save()
                self._log(f"✅ Excel: {excel_path.name}")
            
            self.progress.stop()
            self._log("\n✅ ¡Reporte generado exitosamente!")
            messagebox.showinfo("Éxito", "✅ Reportes generados\n\nVer carpeta: reports/")
            
        except Exception as e:
            self.progress.stop()
            self._log(f"\n❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")


def main():
    """Función principal."""
    root = tk.Tk()
    app = MarketReportGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
