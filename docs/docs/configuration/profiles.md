---
sidebar_position: 1
---

# Profiles

Profiles allow you to save and reuse different sets of investment parameters. This is useful for:

- Different property markets (Paris vs provinces)
- Different risk tolerances (conservative vs optimistic)
- Different loan scenarios (varying interest rates)

## Profile Location

Profiles are stored as YAML files in:

```
~/.config/mortgage-cli/profiles/
```

On macOS/Linux, this expands to `/Users/yourname/.config/mortgage-cli/profiles/`.

## Default Profile

The built-in `default` profile contains typical French rental investment parameters:

```yaml
name: default
description: Default French rental investment profile

mortgage:
  interest_rate: 0.04      # 4.0% annual interest
  insurance_rate: 0.004    # 0.4% mortgage insurance
  duration_years: 20       # 20-year term
  default_down_payment: 0.2  # 20% down payment

budget:
  total_available: 50000   # €50,000 available capital
  target_rent: 1000        # €1,000/month target rent

monthly_costs:
  property_tax: 100        # €100/month property tax
  insurance: 30            # €30/month building insurance
  maintenance: 50          # €50/month maintenance reserve
  management: 0            # €0/month (self-managed)

purchase_costs:
  notary_legal:
    type: percentage
    value: 0.015           # 1.5% of purchase price
  bank_arrangement:
    type: percentage
    value: 0.01            # 1.0% of purchase price
  survey_valuation:
    type: fixed
    value: 750             # €750 flat fee
  mortgage_broker:
    type: fixed
    value: 0
  other:
    type: fixed
    value: 0

thresholds:
  green_below: 0.9         # Green if break-even < 90% of target
  yellow_below: 1.0        # Yellow if break-even < 100% of target
```

## Creating a Profile

### Using the CLI

```bash
mortgage-cli profile create myprofile --description "My custom profile" --base default
```

This creates a copy of the `default` profile that you can customize.

### Manual Creation

Create a new YAML file in the profiles directory:

```bash
touch ~/.config/mortgage-cli/profiles/myprofile.yaml
```

Then edit it with your preferred settings.

## Editing a Profile

Open the profile in your text editor:

```bash
# Using nano
nano ~/.config/mortgage-cli/profiles/myprofile.yaml

# Using VS Code
code ~/.config/mortgage-cli/profiles/myprofile.yaml
```

### Common Customizations

#### Higher Interest Rate (Conservative)

```yaml
mortgage:
  interest_rate: 0.05      # 5.0% instead of 4.0%
```

#### Higher Monthly Costs

```yaml
monthly_costs:
  property_tax: 150        # Higher property tax
  insurance: 50            # Higher insurance
  maintenance: 100         # Larger maintenance reserve
  management: 80           # Professional management (8% of rent)
```

#### Different Thresholds

```yaml
thresholds:
  green_below: 0.85        # More conservative: green only if < 85%
  yellow_below: 0.95       # Yellow up to 95%
```

#### Paris Market Profile

```yaml
name: paris
description: Paris property market parameters

mortgage:
  interest_rate: 0.04
  insurance_rate: 0.004
  duration_years: 25       # Longer term for expensive properties
  default_down_payment: 0.25  # Higher down payment typical

budget:
  total_available: 100000  # More capital needed
  target_rent: 1500        # Higher rents in Paris

monthly_costs:
  property_tax: 80         # Lower per sqm in Paris
  insurance: 40
  maintenance: 100         # Older buildings need more
  management: 120          # Professional management common
```

## Using Profiles

### Specify Profile in Commands

```bash
# Use a specific profile
mortgage-cli analyze --price 200000 --rent 1200 --profile paris

# Use default profile (implicit)
mortgage-cli analyze --price 150000 --rent 900
```

### Compare Profiles

```bash
mortgage-cli profile compare --price 150000 --rent 900 --profiles default,conservative,paris
```

## Profile Schema Reference

### mortgage

| Field | Type | Description |
|-------|------|-------------|
| `interest_rate` | float | Annual interest rate (0.04 = 4%) |
| `insurance_rate` | float | Annual mortgage insurance rate |
| `duration_years` | int | Loan term in years |
| `default_down_payment` | float | Default down payment percentage |

### budget

| Field | Type | Description |
|-------|------|-------------|
| `total_available` | float | Total available capital (€) |
| `target_rent` | float | Target monthly rent (€) |

### monthly_costs

| Field | Type | Description |
|-------|------|-------------|
| `property_tax` | float | Monthly property tax (€) |
| `insurance` | float | Monthly building insurance (€) |
| `maintenance` | float | Monthly maintenance reserve (€) |
| `management` | float | Monthly management fees (€) |

### purchase_costs

Each cost can be `percentage` or `fixed`:

```yaml
# Percentage of purchase price
notary_legal:
  type: percentage
  value: 0.015    # 1.5%

# Fixed amount
survey_valuation:
  type: fixed
  value: 750      # €750
```

| Field | Description |
|-------|-------------|
| `notary_legal` | Notary and legal fees |
| `bank_arrangement` | Bank/mortgage setup fees |
| `survey_valuation` | Property survey/valuation |
| `mortgage_broker` | Broker fees (if applicable) |
| `other` | Any other purchase costs |

### thresholds

| Field | Type | Description |
|-------|------|-------------|
| `green_below` | float | Verdict is GREEN if break-even < this × target |
| `yellow_below` | float | Verdict is YELLOW if break-even < this × target |
