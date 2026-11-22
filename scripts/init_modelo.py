"""
Paso 2 · Crea la dimensión Calendario en data/superstore_modelado.db
ejecutando schema.sql (SQL puro, sin dependencias externas).

Uso (desde la raíz del repositorio):
    python scripts/init_modelo.py
"""
import sqlite3

with open("schema.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

with sqlite3.connect("data/superstore_modelado.db") as conn:
    conn.executescript(schema_sql)
    filas = conn.execute("SELECT COUNT(*) FROM Calendario").fetchone()[0]

print(f"✅ Calendario creado con {filas:,} días.")
