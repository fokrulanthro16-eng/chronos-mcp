# Technical Architecture & Systems Engineering Specification
## ChronosMCP (VeriGraph AI) — Causal Release Safety Engine

This document outlines the internal architecture, mathematical risk scoring models, graph traversal algorithms, Model Context Protocol (MCP) JSON-RPC 2.0 specifications, and cryptographic Merkle attestation mechanics of **ChronosMCP**.

---

## 1. System High-Level Topology

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Atlassian Cloud Tenant                          │
│                                                                        │
│   ┌─────────────────────┐                 ┌────────────────────────┐   │
│   │   Jira Issue View   │                 │   Confluence Spaces    │   │
│   │   SCRUM-1 (Core)    │                 │   POL-402 (PCI-DSS)    │   │
│   │   SCRUM-2 (Mobile)  │                 │   ARCH-109 (Contracts) │   │
│   └──────────┬──────────┘                 └───────────┬────────────┘   │
│              │                                        │                │
│              └───────────────────┬────────────────────┘                │
│                                  │                                     │
│                     Atlassian Teamwork Graph API                       │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      ChronosMCP Forge Application                      │
│                                                                        │
│  ┌─────────────────────────┐            ┌───────────────────────────┐  │
│  │ Custom UI Issue Panel   │            │  Rovo Autonomous Agent    │  │
│  │ React / Tailwind Bundle │            │  chronos-release-guardian │  │
│  └───────────┬─────────────┘            └─────────────┬─────────────┘  │
│              │                                        │                │
│              │        @forge/resolver Dispatcher      │                │
│              └───────────────────┬────────────────────┘                │
│                                  │                                     │
│     ┌────────────────────────────┼──────────────────────────────┐      │
│     ▼                            ▼                              ▼      │
│ ┌──────────────────────┐  ┌──────────────────────┐  ┌────────────────┐ │
│ │  Graph Engine &      │  │  SHA-256 Merkle      │  │ Atlassian MCP  │ │
│ │  Causal Simulator    │  │  Release Ledger      │  │ WebTrigger GW  │ │
│ │  (src/graphEngine)   │  │  (src/cryptoLedger)  │  │ (src/mcpServer)│ │
│ └──────────┬───────────┘  └──────────┬───────────┘  └───────┬────────┘ │
│            │                         │                      │          │
│            └─────────────────────────┼──────────────────────┘          │
│                                      ▼                                 │
│                          Atlassian KVS (@forge/kvs)                    │
└──────────────────────────────────────┬─────────────────────────────────┘
                                       │
                         Model Context Protocol (HTTP)
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      External AI Developer IDEs                        │
│                                                                        │
│      ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐      │
│      │    Cursor AI    │  │ Antigravity AI  │  │ Claude Desktop │      │
│      └─────────────────┘  └─────────────────┘  └────────────────┘      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mathematical Scoring Model: Ship Confidence Score ($S_{CS}$)

ChronosMCP avoids subjective release approval by evaluating releases using a deterministic multi-vector causal loss equation.

Let the **Ship Confidence Score** $S_{CS} \in [0, 100]$ be defined as:

$$S_{CS} = \max\left(0, 100 - \sum_{i=1}^{4} w_i \cdot V_i - \Delta_{\text{blocker}}\right)$$

Where:
- $V_1$: **API Contract Drift Vector** ($w_1 = 0.35$). Evaluates backward incompatibility, breaking type changes, or missing fallback adapters between producer and consumer schemas.
- $V_2$: **Database Migration & Lock Vector** ($w_2 = 0.20$). Assesses schema migration lock duration, table alteration scope, and indexing locks.
- $V_3$: **Regulatory & Confluence Policy Violation Vector** ($w_3 = 0.25$). Measures compliance breaches against enforced Confluence policies (e.g., PCI-DSS v4.0 Zero-Drift Mandate `POL-402`).
- $V_4$: **Cross-Team SLA Ripple Vector** ($w_4 = 0.20$). Computes downstream team notification latency, dependency queue depth, and active sprint boundaries.
- $\Delta_{\text{blocker}}$: Discrete penalty coefficient ($\Delta_{\text{blocker}} = 15 \times N_{\text{unresolved\_blocks}}$).

