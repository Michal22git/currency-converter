# Currency Converter

This script allows converting any amount of a given currency to Polish Zloty (PLN), using selected exchange rate sources.

## Installation

1. Install dependencies:

   ```bash
   pip install -r requirements.txt

2. Usage:
    ```bash
    python -m currency_converter [mode] [amount] [currency] [source]

### Arguments:
    - mode: Specifies whether the script should run in development mode (database.json) or production (sqlite3).
    - amount: The amount of currency to convert.
    - currency: Base currency code (USD, GBP, EUR...).
    - source: Exchange rate source (can be 'local' for local rates or 'nbp' for National Bank of Poland rates).

3. Examples:
    ```bash
    python -m task dev 100 USD local
    python -m task prod 50 EUR nbp
