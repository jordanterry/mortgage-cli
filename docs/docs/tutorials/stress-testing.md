---
sidebar_position: 3
---

# Stress Testing Your Investment

**Difficulty**: Advanced

In this tutorial, you'll learn how to create custom profiles to stress-test your investment under different economic conditions. This helps you understand your risk exposure before committing capital.

## What You'll Learn

- Creating custom profiles for different scenarios
- Comparing the same property across multiple profiles
- Understanding how interest rates affect viability
- Building a risk assessment framework

## Prerequisites

- Completed [Finding Your Price Range](/tutorials/finding-price-range)
- Basic understanding of YAML configuration files

## The Scenario

You've found the perfect property:

| Detail | Value |
|--------|-------|
| **Location** | Nantes, France |
| **Price** | €165,000 |
| **Expected Rent** | €950/month |
| **Down Payment** | 25% (€41,250) |

The numbers look good with current assumptions. But what if:
- Interest rates rise?
- Maintenance costs are higher than expected?
- You can't achieve the target rent?

Let's stress-test this investment.

---

## Step 1: Baseline Analysis

First, let's see how this property performs with default assumptions:

```bash
mortgage-cli analyze --price 165000 --rent 950 --down 25%
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Metric                         ┃ Value            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Property Price                 │ €165,000         │
│ Down Payment                   │ 25% (€41,250)    │
│ Break-even Rent                │ €911/month       │
│ Expected Rent                  │ €950/month       │
│ Monthly Surplus                │ €39              │
│ Cash-on-Cash Return            │ 1.0%             │
│ Verdict                        │ GREEN            │
└────────────────────────────────┴──────────────────┘
```

Looks good - a GREEN verdict with €39/month surplus. But this assumes:
- 4.0% interest rate
- €180/month in fixed costs
- No major surprises

## Step 2: Create a Conservative Profile

Let's create a "pessimistic" profile that models worse conditions:

```bash
mortgage-cli profile create pessimistic --description "Conservative stress test"
```

```
Created profile 'pessimistic' based on 'default'
Edit with: mortgage-cli profile edit pessimistic
```

Now edit the profile. Open `~/.config/mortgage-cli/profiles/pessimistic.yaml`:

```yaml
name: pessimistic
description: Conservative stress test - higher rates and costs

mortgage:
  interest_rate: 0.055      # 5.5% - rates could rise
  insurance_rate: 0.005     # 0.5% - slightly higher
  duration_years: 20
  default_down_payment: 0.25

budget:
  total_available: 50000
  target_rent: 950

monthly_costs:
  property_tax: 130         # 30% higher than default
  insurance: 40             # Higher insurance
  maintenance: 100          # Double the reserve (older building)
  management: 0

purchase_costs:
  notary_legal:
    type: percentage
    value: 0.015
  bank_arrangement:
    type: percentage
    value: 0.01
  survey_valuation:
    type: fixed
    value: 750
  mortgage_broker:
    type: fixed
    value: 0
  other:
    type: fixed
    value: 0

thresholds:
  green_below: 0.85         # Stricter threshold
  yellow_below: 0.95
```

Key changes from default:
- Interest rate: 4.0% → 5.5%
- Monthly fixed costs: €180 → €270
- Stricter verdict thresholds

## Step 3: Create an Optimistic Profile

For comparison, let's also create a best-case scenario:

```bash
mortgage-cli profile create optimistic --description "Best case scenario"
```

Edit `~/.config/mortgage-cli/profiles/optimistic.yaml`:

```yaml
name: optimistic
description: Best case scenario - favorable conditions

mortgage:
  interest_rate: 0.035      # 3.5% - rates could drop
  insurance_rate: 0.003     # Lower insurance (good health)
  duration_years: 25        # Longer term available
  default_down_payment: 0.25

budget:
  total_available: 50000
  target_rent: 950

monthly_costs:
  property_tax: 80          # Lower than average
  insurance: 25
  maintenance: 40           # New building, less maintenance
  management: 0

purchase_costs:
  notary_legal:
    type: percentage
    value: 0.015
  bank_arrangement:
    type: percentage
    value: 0.01
  survey_valuation:
    type: fixed
    value: 750
  mortgage_broker:
    type: fixed
    value: 0
  other:
    type: fixed
    value: 0

thresholds:
  green_below: 0.9
  yellow_below: 1.0
```

Key changes:
- Interest rate: 4.0% → 3.5%
- Term: 20 → 25 years
- Monthly fixed costs: €180 → €145

## Step 4: Compare All Profiles

Now let's see how the same property performs across all scenarios:

```bash
mortgage-cli profile compare --price 165000 --rent 950 --profiles optimistic,default,pessimistic
```

```
Profile Comparison - €165,000 @ €950/month
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Profile       ┃ Break-even Rent ┃ Cash-on-Cash  ┃ Verdict  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ optimistic    │ €746/month      │ 5.3%          │ GREEN    │
│ default       │ €911/month      │ 1.0%          │ GREEN    │
│ pessimistic   │ €1,078/month    │ -3.3%         │ RED      │
└───────────────┴─────────────────┴───────────────┴──────────┘
```

### What This Tells Us

| Scenario | Break-even | Monthly Cash Flow | Assessment |
|----------|------------|-------------------|------------|
| Optimistic | €746 | +€204 | Excellent - strong cash flow |
| Default | €911 | +€39 | Good - positive but thin |
| Pessimistic | €1,078 | -€128 | **Problem** - losing money |

**Critical insight**: Under pessimistic assumptions, you'd lose €128/month - that's €1,536/year out of pocket.

