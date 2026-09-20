# Contributing to Retail Sales Analysis

Thanks for your interest in contributing. Clear, well-scoped contributions are very welcome.

## Getting set up

1. **Fork** and **clone** the repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # Linux/Mac: source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python src/app.py
   ```
   The dashboard opens at `http://localhost:8050`.

## Data

The dashboard reads sample data from the `data/` folder:
- `data/customers.csv`, `data/products.csv` - reference data
- `data/sales_data.xlsx` - sales records

No database is required. Do not commit real or sensitive data.

## Making changes

1. Create a branch: `git checkout -b feature/short-description`
2. Keep changes focused. One feature or fix per pull request.
3. Match the existing style (Dash callbacks, Plotly figures, pandas).
4. Make sure the app still starts and the **CI build** passes.

## Pull requests

1. Push your branch and open a pull request against `main`.
2. Fill in the pull request template: what changed, why, and how you tested it.
3. Link any related issue (for example, `Closes #12`).

For security issues, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.
