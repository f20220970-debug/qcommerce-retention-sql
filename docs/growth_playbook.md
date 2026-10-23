# Growth playbook: from the findings to experiments

Each finding below becomes one intervention a quick-commerce growth team could ship, written as a testable
experiment. Numbers come from `results/summary.md` (3.35M Instacart orders, 206K customers). These are proposals
designed from public data, not results from a live test.

## Summary
| # | Finding | Intervention | Primary metric | Lifecycle stage |
| --- | --- | --- | --- | --- |
| 1 | 51% of repeat orders come within 7 days, with a spike at exactly 7 | Day-6 "time for your weekly shop?" nudge | 14-day repeat rate | Habit formation |
| 2 | A second spike at the 30+ day cap: customers drifting away | Day-21 win-back before the drift | 30-day reactivation rate | Churn risk / win-back |
| 3 | First orders spanning 7+ departments reach 10 orders more often (54% vs 47%) | "Try one new category" nudge on orders 1 and 2 | Departments per customer at order 3; orders by day 60 | Onboarding / width |
| 4 | Dairy & eggs reorder at 67%; the top 5 habit products are all milk | One-tap reorder of a customer's usual dairy basket | Share of orders placed via reorder; weekly orders per customer | Habit formation |

## 1. Day-6 weekly-shop nudge (habit formation)
- **Hypothesis:** customers who usually reorder weekly, reminded on day 6 after their last order, will reorder within 7 days
  more often, because the reminder lands just before their natural weekly slot.
- **Who:** customers with at least 2 orders whose median gap is 5–9 days.
- **Design:** randomised 50/50 holdout at customer level; push or WhatsApp on day 6 at their usual order hour.
- **Primary metric:** share reordering within 14 days. **Guardrails:** notification opt-outs, uninstalls, orders that
  would have happened anyway (compare total orders, not just reminded orders).
- **Sample size:** assuming a ~51% baseline 14-day repeat rate (replace with the real figure), detecting a 2-point
  lift at 95% confidence and 80% power needs about 9,800 customers per group.
- **Stop if:** opt-outs rise more than 0.5 points, or total 28-day orders don't move (the nudge only shifted timing).

## 2. Day-21 win-back (churn risk)
- **Hypothesis:** the 30+ day spike is customers who have lapsed; contacting them at day 21, before the lapse
  hardens, wins more of them back than waiting until day 30+.
- **Who:** customers with at least 3 orders and no order for 21 days.
- **Design:** three arms: no contact; reminder with their usual basket; reminder plus a small free-delivery offer.
  The offer arm tells us whether the message or the money does the work.
- **Primary metric:** reactivation within 30 days. **Guardrail:** offer cost per reactivated customer vs that
  customer's expected margin over the next 60 days.
- **Stop if:** the offer arm wins only by subsidising customers who would have returned anyway (compare with the
  message-only arm).

## 3. "Try one new category" (onboarding and width)
- **Finding to test:** customers whose first order spans more departments go further (54% vs 47% reach 10 orders).
  This is **correlation**: committed households may simply buy more widely. Only an experiment shows whether
  *creating* width causes retention.
- **Hypothesis:** prompting a new customer to add one item from a department they haven't bought from
  (for example bakery with a dairy order) raises the number of orders they place in their first 60 days.
- **Design:** 50/50 split of new customers on orders 1 and 2; a single curated suggestion at cart, not a discount.
- **Primary metric:** orders in the first 60 days. **Secondary:** departments bought by order 3.
  **Guardrail:** cart abandonment at the suggestion step.
- **Stop if:** width rises but 60-day orders don't, which would mean width is a symptom of commitment, not a cause.

## 4. One-tap "usual basket" for dairy (habit formation)
- **Hypothesis:** dairy and eggs are the strongest habit (67% reorder; the top five habit products are all milk),
  so making the usual dairy basket one tap away turns a weekly need into the anchor of every order.
- **Design:** show a "Reorder your usual" card with each customer's most-reordered items on the home screen for a
  randomised half of customers with 3+ orders.
- **Primary metric:** weekly orders per customer. **Secondary:** share of orders started from the card; basket size.
  **Guardrail:** basket size must not fall (people buying only the usual and less else).

## What I'd do first
Start with **#1 (day-6 nudge)**: cheapest to build, the clearest signal in the data, and the fastest readout
(14 days). Run **#3** next, because it answers the most important open question in the analysis: whether width
causes retention or just comes with it.
