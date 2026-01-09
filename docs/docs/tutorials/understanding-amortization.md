---
sidebar_position: 4
---

# Understanding Your Mortgage Over Time

**Difficulty**: Intermediate

In this tutorial, you'll learn how to use amortization schedules to understand how your mortgage payments work over time. This is essential for planning renovations, refinancing decisions, or understanding your equity position.

## What You'll Learn

- How to generate and read amortization schedules
- Understanding principal vs interest payments
- Finding out how much equity you'll have at any point
- Planning for the future with payment breakdowns

## Prerequisites

- Completed [Evaluating Your First Property](/tutorials/first-property)
- Basic understanding of how mortgages work

## The Scenario

You've decided to purchase the property from our first tutorial:

| Detail | Value |
|--------|-------|
| **Price** | €145,000 |
| **Down Payment** | 25% (€36,250) |
| **Loan Amount** | €108,750 |
| **Interest Rate** | 4.0% + 0.4% insurance |
| **Term** | 20 years |

You want to understand:
- How much of your payment goes to interest vs principal?
- How much equity will you have in 5 years?
- When will you own more than you owe?

---

## Step 1: Generate a Yearly Schedule

Let's see how your mortgage breaks down year by year:

```bash
mortgage-cli amortize --price 145000 --down 25%
```

```
Amortization Schedule
Principal: €108,750 | Rate: 4.4% | Term: 20 years | Payment: €680/month
┏━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Year  ┃ Payment     ┃ Principal  ┃ Interest  ┃ Balance      ┃
┡━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1     │ €8,160      │ €3,461     │ €4,699    │ €105,289     │
│ 2     │ €8,160      │ €3,617     │ €4,543    │ €101,672     │
│ 3     │ €8,160      │ €3,780     │ €4,380    │ €97,892      │
│ 4     │ €8,160      │ €3,951     │ €4,209    │ €93,941      │
│ 5     │ €8,160      │ €4,129     │ €4,031    │ €89,812      │
└───────┴─────────────┴────────────┴───────────┴──────────────┘
Total Paid: €40,800 | Total Interest: €21,861 | Principal Paid: €18,939
```

## Step 2: Understanding the Numbers

Let's break down what's happening in Year 1:

| Component | Amount | Percentage |
|-----------|--------|------------|
| Total Payment | €8,160 | 100% |
| → Principal | €3,461 | 42% |
| → Interest | €4,699 | 58% |

In the first year, more than half your payment goes to interest! But watch how this changes over time.

### The Crossover Point

Look at Year 5:
- Principal: €4,129 (51%)
- Interest: €4,031 (49%)

By Year 5, you're finally paying more principal than interest. This is the "crossover point."

## Step 3: See More Detail with Monthly View

For a closer look at the first year:

```bash
mortgage-cli amortize --price 145000 --down 25% --years 1 --frequency monthly
```

```
Amortization Schedule (Monthly)
┏━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Month  ┃ Payment  ┃ Principal ┃ Interest  ┃ Balance      ┃
┡━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1      │ €680     │ €281      │ €399      │ €108,469     │
│ 2      │ €680     │ €282      │ €398      │ €108,187     │
│ 3      │ €680     │ €283      │ €397      │ €107,904     │
│ 4      │ €680     │ €284      │ €396      │ €107,620     │
│ 5      │ €680     │ €285      │ €395      │ €107,335     │
│ 6      │ €680     │ €286      │ €394      │ €107,049     │
│ 7      │ €680     │ €287      │ €393      │ €106,762     │
│ 8      │ €680     │ €288      │ €392      │ €106,474     │
│ 9      │ €680     │ €290      │ €390      │ €106,184     │
│ 10     │ €680     │ €291      │ €389      │ €105,893     │
│ 11     │ €680     │ €292      │ €388      │ €105,601     │
│ 12     │ €680     │ €293      │ €387      │ €105,308     │
└────────┴──────────┴───────────┴───────────┴──────────────┘
```

Notice how:
- Payment stays constant at €680
- Principal portion slowly increases (€281 → €293)
- Interest portion slowly decreases (€399 → €387)
- Balance steadily drops

## Step 4: Calculate Your Equity Position

Your equity is what you actually own:

```
Equity = Property Value - Remaining Loan Balance
```

After 5 years with a €145,000 property:

| Component | Value |
|-----------|-------|
| Property Value | €145,000 |
| Original Loan | €108,750 |
| Remaining Balance (Year 5) | €89,812 |
| **Equity** | **€55,188** |

You started with €36,250 equity (your down payment). After 5 years, you have €55,188 - an increase of €18,938 just from loan paydown.

:::tip
This doesn't include property appreciation! If the property increased 2% per year, it would be worth ~€160,000 after 5 years, giving you ~€70,000 in equity.
:::

## Step 5: View the Full Picture

Let's see all 20 years:

```bash
mortgage-cli amortize --price 145000 --down 25% --years 20
```

