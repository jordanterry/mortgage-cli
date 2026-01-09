---
sidebar_position: 2
---

# Finding Your Price Range

**Difficulty**: Intermediate

In this tutorial, you'll learn how to use the sensitivity matrix to explore multiple investment scenarios at once. This is invaluable when you're searching for properties and want to know your viable price range.

## What You'll Learn

- How to generate and read a sensitivity matrix
- Finding the sweet spot between price and down payment
- Identifying the best opportunities quickly
- Using the matrix to set your property search criteria

## Prerequisites

- Completed [Evaluating Your First Property](/tutorials/first-property)
- Understanding of break-even rent and verdicts

## The Scenario

You're actively searching for rental properties in Bordeaux. The market has properties ranging from €100,000 to €200,000, and typical rents are around €900/month for the type of property you're targeting.

You have €50,000 available for investment and want to know:
- What's the maximum price you can afford?
- What combination of price and down payment gives the best results?
- Which properties should you even bother viewing?

---

## Step 1: Generate Your First Matrix

Let's see break-even rents across different prices and down payments:

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --rent 900
```

You'll see a table like this:

```
Sensitivity Matrix - Break-even Rent (Target: €900/month)
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Down %    ┃ €100,000  ┃ €120,000  ┃ €140,000  ┃ €160,000  ┃ €180,000  ┃ €200,000  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 10%       │ €800      │ €910      │ €1,021    │ €1,131    │ €1,242    │ €1,352    │
│ 15%       │ €770      │ €874      │ €978      │ €1,082    │ €1,186    │ €1,290    │
│ 20%       │ €739      │ €837      │ €935      │ €1,033    │ €1,130    │ €1,228    │
│ 25%       │ €708      │ €800      │ €892      │ €983      │ €1,075    │ €1,167    │
│ 30%       │ €678      │ €763      │ €849      │ €934      │ €1,020    │ €1,105    │
│ 35%       │ €647      │ €727      │ €806      │ €885      │ €964      │ €1,044    │
│ 40%       │ €616      │ €690      │ €763      │ €836      │ €909      │ €982      │
│ 45%       │ €586      │ €653      │ €720      │ €787      │ €854      │ €921      │
│ 50%       │ €555      │ €616      │ €677      │ €738      │ €798      │ €859      │
└───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘
Legend: GREEN = Good (<€810) | YELLOW = Marginal (€810-€900) | RED = Poor (>€900)
```

## Step 2: Reading the Matrix

The matrix shows break-even rent for each combination:
- **Rows**: Down payment percentages (10% to 50%)
- **Columns**: Property prices (€100K to €200K)
- **Cells**: The break-even rent needed for that combination

### Color Coding

With a target rent of €900:
- **GREEN** (break-even < €810): Good investment with safety margin
- **YELLOW** (€810-€900): Marginally viable
- **RED** (> €900): Would lose money monthly

### What This Matrix Tells Us

Looking at the €140,000 column (a mid-range property):

| Down Payment | Break-even | Verdict |
|--------------|------------|---------|
| 10% | €1,021 | RED - Losing €121/month |
| 20% | €935 | RED - Losing €35/month |
| 25% | €892 | YELLOW - Close but works |
| 30% | €849 | GREEN - €51 surplus |

So for a €140,000 property at €900 rent, you'd need at least 25-30% down to make it viable.

## Step 3: Finding Your Maximum Price

Let's narrow down. You want GREEN verdicts - what's the maximum price?

Looking at the 20% down row (your preferred down payment):
- €100,000 → €739 (GREEN)
- €120,000 → €837 (YELLOW)
- €140,000 → €935 (RED)

**At 20% down, properties up to ~€115,000 are solidly viable.**

What if you stretch to 25% down?
- €100,000 → €708 (GREEN)
- €120,000 → €800 (GREEN)
- €140,000 → €892 (YELLOW)

**At 25% down, you can go up to ~€130,000 and still be comfortable.**

## Step 4: Get a Quick Summary

For a faster overview, use the summary output:

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --rent 900 --output summary
```

