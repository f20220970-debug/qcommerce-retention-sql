# FirstClub: customer-experience teardown

**Method.** Themes from public customer reviews on Google Play and the App Store (read October 2026) and
press coverage, combined with my own check of how customers can order. Review quotes are paraphrased; individual
reviews are anecdotes, so each theme is a hypothesis to size with FirstClub's own ticket and funnel data.

**Context.** FirstClub's promise is quality and trust: a curated range, banned ingredients and lab-tested staples,
delivered in 20-30 minutes. Reported metrics are strong: an average order value about twice that of leading
quick-commerce apps and a 60% repeat-purchase rate (TechCrunch, Inc42), and a 4.7-4.8 rating from about 10.7K
Google Play reviews. Because trust *is* the product, every failure below costs more than it would for a
discount-led competitor: a customer who pays for quality and gets an expired item feels cheated, not just
inconvenienced.

## The journey and where it breaks
| Stage | What customers report | Source | Severity |
| --- | --- | --- | --- |
| Access | Ordering is app-only: the website does not let you shop or check out, so there is no option for desktop or office users, or anyone who won't install another app | My check | Medium |
| Opening the app | The app blocks use until a pending update is installed; it asks for location every time even after access was declined | App Store review | Medium |
| Discovery | Few familiar brands; transactional shoppers who come to reorder known products feel lost (the app is designed to be browse-led, not search-led) | The Ken; TechCrunch | Medium |
| Availability | Many items out of stock, forcing extra orders, each with its own platform fee | Google Play review | High |
| Checkout / offers | An offer item was removed from the order after it was placed | Google Play review | High (trust) |
| Delivery | Expired or near-expiry items on a first order; poor produce; incomplete orders; late deliveries | Google Play review; StartupChai | **Critical (trust)** |
| Delivery instructions | A subscriber's milk was repeatedly left outside the insulated bag despite escalation | Google Play review | Medium |
| Getting help | The in-app support bot returned to the home page when uploading a photo; support repeats apologies without resolving; many replies redirect to email | Google Play review; developer replies | **High (trust repair)** |
| Returns | Bag returns rejected at pickup despite the app saying otherwise | App Store review | Low-Medium |

## The 3 friction points that matter most
**1. Quality failures on delivery (critical).** Expired or near-expiry items and poor produce break the one
promise the brand stands for. One reviewer's first-ever order arrived with expired items, so the very first
experience contradicted the brand. First orders matter disproportionately: in my Instacart analysis, half of all
repeat orders happen within a week, so a bad first basket can end the habit before it starts.

**2. Broken trust repair (high).** When something does go wrong, fixing it is slow: the photo upload in the support
bot failed and sent the user back to the home page, and replies push customers to email. A quality brand will
always have some failures; what decides whether the customer stays is how fast and fairly they're fixed.

**3. Access and habit friction (medium).** App-only ordering, forced updates and repeated location prompts all add
friction at the moment a customer wants to reorder, and out-of-stock items force repeat orders with repeat fees.
For a business built on weekly habits, every extra step on the way to "order my usual" is a leak.

## What I would build first
A **30-second "report a problem" flow with instant resolution for fresh items** (see the PRD). It targets the
two most damaging points together: it repairs trust at the exact moment it breaks, and it turns every report into
quality data FirstClub can trace back to the supplier, warehouse or rider, which is the same supply-chain
transparency problem the Product team is hiring for.

Next candidates: a lightweight **web ordering** option for repeat customers (reorder-only to start), and a
**one-tap "usual basket"** (see `growth_playbook.md`, experiment 4).

## Sources
- Google Play: "FirstClub: Quality in Minutes" reviews (August-September 2026).
- App Store: "FirstClub: Quality in minutes" reviews.
- TechCrunch (3 Sep 2025): AOV, 60% repeat rate, browse-led design.
- Inc42: quality-first model and repeat rate.
- The Ken, "Two by Two": a transactional shopper's reaction to unfamiliar brands.
- StartupChai, "Can FirstClub Scale Trust?": praise for quality alongside complaints about late deliveries,
  incomplete orders, app experience, subscription flows and produce.