## Step 5: Find Your Break-even Point

At what interest rate does this investment stop working? Let's create test profiles:

```bash
mortgage-cli profile create rate-4.5 --description "Test at 4.5%"
mortgage-cli profile create rate-5.0 --description "Test at 5.0%"
mortgage-cli profile create rate-5.5 --description "Test at 5.5%"
```

Edit each with just the interest rate changed, then compare:

```bash
mortgage-cli profile compare --price 165000 --rent 950 --profiles default,rate-4.5,rate-5.0,rate-5.5
```

```
Profile Comparison - €165,000 @ €950/month
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Profile       ┃ Break-even Rent ┃ Cash-on-Cash  ┃ Verdict  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ default (4.0%)│ €911/month      │ 1.0%          │ GREEN    │
│ rate-4.5      │ €945/month      │ 0.1%          │ YELLOW   │
│ rate-5.0      │ €980/month      │ -0.8%         │ RED      │
│ rate-5.5      │ €1,015/month    │ -1.7%         │ RED      │
└───────────────┴─────────────────┴───────────────┴──────────┘
```

**Finding**: This investment becomes marginal at 4.5% and unprofitable at 5.0%. Your "rate buffer" is only 0.5-1.0%.

## Step 6: What-If Analysis

### What if rent is lower?

Let's say you can only get €880/month (not €950):

```bash
mortgage-cli profile compare --price 165000 --rent 880 --profiles optimistic,default,pessimistic
```

```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Profile       ┃ Break-even Rent ┃ Cash-on-Cash  ┃ Verdict  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ optimistic    │ €746/month      │ 3.5%          │ GREEN    │
│ default       │ €911/month      │ -0.8%         │ RED      │
│ pessimistic   │ €1,078/month    │ -5.2%         │ RED      │
└───────────────┴─────────────────┴───────────────┴──────────┘
```

Even under default assumptions, the investment fails if rent drops to €880.

### What price makes this bulletproof?

Let's find a price that works even under pessimistic conditions:

```bash
mortgage-cli matrix --price-min 120000 --price-max 165000 --price-step 15000 --rent 950 --profile pessimistic
```

```
Sensitivity Matrix (pessimistic profile)
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Down %    ┃ €120,000  ┃ €135,000  ┃ €150,000  ┃ €165,000  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 20%       │ €885      │ €968      │ €1,050    │ €1,133    │
│ 25%       │ €840      │ €916      │ €993      │ €1,069    │
│ 30%       │ €796      │ €865      │ €935      │ €1,005    │
│ 35%       │ €751      │ €814      │ €877      │ €941      │
└───────────┴───────────┴───────────┴───────────┴───────────┘
```

**Finding**: To get a GREEN verdict (< €807) even in pessimistic conditions:
- €120,000 at 30% down, or
- €135,000 at 35% down

This suggests negotiating the price down to €135,000-€140,000 would significantly reduce your risk.

## Step 7: Build Your Risk Report

Let's create a comprehensive risk assessment:

```bash
# Export all comparisons
mortgage-cli profile compare --price 165000 --rent 950 --profiles optimistic,default,pessimistic --output json > risk-report.json

# Get detailed analysis for worst case
mortgage-cli analyze --price 165000 --rent 950 --down 25% --profile pessimistic --output summary
```

### Risk Assessment Summary

| Factor | Current Value | Sensitivity |
|--------|---------------|-------------|
| Interest Rate | 4.0% | Breaks at 5.0% (+1.0%) |
| Rent | €950 | Breaks at €911 (-4%) |
| Fixed Costs | €180/month | Breaks at €220 (+22%) |
| Price | €165,000 | Safe at €135,000 (-18%) |

**Risk Rating**: MODERATE
- Investment works under normal conditions
- Little margin for adverse scenarios
- Consider negotiating price to €145,000 for safety buffer

---

## What You've Learned

In this tutorial, you've learned how to:

- ✅ Create custom profiles for different scenarios
- ✅ Compare investments across multiple profiles
- ✅ Identify your break-even points for key variables
- ✅ Build a risk assessment framework
- ✅ Make data-driven decisions about property investments

## Try It Yourself

1. **Your local market**: Create profiles for your specific situation (your actual mortgage rate quotes, local property taxes, etc.)

2. **Vacancy analysis**: Create a profile that assumes 1 month vacancy per year (reduce target rent by 8.3%)

3. **Management costs**: Create a profile assuming you hire a property manager (add 8% of rent to monthly costs)

## Best Practices

### When to Use Each Profile

| Profile | Use When |
|---------|----------|
| Optimistic | Establishing maximum potential |
| Default | Day-to-day analysis |
| Pessimistic | Making final investment decisions |

### Red Flags

Reconsider the investment if:
- ❌ RED verdict under default assumptions
- ❌ Less than 10% buffer on rent
- ❌ Less than 1% buffer on interest rate
- ❌ Break-even requires more than market rent

### Green Flags

Strong investment signals:
- ✅ GREEN verdict even under pessimistic assumptions
- ✅ 15%+ rent buffer (break-even well below market)
- ✅ Profitable at 2%+ higher interest rates
- ✅ Positive cash flow in all scenarios

---

## Next Steps

You've now mastered mortgage-cli! Here are some ways to continue:

- Explore the [CLI Reference](/cli-reference/analyze) for all available options
- Learn about [amortization schedules](/cli-reference/amortize) to understand equity building
- Check out the [configuration guide](/configuration/profiles) for advanced profile customization
