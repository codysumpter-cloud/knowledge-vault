# MoneyPrinterV2 YouTube Title Generation Infinite Loop Fix

## Problem
The `generate_metadata` function in `src/classes/YouTube.py` contained recursive logic that could cause an infinite loop when the LLM generated a title longer than 100 characters. This would cause the application to hang indefinitely during video metadata generation.

## Root Cause
When the LLM generated a title > 100 characters, the function would call itself recursively without a proper termination condition, leading to stack overflow or infinite recursion.

## Solution Implemented
Replaced the recursive approach with:
1. A retry loop with maximum 5 attempts
2. After 5 failed attempts, hard truncate the title to 100 characters
3. This ensures the function always terminates and doesn't hang the automation

## Code Changes
**File**: `src/classes/YouTube.py`
**Commit**: cf1c308

**Before** (problematic recursive version):
```python
def generate_metadata(self, niche):
    # ...
    title = self.ollama.generate(f"Generate a YouTube title about {niche}")
    if len(title) > 100:
        return self.generate_metadata(niche)  # Recursive call without limit
    # ...
```

**After** (fixed version):
```python
def generate_metadata(self, niche):
    # ...
    max_attempts = 5
    for attempt in range(max_attempts):
        title = self.ollama.generate(f"Generate a YouTube title about {niche}")
        if len(title) <= 100:
            break
        if attempt == max_attempts - 1:  # Last attempt
            title = title[:100]  # Hard truncate
    # ...
```

## Verification
- Tested with various niches that previously caused long titles
- Confirmed the function now always returns within reasonable time
- Video generation pipeline no longer hangs at metadata stage
- Applied fix pushed to fork: https://github.com/codysumpter-cloud/MoneyPrinterV2

## Prevention for Future
- Always validate LLM output length before using in UI-constrained contexts
- Use iterative approaches with bounds instead of recursion for LLM output processing
- Consider adding logging for when truncation occurs to monitor LLM behavior
