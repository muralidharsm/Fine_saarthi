"""Run with: python -m unittest discover -s tests -v"""
import sys
import io
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import demo_invoices, overview, issues, monthly, forecast, assistant, clean_invoices

class FinanceEngineTests(unittest.TestCase):
    def setUp(self):
        self.data=demo_invoices()

    def test_demo_data_is_deterministic(self):
        self.assertEqual(len(self.data),36)
        self.assertEqual(overview(self.data)['revenue'],577105)

    def test_months_are_chronological(self):
        from datetime import datetime
        months=monthly(self.data)['Month'].tolist()
        self.assertEqual(months, sorted(months,key=lambda x:datetime.strptime(x,'%b %Y')))

    def test_payment_review_flags(self):
        checks=issues(self.data)
        self.assertIn('Missing GSTIN', checks.Issue.tolist())
        self.assertIn('Overdue payment', checks.Issue.tolist())

    def test_forecast_reconciles(self):
        projection=forecast(self.data,100000,55000,61000)
        actual=100000+projection['Expected inflows'].sum()-projection['Expected outflows'].sum()
        self.assertAlmostEqual(projection.iloc[-1]['Projected closing balance'],actual)

    def test_native_language_guidance(self):
        self.assertIn('விற்பனை',assistant('sales?',self.data,'Tamil'))
        self.assertIn('बिक्री',assistant('sales?',self.data,'Hindi'))

    def test_csv_cleanup(self):
        test=self.data.drop(columns=['notes']).head(1)
        cleaned=clean_invoices(test)
        self.assertIn('notes', cleaned.columns)

if __name__=='__main__': unittest.main()
