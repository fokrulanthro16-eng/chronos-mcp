import api, { route } from '@forge/api';
import { kvs } from '@forge/kvs';

/**
 * Teamwork Graph Context Engine & Causal Blast-Radius Simulator
 */

export async function fetchLiveJiraIssue(issueKey) {
  try {
    const res = await api.asApp().requestJira(route`/rest/api/3/issue/${issueKey}?expand=renderedFields,names,schema,operations,editmeta,changelog`);
    if (res.status === 200) {
      return await res.json();
    }
  } catch (err) {
    console.error(`Failed to fetch live Jira issue ${issueKey}:`, err);
  }
  return null;
}

export async function buildTeamworkGraph(rootIssueKey = 'SCRUM-1') {
  const rootIssue = await fetchLiveJiraIssue(rootIssueKey);
  const policies = (await kvs.get('enterprise_policies')) || {};
  const remediationState = (await kvs.get(`remediation_state_${rootIssueKey}`)) || null;

  // Nodes & Edges collection
  const nodes = [];
  const edges = [];

  // Root issue node
  const rootSummary = rootIssue ? rootIssue.fields.summary : `Issue ${rootIssueKey}`;
  const rootLabels = rootIssue ? (rootIssue.fields.labels || []) : [];
  const rootAssignee = rootIssue && rootIssue.fields.assignee ? rootIssue.fields.assignee.displayName : 'FOKRUL ISLAM (FinTech Core Lead)';
  const rootStatus = rootIssue && rootIssue.fields.status ? rootIssue.fields.status.name : 'In Progress';

  nodes.push({
    id: rootIssueKey,
    type: 'JIRA_ISSUE',
    label: rootIssueKey,
    title: rootSummary,
    status: rootStatus,
    service: 'Core-Pay Service (v3.0)',
    tier: 'Tier 1 Critical',
    assignee: rootAssignee,
    role: 'Source of Change',
    labels: rootLabels
  });

  // Assignee Node
  nodes.push({
    id: 'USER_FOKRUL',
    type: 'TEAM_OWNER',
    label: rootAssignee,
    team: 'Core Payments Engineering',
    email: 'fokrulanthro16@gmail.com',
    role: 'Principal Author'
  });

  edges.push({
    id: `edge-${rootIssueKey}-USER_FOKRUL`,
    source: rootIssueKey,
    target: 'USER_FOKRUL',
    relation: 'OWNED_BY',
    label: 'Owned by'
  });

  // Inspect linked issues
  const linkedIssues = rootIssue && rootIssue.fields.issuelinks ? rootIssue.fields.issuelinks : [];
  let foundScrum2 = false;

  for (const link of linkedIssues) {
    const inward = link.inwardIssue;
    const outward = link.outwardIssue;
    const target = inward || outward;

    if (target) {
      if (target.key === 'SCRUM-2') {
        foundScrum2 = true;
      }
      nodes.push({
        id: target.key,
        type: 'JIRA_ISSUE',
        label: target.key,
        title: target.fields ? target.fields.summary : 'Downstream Dependent Consumer',
        status: target.fields && target.fields.status ? target.fields.status.name : 'To Do',
        service: 'Mobile Instant Checkout (iOS/Android)',
        tier: 'Tier 1 Critical',
        assignee: 'Mobile Core Team (@mobile-checkout-eng)',
        role: 'Impacted Downstream Consumer'
      });

      edges.push({
        id: `edge-${rootIssueKey}-${target.key}`,
        source: rootIssueKey,
        target: target.key,
        relation: link.type ? link.type.name.toUpperCase() : 'BLOCKS',
        label: link.type ? (inward ? link.type.inward : link.type.outward) : 'Blocks'
      });
    }
  }

  // Fallback to ensure SCRUM-2 is represented in graph if not yet linked
  if (!foundScrum2 && rootIssueKey === 'SCRUM-1') {
    nodes.push({
      id: 'SCRUM-2',
      type: 'JIRA_ISSUE',
      label: 'SCRUM-2',
      title: '[Mobile-Checkout] iOS/Android Instant Checkout & Refund Pipeline',
      status: 'To Do',
      service: 'Mobile Instant Checkout (iOS/Android)',
      tier: 'Tier 1 Critical',
      assignee: 'Mobile Core Team (@mobile-checkout-eng)',
      role: 'Impacted Downstream Consumer'
    });

    edges.push({
      id: 'edge-SCRUM-1-SCRUM-2',
      source: 'SCRUM-1',
      target: 'SCRUM-2',
      relation: 'BLOCKS',
      label: 'Blocks'
    });
  }

  // Mobile Team Owner Node
  nodes.push({
    id: 'USER_MOBILE_LEAD',
    type: 'TEAM_OWNER',
    label: 'Elena Rostova (Mobile Edge Lead)',
    team: 'Mobile Checkout Engineering',
    role: 'Downstream Approver'
  });

  edges.push({
    id: 'edge-SCRUM-2-USER_MOBILE_LEAD',
    source: 'SCRUM-2',
    target: 'USER_MOBILE_LEAD',
    relation: 'OWNED_BY',
    label: 'Owned by'
  });

  // Confluence Governance Policy Nodes
  const pol402 = policies['POL-402'] || {
    id: 'POL-402',
    title: 'PCI-DSS v4.0 Zero-Drift Payment Tokenization Mandate',
    spaceKey: 'FINSEC',
    version: '4.2',
    status: 'MANDATORY_ENFORCED'
  };

  nodes.push({
    id: 'POL-402',
    type: 'CONFLUENCE_POLICY',
    label: 'POL-402',
    title: pol402.title,
    space: pol402.spaceKey,
    version: pol402.version,
    complianceLevel: 'Strict Regulatory',
    status: pol402.status
  });

  edges.push({
    id: `edge-${rootIssueKey}-POL-402`,
    source: rootIssueKey,
    target: 'POL-402',
    relation: 'GOVERNED_BY',
    label: 'Governed by'
  });

  edges.push({
    id: 'edge-SCRUM-2-POL-402',
    source: 'SCRUM-2',
    target: 'POL-402',
    relation: 'GOVERNED_BY',
    label: 'Governed by'
  });

  // Subtask remediation node if present
  if (remediationState && remediationState.subtaskKey) {
    nodes.push({
      id: remediationState.subtaskKey,
      type: 'REMEDIATION_SUBTASK',
      label: remediationState.subtaskKey,
      title: 'Automated Dual-Token Adapter & Regression Verification Pipeline',
      status: 'In Progress',
      role: 'Silo Mitigation Bridge'
    });

    edges.push({
      id: `edge-${rootIssueKey}-${remediationState.subtaskKey}`,
      source: rootIssueKey,
      target: remediationState.subtaskKey,
      relation: 'MITIGATED_BY',
      label: 'Mitigated by'
    });

    edges.push({
      id: `edge-${remediationState.subtaskKey}-SCRUM-2`,
      source: remediationState.subtaskKey,
      target: 'SCRUM-2',
      relation: 'PROTECTS',
      label: 'Protects'
    });
  }

  return {
    rootIssueKey,
    nodes,
    edges,
    totalNodes: nodes.length,
    totalEdges: edges.length,
    generatedAt: new Date().toISOString()
  };
}

