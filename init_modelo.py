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

# Leer la tabla Calendario ya generada con SQL
df_calendario = pd.read_sql("SELECT * FROM Calendario", engine)

# ✅ Conversión de tipo de fecha
df_calendario["Fecha"] = pd.to_datetime(df_calendario["Fecha"]).dt.date

# Exportar asegurando el tipo correcto
df_calendario.to_sql(
    "Calendario",
    con=engine,
    if_exists="replace",
    index=False,
    dtype={
        "Fecha": sqlalchemy.types.Date(),
        "dia": sqlalchemy.types.Integer(),
        "mes": sqlalchemy.types.Integer(),
        "anio": sqlalchemy.types.Integer(),
        "dia_semana": sqlalchemy.types.Text(),
        "dia_semana_corto": sqlalchemy.types.Text(),
        "num_dia_semana": sqlalchemy.types.Integer(),
        "semana_anio": sqlalchemy.types.Integer(),
        "mes_corto": sqlalchemy.types.Text(),
        "trimestre": sqlalchemy.types.Integer(),
        "semestre":  sqlalchemy.types.Integer(),
    }
)


