"""
Paso 3 · Construye el modelo dimensional (esquema estrella) a partir de `sales`.

Entrada : data/superstore.db          (tabla `sales`, creada en el paso 1)
Salida  : data/superstore_modelado.db (tablas Dim* y FactVentas)

Decisiones de modelado:
- DimCiudad se une por (City, State), no solo por City: 57 ciudades aparecen
  en más de un estado, y unirlas solo por nombre duplicaba filas de hechos.
- Se valida que FactVentas tenga exactamente una fila por registro de venta.

Uso (desde la raíz del repositorio):
    python scripts/load_data_modelado.py
"""
import sqlite3
import pandas as pd

with sqlite3.connect("data/superstore.db") as conn_origen:
    df_sales = pd.read_sql("SELECT * FROM sales", con=conn_origen)
df_sales.columns = df_sales.columns.str.strip()
filas_origen = len(df_sales)

# ── Dimensiones ─────────────────────────────────────────────────────────────
df_segmento = df_sales[["Segment"]].drop_duplicates().reset_index(drop=True)
df_segmento["IDSegmento"] = df_segmento.index + 1

df_shipmode = df_sales[["Ship Mode"]].drop_duplicates().reset_index(drop=True)
df_shipmode["IDShipMode"] = df_shipmode.index + 1

df_categoria = df_sales[["Category"]].drop_duplicates().reset_index(drop=True)
df_categoria["IDCategoria"] = df_categoria.index + 1

subcat = df_sales[["Sub-Category", "Category"]].drop_duplicates().reset_index(drop=True)
df_subcategoria = subcat.merge(df_categoria, on="Category", how="left")
df_subcategoria["IDSubcategoria"] = df_subcategoria.index + 1

productos = df_sales[["Product Name", "Sub-Category"]].drop_duplicates().reset_index(drop=True)
df_producto = productos.merge(df_subcategoria[["Sub-Category", "Category", "IDCategoria", "IDSubcategoria"]], on="Sub-Category", how="left")
df_producto["IDProducto"] = df_producto.index + 1

df_region = df_sales[["Region"]].drop_duplicates().reset_index(drop=True)
df_region["IDRegion"] = df_region.index + 1

df_estado = df_sales[["State"]].drop_duplicates().reset_index(drop=True)
df_estado["IDEstado"] = df_estado.index + 1

ciudades = df_sales[["City", "State"]].drop_duplicates().reset_index(drop=True)
df_ciudad = ciudades.merge(df_estado, on="State", how="left")
df_ciudad["IDCiudad"] = df_ciudad.index + 1

# ── Tabla de hechos ─────────────────────────────────────────────────────────
df_fact = df_sales.merge(df_ciudad[["City", "State", "IDCiudad"]], on=["City", "State"], how="left")
df_fact = df_fact.merge(df_region, on="Region", how="left")
df_fact = df_fact.merge(df_segmento, on="Segment", how="left")
df_fact = df_fact.merge(df_shipmode, on="Ship Mode", how="left")
df_fact = df_fact.merge(df_categoria, on="Category", how="left")
df_fact = df_fact.merge(df_subcategoria[["Sub-Category", "IDSubcategoria"]], on="Sub-Category", how="left")
df_fact = df_fact.merge(df_producto[["Product Name", "IDProducto"]], on="Product Name", how="left")

df_fact["Order Date"] = pd.to_datetime(df_fact["Order Date"]).dt.date

df_fact_ventas = df_fact[[
    "Order ID", "Order Date", "Customer ID", "IDCiudad", "IDRegion", "IDSegmento", "IDShipMode",
    "IDCategoria", "IDSubcategoria", "IDProducto", "Sales", "Profit", "Quantity", "Discount"
]].copy()

# ── Validaciones ────────────────────────────────────────────────────────────
assert len(df_fact_ventas) == filas_origen, (
    f"FactVentas tiene {len(df_fact_ventas)} filas y el origen {filas_origen}: hay fan-out en un join")
assert df_fact_ventas[["IDCiudad", "IDRegion", "IDSegmento", "IDShipMode",
                       "IDCategoria", "IDSubcategoria", "IDProducto"]].notna().all().all(), \
    "Hay llaves sin resolver en FactVentas"
assert abs(df_fact_ventas["Sales"].sum() - df_sales["Sales"].sum()) < 0.01, "Las ventas no cuadran"

# ── Exportación ─────────────────────────────────────────────────────────────
tablas = {
    "DimSegmento": df_segmento, "DimShipMode": df_shipmode, "DimCategoria": df_categoria,
    "DimSubcategoria": df_subcategoria[["IDSubcategoria", "Sub-Category", "Category", "IDCategoria"]],
    "DimRegion": df_region, "DimEstado": df_estado,
    "DimCiudad": df_ciudad[["IDCiudad", "City", "State", "IDEstado"]],
    "DimProducto": df_producto[["IDProducto", "Product Name", "Sub-Category", "Category", "IDCategoria", "IDSubcategoria"]],
    "FactVentas": df_fact_ventas,
}

with sqlite3.connect("data/superstore_modelado.db") as conn:
    for nombre, tabla in tablas.items():
        tabla.to_sql(nombre, con=conn, if_exists="replace", index=False)
        print(f"  {nombre:<16} {len(tabla):>7,} filas")

print(f"\n✅ Modelo dimensional exportado. FactVentas = {len(df_fact_ventas):,} filas "
      f"(una por registro de venta).")
