---
type: operator-dashboard
status: active
updated: 2026-05-11
---
# 🛠️ Operator Dashboard

> **Technical Surface**: Build Pipeline → Sovereign Cloud → System Health → Receipt Discipline.

## 🚀 Build Pipeline Status
| Target | Version | Status | Blocker / Latest Receipt | Action |
| :--- | :--- | :--- | :--- | :--- |
| **iOS** | Build 53 | 🟡 Running | Bundled-model archive verification | Verify TestFlight |
| **macOS** | Build 6 | 🔴 Blocked | Invalid Apple Development cert / Limit | Repair Certs |

---

## ☁️ Sovereign Cloud (VPS)
**Node**: `187.77.223.224` | **Status**: `ONLINE`

### 🔌 Active Services
- **BMO Gateway**: `Running` $\rightarrow$ [[hermes-gateway-routing]]
- **Buddy Brain**: `Running` $\rightarrow$ [[buddy-brain]]
- **Omni Buddy**: `Running` $\rightarrow$ [[omni-buddy]]
- **Money Printer V2**: `Scheduled` $\rightarrow$ [[money-printer-v2-custom]]

### 🗝️ Access & Auth
- [[04-Runbooks/VPS Agent Access|VPS Agent Access Map]]
- [[00-Private/Credentials/Alpaca|Alpaca Trading Credentials]]

---

## ⚙️ System Health & Infrastructure
- **Obsidian OS**: `Operational` $\rightarrow$ [[Knowledge Vault Operating System]]
- **Agent Model**: `Gemma-4-31B-Cloud` $\rightarrow$ `Status: Nominal`
- **Infrastructure Index**: [[03-Infrastructure/Infrastructure Index]]

---

## 🧾 Receipt Discipline
> **Rule**: Every release, config change, or deployment must leave a receipt.
> **Format**: `Path` $\rightarrow$ `Command` $\rightarrow$ `Exit Status` $\rightarrow$ `Verification`.

- **Recent Receipts**:
	- [[Build 53 TestFlight Failure Receipt]]
	- [[VPS Agent Access Map]]
- **Receipt Storage**: [[01-Dashboard/Activity Log/Activity Index]]

---
[[01-Dashboard/Live Command Center|⬅️ Return to Hub]]
