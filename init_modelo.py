import pandas as pd
from sqlalchemy import create_engine, text
import sqlalchemy

# Crear motor
engine = create_engine("sqlite:///data/superstore_modelado.db")

# Leer script SQL
with open("schema.sql", "r", encoding="utf-8") as file:
    schema_sql = file.read()

# Ejecutar script completo
conn = engine.raw_connection()
try:
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    print("✅ Tabla Calendario ejecutada correctamente.")
finally:
    conn.close()

df_calendario = pd.read_sql("SELECT * FROM Calendario", engine)

df_calendario["IDFecha"] = pd.to_numeric(pd.factorize(df_calendario["Fecha"])[0], downcast="integer")
df_calendario["Fecha"] = pd.to_datetime(df_calendario["Fecha"])

# Forzar tipos para columnas relevantes si las tienes
df_calendario = df_calendario.astype({
    "IDFecha": "int32",
    "Fecha": "datetime64[ns]",
    # Añade aquí otras columnas con su tipo si ya existen
})

df_calendario.to_sql(
    "Calendario",
    con=engine,
    if_exists="replace",
    index=False,
    dtype={
        "IDFecha": sqlalchemy.types.Integer(),
        "Fecha": sqlalchemy.types.Date(),
        # Asegura agregar aquí todas las demás columnas si existen
    }
)

