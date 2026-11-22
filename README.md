# Superstore Sales Analysis: Dimensional Model, Data Quality and BI

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An end-to-end sales analysis on the Superstore dataset: raw-data cleaning, a
star-schema model in SQLite, and a Power BI report for sales, customer and
product performance.

**Stack:** Python (pandas, matplotlib, seaborn) · SQL (SQLite) · Power BI · Dimensional modeling

---

## Business questions

- Which regions, products and customers drive revenue and profit?
- How do sales and profit evolve over time?
- Where is margin weak, and which sub-categories need attention?

## Key figures (after cleaning, 2015–2018)

| Metric | Value |
|---|---|
| Sales records | 9,994 |
| Distinct orders | 5,009 |
| Total sales | USD 2,297,201 |
| Total profit | USD 286,397 |
| Profit margin (profit / sales) | 12.5% |

Sales by region: West USD 725k · East USD 679k · Central USD 501k · South USD 392k.

## Data quality: issues found and fixed

Working from the raw file exposed three problems that would have overstated results.

1. **806 corrupted rows at the end of the CSV.** The file held two auxiliary tables
   (people by region, and returned orders) appended after the sales records, with
   no matching columns. They were read as sales with empty keys.
   *Fix:* `scripts/00_limpieza.py` separates the sales records (9,994) from the auxiliary
   tables, which are saved under `data/aux/`. The original file is kept unchanged in `data/raw/`.

2. **Fan-out in the dimensional model.** `DimCiudad` was joined to the fact table on city
   name only, and 57 city names occur in more than one state. Each match duplicated fact rows.
   *Fix:* the join now uses `(City, State)`, and the loader asserts that
   `FactVentas` has exactly one row per sales record.

3. **Inflated totals as a result.** The previous model had 14,178 fact rows against 9,994
   source records, and total sales of USD 3,144,936 instead of USD 2,297,201 (about 37% higher).

## Project structure

```
superstore-ventas/
├── data/
│   ├── raw/superstore_original.csv   # untouched source file
│   ├── aux/                          # auxiliary tables separated during cleaning
│   ├── superstore.csv                # cleaned sales records
│   ├── superstore.db                 # SQLite: table `sales`
│   └── superstore_modelado.db        # SQLite: star schema
├── scripts/
│   ├── 00_limpieza.py                # step 0: cleaning and validation
│   ├── load_to_sql.py                # step 1: load to SQLite
│   ├── init_modelo.py                # step 2: calendar dimension (schema.sql)
│   ├── load_data_modelado.py         # step 3: build dimensions and fact table
│   ├── query_sales.py                # run the analytical queries
│   ├── queries.sql
│   ├── analyze_sales.py              # exploratory charts
│   └── analisis_inicial.py           # initial profiling
├── schema.sql                        # Calendario DDL
├── pbix/Superstore_Reportes.pbix     # Power BI report
└── plots/, images/                   # exported charts and screenshots
```

## Dimensional model (star schema)

**Fact table:** `FactVentas` (one row per sales record): order, customer, city, region,
segment, ship mode, category, sub-category, product, sales, profit, quantity, discount.

**Dimensions:** `DimCiudad`, `DimEstado`, `DimRegion`, `DimSegmento`, `DimShipMode`,
`DimCategoria`, `DimSubcategoria`, `DimProducto`, `Calendario`.

## How to run

Run every command from the repository root.

```bash
pip install -r requirements.txt

python scripts/00_limpieza.py          # clean the raw file
python scripts/load_to_sql.py          # create data/superstore.db
python scripts/init_modelo.py          # create the calendar dimension
python scripts/load_data_modelado.py   # build the star schema
python scripts/query_sales.py          # run the analytical queries
```

## Power BI report

`pbix/Superstore_Reportes.pbix` contains the sales, customer, product and category
dashboards, built on a star schema with active one-to-many relationships from each
dimension to `FactVentas`. To reproduce it, point the ODBC data source at
`data/superstore_modelado.db` and refresh.

## Metric definitions

- **Sales:** revenue of the line item, as recorded in the source.
- **Profit:** profit of the line item, as recorded in the source.
- **Profit margin:** `Profit / Sales`, aggregated as a ratio of sums, not an average of ratios.

## Limitations

- The source covers 2015–2018 only; no forecasting is attempted.
- Customer and product names are taken as given; no entity resolution was performed.

## License

Released under the [MIT License](LICENSE).

## Author

**Ramón Guerra** · Quantitative analyst · SQL · Python · Power BI