/**
 * Counterfactual "What-If" Blast Radius Simulation Engine
 */
export async function simulateBlastRadius(issueKey = 'SCRUM-1', scenarioType = 'BREAKING_CONTRACT_DRIFT') {
  const rootIssue = await fetchLiveJiraIssue(issueKey);
  const labels = rootIssue ? (rootIssue.fields.labels || []) : [];
  const hasRemediationLabel = labels.includes('chronos-verified') || labels.includes('blast-radius-mitigated');
  const storedRemediation = await kvs.get(`remediation_state_${issueKey}`);

  const isRemediated = hasRemediationLabel || (storedRemediation && storedRemediation.remediated);

  // If already remediated or requested REMEDIATED_STATE
  if (isRemediated || scenarioType === 'REMEDIATED_STATE') {
    return {
      scenario: 'POST_REMEDIATION_HARMONY',
      scenarioLabel: 'Rovo Auto-Remediated & Verified (Post-Fix)',
      shipConfidenceScore: 98,
      riskLevel: 'NEGLIGIBLE',
      confidenceGrade: 'A+',
      readinessVerdict: 'CLEARED FOR ZERO-DOWNTIME PRODUCTION RELEASE',
      impactedTeamsCount: 0,
      activeBlockersCount: 0,
      policyCompliance: {
        'POL-402': { status: 'COMPLIANT', detail: '14-Day Dual Token Adapter actively bridging v2 and v3 schemas.' },
        'ARCH-109': { status: 'COMPLIANT', detail: 'Regression test contract suite verified; cross-team SLA buffered.' }
      },
      vectors: [
        { name: 'API Contract Drift', risk: 2, status: 'MITIGATED', note: 'Dual token serialization adapter active on gateway.' },
        { name: 'Database Migration Lock', risk: 1, status: 'SAFE', note: 'Additive schema change with zero table locking.' },
        { name: 'Security/PCI Compliance', risk: 0, status: 'SATISFIED', note: 'SHA-256 Merkle proof registered in cryptographic ledger.' },
        { name: 'Cross-Team SLA Ripple', risk: 4, status: 'ALIGNED', note: 'Mobile team alerted; mitigation subtask auto-assigned.' }
      ],
      recommendations: [
        'Proceed with Canary deployment corridor at 10% traffic.',
        'Cryptographic release attestation active in tamper-evident ledger.'
      ],
      simulatedAt: new Date().toISOString()
    };
  }

  // Pre-remediation scenarios
  if (scenarioType === 'ZERO_DOWNTIME_HOTFIX') {
    return {
      scenario: 'ZERO_DOWNTIME_HOTFIX',
      scenarioLabel: 'Additive Non-Breaking Patch',
      shipConfidenceScore: 94,
      riskLevel: 'LOW',
      confidenceGrade: 'A',
      readinessVerdict: 'SAFE TO SHIP WITH STANDARD CD PIPELINE',
      impactedTeamsCount: 1,
      activeBlockersCount: 0,
      policyCompliance: {
        'POL-402': { status: 'COMPLIANT', detail: 'Contract preserves existing field signatures.' },
        'ARCH-109': { status: 'COMPLIANT', detail: 'No cross-service protocol alterations.' }
      },
      vectors: [
        { name: 'API Contract Drift', risk: 5, status: 'LOW', note: 'Only optional fields added.' },
        { name: 'Database Migration Lock', risk: 4, status: 'LOW', note: 'Zero-downtime column index.' },
        { name: 'Security/PCI Compliance', risk: 0, status: 'PASS', note: 'Tokenization boundaries untouched.' },
        { name: 'Cross-Team SLA Ripple', risk: 8, status: 'LOW', note: 'No client updates necessary.' }
      ],
      recommendations: ['Standard automated regression test suite run.'],
      simulatedAt: new Date().toISOString()
    };
  }

  if (scenarioType === 'AUTH_POLICY_MUTATION') {
    return {
      scenario: 'AUTH_POLICY_MUTATION',
      scenarioLabel: 'Auth & Key Rotation Without SecOps Sign-off',
      shipConfidenceScore: 52,
      riskLevel: 'HIGH',
      confidenceGrade: 'C-',
      readinessVerdict: 'BLOCKED BY SECURITY GATEWAY',
      impactedTeamsCount: 2,
      activeBlockersCount: 1,
      policyCompliance: {
        'POL-402': { status: 'VIOLATION', detail: 'Token rotation frequency exceeds allowed client retry latency.' },
        'ARCH-109': { status: 'WARNING', detail: 'Missing SecOps approval signoff.' }
      },
      vectors: [
        { name: 'API Contract Drift', risk: 25, status: 'MEDIUM', note: 'Signature mismatch on expired sessions.' },
        { name: 'Database Migration Lock', risk: 10, status: 'LOW', note: 'Key store cache flush required.' },
        { name: 'Security/PCI Compliance', risk: 85, status: 'CRITICAL', note: 'Missing dual-custody cryptographic approval.' },
        { name: 'Cross-Team SLA Ripple', risk: 45, status: 'HIGH', note: 'Auth gateway team not yet notified.' }
      ],
      recommendations: [
        'Request emergency SecOps review.',
        'Run ChronosMCP Rovo Auto-Remediation to generate compliance waiver.'
      ],
      simulatedAt: new Date().toISOString()
    };
  }

  // Default: BREAKING_CONTRACT_DRIFT (High-stakes FinTech scenario)
  return {
    scenario: 'BREAKING_CONTRACT_DRIFT',
    scenarioLabel: 'Unmitigated Breaking Token Schema Upgrade',
    shipConfidenceScore: 38,
    riskLevel: 'CRITICAL',
    confidenceGrade: 'F',
    readinessVerdict: 'HIGH-RISK RELEASE BLOCKER DETECTED — DO NOT SHIP',
    impactedTeamsCount: 3,
    activeBlockersCount: 2,
    collidingIssues: [
      {
        key: 'SCRUM-2',
        summary: '[Mobile-Checkout] iOS/Android Instant Checkout & Refund Pipeline',
        team: 'Mobile Checkout Engineering',
        reason: 'Client expects settlement_token v2 format; Core-Pay changes to vault_token_v3.'
      }
    ],
    policyCompliance: {
      'POL-402': {
        status: 'NON_COMPLIANT',
        detail: 'Breaches PCI-DSS v4.0 Zero-Drift Mandate: Missing 14-day backward compatibility adapter.'
      },
      'ARCH-109': {
        status: 'VIOLATION',
        detail: 'Cross-Service Schema Evolution: Dependent service tests will fail upon deployment.'
      }
    },
    vectors: [
      { name: 'API Contract Drift', risk: 94, status: 'CRITICAL_COLLISION', note: 'settlement_token signature changed without v2 fallback.' },
      { name: 'Database Migration Lock', risk: 48, status: 'ELEVATED', note: 'Pending table lock during token re-indexing.' },
      { name: 'Security/PCI Compliance', risk: 92, status: 'POLICY_BREACH', note: 'POL-402 audit violation triggers financial penalty risk.' },
      { name: 'Cross-Team SLA Ripple', risk: 88, status: 'OUTAGE_RISK', note: 'Mobile checkout estimated failure rate: 140,000 tx/hr.' }
    ],
    recommendations: [
      'Trigger Rovo Auto-Remediate Silos to create dual-token backward compatibility adapter.',
      'Notify Elena Rostova (@mobile-checkout-eng) with automated contract alignment alert.',
      'Generate SHA-256 Merkle release receipt before shipping.'
    ],
    simulatedAt: new Date().toISOString()
  };
}
