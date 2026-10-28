# Privacy Policy & Data Residency

**Last Updated:** October 28, 2026  
**Product:** ChronosMCP (VeriGraph AI) for Atlassian Cloud  
**Developer:** Fokrul Islam / ChronosMCP Labs

---

## 1. Data Residency & Processing Philosophy

ChronosMCP is engineered to respect enterprise privacy and comply with global data governance mandates (including GDPR, CCPA, and PCI-DSS v4.0).

- **On-Tenant Execution:** All blast-radius simulations, graph traversals, and ledger hashing occur within the customer's dedicated Atlassian Forge execution environment.
- **Zero Third-Party Storage:** We do not operate external databases, cloud servers, or log aggregators. All operational data is stored exclusively in Atlassian Forge Key-Value Storage (`@forge/kvs`).
- **No PII Tracking:** ChronosMCP processes only technical metadata required to compute release safety (e.g. Jira Issue Keys, summaries, issue link types, Confluence policy titles, and public Atlassian Account IDs of assignees). We do not collect credit card numbers, payment credentials, personal phone numbers, or residential addresses.

---

## 2. Permitted Scopes & Purpose of Use

| Scope | Operational Purpose |
| :--- | :--- |
| `storage:app` | Persisting simulation cache and SHA-256 Merkle release receipts in Forge KVS. |
| `read:jira-work` | Reading issue summaries, descriptions, dependencies, and labels to calculate blast radius. |
| `write:jira-work` | Creating automated mitigation subtasks, updating verification labels, and posting alerts. |
| `read:jira-user` | Retrieving assignee display names and account IDs for immutable audit trail attestation. |
| `read:confluence-content.all` | Checking Confluence compliance policies (e.g. PCI-DSS v4.0 Zero-Drift Mandates). |
| `read:confluence-space.summary` | Resolving spaces containing governance and architectural guidelines. |

---

## 3. Data Retention & Deletion

- Data stored in `@forge/kvs` persists only for the lifetime of the application installation.
- Uninstalling the app via `forge uninstall` or the Atlassian Site Administration Console permanently and irreversibly purges all stored KVS data and audit proofs.

---

## 4. Contact & Compliance Inquiries

For questions regarding data privacy or security compliance:  
**Contact:** `fokrulanthro16@gmail.com`  
**Atlassian Marketplace Vendor:** ChronosMCP Labs
