"""
Program for Unit tests for Sales Analysis
So This file contains a full pytest test suite that verifies every major part of the SalesAnalysis class. Each test focuses on one analytical function,
checks for accuracy, checks boundary cases, and ensures functional correctness.
"""

import pytest
import csv
from assignment2.sales_analysis import SalesAnalysis


@pytest.fixture
def sample_csv_file(tmp_path):
    """
    Create a temporary CSV file for testing, because-
    1. Unit tests should not depend on real external files.
    2. tmp_path provides a temporary folder that gets cleaned up automatically.
    3. We generate known test data so our tests have predictable outcomes.

    This fixture returns the file path as a string for use in tests.
    """
    csv_file = tmp_path / "test_sales.csv"

    # Sample dataset representing a small but diverse set of sales transactions- I have taken first 5 transactions for testing
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

    # this will write the data into the CSV file so SalesAnalysis can load it
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return str(csv_file)  # this will return the path as string so SalesAnalysis can read it


@pytest.fixture
def analysis(sample_csv_file):
    """
    this builds a SalesAnalysis instance using the sample CSV file above. This fixture makes it easy for tests to reuse the same preloaded object without 
    writing duplicate setup logic.
    """
    return SalesAnalysis(sample_csv_file)


class TestSalesAnalysis:
    #Main test suite covering all analytical functions in SalesAnalysis.

    def test_load_data(self, analysis):
        """
        it will test that CSV data is loaded correctly.
        This verifies the File reading works, DictReader parsed rows correctly and the number of loaded rows matches expected count.
        """
        assert len(analysis.data) == 5
        assert analysis.data[0]['product'] == 'Laptop'

    def test_total_revenue(self, analysis):
        """
        this will test whether total revenue is computed correctly using reduce().
        
        Expected:
        2000 + 125 + 450 + 1000 + 400 = 3975
        """
        total = analysis.total_revenue()
        assert total == 3975.00

    def test_revenue_by_category(self, analysis):
        """
        it will test grouping and revenue calculation by product category. I validate the exact revenue totals for each category.
        """
        category_revenue = analysis.revenue_by_category()

        assert category_revenue['Electronics'] == 3000.00
        assert category_revenue['Clothing'] == 125.00
        assert category_revenue['Home & Garden'] == 850.00

    def test_revenue_by_region(self, analysis):
        """
        this will test revenue grouped by region using itertools.groupby.
        
        Ensures grouping + reduce logic produces accurate sums.
        """
        region_revenue = analysis.revenue_by_region()

        assert region_revenue['North'] == 2400.00
        assert region_revenue['South'] == 125.00
        assert region_revenue['East'] == 450.00
        assert region_revenue['West'] == 1000.00

    def test_top_products_by_revenue(self, analysis):
        """
        it test identification of top-selling products. 
        Expected revenue ranking:
        1. Laptop (3000)
        2. Chair (450)
        """
        top_products = analysis.top_products_by_revenue(3)

        assert top_products[0] == ('Laptop', 3000.00)
        assert top_products[1] == ('Chair', 450.00)

    def test_average_transaction_value(self, analysis):
        """
        It test calculation of average revenue per transaction.
        Total revenue = 3975
        Total transactions = 5
        Average = 795
        """
        avg = analysis.average_transaction_value()
        assert avg == 795.00

    def test_monthly_revenue_trend(self, analysis):
        """
        It test monthly revenue totals.
        January = 2000 + 125 + 450 = 2575
        February = 1000 + 400 = 1400
        """
        monthly = analysis.monthly_revenue_trend()

        assert monthly['2024-01'] == 2575.00
        assert monthly['2024-02'] == 1400.00

    def test_quantity_statistics(self, analysis):
        """
        It test minimum, maximum, and average quantity.
        Quantities = [2, 5, 3, 1, 2]
        min = 1
        max = 5
        avg = 2.6
        """
        stats = analysis.quantity_statistics()

        assert stats['min'] == 1.0
        assert stats['max'] == 5.0
        assert stats['average'] == 2.6

    def test_filter_high_value_transactions(self, analysis):
        """
        This will test filtering of transactions above a given threshold.

        With threshold = 500, valid transactions are:
        - 2000.00
        - 1000.00
        """
        high_value = analysis.filter_high_value_transactions(500)

        # Should only return 2 transactions ≥ 500
        assert len(high_value) == 2
        assert all(float(t['total_sales']) >= 500 for t in high_value)

    def test_products_by_region(self, analysis):
        """
        it will test mapping of region → list of unique products. For region 'North', products = Laptop + Table.
        """
        products = analysis.products_by_region()

        assert 'North' in products
        assert set(products['North']) == {'Laptop', 'Table'}

    def test_empty_csv(self, tmp_path):
        """
        this will test behavior when CSV has only headers and no rows.

        Ensures that the Revenue is zero, Average value is zero and Grouping methods return empty dicts
        """
        csv_file = tmp_path / "empty.csv"

        # This write CSV headers only (no data rows)
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
        """
        this tests the analysis logic using a CSV with exactly one transaction. This validates that all calculations reduce to the single value.
        """
        csv_file = tmp_path / "single.csv"

        data = [
            {"transaction_id": "1", "date": "2024-01-15", "product": "Laptop",
             "category": "Electronics", "region": "North", "quantity": "1",
             "unit_price": "1000.00", "total_sales": "1000.00"}
        ]

        # this will write single-row CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        analysis = SalesAnalysis(str(csv_file))

        assert analysis.total_revenue() == 1000.00
        assert analysis.average_transaction_value() == 1000.00
        assert list(analysis.revenue_by_category().values()) == [1000.00]

    def test_data_integrity(self, analysis):
        """
        For Final validation: ensure all computed totals add up consistently.
        The sum of: category revenues and region revenues must equal total revenue (within floating point tolerance).
        """
        category_total = sum(analysis.revenue_by_category().values())
        region_total = sum(analysis.revenue_by_region().values())
        total = analysis.total_revenue()

        # Floating-point comparison uses tolerance check
        assert abs(category_total - total) < 0.01
        assert abs(region_total - total) < 0.01
