-- 1. Total sales
SELECT  
    SUM(p.Price * od.Quantity) AS total_sales
FROM OrderDetails od
JOIN Products p 
    ON od.ProductID = p.ProductID;

-- 2. Top 10 products
SELECT 
    p.ProductName,
    SUM(p.Price * od.Quantity) AS total_sales
FROM OrderDetails od
JOIN Products p 
    ON od.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY total_sales DESC
LIMIT 10;

-- 3. Sales by employee
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

-- 4. Sales by month
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

-- 5. Top customers
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