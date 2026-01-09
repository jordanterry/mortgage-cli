# mortgage-cli

CLI tool for analyzing rental property investments.

## Installation

```bash
pip install mortgage-cli
```

## Quick Start

```bash
# Analyze a single property
mortgage-cli analyze --price 150000 --rent 900

# Generate a sensitivity matrix
mortgage-cli matrix --price-min 100000 --price-max 300000 --rent 1000

# Manage profiles
mortgage-cli profile list
mortgage-cli profile create my-profile
```

## Features

- Break-even rent calculation
- Cash-on-cash return analysis
- Sensitivity matrix generation
- Amortization schedules
- Profile-based configuration
- Multiple output formats (table, JSON, CSV)

## License

MIT
