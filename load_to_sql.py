import pandas as pd
from sqlalchemy import create_engine

# Cargar los datos
df = pd.read_csv("data/superstore.csv", parse_dates=["Order Date", "Ship Date"])

# Crear motor SQLite
engine = create_engine("sqlite:///data/superstore.db")

# Exportar DataFrame a SQL
df.to_sql("sales", con=engine, if_exists="replace", index=False)

print("✅ superstore.db creado exitosamente en /data")
