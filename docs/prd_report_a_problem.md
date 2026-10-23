# PRD: Fix-it-in-30-seconds, instant resolution for quality issues

**Problem.** When a FirstClub order has a quality problem (expired, damaged, missing or poor produce), customers
struggle to report it: in public reviews the support bot's photo upload sent a user back to the home page,
replies repeat apologies, and many are redirected to email. For a brand whose promise *is* quality, a slow fix
turns one bad item into a lost customer.

**Evidence.**
- Google Play and App Store reviews (2026): expired items on a first order; photo upload failing in the support
  bot; support redirecting to email; offer items removed after ordering.
- Habit data (my Instacart SQL analysis): 51% of repeat orders come within 7 days, so a customer who leaves a
  bad first or second order unresolved may never form the weekly habit.

**Users.** All customers, with priority on (a) first and second orders, and (b) fresh categories (fruits,
vegetables, dairy, bakery), where quality varies most and habits are strongest (dairy reorders at 67%).

**Solution (v1).**
1. On the order screen for 48 hours after delivery: a **"Something not right?"** button next to each item.
2. Tap the item, pick a reason (expired, damaged, missing, not fresh, wrong item), take **one photo** (required
   for fresh items), submit. Target: **under 30 seconds, 4 taps.**
3. **Instant resolution** for fresh items under a value threshold (for example ₹300) when the customer's history
   is clean: refund to wallet or free replacement on the next order, the customer's choice. Larger or repeated
   claims go to an agent queue with the photo attached, with a reply within 2 hours.
4. Every report is tagged with SKU, batch, warehouse and rider, feeding a **quality dashboard** for category and
   supply-chain teams.

*Out of scope for v1:* chat redesign, return pickups for non-food items, automatic photo checking.

**Success metric.** 30-day repeat rate of customers who report an issue (versus customers with an issue today).
**Supporting metrics.** Median time to resolution; share of issues resolved without an agent; app-store mentions
of support.
**Counter-metrics.** Refund cost as a share of revenue; claim rate per customer (abuse); agent workload.

**Experiment and rollout.**
- Randomise at customer level: half of customers see the new flow, half keep the current support path, for 4
  weeks in one city (Bangalore).
- Decision rule: ship if the issue-reporters' 30-day repeat rate rises by at least 5 points with refund cost
  under an agreed ceiling and no rise in claims per customer.
- Abuse controls from day one: one instant refund per order, value cap, photo required, and auto-review for
  customers whose claim rate is unusually high.

**Risks and open questions.**
- Abuse: generous instant refunds can be gamed; the cap, photo and history checks need tuning with real data.
- Root cause: fast refunds hide symptoms. The tagging must route problems to the right team, or the same SKU
  keeps failing.
- Baselines: what share of orders have an issue today, and how many of those customers return? (Needs
  FirstClub's ticket data.)
