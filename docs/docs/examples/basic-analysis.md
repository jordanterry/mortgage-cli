---
sidebar_position: 1
---

# Basic Analysis

This guide walks through analyzing a single property investment.

## Scenario

You're considering a €150,000 apartment that could rent for €900/month. You have €50,000 available for investment.

## Step 1: Quick Analysis

Run a basic analysis with default settings:

```bash
mortgage-cli analyze --price 150000 --rent 900
```

Output:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Metric                         ┃ Value           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Property Price                 │ €150,000        │
│ Down Payment                   │ 20% (€30,000)   │
│ Loan Amount                    │ €120,000        │
├────────────────────────────────┼─────────────────┤
│ Monthly Mortgage Payment       │ €705            │
│ Monthly Fixed Costs            │ €180            │
│ Break-even Rent                │ €885/month      │
├────────────────────────────────┼─────────────────┤
│ Expected Rent                  │ €900/month      │
│ Monthly Surplus                │ €15             │
│ Cash-on-Cash Return            │ 0.5%            │
├────────────────────────────────┼─────────────────┤
│ Total Upfront Costs            │ €34,500         │
│ Within Budget                  │ Yes             │
│ Verdict                        │ GREEN           │
└────────────────────────────────┴─────────────────┘
```

## Step 2: Interpret Results

### Break-even Rent: €885/month

This is the minimum rent needed to cover all costs:
- Mortgage payment (€705)
- Property tax (€100)
- Insurance (€30)
- Maintenance reserve (€50)

### Monthly Surplus: €15

With expected rent of €900, you'd have €15/month positive cash flow.

### Cash-on-Cash Return: 0.5%

Annual cash flow (€15 × 12 = €180) divided by total investment (€34,500).

### Verdict: GREEN

Break-even rent (€885) is below 90% of the target rent (€1,000), indicating a good investment.

## Step 3: Try Different Down Payments

See how a larger down payment affects the numbers:

```bash
mortgage-cli analyze --price 150000 --rent 900 --down 30%
```

With 30% down:
- Loan amount: €105,000 (vs €120,000)
- Monthly mortgage: €617 (vs €705)
- Break-even rent: €797 (vs €885)
- Monthly surplus: €103 (vs €15)

The trade-off: you need more capital upfront (€45,000 vs €30,000) but have better cash flow.

## Step 4: Get Detailed Breakdown

Use the summary format for a narrative explanation:

```bash
mortgage-cli analyze --price 150000 --rent 900 --output summary
```

```
INVESTMENT SUMMARY
==================================================

A €150,000 property with 20% down (€30,000) would require
€885/month in rent to break even.

At the expected rent of €900/month, this represents
a monthly surplus of €15.

Total upfront investment: €34,500 (within your €50,000 budget)
Cash-on-cash return: 0.5%

RECOMMENDATION:
Good investment opportunity. Break-even rent is comfortably below
your target, providing a margin of safety.
```

## Step 5: Export for Records

Save the analysis as JSON for your records:

```bash
mortgage-cli analyze --price 150000 --rent 900 --output json > analysis.json
```

Or as CSV:

```bash
mortgage-cli analyze --price 150000 --rent 900 --output csv > analysis.csv
```

## Decision Framework

Based on this analysis:

| Factor | Assessment |
|--------|------------|
| Break-even vs Expected | €885 < €900 ✓ |
| Budget | €34,500 < €50,000 ✓ |
| Cash Flow | Positive (€15/month) ✓ |
| Verdict | GREEN ✓ |

**Conclusion**: This property meets all criteria for a viable investment. The margin is thin (€15/month), so consider:
- Can you reliably achieve €900/month rent?
- Is there room for rent increases?
- What happens during vacancy periods?

## Next Steps

- Use the [matrix command](/cli-reference/matrix) to compare different price points
- Create a [conservative profile](/configuration/profiles) to stress-test assumptions
- View the [amortization schedule](/cli-reference/amortize) to understand equity building
