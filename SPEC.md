# mortgage-cli Specification

## Overview

A command-line tool for analyzing rental property investments, calculating break-even rents, and comparing mortgage scenarios. Built to replace/complement spreadsheet-based analysis with a more portable, scriptable, and reproducible workflow.

---

## Core Functionality

### 1. Break-Even Rent Calculator

The primary calculation determines the minimum monthly rent required to cover all mortgage and property costs.

**Formula:**
```
break_even_rent = PMT(monthly_rate, months, loan_amount) + fixed_monthly_costs

where:
  monthly_rate = (interest_rate + insurance_rate) / 12
  months = loan_duration_years * 12
  loan_amount = purchase_price * (1 - down_payment_percent)
```

### 2. Additional Calculations

| Calculation | Description |
|-------------|-------------|
| **Cash-on-Cash Return** | `(annual_rent - annual_costs) / total_cash_invested * 100%` |
| **Total Cost Breakdown** | Itemized upfront costs: down payment, notary fees, bank fees, survey, etc. |
| **Amortization Schedule** | Month-by-month breakdown of principal vs interest payments |

---

## Commands

### `mortgage-cli analyze`

Analyze a single property investment.

```bash
# Full flag specification
mortgage-cli analyze \
  --price 150000 \
  --rent 900 \
  --down 20% \
  --profile default \
  --output table

# With profile defaults
mortgage-cli analyze --price 150000 --rent 900

# Interactive wizard mode
mortgage-cli analyze --interactive
```

**Required Inputs:**
- `--price`: Property purchase price
- `--rent`: Expected monthly rental income

**Optional Inputs (from profile if not specified):**
- `--down`: Down payment percentage (default: from profile)
- `--profile`: Named profile to use (default: "default")
- `--output`: Output format: `table`, `json`, `csv`, `summary` (default: table)
- `--interactive`: Launch guided wizard mode

**Output (table format with color coding):**
```
Property Analysis: €150,000 @ €900/month rent
═══════════════════════════════════════════════════════════

UPFRONT COSTS
  Down Payment (20%)      €30,000
  Notary/Legal Fees        €4,500
  Bank Arrangement Fee     €1,500
  Survey/Valuation           €400
  ─────────────────────────────────
  Total Upfront           €36,400

MONTHLY BREAKDOWN
  Mortgage Payment          €727
  Fixed Costs               €250
  ─────────────────────────────────
  Break-Even Rent           €977  [YELLOW - within target]

VIABILITY
  Expected Rent             €900
  Break-Even Rent           €977
  Monthly Shortfall         -€77  [WARNING]

  Cash-on-Cash Return      -2.5%
  Budget Status            €36,400 / €80,000 [OK]
```

**Color Coding:**
- **Green**: Break-even rent < 80% of target rent
- **Yellow**: Break-even rent 80-100% of target rent
- **Red**: Break-even rent > target rent
- **Gray/Strikethrough**: Exceeds budget

---

### `mortgage-cli matrix`

Generate a sensitivity matrix (like the spreadsheet view).

```bash
mortgage-cli matrix \
  --price-min 100000 \
  --price-max 280000 \
  --price-step 20000 \
  --down-min 10% \
  --down-max 50% \
  --down-step 5% \
  --rent 1000 \
  --output table
```

**Output:**
```
Break-Even Rent Matrix (Target: €1,000/month, Budget: €80,000)
═══════════════════════════════════════════════════════════════

         €100K   €120K   €140K   €160K   €180K   €200K
10%       €800    €910   €1020   €1130   €1240   €1350
15%       €770    €873    €977   €1081   €1185   €1289
20%       €739    €837    €935   €1032   €1130   €1228
25%       €708    €800    €892    €984   €1075   €1167
30%       €678    €763    €849    €935   €1020   €1106

Legend: [GREEN] < €800 | [YELLOW] €800-€1000 | [RED] > €1000
        [GRAY] = Exceeds €80,000 budget
```

---

### `mortgage-cli profile`

Manage configuration profiles.

```bash
# List profiles
mortgage-cli profile list

# Show profile details
mortgage-cli profile show default

# Create new profile
mortgage-cli profile create conservative

# Edit profile (opens in $EDITOR or interactive prompts)
mortgage-cli profile edit conservative

# Delete profile
mortgage-cli profile delete conservative

# Compare analysis across profiles
mortgage-cli profile compare --price 150000 --rent 900 \
  --profiles default,conservative,aggressive
```

**Profile comparison output:**
```
Profile Comparison: €150,000 @ €900/month
═══════════════════════════════════════════════════════════

                    default     conservative  aggressive
Interest Rate         4.0%           3.5%         4.5%
Duration            20 years       25 years     15 years
Down Payment           20%            30%          15%
─────────────────────────────────────────────────────────
Break-Even Rent       €977           €823       €1,156
Cash-on-Cash         -2.5%          +2.3%        -8.2%
Upfront Cost       €36,400        €51,200      €28,900
Verdict            [YELLOW]        [GREEN]        [RED]
```

---

### `mortgage-cli amortize`

Generate amortization schedule.

```bash
mortgage-cli amortize \
  --price 150000 \
  --down 20% \
  --output table \
  --years 5  # Show first 5 years only
```

**Output:**
```
Amortization Schedule: €120,000 loan @ 4.1% over 20 years
═══════════════════════════════════════════════════════════

Year  |  Principal  |  Interest  |  Balance   | Equity
──────|─────────────|────────────|────────────|────────
  1   |    €3,842   |   €4,874   |  €116,158  |  25.6%
  2   |    €4,001   |   €4,715   |  €112,157  |  27.2%
  3   |    €4,167   |   €4,549   |  €107,990  |  28.9%
  4   |    €4,340   |   €4,376   |  €103,650  |  30.9%
  5   |    €4,520   |   €4,196   |   €99,130  |  33.1%
...
```