```
SENSITIVITY ANALYSIS SUMMARY
==================================================

Analyzed 54 price/down-payment combinations:
  - 18 good opportunities (green)
  - 9 marginal opportunities (yellow)
  - 27 poor opportunities (red)

Top opportunities (lowest break-even rent):
  1. €100,000 with 50% down - break-even: €555/month
  2. €100,000 with 45% down - break-even: €586/month
  3. €100,000 with 40% down - break-even: €616/month
```

This instantly shows that 18 combinations work well, and the best opportunities are lower-priced properties with higher down payments.

## Step 5: Zoom In on Your Range

Now that you know your rough range, let's get more detail around €120,000-€150,000:

```bash
mortgage-cli matrix --price-min 120000 --price-max 150000 --price-step 10000 --down-min 20% --down-max 35% --rent 900
```

```
Sensitivity Matrix - Break-even Rent (Target: €900/month)
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Down %    ┃ €120,000  ┃ €130,000  ┃ €140,000  ┃ €150,000  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 20%       │ €837      │ €886      │ €935      │ €984      │
│ 25%       │ €800      │ €846      │ €892      │ €937      │
│ 30%       │ €763      │ €806      │ €849      │ €892      │
│ 35%       │ €727      │ €766      │ €806      │ €846      │
└───────────┴───────────┴───────────┴───────────┴───────────┘
```

Now you can see the exact boundary:
- **€120,000 at 25% down**: €800 break-even (GREEN)
- **€130,000 at 25% down**: €846 break-even (YELLOW)
- **€130,000 at 30% down**: €806 break-even (GREEN)

## Step 6: Budget Reality Check

Remember, you have €50,000 total. Let's verify which combinations are actually affordable.

For a €130,000 property at 30% down:
```bash
mortgage-cli analyze --price 130000 --rent 900 --down 30%
```

```
│ Total Upfront Costs            │ €42,575          │
│ Within Budget                  │ Yes              │
```

For a €140,000 property at 30% down:
```bash
mortgage-cli analyze --price 140000 --rent 900 --down 30%
```

```
│ Total Upfront Costs            │ €45,850          │
│ Within Budget                  │ Yes              │
```

Both fit your €50,000 budget.

## Step 7: Define Your Search Criteria

Based on this analysis, you now have clear property search criteria:

| Criterion | Value | Reasoning |
|-----------|-------|-----------|
| **Max Price** | €140,000 | GREEN at 30% down |
| **Down Payment** | 30% | Needed for properties above €120K |
| **Min Rent** | €900 | Based on your target |
| **Max Upfront** | €45,850 | Fits €50K budget |

Any property listed under €140,000 that can rent for €900+ is worth investigating.

---

## What You've Learned

In this tutorial, you've learned how to:

- ✅ Generate a sensitivity matrix with `mortgage-cli matrix`
- ✅ Read and interpret the color-coded results
- ✅ Find your maximum viable property price
- ✅ Zoom in on specific price ranges
- ✅ Cross-reference with your budget constraints

## Try It Yourself

1. **Higher rent market**: Generate a matrix for €150,000-€250,000 with €1,200 target rent. What's the sweet spot?

2. **Limited capital**: If you only had €35,000 to invest, what would your maximum property price be? (Hint: you'll need lower down payments)

3. **Export for comparison**: Generate two matrices - one for Bordeaux (€900 rent) and one for Toulouse (€850 rent). Export both to CSV and compare in a spreadsheet.

   ```bash
   mortgage-cli matrix --price-min 100000 --price-max 180000 --rent 900 --output csv > bordeaux.csv
   mortgage-cli matrix --price-min 100000 --price-max 180000 --rent 850 --output csv > toulouse.csv
   ```

## Next Steps

Ready to stress-test your investment assumptions?
- [Stress Testing Your Investment](/tutorials/stress-testing) - Use multiple profiles to evaluate risk under different scenarios
