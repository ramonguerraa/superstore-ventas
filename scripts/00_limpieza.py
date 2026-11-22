"""
Paso 0 · Limpieza de data/superstore.csv

El archivo original tiene 10,800 líneas de datos, pero solo 9,994 son
registros de ventas. Las 806 restantes son dos tablas auxiliares
(personas y devoluciones) anexadas al final del mismo CSV, sin columnas
propias. Si se leen como ventas, contaminan todas las métricas.

Entrada : data/raw/superstore_original.csv   (sin modificar)
Salida  : data/superstore.csv                (9,994 registros de ventas)
          data/aux/personas.csv              (tabla de personas por región)
          data/aux/devoluciones.csv          (órdenes devueltas)

Uso (desde la raíz del repositorio):
    python scripts/00_limpieza.py
"""
from pathlib import Path
import io
import pandas as pd

RAW = Path("data/raw/superstore_original.csv")
OUT_VENTAS = Path("data/superstore.csv")
OUT_PERSONAS = Path("data/aux/personas.csv")
OUT_DEVOLUCIONES = Path("data/aux/devoluciones.csv")

ENCODING = "ISO-8859-1"
ENCABEZADO_PERSONAS = "Person,Region"
ENCABEZADO_DEVOLUCIONES = "Returned,Order ID"


def main():
    lineas = RAW.read_text(encoding=ENCODING).splitlines(keepends=True)

    # Localizar los encabezados de las tablas anexadas
    idx_personas = next(i for i, l in enumerate(lineas) if l.strip() == ENCABEZADO_PERSONAS)
    idx_devol = next(i for i, l in enumerate(lineas) if l.strip() == ENCABEZADO_DEVOLUCIONES)

    lineas_ventas = [l for l in lineas[:idx_personas] if l.strip()]
    lineas_personas = lineas[idx_personas:idx_devol]
    lineas_devol = lineas[idx_devol:]

    OUT_PERSONAS.parent.mkdir(parents=True, exist_ok=True)
    OUT_VENTAS.write_text("".join(lineas_ventas), encoding=ENCODING)
    OUT_PERSONAS.write_text("".join(lineas_personas), encoding=ENCODING)
    OUT_DEVOLUCIONES.write_text("".join(lineas_devol), encoding=ENCODING)

    # Validaciones sobre los registros de ventas
    ventas = pd.read_csv(io.StringIO("".join(lineas_ventas)))
    ventas.columns = ventas.columns.str.strip()

    assert ventas["Sales"].notna().all(), "Hay registros de ventas sin monto"
    assert ventas["Row ID"].is_unique, "Row ID no es único"
    assert ventas.duplicated().sum() == 0, "Hay filas duplicadas exactas"

    print(f"Filas de ventas válidas : {len(ventas):,}")
    print(f"Filas auxiliares movidas: {len(lineas) - len(lineas_ventas) - 1:,} "
          f"(personas: {len(lineas_personas) - 1}, devoluciones: {len(lineas_devol) - 1})")
    print(f"Ventas totales (USD)    : {ventas['Sales'].sum():,.2f}")
    print(f"Rango de fechas         : {ventas['Order Date'].min()} → {ventas['Order Date'].max()}")


if __name__ == "__main__":
    main()