---

## Profile Schema

Profiles are stored in `~/.config/mortgage-cli/profiles/` as YAML files.

```yaml
# ~/.config/mortgage-cli/profiles/default.yaml
name: default
description: Standard investment parameters

# Mortgage terms
mortgage:
  interest_rate: 0.04      # 4% annual
  insurance_rate: 0.001    # 0.1% annual
  duration_years: 20
  default_down_payment: 0.20  # 20%

# Budget constraints
budget:
  total_available: 80000
  target_rent: 1000

# Fixed monthly costs (ongoing)
monthly_costs:
  property_tax: 50
  insurance: 50
  maintenance: 100
  management: 50
  # total = €250/month

# Purchase costs (one-time, itemized)
purchase_costs:
  notary_legal:
    type: percentage
    value: 0.03           # 3% of purchase price
  bank_arrangement:
    type: percentage
    value: 0.01           # 1% of purchase price
  survey_valuation:
    type: fixed
    value: 400
  mortgage_broker:
    type: fixed
    value: 0              # Optional
  other:
    type: fixed
    value: 0

# Thresholds for color coding
thresholds:
  green_below: 0.80       # < 80% of target rent
  yellow_below: 1.00      # 80-100% of target rent
  # Red = > 100% of target rent
```

---

## Output Formats

### Table (default)
Colored terminal output with ASCII/Unicode tables.

### JSON
```json
{
  "property": {
    "price": 150000,
    "expected_rent": 900
  },
  "analysis": {
    "break_even_rent": 977.42,
    "cash_on_cash_return": -0.025,
    "verdict": "yellow"
  },
  "upfront_costs": {
    "down_payment": 30000,
    "notary_legal": 4500,
    "bank_arrangement": 1500,
    "survey": 400,
    "total": 36400
  },
  "monthly": {
    "mortgage_payment": 727.42,
    "fixed_costs": 250,
    "total": 977.42
  },
  "warnings": [
    "Break-even rent exceeds expected rent by €77/month"
  ]
}
```

### CSV
Standard CSV export suitable for spreadsheet import.

### Summary
Human-readable narrative format:
```
INVESTMENT SUMMARY

A €150,000 property with 20% down (€30,000) would require
€977/month in rent to break even. At the expected rent of
€900/month, this represents a monthly shortfall of €77.

Total upfront investment: €36,400 (within your €80,000 budget)
Cash-on-cash return: -2.5% (negative due to shortfall)

RECOMMENDATION: This property is marginally viable. Consider
negotiating a lower price or higher rent to improve returns.
```

---

## Validation & Warnings

The CLI provides these automatic checks:

| Check | Condition | Warning |
|-------|-----------|---------|
| **Budget exceeded** | Upfront costs > `budget.total_available` | "Total costs €X exceed budget of €Y" |
| **Negative cash flow** | Break-even > expected rent | "Monthly shortfall of €X" |
| **Affordability** | Break-even > 150% of target | "Break-even rent may be unrealistic for this market" |

---

## Installation

```bash
# Homebrew (primary distribution)
brew tap jordanterry/mortgage-cli
brew install mortgage-cli

# First run - creates default profile
mortgage-cli profile create default --interactive
```

---

## Configuration Files

```
~/.config/mortgage-cli/
├── config.yaml           # Global settings
└── profiles/
    ├── default.yaml
    ├── conservative.yaml
    └── aggressive.yaml
```

**Global config:**
```yaml
# ~/.config/mortgage-cli/config.yaml
default_profile: default
default_output: table
currency: EUR
currency_symbol: €
locale: en_GB
```

---

## Future Enhancements (Out of Scope for v1)

- [ ] Spreadsheet version tracking and migration
- [ ] Property batch analysis from CSV/JSON
- [ ] Market rental data integration
- [ ] TUI dashboard with live updates
- [ ] Multiple currency support
- [ ] Tax calculation integration
- [ ] Investment portfolio tracking

---

## Technical Requirements

- **Language**: Python 3.9+
- **Key Dependencies**:
  - `typer` - CLI framework
  - `rich` - Terminal formatting and tables
  - `pydantic` - Profile schema validation
  - `numpy-financial` - PMT and financial calculations
  - `pyyaml` - Profile storage
- **Distribution**: Homebrew formula
- **Testing**: pytest with property-based testing for calculations

---

## Example Session

```bash
$ mortgage-cli profile list
NAME           DESCRIPTION
default        Standard investment parameters
conservative   Lower risk, higher down payment

$ mortgage-cli analyze --price 180000 --rent 1100
Property Analysis: €180,000 @ €1,100/month rent
═══════════════════════════════════════════════

UPFRONT COSTS
  Down Payment (20%)      €36,000
  Notary/Legal Fees        €5,400
  Bank Arrangement Fee     €1,800
  Survey/Valuation           €400
  ─────────────────────────────────
  Total Upfront           €43,600

MONTHLY BREAKDOWN
  Mortgage Payment          €880
  Fixed Costs               €250
  ─────────────────────────────────
  Break-Even Rent         €1,130  [YELLOW]

Expected: €1,100 | Break-Even: €1,130 | Shortfall: €30/month

$ mortgage-cli analyze --price 180000 --rent 1100 --output json | jq .analysis
{
  "break_even_rent": 1130.22,
  "cash_on_cash_return": -0.008,
  "verdict": "yellow"
}
```
