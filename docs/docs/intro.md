---
slug: /
sidebar_position: 1
---

# Getting Started

**mortgage-cli** is a command-line tool for analyzing rental property investments. It helps you calculate break-even rent, evaluate investment viability, and compare different financing scenarios.

## Features

- **Break-even Analysis**: Calculate the minimum rent needed to cover all costs
- **Sensitivity Matrix**: Compare multiple price/down-payment combinations at once
- **Amortization Schedules**: View detailed payment breakdowns over time
- **Profile Management**: Save and reuse different investment parameters
- **Multiple Output Formats**: Table, JSON, CSV, or narrative summary

## Installation

### Using pip

```bash
pip install mortgage-cli
```

### From Source

```bash
git clone https://github.com/jordanterry/mortgage-cli.git
cd mortgage-cli
pip install -e .
```

## Quick Start

### Analyze a Property

```bash
mortgage-cli analyze --price 150000 --rent 900
```

This calculates the break-even rent for a €150,000 property with an expected rent of €900/month.

### Example Output

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

### Generate a Sensitivity Matrix

```bash
mortgage-cli matrix --price-min 100000 --price-max 200000 --rent 1000
```

This shows break-even rent for different price/down-payment combinations.

## Key Concepts

### Break-even Rent

The minimum monthly rent needed to cover:
- Mortgage payment (principal + interest + insurance)
- Property tax
- Building insurance
- Maintenance reserve
- Management fees

### Verdict Colors

| Color  | Meaning |
|--------|---------|
| GREEN  | Break-even rent is below 90% of target - good investment |
| YELLOW | Break-even rent is 90-100% of target - marginal |
| RED    | Break-even rent exceeds target - poor investment |

### Profiles

Profiles store your investment parameters (interest rates, costs, thresholds). The built-in `default` profile uses typical French property investment values.

## Next Steps

### Tutorials

New to mortgage-cli? Start with these step-by-step tutorials:

1. [Evaluating Your First Property](/tutorials/first-property) - Learn the basics with a real scenario
2. [Finding Your Price Range](/tutorials/finding-price-range) - Use the sensitivity matrix to explore options
3. [Stress Testing Your Investment](/tutorials/stress-testing) - Create profiles to evaluate risk
4. [Understanding Amortization](/tutorials/understanding-amortization) - See how your mortgage works over time

### Reference

- [CLI Reference](/cli-reference/analyze) - Detailed command documentation
- [Configuration](/configuration/profiles) - Customize profiles for your needs
- [Examples](/examples/basic-analysis) - Quick examples and recipes
