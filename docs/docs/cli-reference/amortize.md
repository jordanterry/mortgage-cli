---
sidebar_position: 3
---

# amortize

Generate an amortization schedule showing how your mortgage payments break down over time.

## Usage

```bash
mortgage-cli amortize [OPTIONS]
```

## Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--price` | `-p` | FLOAT | *required* | Property purchase price |
| `--down` | `-d` | TEXT | Profile default | Down payment percentage (e.g., "20%") |
| `--years` | | INT | `5` | Number of years to show |
| `--frequency` | | TEXT | `yearly` | Display frequency: monthly, quarterly, yearly |
| `--profile` | | TEXT | `default` | Profile name to use |
| `--output` | `-o` | TEXT | `table` | Output format: table, json, csv |

## Examples

### Basic Amortization

```bash
mortgage-cli amortize --price 150000
```

Output:
```
Amortization Schedule
Principal: €120,000 | Rate: 4.5% | Term: 20 years
┏━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Year  ┃ Payment     ┃ Principal ┃ Interest  ┃ Balance      ┃
┡━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1     │ €9,119.04   │ €3,805.42 │ €5,313.62 │ €116,194.58  │
│ 2     │ €9,119.04   │ €3,979.77 │ €5,139.27 │ €112,214.81  │
│ 3     │ €9,119.04   │ €4,162.06 │ €4,956.98 │ €108,052.75  │
│ 4     │ €9,119.04   │ €4,352.63 │ €4,766.41 │ €103,700.12  │
│ 5     │ €9,119.04   │ €4,551.86 │ €4,567.18 │ €99,148.26   │
└───────┴─────────────┴───────────┴───────────┴──────────────┘
Total Paid: €45,595.20 | Total Interest: €24,446.94
```

### Monthly Breakdown

```bash
mortgage-cli amortize --price 150000 --years 1 --frequency monthly
```

```
Amortization Schedule
Principal: €120,000 | Rate: 4.5% | Term: 20 years
┏━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Month  ┃ Payment   ┃ Principal ┃ Interest  ┃ Balance      ┃
┡━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1      │ €759.92   │ €309.92   │ €450.00   │ €119,690.08  │
│ 2      │ €759.92   │ €311.08   │ €448.84   │ €119,379.00  │
│ 3      │ €759.92   │ €312.25   │ €447.67   │ €119,066.75  │
│ ...    │ ...       │ ...       │ ...       │ ...          │
│ 12     │ €759.92   │ €322.67   │ €437.25   │ €116,194.58  │
└────────┴───────────┴───────────┴───────────┴──────────────┘
```

### Custom Down Payment

```bash
mortgage-cli amortize --price 200000 --down 30%
```

### Full Term View

```bash
mortgage-cli amortize --price 150000 --years 20
```

### Quarterly View

```bash
mortgage-cli amortize --price 150000 --frequency quarterly --years 2
```

### Export to CSV

```bash
mortgage-cli amortize --price 150000 --years 20 --frequency yearly --output csv > schedule.csv
```

### JSON for Analysis

```bash
mortgage-cli amortize --price 150000 --output json
```

```json
{
  "summary": {
    "principal": 120000.0,
    "annual_rate": 0.045,
    "term_years": 20,
    "monthly_payment": 759.92
  },
  "schedule": [
    {
      "period": 1,
      "payment": 9119.04,
      "principal": 3805.42,
      "interest": 5313.62,
      "balance": 116194.58
    }
  ],
  "totals": {
    "total_paid": 45595.20,
    "total_interest": 24446.94
  }
}
```

## Understanding Amortization

### How Mortgages Work

Each payment covers:
1. **Interest**: Calculated on the remaining balance
2. **Principal**: The remainder goes toward reducing the loan

Early in the loan, most of your payment goes to interest. Over time, more goes to principal.

### Key Insights

- **Year 1**: Interest typically accounts for 50-60% of payments
- **Midpoint**: Around year 10, the split becomes roughly equal
- **Final Years**: Most of your payment reduces the principal

### Use Cases

1. **Planning**: Understand how much equity you'll build over time
2. **Refinancing**: See how much principal remains at any point
3. **Early Payoff**: Calculate interest savings from extra payments
4. **Tax Planning**: Interest payments may be tax-deductible