```
Amortization Schedule
Principal: €108,750 | Rate: 4.4% | Term: 20 years | Payment: €680/month
┏━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Year  ┃ Payment     ┃ Principal  ┃ Interest  ┃ Balance      ┃
┡━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1     │ €8,160      │ €3,461     │ €4,699    │ €105,289     │
│ 2     │ €8,160      │ €3,617     │ €4,543    │ €101,672     │
│ 3     │ €8,160      │ €3,780     │ €4,380    │ €97,892      │
│ 4     │ €8,160      │ €3,951     │ €4,209    │ €93,941      │
│ 5     │ €8,160      │ €4,129     │ €4,031    │ €89,812      │
│ 6     │ €8,160      │ €4,315     │ €3,845    │ €85,497      │
│ 7     │ €8,160      │ €4,509     │ €3,651    │ €80,988      │
│ 8     │ €8,160      │ €4,712     │ €3,448    │ €76,276      │
│ 9     │ €8,160      │ €4,924     │ €3,236    │ €71,352      │
│ 10    │ €8,160      │ €5,145     │ €3,015    │ €66,207      │
│ 11    │ €8,160      │ €5,377     │ €2,783    │ €60,830      │
│ 12    │ €8,160      │ €5,619     │ €2,541    │ €55,211      │
│ 13    │ €8,160      │ €5,871     │ €2,289    │ €49,340      │
│ 14    │ €8,160      │ €6,135     │ €2,025    │ €43,205      │
│ 15    │ €8,160      │ €6,411     │ €1,749    │ €36,794      │
│ 16    │ €8,160      │ €6,699     │ €1,461    │ €30,095      │
│ 17    │ €8,160      │ €7,000     │ €1,160    │ €23,095      │
│ 18    │ €8,160      │ €7,315     │ €845      │ €15,780      │
│ 19    │ €8,160      │ €7,644     │ €516      │ €8,136       │
│ 20    │ €8,160      │ €8,136     │ €174      │ €0           │
└───────┴─────────────┴────────────┴───────────┴──────────────┘
Total Paid: €163,200 | Total Interest: €54,450 | Principal Paid: €108,750
```

### Key Insights

**Total Cost of the Loan:**
- Principal borrowed: €108,750
- Total interest paid: €54,450
- Total cost: €163,200

You'll pay about 50% extra in interest over 20 years.

**Equity Building Over Time:**

| Year | Balance | Equity | % Owned |
|------|---------|--------|---------|
| 0 | €108,750 | €36,250 | 25% |
| 5 | €89,812 | €55,188 | 38% |
| 10 | €66,207 | €78,793 | 54% |
| 15 | €36,794 | €108,206 | 75% |
| 20 | €0 | €145,000 | 100% |

By Year 10, you own more than you owe!

## Step 6: Export for Financial Planning

Save the full schedule for your records:

```bash
mortgage-cli amortize --price 145000 --down 25% --years 20 --output csv > mortgage-schedule.csv
```

Open this in Excel or Google Sheets to:
- Create charts of equity growth
- Calculate scenarios with extra payments
- Plan refinancing timing

## Step 7: Compare Different Terms

What if you got a 25-year mortgage instead of 20?

First, create a profile with a longer term:

```bash
mortgage-cli profile create term-25 --description "25-year mortgage"
```

Edit `~/.config/mortgage-cli/profiles/term-25.yaml` to set `duration_years: 25`, then:

```bash
mortgage-cli amortize --price 145000 --down 25% --years 10 --profile term-25
```

### Comparison: 20 vs 25 Year Term

| Metric | 20-Year | 25-Year |
|--------|---------|---------|
| Monthly Payment | €680 | €594 |
| Total Interest | €54,450 | €69,450 |
| Balance at Year 5 | €89,812 | €95,234 |
| Balance at Year 10 | €66,207 | €78,124 |

Trade-off:
- 25-year: Lower monthly payment (€86 less)
- 20-year: €15,000 less interest over life of loan

---

## What You've Learned

In this tutorial, you've learned how to:

- ✅ Generate amortization schedules at different frequencies
- ✅ Understand the principal/interest split
- ✅ Calculate your equity position at any point
- ✅ Find the crossover point where principal exceeds interest
- ✅ Compare different loan terms

## Try It Yourself

1. **Extra payments**: If you paid €100 extra per month, how much faster would you pay off the loan? (Hint: recalculate with a higher down payment to simulate)

2. **Refinancing decision**: At Year 7, you can refinance at 3.5%. Generate schedules for both scenarios and compare total remaining interest.

3. **Investment property**: Compare two properties - €145,000 at 25% down vs €180,000 at 20% down. Which builds equity faster?

## Key Takeaways

- **Early years**: Most of your payment goes to interest
- **Middle years**: The crossover point where you start building equity faster
- **Later years**: Most of your payment goes to principal
- **Longer terms**: Lower payments but significantly more total interest
- **Your equity**: Grows slowly at first, then accelerates

Understanding amortization helps you make smarter decisions about:
- When to refinance
- Whether to make extra payments
- How long to hold a property
- When you'll have enough equity for your next investment
