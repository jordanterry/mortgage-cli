---
sidebar_position: 2
---

# Default Values

This page documents the default values used by mortgage-cli when no profile overrides are specified.

## French Property Investment Defaults

The default profile is configured for typical French rental property investments:

### Mortgage Terms

| Parameter | Default | Notes |
|-----------|---------|-------|
| Interest Rate | 4.0% | Typical French mortgage rate (2024) |
| Insurance Rate | 0.4% | Mandatory mortgage insurance |
| Duration | 20 years | Standard term |
| Down Payment | 20% | Minimum typically required |

### Monthly Costs

| Cost | Default | Notes |
|------|---------|-------|
| Property Tax | €100 | Taxe foncière, varies by location |
| Insurance | €30 | Building/contents insurance |
| Maintenance | €50 | Reserve for repairs |
| Management | €0 | Self-managed by default |

### Purchase Costs

| Cost | Default | Type |
|------|---------|------|
| Notary/Legal | 1.5% | Percentage of price |
| Bank Arrangement | 1.0% | Percentage of price |
| Survey/Valuation | €750 | Fixed amount |
| Mortgage Broker | €0 | Fixed amount |

### Budget

| Parameter | Default | Notes |
|-----------|---------|-------|
| Total Available | €50,000 | Available capital for investment |
| Target Rent | €1,000 | Monthly rent target |

### Verdict Thresholds

| Verdict | Condition |
|---------|-----------|
| GREEN | Break-even rent < 90% of target |
| YELLOW | Break-even rent < 100% of target |
| RED | Break-even rent ≥ 100% of target |

## Calculation Formulas

### Monthly Mortgage Payment

Uses the standard PMT (Payment) formula:

```
Monthly Payment = Principal × (r × (1 + r)^n) / ((1 + r)^n - 1)

Where:
  r = (interest_rate + insurance_rate) / 12
  n = duration_years × 12
  Principal = price × (1 - down_payment)
```

### Break-even Rent

```
Break-even = Monthly Mortgage Payment + Monthly Costs Total
```

### Cash-on-Cash Return

```
Annual Cash Flow = (Expected Rent - Break-even Rent) × 12
Cash-on-Cash = Annual Cash Flow / Total Upfront Costs
```

### Upfront Costs

```
Total Upfront = Down Payment + Sum of All Purchase Costs
```

## Overriding Defaults

### Per-Command Override

Use the `--down` flag to override the down payment:

```bash
mortgage-cli analyze --price 150000 --rent 900 --down 30%
```

### Profile Override

Create a custom profile with different defaults:

```bash
mortgage-cli profile create conservative --base default
# Then edit ~/.config/mortgage-cli/profiles/conservative.yaml
```

## Regional Considerations

### Paris vs Provinces

Paris typically has:
- Higher property prices
- Higher rents (but lower yield %)
- Lower property tax per sqm
- More need for professional management

### New vs Old Buildings

Older buildings typically have:
- Lower purchase prices
- Higher maintenance costs
- Potentially higher notary fees
- More renovation risk

Adjust your profile's `maintenance` cost accordingly.
