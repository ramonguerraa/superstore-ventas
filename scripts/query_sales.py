"""
Ejecuta las consultas de scripts/queries.sql sobre data/superstore.db.

Uso (desde la raíz del repositorio):
    python scripts/query_sales.py
"""
import sqlite3
import pandas as pd

with open("scripts/queries.sql", "r", encoding="utf-8") as f:
    consultas = [q.strip() for q in f.read().split("-- ###") if q.strip()]

with sqlite3.connect("data/superstore.db") as conn:
    for i, consulta in enumerate(consultas, start=1):
        sql = "\n".join(l for l in consulta.splitlines() if not l.strip().startswith("--")).strip()
        if not sql:
            continue
        try:
            print(f"\n🔍 Consulta #{i}")
            print(pd.read_sql_query(sql, conn))
        except Exception as e:
            print(f"❌ Error en consulta #{i}: {e}")
