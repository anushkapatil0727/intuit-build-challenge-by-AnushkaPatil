"""
Unit tests for Sales Analysis
"""

import pytest
import csv
from assignment2.sales_analysis import SalesAnalysis


@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a temporary CSV file for testing"""
    csv_file = tmp_path / "test_sales.csv"
    
    data = [
        {"transaction_id": "1", "date": "2024-01-15", "product": "Laptop", 
         "category": "Electronics", "region": "North", "quantity": "2", 
         "unit_price": "1000.00", "total_sales": "2000.00"},
        {"transaction_id": "2", "date": "2024-01-16", "product": "Shirt", 
         "category": "Clothing", "region": "South", "quantity": "5", 
         "unit_price": "25.00", "total_sales": "125.00"},
        {"transaction_id": "3", "date": "2024-01-17", "product": "Chair", 
         "category": "Home & Garden", "region": "East", "quantity": "3", 
         "unit_price": "150.00", "total_sales": "450.00"},
        {"transaction_id": "4", "date": "2024-02-15", "product": "Laptop", 
         "category": "Electronics", "region": "West", "quantity": "1", 
         "unit_price": "1000.00", "total_sales": "1000.00"},
        {"transaction_id": "5", "date": "2024-02-16", "product": "Table", 
         "category": "Home & Garden", "region": "North", "quantity": "2", 
         "unit_price": "200.00", "total_sales": "400.00"},
    ]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    return str(csv_file)


@pytest.fixture
def analysis(sample_csv_file):
    """Create SalesAnalysis instance with test data"""
    return SalesAnalysis(sample_csv_file)


class TestSalesAnalysis:
    """Test suite for SalesAnalysis class"""
    
    def test_load_data(self, analysis):
        """Test that data loads correctly"""
        assert len(analysis.data) == 5
        assert analysis.data[0]['product'] == 'Laptop'
    
    def test_total_revenue(self, analysis):
        """Test total revenue calculation"""
        total = analysis.total_revenue()
        assert total == 3975.00
    
    def test_revenue_by_category(self, analysis):
        """Test revenue grouped by category"""
        category_revenue = analysis.revenue_by_category()
        
        assert category_revenue['Electronics'] == 3000.00
        assert category_revenue['Clothing'] == 125.00
        assert category_revenue['Home & Garden'] == 850.00
    
    def test_revenue_by_region(self, analysis):
        """Test revenue grouped by region"""
        region_revenue = analysis.revenue_by_region()
        
        assert region_revenue['North'] == 2400.00
        assert region_revenue['South'] == 125.00
        assert region_revenue['East'] == 450.00
        assert region_revenue['West'] == 1000.00
    
    def test_top_products_by_revenue(self, analysis):
        """Test top products ranking"""
        top_products = analysis.top_products_by_revenue(3)
        
        assert top_products[0] == ('Laptop', 3000.00)
        assert top_products[1] == ('Chair', 450.00)
    
    def test_average_transaction_value(self, analysis):
        """Test average transaction value"""
        avg = analysis.average_transaction_value()
        assert avg == 795.00  # 3975 / 5
    
    def test_monthly_revenue_trend(self, analysis):
        """Test monthly revenue aggregation"""
        monthly = analysis.monthly_revenue_trend()
        
        assert monthly['2024-01'] == 2575.00
        assert monthly['2024-02'] == 1400.00
    
    def test_quantity_statistics(self, analysis):
        """Test quantity statistics calculation"""
        stats = analysis.quantity_statistics()
        
        assert stats['min'] == 1.0
        assert stats['max'] == 5.0
        assert stats['average'] == 2.6  # (2+5+3+1+2) / 5
    
    def test_filter_high_value_transactions(self, analysis):
        """Test filtering high-value transactions"""
        high_value = analysis.filter_high_value_transactions(500)
        
        # FIXED TEST — Correct expected count is 2, not 3
        assert len(high_value) == 2
        assert all(float(t['total_sales']) >= 500 for t in high_value)
    
    def test_products_by_region(self, analysis):
        """Test products grouped by region"""
        products = analysis.products_by_region()
        
        assert 'North' in products
        assert set(products['North']) == {'Laptop', 'Table'}
    
    def test_empty_csv(self, tmp_path):
        """Test handling of empty CSV file"""
        csv_file = tmp_path / "empty.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'transaction_id', 'date', 'product', 'category', 
                'region', 'quantity', 'unit_price', 'total_sales'
            ])
            writer.writeheader()
        
        analysis = SalesAnalysis(str(csv_file))
        
        assert analysis.total_revenue() == 0.0
        assert analysis.average_transaction_value() == 0.0
        assert analysis.revenue_by_category() == {}
    
    def test_single_transaction(self, tmp_path):
        """Test with single transaction"""
        csv_file = tmp_path / "single.csv"
        
        data = [
            {"transaction_id": "1", "date": "2024-01-15", "product": "Laptop", 
             "category": "Electronics", "region": "North", "quantity": "1", 
             "unit_price": "1000.00", "total_sales": "1000.00"}
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        analysis = SalesAnalysis(str(csv_file))
        
        assert analysis.total_revenue() == 1000.00
        assert analysis.average_transaction_value() == 1000.00
        assert list(analysis.revenue_by_category().values()) == [1000.00]
    
    def test_data_integrity(self, analysis):
        """Ensure data aggregated by category and region matches total"""
        category_total = sum(analysis.revenue_by_category().values())
        region_total = sum(analysis.revenue_by_region().values())
        total = analysis.total_revenue()
        
        assert abs(category_total - total) < 0.01
        assert abs(region_total - total) < 0.01
