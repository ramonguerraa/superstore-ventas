import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, Float
import sqlalchemy

# Conexiones a bases de datos
engine_origen = create_engine("sqlite:///data/superstore.db")
engine_modelado = create_engine("sqlite:///data/superstore_modelado.db")

# Leer tabla original
df_sales = pd.read_sql("SELECT * FROM sales", con=engine_origen)

print("✅ Datos cargados desde 'superstore.db'")

print("Columnas disponibles en df_sales:")
print(df_sales.columns.tolist())

df_sales.columns = df_sales.columns.str.strip()  # elimina espacios antes y después

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
df_subcategoria = df_sales[["Sub-Category", "Category"]].drop_duplicates().reset_index(drop=True)
df_subcategoria = df_subcategoria.merge(df_categoria, on="Category")
df_subcategoria["IDSubcategoria"] = df_subcategoria.index + 1

#DimProducto
df_producto = df_sales[["Product Name", "Sub-Category"]].drop_duplicates().reset_index(drop=True)
df_producto = df_producto.merge(df_subcategoria, on="Sub-Category")
df_producto["IDProducto"] = df_producto.index + 1

#DimRegion
df_region = df_sales[["Region"]].drop_duplicates().reset_index(drop=True)
df_region["IDRegion"] = df_region.index + 1

#DimPais
df_pais = df_sales[["Country", "Region"]].drop_duplicates().reset_index(drop=True)
df_pais = df_pais.merge(df_region, on="Region")
df_pais["IDPais"] = df_pais.index + 1

#DimEstado
df_estado = df_sales[["State", "Country"]].drop_duplicates().reset_index(drop=True)
df_estado = df_estado.merge(df_pais, on="Country")
df_estado["IDEstado"] = df_estado.index + 1

#DimCiudad
df_ciudad = df_sales[["City", "State"]].drop_duplicates().reset_index(drop=True)
df_ciudad = df_ciudad.merge(df_estado, on="State")
df_ciudad["IDCiudad"] = df_ciudad.index + 1

# Crear la conexión a la base de datos modelada
engine = create_engine("sqlite:///data/superstore_modelado.db")
conn = engine.connect()

# Unir dimensiones a la tabla de ventas
df_fact = df_sales.copy()

# Producto
df_fact = df_fact.merge(df_producto[["IDProducto", "Product Name"]], left_on="Product Name", right_on="Product Name")

# Ciudad (desde DimCiudad, ya incluye Estado→País→Región→Mercado)
df_fact = df_fact.merge(df_ciudad[["City", "IDCiudad"]], on="City")

# Segmento
df_fact = df_fact.merge(df_segmento, on="Segment")

# Ship Mode
df_fact = df_fact.merge(df_shipmode, on="Ship Mode")

# Categoría
df_fact = df_fact.merge(df_categoria, on="Category")

df_calendario = pd.read_sql("SELECT ROWID AS IDFecha, Fecha FROM Calendario", con=engine_modelado)

df_fact = df_fact.merge(df_calendario, how="left", left_on="Order Date", right_on="Fecha")

df_fact_ventas = df_fact[[
    "Order ID", "IDProducto", "IDCiudad", "IDSegmento",
    "IDShipMode", "IDCategoria", "IDFecha",
    "Sales", "Profit", "Quantity", "Discount"
]]

# Asegura que todos los IDs sean enteros y no nulos
# Forzamos los IDs a enteros válidos, reemplazando NaN con 0 y asegurando int32
cols_id = ["IDProducto", "IDCiudad", "IDSegmento", "IDShipMode", "IDCategoria", "IDFecha"]

for col in cols_id:
    df_fact_ventas[col] = pd.to_numeric(df_fact_ventas[col], errors="coerce").fillna(0).astype("int32")


for col in cols_id:
    df_fact_ventas.loc[:, col] = (
        pd.to_numeric(df_fact_ventas[col], downcast="integer", errors="coerce")
        .fillna(0)
        .astype("int32")
    )

print(df_fact_ventas.dtypes)
print(df_fact_ventas.head())

# Forzar el tipo correcto para todas las columnas clave
campos_ids = ["IDProducto", "IDCiudad", "IDSegmento", "IDShipMode", "IDCategoria", "IDFecha"]

for col in campos_ids:
    df_fact_ventas.loc[:, col] = (
        pd.to_numeric(df_fact_ventas[col], errors="coerce")
        .fillna(0)
        .astype("int32")
    )

# Segmento
df_segmento.to_sql("DimSegmento", engine_modelado, if_exists="replace", index=False,
    dtype={"IDSegmento": Integer(), "Segment": Text()})

# ShipMode
df_shipmode.to_sql("DimShipMode", engine_modelado, if_exists="replace", index=False,
    dtype={"IDShipMode": Integer(), "Ship Mode": Text()})

# Categoría
df_categoria.to_sql("DimCategoria", engine_modelado, if_exists="replace", index=False,
    dtype={"IDCategoria": Integer(), "Category": Text(), "Sub-Category": Text()})

# Región
df_region.to_sql("DimRegion", engine_modelado, if_exists="replace", index=False,
    dtype={"IDRegion": Integer(), "Region": Text()})

# País
df_pais.to_sql("DimPais", engine_modelado, if_exists="replace", index=False,
    dtype={"IDPais": Integer(), "Country": Text(), "IDRegion": Integer()})

# Estado
df_estado.to_sql("DimEstado", engine_modelado, if_exists="replace", index=False,
    dtype={"IDEstado": Integer(), "State": Text(), "IDPais": Integer()})

# Ciudad
df_ciudad.to_sql("DimCiudad", engine_modelado, if_exists="replace", index=False,
    dtype={"IDCiudad": Integer(), "City": Text(), "IDEstado": Integer()})

# Producto
df_producto.to_sql("DimProducto", engine_modelado, if_exists="replace", index=False,
    dtype={
        "IDProducto": Integer(),
        "Product ID": Text(),
        "Product Name": Text(),
        "Category": Text(),
        "Sub-Category": Text()
    })


with engine.connect() as conn:
    df_fact_ventas.to_sql(
        "FactVentas",
        conn,
        if_exists="replace",
        index=False,
        dtype={
            "Order ID": sqlalchemy.types.Text(),
            "IDProducto": sqlalchemy.types.Integer(),
            "IDCiudad": sqlalchemy.types.Integer(),
            "IDSegmento": sqlalchemy.types.Integer(),
            "IDShipMode": sqlalchemy.types.Integer(),
            "IDCategoria": sqlalchemy.types.Integer(),
            "IDFecha": sqlalchemy.types.Integer(),
            "Sales": sqlalchemy.types.Float(),
            "Quantity": sqlalchemy.types.Integer(),
            "Discount": sqlalchemy.types.Float(),
            "Profit": sqlalchemy.types.Float(),
        }
    )



