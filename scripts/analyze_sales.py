import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_csv("data/superstore.csv", parse_dates=["Order Date", "Ship Date"])

# Mostrar columnas disponibles
print("Columnas disponibles:", df.columns.tolist())

# Ver estructura general
print("📄 Primeras filas:")
print(df.head())

print("\n📊 Información del DataFrame:")
print(df.info())

print("\n🔍 Valores nulos por columna:")
print(df.isnull().sum())

# Se eliminan los valores nulos
df = df.dropna()

# Crear columnas nuevas
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month

# Agregar columna de ganancias (si tienes columna 'Profit')
if 'Profit' in df.columns:
    df["Profit Margin"] = df["Profit"] / df["Sales"]
else:
    print("⚠️ No se encontró columna 'Profit' para calcular margen.")

# Verificación rápida
print("\n📅 Años únicos en los datos:")
print(df["Year"].unique())

print("\n🧮 Descripción de ventas y ganancias:")
print(df[["Sales"]].describe())

# Agrupación por región y año
region_year = df.groupby(['Region', 'Year']).agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).reset_index()

print("\n📍 Ventas y ganancias por región y año:")
print(region_year)

# Visualización
plt.figure(figsize=(10, 6))
sns.barplot(data=region_year, x='Year', y='Sales', hue='Region')
plt.title("Ventas por Región y Año")
plt.ylabel("Total Ventas")
plt.xlabel("Año")
plt.tight_layout()
plt.savefig("plots/ventas_region_anual.png")
plt.show()

top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)

print("\n🏆 Top 10 productos más vendidos:")
print(top_products)

# Gráfico
plt.figure(figsize=(10, 6))
sns.barplot(x=top_products.values, y=top_products.index, palette="viridis")
plt.title("Top 10 productos por ventas")
plt.xlabel("Ventas totales")
plt.ylabel("Producto")
plt.tight_layout()
plt.savefig("plots/top_productos.png")
plt.show()

top_clients = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)

print("\n👤 Top 10 clientes por volumen de compra:")
print(top_clients)

# Visualización
plt.figure(figsize=(10, 6))
sns.barplot(x=top_clients.values, y=top_clients.index, palette="magma")
plt.title("Top 10 clientes por compras")
plt.xlabel("Total vendido")
plt.ylabel("Cliente")
plt.tight_layout()
plt.savefig("plots/top_clientes.png")
plt.show()