### Confidence Tier Stratification:
- **$S_{CS} \ge 90\%$ (Tier A / Ready):** Cleared for zero-downtime automated CD release.
- **$70\% \le S_{CS} < 90\%$ (Tier B / Guarded):** Low risk; requires peer sign-off.
- **$50\% \le S_{CS} < 70\%$ (Tier C / Warning):** Elevated risk; contract drift detected; mitigation required.
- **$S_{CS} < 50\%$ (Tier F / Critical Blocker):** Immediate release block. Downstream outage guaranteed.

---

## 3. Teamwork Graph (TWG) Topology & Traversal

The Graph Engine (`src/graphEngine.js`) constructs an adjacency representation $G = (V, E)$:

### Vertex Types ($V$):
1. $v_{\text{jira}} \in V_{\text{jira}}$: Jira issues (e.g. `SCRUM-1`, `SCRUM-2`, `SCRUM-5`).
2. $v_{\text{policy}} \in V_{\text{policy}}$: Confluence regulatory policies (e.g. `POL-402`, `ARCH-109`).
3. $v_{\text{owner}} \in V_{\text{owner}}$: Engineering leads & approvers (e.g. `FOKRUL ISLAM`, `Elena Rostova`).
4. $v_{\text{service}} \in V_{\text{service}}$: Microservices (e.g. `Core-Pay v3`, `Mobile-Checkout`).

### Directed Edge Relationships ($E$):
- $(v_{\text{jira}_1}, v_{\text{jira}_2}) \in E_{\text{BLOCKS}}$: Upstream issue blocks downstream consumer.
- $(v_{\text{jira}}, v_{\text{policy}}) \in E_{\text{GOVERNED\_BY}}$: Ticket scope bounded by regulatory policy.
- $(v_{\text{jira}}, v_{\text{owner}}) \in E_{\text{OWNED\_BY}}$: Accountability and sign-off authority.
- $(v_{\text{subtask}}, v_{\text{jira}}) \in E_{\text{MITIGATES}}$: Automated bridge resolving schema drift.
- $(v_{\text{subtask}}, v_{\text{jira}_2}) \in E_{\text{PROTECTS}}$: Ensures consumer receives backward-compatible payload.

---

## 4. Model Context Protocol (MCP) Specification (JSON-RPC 2.0)

ChronosMCP exposes a Forge `webtrigger` operating as a spec-compliant Model Context Protocol server (`2024-11-05`).

### Supported MCP Methods:
1. `initialize`: Returns protocol version, server capabilities (`tools: {}`, `resources: {}`), and server metadata.
2. `tools/list`: Lists exposed tools and schema definitions.
3. `tools/call`: Executes backend operations inside Atlassian Forge.
4. `resources/list` & `resources/read`: Exposes virtual URIs (`jira://...`, `confluence://...`).

### Registered Tool Contracts:
```typescript
interface SimulateIssueBlastRadiusInput {
  issueKey: string; // e.g. "SCRUM-1"
  scenarioType?: "BREAKING_CONTRACT_DRIFT" | "AUTH_POLICY_MUTATION" | "ZERO_DOWNTIME_HOTFIX" | "REMEDIATED_STATE";
}

interface GetTeamworkGraphContextInput {
  issueKey: string; // e.g. "SCRUM-1"
}

interface TriggerCrossTeamAlignmentInput {
  issueKey: string; // e.g. "SCRUM-1"
}

interface VerifyCryptographicReleaseProofInput {
  issueKey: string; // e.g. "SCRUM-1"
  receiptHash?: string; // Optional SHA-256 hash or receipt ID
}

interface MintCryptographicReceiptInput {
  issueKey: string; // e.g. "SCRUM-1"
}
```

---

## 5. Zero-Trust SHA-256 Merkle Context Proofs

Before any deployment proceeds, ChronosMCP generates an immutable cryptographic release receipt:

1. **Context Ingestion:** Gathers issue key, summary, dependency link states, Confluence policy checksums, approver account ID, and computed $S_{CS}$.
2. **Canonical JSON Serialization:** Formats context object with sorted deterministic keys to eliminate whitespace/ordering volatility.
3. **Cryptographic Hashing:**
   $$H_{\text{receipt}} = \text{SHA-256}\left(\text{JSON}_{\text{canonical}}\right)$$
4. **Persistence:** Written to Atlassian Tenant KVS storage (`crypto_ledger_${issueKey}`).
5. **Independent Client Verification:** External consumers can recompute the SHA-256 hash across the serialized payload to mathematically guarantee zero post-attestation tampering.
