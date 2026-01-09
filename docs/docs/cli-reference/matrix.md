---
sidebar_position: 2
---

# matrix

Generate a sensitivity matrix comparing break-even rent across different price and down payment combinations.

## Usage

```bash
mortgage-cli matrix [OPTIONS]
```

## Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--price-min` | | FLOAT | *required* | Minimum property price |
| `--price-max` | | FLOAT | *required* | Maximum property price |
| `--price-step` | | FLOAT | `20000` | Price increment |
| `--down-min` | | TEXT | `10%` | Minimum down payment percentage |
| `--down-max` | | TEXT | `50%` | Maximum down payment percentage |
| `--down-step` | | TEXT | `5%` | Down payment increment |
| `--rent` | `-r` | FLOAT | Profile target | Target rent for color coding |
| `--profile` | | TEXT | `default` | Profile name to use |
| `--output` | `-o` | TEXT | `table` | Output format: table, json, csv, summary |

## Examples

### Basic Matrix

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000
```

Output:
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
│ 40%       │ €616      │ €690      │ €763      │ €836      │ €909      │ €982     │
│ 45%       │ €586      │ €653      │ €720      │ €787      │ €854      │ €921     │
│ 50%       │ €555      │ €616      │ €677      │ €738      │ €798      │ €859     │
└───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘
Legend: GREEN = Good (<90% target) | YELLOW = Marginal (90-100%) | RED = Poor (>100%)
```

### With Custom Target Rent

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --rent 1200
```

### Smaller Price Steps

```bash
mortgage-cli matrix --price-min 140000 --price-max 160000 --price-step 5000
```

### Custom Down Payment Range

```bash
mortgage-cli matrix --price-min 100000 --price-max 150000 --down-min 20% --down-max 40% --down-step 10%
```

### JSON Output for Processing

```bash
mortgage-cli matrix --price-min 100000 --price-max 150000 --output json > matrix.json
```

```json
{
  "target_rent": 1000.0,
  "prices": [100000, 120000, 140000],
  "down_payments": [0.1, 0.15, 0.2],
  "matrix": [
    [
      {"price": 100000, "down_payment_percent": 0.1, "break_even_rent": 800.14, "verdict": "green"},
      {"price": 120000, "down_payment_percent": 0.1, "break_even_rent": 910.16, "verdict": "yellow"},
      {"price": 140000, "down_payment_percent": 0.1, "break_even_rent": 1020.19, "verdict": "red"}
    ]
  ]
}
```

### Summary Output

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --output summary
```

```
SENSITIVITY ANALYSIS SUMMARY
==================================================

Analyzed 54 price/down-payment combinations:
  - 18 good opportunities (green)
  - 12 marginal opportunities (yellow)
  - 24 poor opportunities (red)

Top opportunities (lowest break-even rent):
  1. €100,000 with 50% down - break-even: €555/month
  2. €100,000 with 45% down - break-even: €586/month
  3. €100,000 with 40% down - break-even: €616/month
```

## Understanding the Matrix

### Color Coding

The matrix uses color coding based on your profile's thresholds:

- **GREEN**: Break-even rent is below 90% of target rent (good investment)
- **YELLOW**: Break-even rent is 90-100% of target rent (marginal)
- **RED**: Break-even rent exceeds target rent (poor investment)

### Reading the Matrix

1. **Rows** represent down payment percentages (higher = more cash upfront)
2. **Columns** represent property prices
3. **Cells** show the break-even rent for that combination

### Tips

- Look for green cells that match your available capital
- Higher down payments always reduce break-even rent
- Use the summary output to quickly identify the best opportunities
