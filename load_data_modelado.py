import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, Float

# Conexiones a bases de datos
engine_origen = create_engine("sqlite:///data/superstore.db")
engine_modelado = create_engine("sqlite:///data/superstore_modelado.db")

# Leer tabla original
df_sales = pd.read_sql("SELECT * FROM sales", con=engine_origen)
print("\n✅ Datos cargados desde 'superstore.db'")
print("Columnas disponibles en df_sales:")
print(df_sales.columns.tolist())

# Limpieza de columnas
df_sales.columns = df_sales.columns.str.strip()

# Creación de tablas dimensionales

# DimSegmento
df_segmento = df_sales[["Segment"]].drop_duplicates().reset_index(drop=True)
df_segmento["IDSegmento"] = df_segmento.index + 1

# DimShipMode
df_shipmode = df_sales[["Ship Mode"]].drop_duplicates().reset_index(drop=True)
df_shipmode["IDShipMode"] = df_shipmode.index + 1

# DimCategoria
df_categoria = df_sales[["Category"]].drop_duplicates().reset_index(drop=True)
df_categoria["IDCategoria"] = df_categoria.index + 1

# DimSubcategoria
subcat = df_sales[["Sub-Category", "Category"]].drop_duplicates().reset_index(drop=True)
df_subcategoria = subcat.merge(df_categoria, on="Category", how="left")
df_subcategoria["IDSubcategoria"] = df_subcategoria.index + 1

# DimProducto
productos = df_sales[["Product Name", "Sub-Category"]].drop_duplicates().reset_index(drop=True)
df_producto = productos.merge(df_subcategoria, on="Sub-Category", how="left")
df_producto["IDProducto"] = df_producto.index + 1

# DimRegion
df_region = df_sales[["Region"]].drop_duplicates().reset_index(drop=True)
df_region["IDRegion"] = df_region.index + 1

# DimEstado
df_estado = df_sales[["State"]].drop_duplicates().reset_index(drop=True)
df_estado["IDEstado"] = df_estado.index + 1

# DimCiudad
ciudades = df_sales[["City", "State"]].drop_duplicates().reset_index(drop=True)
df_ciudad = ciudades.merge(df_estado, on="State", how="left")
df_ciudad["IDCiudad"] = df_ciudad.index + 1

# Construcción de la tabla de hechos

# Copia del dataset original
df_fact = df_sales.copy()

# Agregar IDs desde las dimensiones

# Ciudad (encadena hacia Estado)
df_fact = df_fact.merge(df_ciudad[["City", "IDCiudad"]], on="City", how="left")

#Region
df_fact = df_fact.merge(df_region, on="Region", how="left")

# Segmento
df_fact = df_fact.merge(df_segmento, on="Segment", how="left")

# Ship Mode
df_fact = df_fact.merge(df_shipmode, on="Ship Mode", how="left")

# Categoría
df_fact = df_fact.merge(df_categoria, on="Category", how="left")

# Subcategoría
df_fact = df_fact.merge(df_subcategoria[["Sub-Category", "IDSubcategoria"]], on="Sub-Category", how="left")

# Producto
df_fact = df_fact.merge(df_producto[["Product Name", "IDProducto"]], on="Product Name", how="left")

# Formateamos la fecha
df_fact["Order Date"] = pd.to_datetime(df_fact["Order Date"]).dt.date

# Selección final de columnas para la tabla de hechos
df_fact_ventas = df_fact[[
    "Order ID", "Order Date", "IDCiudad", "IDRegion", "IDSegmento", "IDShipMode", "IDCategoria",
    "IDSubcategoria", "IDProducto", "Sales", "Profit", "Quantity", "Discount"
]]

# Forzar tipos de columnas ID a enteros
cols_id = ["IDCiudad", "IDRegion", "IDSegmento", "IDShipMode", "IDCategoria", "IDSubcategoria", "IDProducto"]
for col in cols_id:
    df_fact_ventas.loc[:, col] = pd.to_numeric(df_fact_ventas[col], errors="coerce").fillna(0).astype("int32")


df_producto["IDSubcategoria"] = df_producto["IDSubcategoria"].astype("int32")

# Exportar tablas dimensionales

df_segmento.to_sql("DimSegmento", engine_modelado, if_exists="replace", index=False,
                   dtype={"IDSegmento": Integer(), "Segment": Text()})

df_shipmode.to_sql("DimShipMode", engine_modelado, if_exists="replace", index=False,
                   dtype={"IDShipMode": Integer(), "Ship Mode": Text()})

df_categoria.to_sql("DimCategoria", engine_modelado, if_exists="replace", index=False,
                    dtype={"IDCategoria": Integer(), "Category": Text()})

df_subcategoria.to_sql("DimSubcategoria", engine_modelado, if_exists="replace", index=False,
                        dtype={"IDSubcategoria": Integer(), "Sub-Category": Text(), "IDCategoria": Integer()})

df_region.to_sql("DimRegion", engine_modelado, if_exists="replace", index=False,
                 dtype={"IDRegion": Integer(), "Region": Text()})

df_estado.to_sql("DimEstado", engine_modelado, if_exists="replace", index=False,
                 dtype={"IDEstado": Integer(), "State": Text()})

df_ciudad.to_sql("DimCiudad", engine_modelado, if_exists="replace", index=False,
                 dtype={"IDCiudad": Integer(), "City": Text(), "IDEstado": Integer()})

df_producto.to_sql("DimProducto", engine_modelado, if_exists="replace", index=False,
                   dtype={"Product Name": Text(), 
                          "Sub-Category": Text(), 
                          "IDSubcategoria": Integer(), 
                          "IDProducto": Integer()
                          }
                   )

# Exportar tabla de hechos
with engine_modelado.connect() as conn:
    df_fact_ventas.to_sql(
        "FactVentas",
        conn,
        if_exists="replace",
        index=False,
        dtype={
            "Order ID": Text(),
            "Order Date": sqlalchemy.types.Date(),
            "IDProducto": Integer(),
            "IDCiudad": Integer(),
            "IDSegmento": Integer(),
            "IDShipMode": Integer(),
            "IDCategoria": Integer(),
            "IDSubcategoria": Integer(),
            "Sales": Float(),
            "Quantity": Integer(),
            "Discount": Float(),
            "Profit": Float(),
        }
    )

print("\n✅ Exportación de modelo dimensional completada con éxito.")

import sqlite3

with sqlite3.connect("data/superstore_modelado.db") as conn:
    print("\n🔍 DimEstado:")
    df_estado = pd.read_sql("SELECT * FROM DimEstado", conn)
    print(df_estado.dtypes)
    print(df_estado.head())
    print(f"Filas: {df_estado.shape[0]}")




