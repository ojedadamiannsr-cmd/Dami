"""
tests/test_calculator.py - Tests unitarios para MetricsCalculator
"""

import unittest
import pandas as pd
from modules.calculator import MetricsCalculator


class TestMetricsCalculator(unittest.TestCase):
    """Tests para cálculos de métricas."""
    
    def test_percentage_change(self):
        """Test variación porcentual."""
        result = MetricsCalculator.calculate_percentage_change(100, 80)
        self.assertAlmostEqual(result, 25.0, places=2)
    
    def test_percentage_change_negative(self):
        """Test variación porcentual negativa."""
        result = MetricsCalculator.calculate_percentage_change(80, 100)
        self.assertAlmostEqual(result, -20.0, places=2)
    
    def test_market_share(self):
        """Test cálculo de market share."""
        result = MetricsCalculator.calculate_market_share(100, 500)
        self.assertAlmostEqual(result, 20.0, places=2)
    
    def test_saar(self):
        """Test cálculo de SAAR."""
        result = MetricsCalculator.calculate_saar(1000, 1.0)
        self.assertAlmostEqual(result, 12000, places=0)
    
    def test_saar_with_seasonality(self):
        """Test SAAR con índice de seasonalidad."""
        result = MetricsCalculator.calculate_saar(1000, 0.8)
        self.assertAlmostEqual(result, 15000, places=0)
    
    def test_forecast_delta(self):
        """Test delta vs forecast."""
        result = MetricsCalculator.calculate_forecast_delta(12000, 10000)
        self.assertAlmostEqual(result, 20.0, places=2)


class TestDataProcessing(unittest.TestCase):
    """Tests para procesamiento de datos."""
    
    def setUp(self):
        """Prepara datos para tests."""
        self.market_df = pd.DataFrame({
            "Marca": ["TOYOTA", "JAC", "CHANGAN"],
            "Mes Actual": [680, 520, 385],
            "Mes PY": [648, 478, 395],
            "YTD": [1850, 1420, 1210],
            "YTD PY": [1790, 1305, 1180],
        })
        
        self.seasonality_df = pd.DataFrame({
            "Mes": ["May"],
            "Índice": [1.0325],
        })
    
    def test_process_market_data(self):
        """Test procesamiento de datos de mercado."""
        result = MetricsCalculator.process_market_data(
            self.market_df,
            self.seasonality_df
        )
        
        # Verificar que se agregaron las nuevas columnas
        self.assertIn("vs PY %", result.columns)
        self.assertIn("Market Share %", result.columns)
        self.assertIn("SAAR", result.columns)
        
        # Verificar que el número de filas se mantiene
        self.assertEqual(len(result), len(self.market_df))


if __name__ == "__main__":
    unittest.main()
