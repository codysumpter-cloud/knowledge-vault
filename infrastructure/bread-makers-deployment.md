# Bread Makers Deployment Guide

## Overview
The "Bread Makers" suite consists of `TradingAgents` and `Money Printer v2`, orchestrated under a central directory to maintain isolation and ease of management.

## Architecture
- **Root Directory:** `~/bread-makers`
- **Project Structure:**
  - `~/bread-makers/TradingAgents/` (GitHub: TradingAgents/TradingAgents)
  - `~/bread-makers/money-printer-v2/` (GitHub: MoneyPrinterV2/MoneyPrinterV2)

## Setup Lessons & Pitfalls

### Python Versioning
- **Requirement:** `TradingAgents` explicitly requested Python 3.13.
- **Constraint:** The environment provided Python 3.12.
- **Resolution:** Verified that Python 3.12 is sufficient for the current dependencies. Created the virtual environment using 3.12 without regressions.
- **Lesson:** Always verify if a strict version requirement is an absolute dependency or a recommendation before spending excessive time on environment upgrades.

### Installation Flow
1. Created the orchestration root: `mkdir ~/bread-makers`.
2. Cloned repositories into the root.
3. Initialized separate virtual environments for each tool to prevent dependency conflicts.
4. Executed setup scripts. Note: `Money Printer v2` setup scripts may appear to timeout but generally complete critical installations; monitoring logs is key.

## Maintenance
To activate the environments:
- TradingAgents: `source ~/bread-makers/TradingAgents/venv/bin/activate`
- Money Printer: `source ~/bread-makers/money-printer-v2/venv/bin/activate`
