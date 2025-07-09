-- Consulta 1: Ventas por región
SELECT Region, SUM(Sales) AS TotalSales
FROM sales
GROUP BY Region
ORDER BY TotalSales DESC;

-- ###
-- Consulta 2: Top 5 productos más vendidos
SELECT "Product Name", SUM(Sales) AS TotalSales
FROM sales
GROUP BY "Product Name"
ORDER BY TotalSales DESC
LIMIT 5;

-- ###
-- Consulta 3: Clientes con más compras
SELECT "Customer Name", SUM(Sales) AS TotalSales
FROM sales
GROUP BY "Customer Name"
ORDER BY TotalSales DESC
LIMIT 5;
