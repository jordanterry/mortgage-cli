---
sidebar_position: 4
---

# profile

Manage investment profiles for different scenarios and markets.

## Usage

```bash
mortgage-cli profile <COMMAND> [OPTIONS]
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List all available profiles |
| `show` | Display details of a specific profile |
| `create` | Create a new profile |
| `delete` | Delete a profile |
| `compare` | Compare analysis across multiple profiles |

---

## profile list

List all available profiles.

```bash
mortgage-cli profile list [OPTIONS]
```

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output` | `-o` | TEXT | `table` | Output format: table, json |

### Example

```bash
mortgage-cli profile list
```

```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name          ┃ Description                             ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ default       │ Default French rental investment profile│
│ conservative  │ Conservative estimates with buffer      │
│ paris         │ Paris property market parameters        │
└───────────────┴─────────────────────────────────────────┘
```

---

## profile show

Display all settings for a profile.

```bash
mortgage-cli profile show <NAME>
```

### Arguments

| Argument | Description |
|----------|-------------|
| `NAME` | Profile name to display |

### Example

```bash
mortgage-cli profile show default
```

```
Profile: default
Description: Default French rental investment profile

Mortgage Terms
  Interest Rate: 4.0%
  Insurance Rate: 0.40%
  Duration: 20 years
  Default Down Payment: 20%

Budget
  Total Available: €50,000
  Target Rent: €1,000/month

Monthly Costs
  Property Tax: €100
  Insurance: €30
  Maintenance: €50
  Management: €0
  Total: €180/month

Purchase Costs
  Notary/Legal: 1.5% of price
  Bank Arrangement: 1.0% of price
  Survey/Valuation: €750

Thresholds
  Green Below: 90% of target
  Yellow Below: 100% of target
```

---

## profile create

Create a new profile by copying from an existing one.

```bash
mortgage-cli profile create <NAME> [OPTIONS]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `NAME` | Name for the new profile |

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--description` | `-d` | TEXT | | Profile description |
| `--base` | `-b` | TEXT | `default` | Profile to copy settings from |

### Example

```bash
mortgage-cli profile create conservative --description "Conservative estimates" --base default
```

```
Created profile 'conservative' based on 'default'
Edit with: mortgage-cli profile edit conservative
```

### Editing Profiles

Profiles are stored as YAML files in `~/.config/mortgage-cli/profiles/`. To customize a profile, edit the YAML file directly:

```bash
# macOS/Linux
nano ~/.config/mortgage-cli/profiles/conservative.yaml

# Or use your preferred editor
code ~/.config/mortgage-cli/profiles/conservative.yaml
```

---

## profile delete

Delete a profile.

```bash
mortgage-cli profile delete <NAME> [OPTIONS]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `NAME` | Profile name to delete |

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--force` | `-f` | FLAG | | Skip confirmation prompt |

### Example

```bash
mortgage-cli profile delete old-profile
```

```
Delete profile 'old-profile'? [y/N]: y
Deleted profile 'old-profile'
```

:::note
The built-in `default` profile cannot be deleted.
:::

---

## profile compare

Compare analysis results across multiple profiles for the same property.

```bash
mortgage-cli profile compare [OPTIONS]
```

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--price` | `-p` | FLOAT | *required* | Property purchase price |
| `--rent` | `-r` | FLOAT | *required* | Expected monthly rent |
| `--profiles` | | TEXT | *required* | Comma-separated profile names |
| `--output` | `-o` | TEXT | `table` | Output format: table, json |

### Example

```bash
mortgage-cli profile compare --price 150000 --rent 900 --profiles default,conservative,optimistic
```

```
Profile Comparison - €150,000 @ €900/month
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Profile       ┃ Break-even Rent ┃ Cash-on-Cash  ┃ Verdict  ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ optimistic    │ €820/month      │ 2.8%          │ GREEN    │
│ default       │ €885/month      │ 0.5%          │ GREEN    │
│ conservative  │ €950/month      │ -1.5%         │ YELLOW   │
└───────────────┴─────────────────┴───────────────┴──────────┘
```

### Use Cases

1. **Risk Assessment**: Compare optimistic vs conservative assumptions
2. **Market Comparison**: Use different profiles for different cities
3. **Scenario Planning**: Test different interest rate environments
