
# Products Name Cleaner & Sales Analytics

## Project Goal

Build a product standardization and sales analytics platform.

## Data Source

- Original data: Parquet
- Approximate records: 19.4 million
- Unique raw product names: 32,364
- Processing engine: DuckDB

## Core Modules

1. Product Master
   - Unique Product ID
   - English Standard Name
   - Chinese Auxiliary Name

2. Product Name Mapping
   - Original Product Name
   - Standard Product ID
   - Review Status
   - Matching Evidence

3. Sales Detail
   - Preserve every original sales record
   - Add Standard Product ID
   - Never overwrite source data

4. Sales Analytics
   - Product sales
   - Sales revenue
   - Merchant analysis
   - Time trends

5. Device Analytics
   - Distinct device count
   - Device model distribution

## Technical Direction

- Python
- DuckDB
- Parquet
- Streamlit
- Reuse mature open-source components where possible

## Data Safety

- Never upload confidential source data to GitHub.
- Never automatically merge products without review.
- Preserve original sales records.
