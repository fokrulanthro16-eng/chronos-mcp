import Resolver from '@forge/resolver';
import { seedEnterpriseScenario } from './seedEnterpriseScenario.js';
import { buildTeamworkGraph, simulateBlastRadius, fetchLiveJiraIssue } from './graphEngine.js';
import { mintCryptographicReceipt, getReceiptHistory, verifyReceipt } from './cryptoLedger.js';
import { executeAnalyzeBlastRadius, executeAutoRemediateSilos, executeMintCryptographicReceipt } from './rovoActions.js';
import { handleMcpRequest } from './mcpServer.js';
import { kvs } from '@forge/kvs';

const resolver = new Resolver();

// 1. Resolver: Get full issue context, graph, simulation, and ledger
resolver.define('getIssueContext', async (req) => {
  const issueKey = (req.payload && req.payload.issueKey) || (req.context && req.context.extension && req.context.extension.issue && req.context.extension.issue.key) || 'SCRUM-1';
  const scenarioType = (req.payload && req.payload.scenarioType) || 'BREAKING_CONTRACT_DRIFT';

  const [issue, graph, simulation, receipts, remediationState] = await Promise.all([
    fetchLiveJiraIssue(issueKey),
    buildTeamworkGraph(issueKey),
    simulateBlastRadius(issueKey, scenarioType),
    getReceiptHistory(issueKey),
    kvs.get(`remediation_state_${issueKey}`)
  ]);

  return {
    issueKey,
    issue: issue ? {
      key: issue.key,
      summary: issue.fields.summary,
      status: issue.fields.status.name,
      assignee: issue.fields.assignee ? issue.fields.assignee.displayName : 'FOKRUL ISLAM',
      labels: issue.fields.labels || []
    } : null,
    graph,
    simulation,
    receipts,
    remediationState
  };
});

// 2. Resolver: Seed enterprise FinTech scenario (SCRUM-1 & SCRUM-2)
resolver.define('seedEnterpriseScenario', async () => {
  const result = await seedEnterpriseScenario();
  return result;
});

// 3. Resolver: Run blast radius simulation with chosen scenario
resolver.define('runBlastSimulation', async (req) => {
  const issueKey = (req.payload && req.payload.issueKey) || 'SCRUM-1';
  const scenarioType = (req.payload && req.payload.scenarioType) || 'BREAKING_CONTRACT_DRIFT';
  const simulation = await simulateBlastRadius(issueKey, scenarioType);
  return simulation;
});

// 4. Resolver: Auto-remediate silos (creates subtasks, alerts mobile team, updates labels)
resolver.define('autoRemediateSilos', async (req) => {
  const issueKey = (req.payload && req.payload.issueKey) || 'SCRUM-1';
  const result = await executeAutoRemediateSilos(issueKey);
  return result;
});

// 5. Resolver: Mint SHA-256 Merkle release receipt
resolver.define('mintCryptographicReceipt', async (req) => {
  const issueKey = (req.payload && req.payload.issueKey) || 'SCRUM-1';
  const result = await executeMintCryptographicReceipt(issueKey);
  return result;
});

// 6. Resolver: Verify receipt cryptographic integrity
resolver.define('verifyReceipt', async (req) => {
  const hash = req.payload && req.payload.hash;
  const issueKey = (req.payload && req.payload.issueKey) || 'SCRUM-1';
  const result = await verifyReceipt(hash, issueKey);
  return result;
});

// 7. Resolver: Get MCP Diagnostics & configuration
resolver.define('getMcpDiagnostics', async () => {
  return {
    mcpName: 'chronos-atlassian-mcp-server',
    version: '1.0.0',
    protocolVersion: '2024-11-05',
    targetSite: 'fokrulanthro16.atlassian.net',
    status: 'ONLINE'
  };
});

export const resolverHandler = resolver.getDefinitions();

/**
 * Rovo Agent Action Handler
 */
export const rovoHandler = async (event, context) => {
  console.log('Rovo action invoked:', JSON.stringify(event));
  const actionKey = (context && context.moduleKey) || (event && event.action) || 'analyze-blast-radius';
  const issueKey = (event && event.inputs && event.inputs.issueKey) || 'SCRUM-1';

  try {
    if (actionKey.includes('analyze-blast-radius')) {
      return await executeAnalyzeBlastRadius(issueKey);
    }
    if (actionKey.includes('auto-remediate-silos')) {
      return await executeAutoRemediateSilos(issueKey);
    }
    if (actionKey.includes('mint-cryptographic-receipt')) {
      return await executeMintCryptographicReceipt(issueKey);
    }

    // Default fallback
    return await executeAnalyzeBlastRadius(issueKey);
  } catch (err) {
    console.error(`Error executing Rovo action ${actionKey}:`, err);
    return {
      success: false,
      error: err.message
    };
  }
};

/**
 * Forge WebTrigger: Model Context Protocol (MCP) JSON-RPC 2.0 Handler
 */
export const mcpHandler = async (request) => {
  return await handleMcpRequest(request);
};
