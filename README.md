# 📊 Análisis de Ventas - Superstore

Este proyecto presenta un análisis completo de ventas basado en el dataset ficticio **Sample Superstore**, incluyendo limpieza de datos, consultas SQL y visualizaciones interactivas con Python y Power BI.

---

## 📁 Estructura del Proyecto

```bash
superstore_ventas/
├── analyze_sales.py       ← Limpieza y análisis con pandas
├── load_to_sql.py         ← Carga a base de datos SQLite
├── query_sales.py         ← Ejecución de consultas SQL
├── queries.sql            ← Conjunto de consultas reutilizables
├── plots/                 ← Imágenes generadas con Python
├── data/                  ← Dataset y base SQLite
└── README.md              ← Documentación del proyecto
```


---

## 🧪 Tecnologías utilizadas

- Python (Pandas, Seaborn, SQLAlchemy)
- SQLite y SQL
- Power BI
- Git + GitHub

---

## 🧼 Limpieza y preparación de datos

Los datos fueron procesados con Python, creando columnas derivadas como:

- Año y mes del pedido (`Order Date`)
- Margen de ganancia (`Profit / Sales`)
- Categorías y regiones agrupadas

---

## 🔍 Consultas SQL destacadas

- Ventas por región y año
- Top 10 productos por ingresos
- Clientes con mayor volumen de compra
- Margen promedio por subcategoría

---

## 📈 Visualizaciones (Python)

A continuación se muestran algunas gráficas generadas en Python:

### 📍 Ventas por región
![Ventas por región](plots/ventas_region.png)

### 🏆 Top 10 productos
![Top productos](plots/top_productos.png)

### 👤 Clientes más valiosos
![Top clientes](plots/top_clientes.png)

---

## 📊 Dashboard en Power BI

**En construcción...** pronto se añadirá el diseño final con:

- KPIs dinámicos
- Segmentación por categoría y año
- Gráficos de línea, barras y mapas

*Ejemplo de vista (imagen temporal):*
![Ejemplo dashboard](plots/dashboard_preview.png)

---

## 📥 Cómo ejecutar localmente

1. Clona este repositorio
2. Crea y activa un entorno virtual
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
4. Corre los scripts en orden:

* `analyze_sales.py`

* `load_to_sql.py`

* `query_sales.py`

## 📬 Contacto
### ¿Tienes feedback o preguntas?
### Escríbeme por GitHub o conecta en LinkedIn.