import pandas as pd

# Cargar los datos
df = pd.read_csv("data/superstore.csv", encoding="ISO-8859-1")  # Cambia el path si es necesario

# Mostrar estructura general
print("🔎 Columnas del dataset:")
print(df.columns.tolist())

print("\n📊 Resumen de los datos:")
print(df.describe(include='all').transpose())

print("\n📌 Valores únicos por columna categórica:")
for col in df.select_dtypes(include='object').columns:
    print(f"{col}: {df[col].nunique()} únicos")

print("\n🧪 Muestra de datos:")
print(df.head(5))
