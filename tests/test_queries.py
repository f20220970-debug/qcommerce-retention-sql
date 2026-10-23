"""Run the real SQL files on a tiny hand-made dataset with known answers."""
from pathlib import Path

import duckdb
import pytest

SQL = Path(__file__).resolve().parents[1] / "sql"


def q(con, name, **params):
    text = (SQL / name).read_text()
    for k, v in params.items():
        text = text.replace("{" + k + "}", str(v))
    return con.execute(text).df()


@pytest.fixture
def con():
    c = duckdb.connect()
    c.execute("CREATE TABLE departments AS SELECT * FROM (VALUES (1, 'produce'), (2, 'dairy')) t(department_id, department)")
    c.execute("CREATE TABLE products AS SELECT * FROM (VALUES (1, 'Banana', 1, 1), (2, 'Milk', 2, 2), (3, 'Kale', 1, 1)) t(product_id, product_name, aisle_id, department_id)")
    # user 1: 3 orders; user 2: 1 order
    c.execute("""CREATE TABLE orders AS SELECT * FROM (VALUES
        (10, 1, 'prior', 1, 0, 9, NULL), (11, 1, 'prior', 2, 1, 9, 7.0), (12, 1, 'train', 3, 2, 10, 7.0),
        (20, 2, 'prior', 1, 3, 18, NULL)) t(order_id, user_id, eval_set, order_number, order_dow, order_hour_of_day, days_since_prior_order)""")
    c.execute("""CREATE TABLE order_items AS SELECT * FROM (VALUES
        (10, 1, 1, 0), (10, 2, 2, 0), (11, 1, 1, 1), (12, 1, 1, 1), (12, 3, 2, 0), (20, 3, 1, 0))
        t(order_id, product_id, add_to_cart_order, reordered)""")
    return c


def test_overview(con):
    r = q(con, "01_overview.sql").iloc[0]
    assert r.customers == 2 and r.orders == 4
    assert r.share_items_reordered == pytest.approx(2 / 6, abs=1e-4)


def test_reorder_by_department(con):
    r = q(con, "02_reorder_by_department.sql").set_index("department")
    assert r.loc["produce", "reorder_rate"] == pytest.approx(0.4)        # bananas x3 (2 reorders) + kale x2
    assert r["share_of_items"].sum() == pytest.approx(1.0)


def test_habit_window(con):
    r = q(con, "03_habit_window.sql")
    assert list(r["days_since_prior"]) == [7] and r["share"].iloc[0] == 1.0


def test_retention_curve(con):
    r = q(con, "04_retention_curve.sql").set_index("order_number")
    assert r.loc[2, "share_reaching"] == 0.5 and r.loc[3, "share_reaching"] == 0.5   # user 1 has 3 orders
    assert r.loc[5, "customers_reaching"] == 0


def test_breadth_vs_retention(con):
    r = q(con, "06_breadth_vs_retention.sql").set_index("departments_in_first_order")
    assert r.loc["2", "avg_total_orders"] == 3 and r.loc["1", "avg_total_orders"] == 1


def test_habit_products_threshold(con):
    assert len(q(con, "08_habit_products.sql", min_count=3)) == 1        # only bananas bought 3+ times
