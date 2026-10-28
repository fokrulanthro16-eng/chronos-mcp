import api, { route } from '@forge/api';
import { kvs } from '@forge/kvs';

/**
 * Builds an Atlassian Document Format (ADF) object from plain text paragraphs
 */
function createAdfDocument(paragraphs) {
  return {
    version: 1,
    type: 'doc',
    content: paragraphs.map(text => ({
      type: 'paragraph',
      content: [
        {
          type: 'text',
          text: text
        }
      ]
    }))
  };
}

export async function seedEnterpriseScenario() {
  const results = {
    updatedIssues: [],
    linkedIssues: false,
    seededPolicies: false,
    timestamp: new Date().toISOString()
  };

  const scrum1Desc = [
    "RFC-8819: Payment Settlement API v3 & Tokenization Deprecation",
    "CRITICAL BREAKING CHANGE: Deprecating settlement_token v2 format in favor of vault_token_v3 with SHA-256 HMAC payload signatures.",
    "The settlement endpoint /v2/settle enforces 300ms timeout clamping and strict idempotency headers.",
    "Downstream consumers lacking contract versioning will experience HTTP 422 payload rejection and transaction rollback."
  ];

  const scrum2Desc = [
    "Consumer Specification: iOS 18 & Android 15 Instant Checkout Pipeline",
    "DOWNSTREAM DEPENDENCY WARNING: Mobile instant checkout pipeline directly consumes Core-Pay settlement_token v2 contract.",
    "Governed by Confluence Policy POL-402 (PCI-DSS v4.0 Tokenization & Contract Zero-Drift Mandate).",
    "Breaking token payload modification causes immediate client checkout failure across ~140,000 active checkout sessions/hr.",
    "Service Owner: Mobile Checkout Core Team (@mobile-checkout-eng)"
  ];

  // 1. Update SCRUM-1
  try {
    const updateScrum1Res = await api.asApp().requestJira(route`/rest/api/3/issue/SCRUM-1`, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        fields: {
          summary: "[Core-Pay] Upgrade Payment Settlement API v3 & Tokenization Schema",
          description: createAdfDocument(scrum1Desc),
          labels: ["payments-core", "breaking-change-candidate", "chronos-monitored"]
        }
      })
    });
    results.updatedIssues.push({ key: 'SCRUM-1', status: updateScrum1Res.status });
  } catch (err) {
    console.error("Error updating SCRUM-1:", err);
    results.updatedIssues.push({ key: 'SCRUM-1', error: err.message });
  }

  // 2. Update SCRUM-2
  try {
    const updateScrum2Res = await api.asApp().requestJira(route`/rest/api/3/issue/SCRUM-2`, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        fields: {
          summary: "[Mobile-Checkout] iOS/Android Instant Checkout & Refund Pipeline",
          description: createAdfDocument(scrum2Desc),
          labels: ["mobile-consumer", "pci-compliance", "critical-path"]
        }
      })
    });
    results.updatedIssues.push({ key: 'SCRUM-2', status: updateScrum2Res.status });
  } catch (err) {
    console.error("Error updating SCRUM-2:", err);
    results.updatedIssues.push({ key: 'SCRUM-2', error: err.message });
  }

  // 3. Create Jira Issue Link: SCRUM-1 blocks SCRUM-2
  try {
    const linkRes = await api.asApp().requestJira(route`/rest/api/3/issueLink`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        type: {
          name: "Blocks"
        },
        inwardIssue: {
          key: "SCRUM-2"
        },
        outwardIssue: {
          key: "SCRUM-1"
        },
        comment: {
          body: createAdfDocument([
            "[ChronosMCP Teamwork Graph] Causal link registered: SCRUM-1 (Core-Pay v3) blocks downstream consumer SCRUM-2 (Mobile-Checkout)."
          ])
        }
      })
    });
    results.linkedIssues = (linkRes.status === 201 || linkRes.status === 200 || linkRes.status === 400); // 400 if already linked
  } catch (err) {
    console.warn("Issue link creation notice:", err.message);
    results.linkedIssues = true;
  }

  // 4. Seed Governance Policies & Graph Meta in Forge Storage
  const policies = {
    'POL-402': {
      id: 'POL-402',
      title: 'PCI-DSS v4.0 Zero-Drift Payment Tokenization Mandate',
      spaceKey: 'FINSEC',
      version: '4.2',
      status: 'MANDATORY_ENFORCED',
      rules: [
        'Breaking changes to settlement_token must provide 14-day backward-compatibility adapter',
        'All client callers must support SHA-256 HMAC contract verification',
        'Dual-token acceptance window required before decommissioning legacy endpoints'
      ],
      governedServices: ['Core-Pay', 'Mobile-Checkout', 'Fraud-Shield']
    },
    'ARCH-109': {
      id: 'ARCH-109',
      title: 'Cross-Service Schema Evolution & API Contract Governance',
      spaceKey: 'ENGARCH',
      version: '2.1',
      status: 'ACTIVE',
      rules: [
        'Downstream consumer contract test suite must run prior to release tagging',
        'Automatic cross-team SLA buffer of 48 hours for breaking schema deployments'
      ],
      governedServices: ['All-Distributed-Services']
    }
  };

  await kvs.set('enterprise_policies', policies);
  await kvs.set('blast_simulation_state_SCRUM-1', {
    status: 'CRITICAL_RISK',
    shipConfidenceScore: 38,
    remediated: false,
    timestamp: new Date().toISOString()
  });

  results.seededPolicies = true;
  return results;
}
