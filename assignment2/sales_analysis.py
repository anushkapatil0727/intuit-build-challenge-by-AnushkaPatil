"""
Comments on this program for Sales Data Analysis using Functional Programming - So This module performs a complete analysis of sales data stored in a CSV file.
It intentionally uses functional-style programming tools such as: lambda expressions, map(), filter(), reduce(), itertools.groupby, operator.itemgetter
This is to demonstrate data transformation and aggregation using pure functions,minimal mutations, and declarative design.
"""

import csv                       # Used to read structured CSV data into Python
from functools import reduce      # Enables functional-style aggregation
from itertools import groupby     # Used to group records based on a shared key
from typing import List, Dict, Tuple, Callable
from operator import itemgetter   # Helps extract dictionary fields in sorting/grouping
from datetime import datetime


class SalesAnalysis:
    """
    this is a class dedicated to analyzing sales data using a functional programming approach. Key features demonstrated:
    1.Transformations using map() and lambda
    2. Filtering using filter()
    3. Aggregation using reduce()
    4. Grouping using itertools.groupby
    5. Sorting and functional composition to generate insights
    """

    def __init__(self, csv_file_path: str):
        """
        Initializes the analysis by loading a CSV file.
        Args:
            csv_file_path: Path to the input sales CSV.

        We immediately load the data into memory so that all methods operate on the same dataset without repeatedly reading the file.
        """
        self.csv_file_path = csv_file_path
        self.data = self._load_data()  # this Load CSV into a list of dictionaries

    def _load_data(self) -> List[Dict]:
        """
        it will Read the CSV and converts each row into a dictionary.
        Returns A list of rows, where each row is a dict mapping column names to values.
        """
        with open(self.csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # it automatically maps header -> value
            return list(reader)            # it Convert iterator to list for reuse

    def _to_numeric(self, value: str) -> float:
        """
        this Safely convert a string value into a float. So If conversion fails (e.g like, missing value or bad formatting),
        we default to 0.0 to keep calculations from breaking.
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def total_revenue(self) -> float:
        """
        this will calculates total revenue across all records.

        Uses reduce() so that we: Start with an accumulator (0.0), Add each row’s total_sales to it, End up with a single numeric result
        """
        return reduce(
            lambda acc, record: acc + self._to_numeric(record['total_sales']),
            self.data,
            0.0
        )

    def revenue_by_category(self) -> Dict[str, float]:
        """
        it Groups revenue by product category.
        Here, groupby() requires sorted input, so we sort by 'category' first.
        Then for each category group, we sum up its total sales using reduce().
        """
        sorted_data = sorted(self.data, key=itemgetter('category'))
        grouped = groupby(sorted_data, key=itemgetter('category'))

        return {
            category: reduce(
                lambda acc, record: acc + self._to_numeric(record['total_sales']),
                list(records),       # Convert iterator to list so reduce can be reused
                0.0
            )
            for category, records in grouped
        }

    def revenue_by_region(self) -> Dict[str, float]:
        """
        Same pattern as revenue_by_category, but grouped by region instead.
        Produces a dictionary: { region_name: total_revenue }
        """
        sorted_data = sorted(self.data, key=itemgetter('region'))
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
        Identifies the highest revenue-generating products.
        Steps:
        1. Sort records by product name so groupby groups correctly.
        2. Use reduce to sum revenue per product.
        3. Sort products by total revenue descending.
        4. Return top N products.
        """
        sorted_data = sorted(self.data, key=itemgetter('product'))
        grouped = groupby(sorted_data, key=itemgetter('product'))

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

        # Sort products by their revenue (descending)
        return sorted(product_revenues, key=lambda x: x[1], reverse=True)[:n]

    def average_transaction_value(self) -> float:
        """
        this computes average revenue per transaction.

        It Uses: reduce() to sum revenue as well as len(self.data) to count transactions
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
        this will calculates monthly revenue totals based on the 'date' field.
        Steps used:
        1. Extract YYYY-MM from each date using map() and lambda
        2. Sort by month
        3. Group using groupby()
        4. Sum revenue per month
        """
        # Add a 'year_month' field to each record using map transformation
        data_with_month = list(map(
            lambda record: {
                **record,                      # Start with original row
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
        it computes min, max, and average quantity across all transactions.

        Uses: map() to extract numeric quantities, reduce() to compute min and max manually and reduce() to sum quantities for average
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
        Returns transactions where total_sales >= threshold. Uses filter() with a lambda condition.
        """
        return list(filter(
            lambda record: self._to_numeric(record['total_sales']) >= threshold,
            self.data
        ))

    def products_by_region(self) -> Dict[str, List[str]]:
        """
        Lists all unique products sold per region.

        Uses:
        1. sorted() + groupby() to group transactions by region
        2. map() to extract product names
        3. set() to ensure uniqueness
        """
        sorted_data = sorted(self.data, key=itemgetter('region'))
        grouped = groupby(sorted_data, key=itemgetter('region'))

        return {
            region: list(set(map(
                lambda record: record['product'],  # Extract product name
                list(records)
            )))
            for region, records in grouped
        }


def format_currency(amount: float) -> str:
    """
    this is a Utility function to convert a number into a formatted currency string.
    Example: 1234.5 -> "$1,234.50"
    """
    return f"${amount:,.2f}"


def print_analysis_results(analysis: SalesAnalysis):
    
    #this is a Helper function to print all analysis results in a structured way. This provides a clean console output that summarizes all insights.
    
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
    for month, revenue in sorted(monthly_revenue.items())[:6]:  # Print only first 6 months
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
    # this Executes the analysis only if this file is run directly.
    # This keeps the module import-safe for unit testing.
    analysis = SalesAnalysis("sample_sales.csv")
    print_analysis_results(analysis)
