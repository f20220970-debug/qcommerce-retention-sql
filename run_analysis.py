"""Run the whole analysis: load the Instacart CSVs into DuckDB, run every query in sql/,
save each result to results/, draw the charts and write results/summary.md.

    python run_analysis.py --reload    # first run (loads the CSVs, ~1-3 minutes)
    python run_analysis.py             # later runs reuse data/instacart.duckdb
"""
import argparse
import time
from pathlib import Path

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA, SQL, RESULTS, CHARTS = ROOT / "data", ROOT / "sql", ROOT / "results", ROOT / "charts"
DB = DATA / "instacart.duckdb"
NEEDED = ["orders.csv", "order_products__prior.csv", "order_products__train.csv",
          "products.csv", "aisles.csv", "departments.csv"]


def sql(name: str, **params) -> str:
    text = (SQL / name).read_text()
    for k, v in params.items():
        text = text.replace("{" + k + "}", str(v))
    return text


def load(con):
    missing = [f for f in NEEDED if not (DATA / f).exists()]
    if missing:
        raise SystemExit(f"Missing files in data/: {missing}. See README step 2.")
    t0 = time.time()
    con.execute(sql("00_load.sql", data=DATA.as_posix()))
    print(f"  loaded CSVs in {time.time() - t0:.0f}s")


def run_queries(con, min_count):
    RESULTS.mkdir(exist_ok=True)
    out = {}
    for f in sorted(SQL.glob("0[1-9]_*.sql")):
        df = con.execute(sql(f.name, min_count=min_count)).df()
        df.to_csv(RESULTS / f"{f.stem}.csv", index=False)
        out[f.stem[:2]] = df
        print(f"  {f.name}: {len(df)} rows")
    return out


def charts(r):
    CHARTS.mkdir(exist_ok=True)
    teal, grey = "#2C7A7B", "#9DB4C0"

    d = r["02"].sort_values("reorder_rate")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(d["department"], 100 * d["reorder_rate"], color=teal)
    ax.set_xlabel("Reorder rate (%)"); ax.set_title("Which categories build habits: reorder rate by department")
    fig.tight_layout(); fig.savefig(CHARTS / "reorder_by_department.png", dpi=120); plt.close(fig)

    d = r["03"]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(d["days_since_prior"], 100 * d["share"], color=[teal if x in (7, 30) else grey for x in d["days_since_prior"]])
    ax.set_xlabel("Days since previous order (30 = 30 or more)"); ax.set_ylabel("% of repeat orders")
    ax.set_title("The habit window: days between orders")
    fig.tight_layout(); fig.savefig(CHARTS / "habit_window.png", dpi=120); plt.close(fig)

    d = r["04"]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(d["order_number"], 100 * d["share_reaching"], marker="o", color=teal)
    ax.set_xscale("log"); ax.set_xticks(d["order_number"]); ax.set_xticklabels(d["order_number"])
    ax.set_xlabel("Order number (log scale)"); ax.set_ylabel("% of customers reaching it")
    ax.set_title("Retention curve: how far customers go")
    fig.tight_layout(); fig.savefig(CHARTS / "retention_curve.png", dpi=120); plt.close(fig)

    d = r["06"]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(d["departments_in_first_order"], 100 * d["share_reaching_10_orders"], color=teal)
    ax.set_xlabel("Departments in first order"); ax.set_ylabel("% reaching 10+ orders")
    ax.set_title("Width in the first order vs long-term retention (correlation)")
    fig.tight_layout(); fig.savefig(CHARTS / "breadth_vs_retention.png", dpi=120); plt.close(fig)

    d = r["09"].pivot(index="day_of_week", columns="hour", values="orders").fillna(0)
    fig, ax = plt.subplots(figsize=(11, 3.6))
    im = ax.imshow(d.values, aspect="auto", cmap="YlGnBu")
    ax.set_yticks(range(len(d.index))); ax.set_yticklabels([f"day {i}" for i in d.index])
    ax.set_xticks(range(0, 24, 2)); ax.set_xticklabels(range(0, 24, 2))
    ax.set_xlabel("Hour of day"); ax.set_title("When people order")
    fig.colorbar(im, ax=ax, label="orders"); fig.tight_layout(); fig.savefig(CHARTS / "order_heatmap.png", dpi=120); plt.close(fig)


def summary(r):
    o = r["01"].iloc[0]
    dep = r["02"].sort_values("reorder_rate", ascending=False)
    hw = r["03"].set_index("days_since_prior")
    ret = r["04"].set_index("order_number")
    conc = r["05"]
    br = r["06"]
    fb = r["07"]
    hp = r["08"]
    heat = r["09"]
    pk = heat.loc[heat["orders"].idxmax()]
    within7 = hw.loc[hw.index <= 7, "share"].sum()
    lines = [
        "# Results summary",
        "",
        f"- Scale: {int(o.customers):,} customers, {int(o.orders):,} orders, {int(o.products):,} products; "
        f"{o.avg_items_per_order} items per order; {o.avg_orders_per_customer} orders per customer.",
        f"- {100 * o.share_items_reordered:.1f}% of all items bought were reorders.",
        f"- Most habitual categories: " + ", ".join(f"{a} {100 * b:.0f}%" for a, b in dep[["department", "reorder_rate"]].head(3).values)
        + "; least: " + ", ".join(f"{a} {100 * b:.0f}%" for a, b in dep[["department", "reorder_rate"]].tail(3).values) + ".",
        f"- Habit window: {100 * within7:.0f}% of repeat orders come within 7 days; peaks at 7 days "
        f"({100 * hw.loc[7, 'share']:.1f}%) and at the 30+ cap ({100 * hw.loc[30, 'share']:.1f}%).",
        f"- Retention (customers here all have 4+ orders): {100 * ret.loc[10, 'share_reaching']:.0f}% reach order 10, "
        f"{100 * ret.loc[20, 'share_reaching']:.0f}% reach 20, {100 * ret.loc[50, 'share_reaching']:.0f}% reach 50.",
        f"- Concentration: the top 10% of customers place {100 * conc.iloc[0]['share_of_orders']:.0f}% of orders; "
        f"the top 20% place {100 * conc.iloc[1]['cumulative_share']:.0f}%.",
        "- Width vs retention (correlation): share reaching 10+ orders by departments in the first order: "
        + ", ".join(f"{a}: {100 * b:.0f}%" for a, b in br[["departments_in_first_order", "share_reaching_10_orders"]].values) + ".",
        "- First basket size vs reaching 10+ orders: "
        + ", ".join(f"{a}: {100 * b:.0f}%" for a, b in fb[["first_basket", "share_reaching_10_orders"]].values) + ".",
        f"- Top habit products: " + ", ".join(f"{a} ({100 * b:.0f}%)" for a, b in hp[["product_name", "reorder_rate"]].head(5).values) + ".",
        f"- Busiest slot: day {int(pk.day_of_week)}, {int(pk.hour)}:00 ({int(pk.orders):,} orders).",
    ]
    (RESULTS / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reload", action="store_true", help="(re)load the CSVs into DuckDB")
    ap.add_argument("--min-count", type=int, default=5000, help="minimum purchases for habit-product ranking")
    a = ap.parse_args()
    con = duckdb.connect(str(DB))
    if a.reload or not con.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='orders'").fetchone()[0]:
        load(con)
    r = run_queries(con, a.min_count)
    charts(r)
    summary(r)


if __name__ == "__main__":
    main()
