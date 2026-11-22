"""
Paso 1 · Carga de la data limpia a SQLite (tabla `sales`).

Entrada : data/superstore.csv
Salida  : data/superstore.db  (tabla `sales`)

Uso (desde la raíz del repositorio):
    python scripts/load_to_sql.py
"""
import sqlite3
import pandas as pd

df = pd.read_csv("data/superstore.csv", encoding="ISO-8859-1", parse_dates=["Order Date", "Ship Date"])
df.columns = df.columns.str.strip()

with sqlite3.connect("data/superstore.db") as conn:
    df.to_sql("sales", con=conn, if_exists="replace", index=False)

print(f"✅ data/superstore.db creada con {len(df):,} registros en la tabla `sales`.")
