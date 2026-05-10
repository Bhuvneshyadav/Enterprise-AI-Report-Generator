CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(100) NOT NULL,
    product VARCHAR(100) NOT NULL,
    revenue DECIMAL(12, 2) NOT NULL,
    sale_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    salary DECIMAL(12, 2) NOT NULL
);

INSERT INTO sales (region, product, revenue, sale_date) VALUES
    ('North', 'Laptop', 120000.00, '2026-01-15'),
    ('North', 'Monitor', 45000.00, '2026-01-20'),
    ('South', 'Laptop', 98000.00, '2026-02-05'),
    ('East', 'Keyboard', 18000.00, '2026-02-12'),
    ('West', 'Monitor', 52000.00, '2026-03-03');

INSERT INTO employees (department, salary) VALUES
    ('Engineering', 95000.00),
    ('Sales', 72000.00),
    ('Finance', 81000.00),
    ('HR', 65000.00);
