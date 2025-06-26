import pandas as pd
from sqlalchemy import create_engine

# Conectar a la base de datos
engine = create_engine("sqlite:///data/superstore.db")

# Leer todas las consultas del archivo SQL
with open("queries.sql", "r", encoding="utf-8") as file:
    content = file.read()

# Separar consultas por marcador personalizado
queries = [q.strip() for q in content.split("-- ###") if q.strip()]

# Ejecutar y mostrar cada consulta
for i, query in enumerate(queries, start=1):
    print(f"\n🔍 Ejecutando consulta #{i}:\n")
    print(query)  # Muestra la consulta (opcional)

    try:
        df = pd.read_sql_query(query, con=engine)
        print(df)
    except Exception as e:
        print(f"❌ Error al ejecutar consulta #{i}: {e}")
