from pathlib import Path
import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "Northwind.db"
print(DB_PATH)
print(DB_PATH.exists())

conn = sql.connect(DB_PATH)

# 1. Ingresos totales
query_total_sales = '''
SELECT  
    SUM(p.Price * od.Quantity) AS total_sales
FROM OrderDetails od
JOIN Products p 
    ON od.ProductID = p.ProductID;
'''

df_total_sales = pd.read_sql_query(query_total_sales, conn)
total_sales = df_total_sales.loc[0, "total_sales"]
print(f"Ingresos totales: {total_sales}")


# 2. Top 10 productos más rentables
query_top_products = '''
SELECT 
    p.ProductName,
    SUM(p.Price * od.Quantity) AS total_sales
FROM OrderDetails od
JOIN Products p 
    ON od.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY total_sales DESC
LIMIT 10;
'''

df_top_products = pd.read_sql_query(query_top_products, conn)
df_top_products.plot(x="ProductName", y="total_sales", kind="bar", figsize=(10, 7), legend=False)

plt.title("Top 10 productos más rentables")
plt.xlabel("Productos")
plt.ylabel("Ventas totales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 3. Ventas por empleado
query_top_employees = '''
SELECT 
    e.FirstName || ' ' || e.LastName AS Employee,
    SUM(p.Price * od.Quantity) AS total_sales
FROM Orders o
JOIN Employees e 
    ON o.EmployeeID = e.EmployeeID
JOIN OrderDetails od
    ON o.OrderID = od.OrderID
JOIN Products p
    ON od.ProductID = p.ProductID
GROUP BY e.EmployeeID, e.FirstName, e.LastName
ORDER BY total_sales DESC;
'''

df_top_employees = pd.read_sql_query(query_top_employees, conn)
df_top_employees.plot(x="Employee", y="total_sales", kind="bar", figsize=(10, 7), legend=False)

plt.title("Ventas por empleado")
plt.xlabel("Empleados")
plt.ylabel("Total vendido")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 4. Ingresos por mes
query_sales_by_month = '''
SELECT 
   strftime('%Y-%m', o.OrderDate) AS month,
   SUM(p.Price * od.Quantity) AS total_sales
FROM Orders o
JOIN OrderDetails od
   ON o.OrderID = od.OrderID
JOIN Products p
   ON od.ProductID = p.ProductID
GROUP BY strftime('%Y-%m', o.OrderDate)
ORDER BY month;
'''

df_sales_by_month = pd.read_sql_query(query_sales_by_month, conn)
df_sales_by_month.plot(x="month", y="total_sales", kind="bar", figsize=(10, 7), legend=False)

plt.title("Ingresos por mes")
plt.xlabel("Meses")
plt.ylabel("Ingresos")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# 5. Clientes con mayores compras
query_top_customers = '''
SELECT 
    c.ContactName AS customer,
    COUNT(DISTINCT o.OrderID) AS total_orders,
    SUM(p.Price * od.Quantity) AS total_sales
FROM Orders o
JOIN OrderDetails od
    ON o.OrderID = od.OrderID
JOIN Products p
    ON od.ProductID = p.ProductID
JOIN Customers c
    ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.ContactName
ORDER BY total_sales DESC;
'''

df_top_customers = pd.read_sql_query(query_top_customers, conn)
df_top_customers.plot(x="customer", y="total_sales", kind="bar", figsize=(10, 7), legend=False)

plt.title("Clientes con mayores compras")
plt.xlabel("Clientes")
plt.ylabel("Ventas totales")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# 6. Total de unidades vendidas
query_units_sold = '''
SELECT 
    SUM(Quantity) AS total_units_sold
FROM OrderDetails;
'''

df_units_sold = pd.read_sql_query(query_units_sold, conn)
units_sold = df_units_sold.loc[0, "total_units_sold"]
print(f"Unidades vendidas: {units_sold}")


# 7. Total de órdenes
query_total_orders = '''
SELECT 
    COUNT(DISTINCT OrderID) AS total_orders
FROM Orders;
'''

df_total_orders = pd.read_sql_query(query_total_orders, conn)
total_orders = df_total_orders.loc[0, "total_orders"]
print(f"Órdenes totales: {total_orders}")


# 8. Ticket promedio
query_avg_ticket = '''
SELECT 
    SUM(p.Price * od.Quantity) * 1.0 / COUNT(DISTINCT od.OrderID) AS avg_ticket
FROM OrderDetails od
JOIN Products p
    ON od.ProductID = p.ProductID;
'''

df_avg_ticket = pd.read_sql_query(query_avg_ticket, conn)
avg_ticket = df_avg_ticket.loc[0, "avg_ticket"]
print(f"Ticket promedio: {avg_ticket:.2f}")

conn.close()