# Build Challenge - Python Implementation

This repository contains solutions for two programming assignments demonstrating concurrent programming and functional data analysis capabilities.

## Project Structure
```
build-challenge/
├── README.md
├── requirements.txt
├── assignment1/
│   ├── producer_consumer.py      # Producer-consumer implementation
│   └── test_producer_consumer.py # Unit tests
└── assignment2/
    ├── sales_analysis.py          # Data analysis implementation
    ├── sample_sales.csv           # Sample sales dataset
    └── test_sales_analysis.py     # Unit tests
```

## Requirements

- Python 3.8+
- pytest (for running tests)

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repo-url>
cd build-challenge
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Assignment 1: Producer-Consumer Pattern

### Description
Implements a classic producer-consumer pattern with thread synchronization using Python's `queue.Queue` and threading primitives. The producer reads items from a source container and places them in a shared queue. The consumer retrieves items from the queue and stores them in a destination container.

### Design Decisions
- **queue.Queue**: Used for thread-safe blocking queue operations (inherently handles wait/notify)
- **Threading**: Separate producer and consumer threads for concurrent execution
- **Graceful Shutdown**: Sentinel value (None) signals completion
- **Configurable**: Queue size, production rate, and data size are parameterizable

### Running Assignment 1

Run the main program:
```bash
python3 assignment1/producer_consumer.py
```

Run unit tests:
```bash
pytest assignment1/test_producer_consumer.py -v
```

### Sample Output - Screenshots attached
```
Producer: Starting production...
Producer: Produced item 0
Consumer: Starting consumption...
Consumer: Consumed item 0
Producer: Produced item 1
Consumer: Consumed item 1
Producer: Produced item 2
Consumer: Consumed item 2
...
Producer: Produced item 99
Producer: Finished producing
Consumer: Consumed item 99
Consumer: Finished consuming

=== Summary ===
Total items produced: 100
Total items consumed: 100
Source container size: 0
Destination container size: 100
```

## Assignment 2: Sales Data Analysis

### Description
Performs comprehensive data analysis on CSV sales data using functional programming paradigms including lambda expressions, map/filter operations, and grouping. Analyzes sales transactions across multiple dimensions.

### Dataset
The `sample_sales.csv` contains 1000 sales transactions with the following fields:
- **transaction_id**: Unique identifier
- **date**: Transaction date (YYYY-MM-DD)
- **product**: Product name
- **category**: Product category
- **region**: Sales region
- **quantity**: Units sold
- **unit_price**: Price per unit
- **total_sales**: Total transaction value

### Analyses Performed
1. **Total Revenue**: Sum of all sales
2. **Revenue by Category**: Aggregated sales per product category
3. **Revenue by Region**: Aggregated sales per region
4. **Top 5 Products**: Highest revenue-generating products
5. **Average Transaction Value**: Mean sales per transaction
6. **Monthly Revenue Trend**: Sales aggregated by month
7. **Quantity Statistics**: Min, max, average units per transaction

### Design Decisions
- **Functional Programming**: Heavy use of map, filter, reduce, lambda expressions
- **itertools.groupby**: For grouping operations (requires sorted data)
- **functools.reduce**: For aggregation operations
- **Pure Functions**: Analysis functions are side-effect free and testable

### Running Assignment 2

Run the main program:
```bash
python3 assignment2/sales_analysis.py
```

Run unit tests:
```bash
pytest assignment2/test_sales_analysis.py -v
```

### Sample Output - Screenshot Attached
```
=== Sales Data Analysis ===

1. Total Revenue: $2,548,750.00

2. Revenue by Category:
   Electronics: $1,234,500.00
   Clothing: $654,250.00
   Home & Garden: $660,000.00

3. Revenue by Region:
   North: $850,000.00
   South: $636,250.00
   East: $531,250.00
   West: $531,250.00

4. Top 5 Products by Revenue:
   1. Laptop: $450,000.00
   2. Smartphone: $380,000.00
   3. Tablet: $275,000.00
   4. Sofa: $245,000.00
   5. Jacket: $198,000.00

5. Average Transaction Value: $2,548.75

6. Monthly Revenue Trend:
   2024-01: $212,500.00
   2024-02: $198,750.00
   2024-03: $225,000.00
   ...

7. Quantity Statistics:
   Minimum: 1
   Maximum: 10
   Average: 5.23
```

## Running All Tests

Run all tests with coverage:
```bash
pytest -v
```

Run with coverage report:
```bash
pytest --cov=assignment1 --cov=assignment2 --cov-report=term-missing
```

## Design Principles

### Assignment 1
- Thread safety through blocking queues
- Clean separation of producer/consumer logic
- Configurable parameters for different scenarios
- Proper thread lifecycle management

### Assignment 2
- Functional programming paradigms throughout
- Immutable data transformations
- Composable analysis functions
- Clear separation of data loading and analysis

## Author

Round 4 - Build Challenge Submission for Intuit by Anushka Patil
Role - Software Engineer 1


## requirements.txt
```
pytest>=7.4.0
pytest-cov>=4.1.0