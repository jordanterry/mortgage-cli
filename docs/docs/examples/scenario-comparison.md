---
sidebar_position: 2
---

# Scenario Comparison

This guide shows how to compare different investment scenarios using the sensitivity matrix and profile comparison features.

## Use Case: Finding the Right Price Point

You're searching for properties in an area where prices range from €100,000 to €200,000, and rents are typically €900-1,100/month.

### Generate a Price Matrix

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --rent 1000
```

```
Sensitivity Matrix - Break-even Rent (Target: €1,000/month)
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
└───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘
```

### Reading the Matrix

- **GREEN cells**: Good investments (break-even < €900)
- **YELLOW cells**: Marginal (€900-1,000)
- **RED cells**: Poor investments (> €1,000)

From this matrix, you can see:
- Properties up to €140,000 with 20% down are viable
- Properties up to €160,000 need 25-30% down to be viable
- €200,000 properties require 40%+ down to break even under €1,000

### Get Top Opportunities

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --rent 1000 --output summary
```

```
SENSITIVITY ANALYSIS SUMMARY
==================================================

Analyzed 42 price/down-payment combinations:
  - 15 good opportunities (green)
  - 8 marginal opportunities (yellow)
  - 19 poor opportunities (red)

Top opportunities (lowest break-even rent):
  1. €100,000 with 40% down - break-even: €616/month
  2. €100,000 with 35% down - break-even: €647/month
  3. €100,000 with 30% down - break-even: €678/month
```

## Use Case: Stress Testing with Profiles

Create profiles for different scenarios to stress-test your investment.

### 1. Create Profiles

```bash
# Conservative profile (higher rates, costs)
mortgage-cli profile create conservative -d "Higher rates and costs"

# Optimistic profile (lower rates)
mortgage-cli profile create optimistic -d "Best case scenario"
```

### 2. Edit the Profiles

Edit `~/.config/mortgage-cli/profiles/conservative.yaml`:

```yaml
name: conservative
description: Higher rates and costs

mortgage:
  interest_rate: 0.05      # 5% instead of 4%
  insurance_rate: 0.004
  duration_years: 20
  default_down_payment: 0.2

monthly_costs:
  property_tax: 120        # Higher tax
  insurance: 40
  maintenance: 80          # Larger reserve
  management: 0
```

Edit `~/.config/mortgage-cli/profiles/optimistic.yaml`:

```yaml
name: optimistic
description: Best case scenario

mortgage:
  interest_rate: 0.035     # 3.5%
  insurance_rate: 0.003    # Lower insurance
  duration_years: 25       # Longer term
  default_down_payment: 0.2

monthly_costs:
  property_tax: 80
  insurance: 25
  maintenance: 40
  management: 0
```

### 3. Compare Profiles

```bash
mortgage-cli profile compare --price 150000 --rent 900 --profiles optimistic,default,conservative
```

```
Profile Comparison - €150,000 @ €900/month
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Profile       ┃ Break-even Rent ┃ Cash-on-Cash  ┃ Verdict  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ optimistic    │ €780/month      │ 4.2%          │ GREEN    │
│ default       │ €885/month      │ 0.5%          │ GREEN    │
│ conservative  │ €990/month      │ -3.1%         │ YELLOW   │
└───────────────┴─────────────────┴───────────────┴──────────┘
```

### 4. Interpretation

| Scenario | Break-even | Assessment |
|----------|------------|------------|
| Optimistic | €780 | Comfortable margin, good investment |
| Default | €885 | Viable, thin margins |
| Conservative | €990 | Barely viable, negative cash flow |

**Risk Assessment**: This property works under normal assumptions but becomes marginal if interest rates rise or costs increase. Consider negotiating a lower price or finding a property with better fundamentals.

## Use Case: Budget Optimization

You have exactly €40,000 to invest. Find the maximum property price.

### Check Budget Constraints

```bash
mortgage-cli matrix --price-min 120000 --price-max 180000 --price-step 10000 --output json | grep within_budget
```

Or visually check each price point:

```bash
for price in 120000 130000 140000 150000 160000; do
  echo "=== €$price ==="
  mortgage-cli analyze --price $price --rent 900 --output summary | grep -A1 "upfront"
done
```

### Results

| Price | Upfront Costs | Within €40k Budget? |
|-------|---------------|---------------------|
| €120,000 | €28,300 | Yes |
| €130,000 | €30,450 | Yes |
| €140,000 | €32,600 | Yes |
| €150,000 | €34,750 | Yes |
| €160,000 | €36,900 | Yes |
| €170,000 | €39,050 | Yes |
| €180,000 | €41,200 | No |

**Maximum price within budget**: ~€175,000 with 20% down.

## Exporting for Further Analysis

### Export Matrix to CSV

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --output csv > matrix.csv
```

Open in Excel or Google Sheets for custom analysis.

### Export to JSON for Programming

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --output json > matrix.json
```

Use with Python, JavaScript, or other tools for custom visualizations.
