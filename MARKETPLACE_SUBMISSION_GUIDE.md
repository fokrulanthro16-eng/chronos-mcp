# ChronosMCP (VeriGraph AI) — Marketplace Submission & Distribution Guide

> **Bonus Prize Track 4:** Best Marketplace Published App ($1,500)
> **App Name:** ChronosMCP (VeriGraph AI)
> **App ID:** `84d8afae-9ec0-47fc-8212-e27f79430216`
> **App ARI:** `ari:cloud:ecosystem::app/84d8afae-9ec0-47fc-8212-e27f79430216`
> **Target Cloud Site:** `https://fokrulanthro16.atlassian.net`
> **Production Deployed Version:** `v2.1.0`

---

## 1. How to Generate the Public Installation Link (Judge Sharing)

Because ChronosMCP has already been deployed to the `production` environment via `forge deploy -e production`, you can immediately generate the public installation link:

1. Navigate to the **Atlassian Developer Console**:
   👉 [developer.atlassian.com/console/myapps/84d8afae-9ec0-47fc-8212-e27f79430216/manage/distribution](https://developer.atlassian.com/console/myapps/84d8afae-9ec0-47fc-8212-e27f79430216/manage/distribution)
2. In the **Distribution** tab:
   - Under **App distribution**, toggle the switch to **Sharing**.
   - Review and accept the Atlassian Developer Terms if prompted.
   - Click **Generate installation link** for the `production` environment.
3. Copy the generated link (e.g., `https://forge.cdn.prod.atlassian-dev.net/apps/84d8afae-9ec0-47fc-8212-e27f79430216/install?...`) and paste it into your Devpost submission form under **App Installation Link**.

---

## 2. Atlassian Marketplace Listing Metadata (Ready to Copy/Paste)

### Basic App Information
- **App Name:** `ChronosMCP: Blast-Radius & Ship Confidence`
- **Tagline (Max 100 chars):** `Causal blast-radius simulation, Rovo auto-remediation, and MCP bridge for zero-downtime shipping.`
- **Category 1:** `DevOps & CI/CD`
- **Category 2:** `Project Management & AI Tools`
- **Supported Products:** `Jira Cloud`

### Highlights (Key Selling Points)
1. **Deterministic Ship Confidence Score (0-100%):** Real-time counterfactual simulation analyzing API contract drift, database table locks, security breaches, and cross-team SLA ripple effects.
2. **Autonomous Rovo Silo Remediation:** 1-click automatic Jira subtask generation, cross-team issue linking, and automated warning comments on affected downstream consumer boards.
3. **Spec-Compliant Atlassian MCP Server:** Native JSON-RPC 2.0 WebTrigger allowing external AI IDEs (Antigravity, Cursor, Claude Desktop) to query live Teamwork Graph context.
4. **Zero-Trust SHA-256 Release Ledger:** Tamper-evident Merkle context receipts stored in Forge KVS for automated regulatory and PCI-DSS v4.0 compliance auditing.

### Detailed Marketplace Description
```markdown
### Stop shipping blind. Build with context. Ship with confidence.

Modern engineering teams ship breaking changes because critical context is trapped in silos. A backend engineer modifies an API endpoint or tokenization payload in Jira without realizing it breaks a downstream mobile pipeline or breaches an updated Confluence compliance policy.

**ChronosMCP (VeriGraph AI)** is an enterprise-grade release control plane built natively on Atlassian Forge. It connects your **Teamwork Graph**, an **Autonomous Rovo AI Agent**, an **Atlassian MCP Server**, and a **SHA-256 Release Ledger** into one unified command center inside Jira.

#### 🌟 Key Capabilities
- **Causal Blast-Radius Flight Simulator:** Visualizes upstream changes and calculates a live 0-100% Ship Confidence Score across 4 failure vectors before code reaches production.
- **Teamwork Graph Explorer:** Interactive SVG graph topology mapping source issues, downstream blockers, Confluence policies, and team approvers.
- **Rovo Auto-Remediation:** In 1 click, Rovo provisions mitigation subtasks, alerts downstream engineering owners, and elevates Ship Confidence from 38% to 98%.
- **Model Context Protocol (MCP) Bridge:** Native JSON-RPC 2.0 server exposed via Forge WebTrigger, allowing AI coding assistants (Cursor, Antigravity, Claude Desktop) to inspect live Jira context in real time.
- **Cryptographic Merkle Proofs:** SHA-256 tamper-evident receipts stored in Forge KVS for instant compliance sign-off.
```

---

## 3. Security, Privacy & Compliance Statement

- **Data Residency & Storage:** All context graphs, audit receipts, and policies are stored strictly within the customer's Atlassian tenant using native Atlassian Forge KVS (`@forge/kvs`). No external databases or unapproved egress endpoints are utilized.
- **Permission Scopes:**
  - `storage:app`: Secure, isolated tenant-level storage.
  - `read:jira-work` & `write:jira-work`: Reads issue dependencies and creates mitigation subtasks/comments.
  - `read:jira-user`: Resolves engineering team leads and approvers.
  - `read:confluence-content.all` & `read:confluence-space.summary`: Audits regulatory compliance policies.
- **Zero Lint Warnings:** Manifest and source code strictly pass `forge lint` with 0 errors and 0 warnings.
- **Runtime:** Native Node.js 22 (`nodejs22.x`) on AWS serverless infrastructure managed by Atlassian.

---

## 4. Support & Documentation URLs
- **Documentation & User Guide:** [DEVPOST_SUBMISSION.md](./DEVPOST_SUBMISSION.md)
- **Support Email:** `fokrulanthro16@gmail.com`
- **Target Demo Site:** `https://fokrulanthro16.atlassian.net`
- **Issue Tracker:** `https://fokrulanthro16.atlassian.net/browse/SCRUM`
