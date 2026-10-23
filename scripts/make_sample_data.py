"""Generate small FAKE files with the exact Instacart schema, to test the pipeline before
downloading the real data. Delete the CSVs in data/ afterwards; the numbers mean nothing."""
import csv
import random
from pathlib import Path

random.seed(7)
D = Path(__file__).resolve().parents[1] / "data"
D.mkdir(exist_ok=True)
deps = ["produce", "dairy eggs", "snacks", "beverages", "frozen", "pantry", "bakery", "household", "personal care", "babies"]
with open(D / "departments.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["department_id", "department"]); [w.writerow([i + 1, d]) for i, d in enumerate(deps)]
with open(D / "aisles.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["aisle_id", "aisle"]); [w.writerow([i, f"aisle {i}"]) for i in range(1, 31)]
with open(D / "products.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["product_id", "product_name", "aisle_id", "department_id"])
    for p in range(1, 401):
        w.writerow([p, f"Product {p}", random.randint(1, 30), random.randint(1, len(deps))])
oid = 0
with open(D / "orders.csv", "w", newline="") as fo, open(D / "order_products__prior.csv", "w", newline="") as fp, \
     open(D / "order_products__train.csv", "w", newline="") as ft:
    wo, wp, wt = csv.writer(fo), csv.writer(fp), csv.writer(ft)
    wo.writerow(["order_id", "user_id", "eval_set", "order_number", "order_dow", "order_hour_of_day", "days_since_prior_order"])
    for w in (wp, wt):
        w.writerow(["order_id", "product_id", "add_to_cart_order", "reordered"])
    for u in range(1, 1501):
        n = random.randint(4, 60)
        fav = random.sample(range(1, 401), 8)
        seen = set()
        for k in range(1, n + 1):
            oid += 1
            ev = "train" if k == n else "prior"
            gap = "" if k == 1 else min(30, max(0, int(random.choice([7, 7, 3, 14, 30, random.randint(1, 30)]) + random.randint(-2, 2))))
            wo.writerow([oid, u, ev, k, random.randint(0, 6), random.choice([9, 10, 11, 14, 15, 16, 20]), gap])
            items = random.sample(fav, 3) + random.sample(range(1, 401), random.randint(1, 10))
            for pos, p in enumerate(items, 1):
                (wt if ev == "train" else wp).writerow([oid, p, pos, 1 if p in seen else 0])
                seen.add(p)
print(f"fake data written to {D}")
