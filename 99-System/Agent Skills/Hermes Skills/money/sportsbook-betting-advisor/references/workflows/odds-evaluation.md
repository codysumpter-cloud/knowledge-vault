# Odds Evaluation Workflow

## Purpose

Convert a sportsbook line into a clear decision-support note.

## American odds conversion

Positive odds:

```txt
implied_probability = 100 / (odds + 100)
```

Negative odds:

```txt
implied_probability = abs(odds) / (abs(odds) + 100)
```

## Workflow

```txt
1. Identify event and market.
2. Capture offered odds.
3. Convert to implied probability.
4. Compare to user's estimated probability, if supplied.
5. Discuss uncertainty and missing data.
6. Identify reasons to pass.
7. Produce manual-only checklist.
```

## Example output

```txt
Decision-support summary:
The offered line implies roughly X% break-even probability. Your thesis needs the true probability to be meaningfully above that after accounting for uncertainty and sportsbook margin.

Risks:
- injury/news uncertainty
- model overconfidence
- market already moved
- limited sample size
- bankroll exposure

No-action case:
Pass if you cannot explain why your estimate beats the market after vig.
```

## Required warning

This is decision support, not a guarantee or instruction to wager/trade. Only risk money you can afford to lose, and confirm legality and platform eligibility in your jurisdiction.
