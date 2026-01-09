---
sidebar_position: 1
---

# analyze

Analyze a single property investment.

## Usage

```bash
mortgage-cli analyze [OPTIONS]
```

## Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--price` | `-p` | FLOAT | *required* | Property purchase price |
| `--rent` | `-r` | FLOAT | *required* | Expected monthly rental income |
| `--down` | `-d` | TEXT | Profile default | Down payment percentage (e.g., "20%") |
| `--profile` | | TEXT | `default` | Profile name to use for calculations |
| `--output` | `-o` | TEXT | `table` | Output format: table, json, csv, summary |

## Examples

### Basic Analysis

```bash
mortgage-cli analyze --price 150000 --rent 900
```

Output:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Metric                   ┃ Value         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Property Price           │ €150,000      │
│ Down Payment             │ 20% (€30,000) │
│ Break-even Rent          │ €885/month    │
│ Expected Rent            │ €900/month    │
│ Monthly Surplus          │ €15           │
│ Cash-on-Cash Return      │ 0.5%          │
│ Verdict                  │ GREEN         │
└──────────────────────────┴───────────────┘
```

### Custom Down Payment

```bash
mortgage-cli analyze --price 200000 --rent 1200 --down 30%
```

### JSON Output

```bash
mortgage-cli analyze --price 150000 --rent 900 --output json
```

```json
{
  "analysis": {
    "property_price": 150000.0,
    "down_payment_percent": 0.2,
    "break_even_rent": 884.61,
    "expected_rent": 900.0,
    "monthly_surplus_shortfall": 15.39,
    "cash_on_cash_return": 0.005,
    "verdict": "green",
    "within_budget": true
  },
  "upfront_costs": {
    "down_payment": 30000.0,
    "notary_legal": 2250.0,
    "bank_arrangement": 1500.0,
    "survey_valuation": 750.0,
    "mortgage_broker": 0.0,
    "other": 0.0,
    "total": 34500.0
  }
}
```

### Using a Different Profile

```bash
mortgage-cli analyze --price 150000 --rent 900 --profile conservative
```

### Narrative Summary

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

## Output Fields

### Analysis Section

| Field | Description |
|-------|-------------|
| Property Price | The purchase price being analyzed |
| Down Payment | Percentage and absolute amount |
| Break-even Rent | Minimum rent to cover all costs |
| Expected Rent | The rent you expect to achieve |
| Monthly Surplus/Shortfall | Difference between expected and break-even |
| Cash-on-Cash Return | Annual cash flow / total investment |
| Verdict | GREEN, YELLOW, or RED assessment |

### Upfront Costs Section

| Field | Description |
|-------|-------------|
| Down Payment | Cash put down on purchase |
| Notary/Legal | Legal fees (typically % of price) |
| Bank Arrangement | Mortgage setup fees |
| Survey/Valuation | Property inspection costs |
| Total | Sum of all upfront costs |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid profile, invalid input) |
