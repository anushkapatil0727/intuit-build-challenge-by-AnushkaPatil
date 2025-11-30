"""
Sales Data Analysis using Functional Programming

Performs comprehensive data analysis on CSV sales data using functional
programming paradigms including lambda expressions, map/filter operations,
itertools, and functools for aggregation and grouping.
"""

import csv
from functools import reduce
from itertools import groupby
from typing import List, Dict, Tuple, Callable
from operator import itemgetter
from datetime import datetime


class SalesAnalysis:
    """
    Sales data analysis using functional programming techniques.
    
    Demonstrates:
    - Lambda expressions
    - Map/filter/reduce operations
    - Grouping operations using itertools.groupby
    - Functional composition
    """
    
    def __init__(self, csv_file_path: str):
        """
        Initialize sales analysis with CSV data.
        
        Args:
            csv_file_path: Path to the CSV file containing sales data
        """
        self.csv_file_path = csv_file_path
        self.data = self._load_data()
    
    def _load_data(self) -> List[Dict]:
        """
        Load data from CSV file.
        
        Returns:
            List of dictionaries representing sales transactions
        """
        with open(self.csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    
    def _to_numeric(self, value: str) -> float:
        """Convert string to numeric value."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def total_revenue(self) -> float:
        """
        Calculate total revenue using reduce and lambda.
        
        Returns:
            Total revenue across all transactions
        """
        return reduce(
            lambda acc, record: acc + self._to_numeric(record['total_sales']),
            self.data,
            0.0
        )
    
    def revenue_by_category(self) -> Dict[str, float]:
        """
        Calculate revenue grouped by product category using groupby.
        
        Returns:
            Dictionary mapping category to total revenue
        """
        # Sort by category for groupby
        sorted_data = sorted(self.data, key=itemgetter('category'))
        
        # Group and aggregate using functional approach
        grouped = groupby(sorted_data, key=itemgetter('category'))
        
        return {
            category: reduce(
                lambda acc, record: acc + self._to_numeric(record['total_sales']),
                list(records),
                0.0
            )
            for category, records in grouped
        }
    
    def revenue_by_region(self) -> Dict[str, float]:
        """
        Calculate revenue grouped by region using groupby.
        
        Returns:
            Dictionary mapping region to total revenue
        """
        # Sort by region for groupby
        sorted_data = sorted(self.data, key=itemgetter('region'))
        
        # Group and aggregate
        grouped = groupby(sorted_data, key=itemgetter('region'))
        
        return {
            region: reduce(
                lambda acc, record: acc + self._to_numeric(record['total_sales']),
                list(records),
                0.0
            )
            for region, records in grouped
        }
    
    def top_products_by_revenue(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        Find top N products by revenue using functional operations.
        
        Args:
            n: Number of top products to return
            
        Returns:
            List of tuples (product_name, revenue) sorted by revenue descending
        """
        # Sort by product for groupby
        sorted_data = sorted(self.data, key=itemgetter('product'))
        grouped = groupby(sorted_data, key=itemgetter('product'))
        
        # Calculate revenue per product
        product_revenues = [
            (
                product,
                reduce(
                    lambda acc, record: acc + self._to_numeric(record['total_sales']),
                    list(records),
                    0.0
                )
            )
            for product, records in grouped
        ]
        
        # Sort by revenue descending and take top N
        return sorted(product_revenues, key=lambda x: x[1], reverse=True)[:n]
    
    def average_transaction_value(self) -> float:
        """
        Calculate average transaction value using map and reduce.
        
        Returns:
            Average sales value per transaction
        """
        if not self.data:
            return 0.0
        
        total = reduce(
            lambda acc, record: acc + self._to_numeric(record['total_sales']),
            self.data,
            0.0
        )
        
        return total / len(self.data)
    
    def monthly_revenue_trend(self) -> Dict[str, float]:
        """
        Calculate revenue trend by month using groupby.
        
        Returns:
            Dictionary mapping year-month to revenue
        """
        # Extract year-month and sort
        data_with_month = list(map(
            lambda record: {
                **record,
                'year_month': record['date'][:7]  # Extract YYYY-MM
            },
            self.data
        ))
        
        sorted_data = sorted(data_with_month, key=itemgetter('year_month'))
        grouped = groupby(sorted_data, key=itemgetter('year_month'))
        
        return {
            month: reduce(
                lambda acc, record: acc + self._to_numeric(record['total_sales']),
                list(records),
                0.0
            )
            for month, records in grouped
        }
    
    def quantity_statistics(self) -> Dict[str, float]:
        """
        Calculate quantity statistics using functional operations.
        
        Returns:
            Dictionary with min, max, and average quantity
        """
        quantities = list(map(
            lambda record: self._to_numeric(record['quantity']),
            self.data
        ))
        
        if not quantities:
            return {'min': 0, 'max': 0, 'average': 0}
        
        return {
            'min': reduce(lambda a, b: a if a < b else b, quantities),
            'max': reduce(lambda a, b: a if a > b else b, quantities),
            'average': reduce(lambda acc, q: acc + q, quantities, 0.0) / len(quantities)
        }
    
    def filter_high_value_transactions(self, threshold: float) -> List[Dict]:
        """
        Filter transactions above a threshold using filter and lambda.
        
        Args:
            threshold: Minimum transaction value
            
        Returns:
            List of transactions with total_sales >= threshold
        """
        return list(filter(
            lambda record: self._to_numeric(record['total_sales']) >= threshold,
            self.data
        ))
    
    def products_by_region(self) -> Dict[str, List[str]]:
        """
        Get unique products sold in each region using functional operations.
        
        Returns:
            Dictionary mapping region to list of unique products
        """
        sorted_data = sorted(self.data, key=itemgetter('region'))
        grouped = groupby(sorted_data, key=itemgetter('region'))
        
        return {
            region: list(set(map(
                lambda record: record['product'],
                list(records)
            )))
            for region, records in grouped
        }


def format_currency(amount: float) -> str:
    """Format amount as currency string."""
    return f"${amount:,.2f}"


def print_analysis_results(analysis: SalesAnalysis):
    """Print all analysis results to console."""
    print("=== Sales Data Analysis ===\n")
    
    # 1. Total Revenue
    total_rev = analysis.total_revenue()
    print(f"1. Total Revenue: {format_currency(total_rev)}\n")
    
    # 2. Revenue by Category
    print("2. Revenue by Category:")
    category_revenue = analysis.revenue_by_category()
    for category, revenue in sorted(category_revenue.items(), key=lambda x: x[1], reverse=True):
        print(f"   {category}: {format_currency(revenue)}")
    print()
    
    # 3. Revenue by Region
    print("3. Revenue by Region:")
    region_revenue = analysis.revenue_by_region()
    for region, revenue in sorted(region_revenue.items(), key=lambda x: x[1], reverse=True):
        print(f"   {region}: {format_currency(revenue)}")
    print()
    
    # 4. Top 5 Products
    print("4. Top 5 Products by Revenue:")
    top_products = analysis.top_products_by_revenue(5)
    for i, (product, revenue) in enumerate(top_products, 1):
        print(f"   {i}. {product}: {format_currency(revenue)}")
    print()
    
    # 5. Average Transaction Value
    avg_transaction = analysis.average_transaction_value()
    print(f"5. Average Transaction Value: {format_currency(avg_transaction)}\n")
    
    # 6. Monthly Revenue Trend
    print("6. Monthly Revenue Trend:")
    monthly_revenue = analysis.monthly_revenue_trend()
    for month, revenue in sorted(monthly_revenue.items())[:6]:  # Show first 6 months
        print(f"   {month}: {format_currency(revenue)}")
    if len(monthly_revenue) > 6:
        print(f"   ... ({len(monthly_revenue) - 6} more months)")
    print()
    
    # 7. Quantity Statistics
    print("7. Quantity Statistics:")
    qty_stats = analysis.quantity_statistics()
    print(f"   Minimum: {qty_stats['min']:.0f}")
    print(f"   Maximum: {qty_stats['max']:.0f}")
    print(f"   Average: {qty_stats['average']:.2f}")
    print()
    
    # 8. High Value Transactions
    high_value = analysis.filter_high_value_transactions(5000)
    print(f"8. High Value Transactions (>= $5,000): {len(high_value)} transactions\n")
    
    # 9. Products by Region
    print("9. Products by Region:")
    products_by_region = analysis.products_by_region()
    for region, products in sorted(products_by_region.items()):
        print(f"   {region}: {len(products)} unique products")
    print()


if __name__ == "__main__":
    # Run analysis
    analysis = SalesAnalysis("sample_sales.csv")
    print_analysis_results(analysis)