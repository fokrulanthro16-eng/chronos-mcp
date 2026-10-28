# Security Policy & Vulnerability Disclosure

ChronosMCP (VeriGraph AI) is designed to operate within mission-critical FinTech, healthcare, and enterprise software delivery environments. Security, tenant isolation, and cryptographic integrity are foundational to every layer of our platform.

---

## 1. Security Architecture & Threat Model

### Atlassian Forge Native Sandbox
- **Zero External Egress:** ChronosMCP runs strictly inside the Atlassian Forge managed serverless runtime (`nodejs22.x`). No external database, third-party analytics, or unauthorized telemetry endpoints are queried.
- **Tenant Isolation:** All storage calls utilize `@forge/kvs`, ensuring strict tenant-level isolation enforced by AWS and Atlassian ecosystem boundaries. One customer tenant can never access or read keys from another tenant.
- **Least-Privilege Scopes:**
  - `storage:app`: Required to store audit ledgers and blast radius simulation cache.
  - `read:jira-work` & `write:jira-work`: Required to inspect issue links, create mitigation subtasks, and add alignment alerts.
  - `read:jira-user`: Required to resolve issue assignees and approvers for cryptographic audit receipts.
  - `read:confluence-content.all` & `read:confluence-space.summary`: Required to audit regulatory compliance policies.

---

## 2. Cryptographic Release Ledger Security
- All release proofs are generated using the standard **FIPS-compliant SHA-256** cryptographic hash algorithm.
- Payloads are serialized using deterministic canonical sorting, ensuring reproducible Merkle hash calculation.
- Any unauthorized post-approval modification to ticket summaries, linked issues, or policy checksums invalidates the cryptographic receipt.

---

## 3. Reporting a Vulnerability

If you discover a potential security vulnerability within ChronosMCP, please follow responsible disclosure guidelines:

1. **Email:** Report findings directly to `fokrulanthro16@gmail.com` with the subject line: `[SECURITY] ChronosMCP Vulnerability Report`.
2. **Details:** Provide reproduction steps, affected versions, and sample payloads.
3. **Response SLA:** We acknowledge all security reports within 24 hours and provide an evaluation within 72 hours.
4. **Public Disclosure:** Please refrain from publicly disclosing issues until a remediation patch has been verified and deployed.
