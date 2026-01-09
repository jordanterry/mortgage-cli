---
sidebar_position: 1
---

# Evaluating Your First Property

**Difficulty**: Beginner

In this tutorial, you'll learn how to use mortgage-cli to evaluate a rental property investment. We'll walk through a real scenario step by step.

## What You'll Learn

- How to run a basic property analysis
- Understanding the output metrics
- Interpreting the verdict system
- Exploring different down payment options

## Prerequisites

- mortgage-cli installed (`pip install mortgage-cli`)
- Basic understanding of rental property investing

## The Scenario

You've found a promising apartment listing:

| Detail | Value |
|--------|-------|
| **Location** | Lyon, France |
| **Asking Price** | €145,000 |
| **Expected Rent** | €850/month |
| **Type** | 2-bedroom apartment |

You have €45,000 saved for investment. Let's see if this property makes financial sense.

---

## Step 1: Run Your First Analysis

Let's start with a basic analysis using the default 20% down payment:

```bash
mortgage-cli analyze --price 145000 --rent 850
```

You should see output like this:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Metric                         ┃ Value            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Property Price                 │ €145,000         │
│ Down Payment                   │ 20% (€29,000)    │
│ Loan Amount                    │ €116,000         │
├────────────────────────────────┼──────────────────┤
│ Monthly Mortgage Payment       │ €681             │
│ Monthly Fixed Costs            │ €180             │
│ Break-even Rent                │ €861/month       │
├────────────────────────────────┼──────────────────┤
│ Expected Rent                  │ €850/month       │
│ Monthly Shortfall              │ -€11             │
│ Cash-on-Cash Return            │ -0.4%            │
├────────────────────────────────┼──────────────────┤
│ Total Upfront Costs            │ €33,388          │
│ Within Budget                  │ Yes              │
│ Verdict                        │ YELLOW           │
└────────────────────────────────┴──────────────────┘
```

## Step 2: Understanding the Output

Let's break down what each metric means:

### The Numbers

| Metric | Value | What It Means |
|--------|-------|---------------|
| Down Payment | €29,000 | Cash you put down (20% of €145,000) |
| Loan Amount | €116,000 | What you're borrowing |
| Monthly Mortgage | €681 | Your loan payment (principal + interest + insurance) |
| Fixed Costs | €180 | Property tax, insurance, maintenance |
| Break-even Rent | €861 | Minimum rent to cover all costs |

### The Verdict

The **YELLOW** verdict means this is a marginal investment:
- Break-even rent (€861) is very close to expected rent (€850)
- You'd have a small monthly shortfall of €11
- The investment works, but with no safety margin

:::tip Understanding Verdicts
- **GREEN**: Break-even rent is below 90% of your target - comfortable margin
- **YELLOW**: Break-even rent is 90-100% of target - it works, but tight
- **RED**: Break-even rent exceeds target - you'd lose money monthly
:::

## Step 3: Try a Higher Down Payment

Since you have €45,000 available, let's see if putting more down improves the situation:

```bash
mortgage-cli analyze --price 145000 --rent 850 --down 25%
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Metric                         ┃ Value            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Property Price                 │ €145,000         │
│ Down Payment                   │ 25% (€36,250)    │
│ Loan Amount                    │ €108,750         │
├────────────────────────────────┼──────────────────┤
│ Monthly Mortgage Payment       │ €639             │
│ Monthly Fixed Costs            │ €180             │
│ Break-even Rent                │ €819/month       │
├────────────────────────────────┼──────────────────┤
│ Expected Rent                  │ €850/month       │
│ Monthly Surplus                │ €31              │
│ Cash-on-Cash Return            │ 0.9%             │
├────────────────────────────────┼──────────────────┤
│ Total Upfront Costs            │ €40,638          │
│ Within Budget                  │ Yes              │
│ Verdict                        │ GREEN            │
└────────────────────────────────┴──────────────────┘
```

Much better! With 25% down:
- Break-even rent drops to €819 (from €861)
- Monthly surplus of €31 instead of shortfall
- Verdict changes from YELLOW to **GREEN**
- Still within your €45,000 budget

## Step 4: Compare Multiple Scenarios

Let's quickly compare different down payment amounts:

```bash
mortgage-cli analyze --price 145000 --rent 850 --down 30%
```

```
│ Down Payment                   │ 30% (€43,500)    │
│ Break-even Rent                │ €776/month       │
│ Monthly Surplus                │ €74              │
│ Cash-on-Cash Return            │ 1.8%             │
│ Total Upfront Costs            │ €47,888          │
│ Verdict                        │ GREEN            │
```

Wait - the upfront costs (€47,888) exceed your €45,000 budget! Let's check what the tool says:

```
│ Within Budget                  │ No               │
```

So 30% down gives better cash flow but requires more capital than you have.

### Summary of Options

| Down Payment | Break-even | Monthly Cash Flow | Upfront Cost | Verdict |
|--------------|------------|-------------------|--------------|---------|
| 20% | €861 | -€11 | €33,388 | YELLOW |
| 25% | €819 | +€31 | €40,638 | GREEN |
| 30% | €776 | +€74 | €47,888 | GREEN (over budget) |

## Step 5: Get a Detailed Summary

For a narrative explanation you can share with others, use the summary output:

```bash
mortgage-cli analyze --price 145000 --rent 850 --down 25% --output summary
```

```
INVESTMENT SUMMARY
==================================================

A €145,000 property with 25% down (€36,250) would require
€819/month in rent to break even.

At the expected rent of €850/month, this represents
a monthly surplus of €31.

Total upfront investment: €40,638 (within your €50,000 budget)
Cash-on-cash return: 0.9%

RECOMMENDATION:
Good investment opportunity. Break-even rent is comfortably below
your target, providing a margin of safety.
```

## Step 6: Save for Your Records

Export the analysis to JSON for your records:

```bash
mortgage-cli analyze --price 145000 --rent 850 --down 25% --output json > lyon-apartment.json
```

---

## What You've Learned

In this tutorial, you've learned how to:

- ✅ Run a basic property analysis with `mortgage-cli analyze`
- ✅ Interpret break-even rent and monthly cash flow
- ✅ Understand the GREEN/YELLOW/RED verdict system
- ✅ Compare different down payment scenarios
- ✅ Export results in different formats

## Try It Yourself

Practice with these exercises:

1. **Change the rent**: What if you could only get €800/month? What down payment would you need for a GREEN verdict?

2. **Negotiate the price**: If you negotiated the price down to €135,000, how does the analysis change with 20% down?

3. **Different property**: Run an analysis on a €200,000 property with €1,100/month expected rent.

## Next Steps

Ready for more? Continue to the next tutorial:
- [Finding Your Price Range](/tutorials/finding-price-range) - Use the sensitivity matrix to explore multiple scenarios at once
