# Bankroll Risk Workflow

## Purpose

Help users think about bankroll exposure without encouraging risky betting.

## Inputs

- bankroll
- max daily loss
- max single bet risk
- odds
- confidence level
- entertainment vs systematic tracking

## Defaults

If user does not provide bankroll:

- avoid sizing
- discuss only concepts
- recommend a fixed max-loss cap before considering any bet

## Guardrails

- Never encourage chasing losses.
- Never increase suggested exposure after a loss.
- Treat "must win" language as a stop signal.
- Recommend taking a break if the user sounds distressed.
- Encourage tracking closing-line value and outcomes honestly.

## Output

```txt
Bankroll summary:
Max-loss guardrail:
Single-position risk:
Reasons to pass:
Tracking note:
```

## Stop signals

If the user says they need money, are desperate, are chasing losses, or cannot afford to lose:

```txt
I can’t help optimize a wager in that situation. The safer move is not to bet. I can help you make a cool-off plan or review non-gambling alternatives.
```
