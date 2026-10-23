-- Load the six Instacart CSVs into tables (run by run_analysis.py with the data folder path).
-- order_items combines the 'prior' and 'train' baskets: every order whose contents are known.
CREATE OR REPLACE TABLE departments AS SELECT * FROM read_csv_auto('{data}/departments.csv');
CREATE OR REPLACE TABLE aisles      AS SELECT * FROM read_csv_auto('{data}/aisles.csv');
CREATE OR REPLACE TABLE products    AS SELECT * FROM read_csv_auto('{data}/products.csv');
CREATE OR REPLACE TABLE orders      AS
    SELECT * FROM read_csv_auto('{data}/orders.csv')
    WHERE eval_set IN ('prior', 'train');                   -- 'test' orders have no basket data
CREATE OR REPLACE TABLE order_items AS
    SELECT * FROM read_csv_auto('{data}/order_products__prior.csv')
    UNION ALL
    SELECT * FROM read_csv_auto('{data}/order_products__train.csv');
