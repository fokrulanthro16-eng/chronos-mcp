import { simulateBlastRadius, buildTeamworkGraph } from './graphEngine.js';
import { executeAutoRemediateSilos, executeMintCryptographicReceipt } from './rovoActions.js';
import { verifyReceipt, getReceiptHistory } from './cryptoLedger.js';
import { kvs } from '@forge/kvs';

/**
 * Spec-Compliant Model Context Protocol (MCP) JSON-RPC 2.0 Server
 * Accessible via Forge WebTrigger
 */

const SERVER_INFO = {
  name: 'chronos-atlassian-mcp-server',
  title: 'ChronosMCP Context & Blast-Radius Engine',
  version: '1.0.0',
  protocolVersion: '2024-11-05',
  atlassianSite: 'fokrulanthro16.atlassian.net'
};

const MCP_TOOLS = [
  {
    name: 'simulate_issue_blast_radius',
    description: 'Simulates causal ripple effects, downstream Jira issue collisions, and calculates live Ship Confidence Score across the Teamwork Graph.',
    inputSchema: {
      type: 'object',
      properties: {
        issueKey: {
          type: 'string',
          description: 'The Jira issue key to simulate (e.g. SCRUM-1)'
        },
        scenarioType: {
          type: 'string',
          description: 'Scenario vector: BREAKING_CONTRACT_DRIFT, AUTH_POLICY_MUTATION, ZERO_DOWNTIME_HOTFIX, or REMEDIATED_STATE',
          enum: ['BREAKING_CONTRACT_DRIFT', 'AUTH_POLICY_MUTATION', 'ZERO_DOWNTIME_HOTFIX', 'REMEDIATED_STATE']
        }
      },
      required: ['issueKey']
    }
  },
  {
    name: 'get_teamwork_graph_context',
    description: 'Retrieves multi-hop organizational graph context including dependent Jira issues, Confluence governance policies, service tiers, and engineering team owners.',
    inputSchema: {
      type: 'object',
      properties: {
        issueKey: {
          type: 'string',
          description: 'The root Jira issue key (e.g. SCRUM-1)'
        }
      },
      required: ['issueKey']
    }
  },
  {
    name: 'trigger_cross_team_alignment',
    description: 'Autonomously provisions Jira mitigation subtasks, links dependent issues, posts cross-team alignment warnings, and resolves silos.',
    inputSchema: {
      type: 'object',
      properties: {
        issueKey: {
          type: 'string',
          description: 'The Jira issue key requiring cross-silo remediation (e.g. SCRUM-1)'
        }
      },
      required: ['issueKey']
    }
  },
  {
    name: 'mint_cryptographic_receipt',
    description: 'Mints a tamper-evident SHA-256 Merkle Context Proof for the issue payload, linked dependencies, and regulatory compliance state into Forge KVS.',
    inputSchema: {
      type: 'object',
      properties: {
        issueKey: {
          type: 'string',
          description: 'The Jira issue key to attest (e.g. SCRUM-1)'
        }
      },
      required: ['issueKey']
    }
  },
  {
    name: 'verify_cryptographic_release_proof',
    description: 'Verifies the tamper-evident SHA-256 Merkle Context Proof stored in the release ledger for compliance verification.',
    inputSchema: {
      type: 'object',
      properties: {
        issueKey: {
          type: 'string',
          description: 'The Jira issue key (e.g. SCRUM-1)'
        },
        receiptHash: {
          type: 'string',
          description: 'The SHA-256 hash or receipt ID to verify (optional; if omitted, checks the latest receipt)'
        }
      },
      required: ['issueKey']
    }
  }
];

const MCP_RESOURCES = [
  {
    uri: 'jira://fokrulanthro16.atlassian.net/graph/SCRUM-1',
    name: 'Live Teamwork Graph Context: SCRUM-1',
    mimeType: 'application/json',
    description: 'Live multi-hop dependency graph for Core Payments Upgrade v3'
  },
  {
    uri: 'confluence://fokrulanthro16.atlassian.net/policies/POL-402',
    name: 'PCI-DSS v4.0 Zero-Drift Policy',
    mimeType: 'application/json',
    description: 'Confluence regulatory compliance policy governing payment token drift'
  }
];

export async function handleMcpRequest(request) {
  // Check HTTP method
  const method = request.method ? request.method.toUpperCase() : 'GET';

  // Handle GET request: Diagnostics & Interactive Judge Dashboard
  if (method === 'GET') {
    const policies = (await kvs.get('enterprise_policies')) || {};
    const diagnosticsPayload = {
      status: 'ONLINE',
      protocol: 'Model Context Protocol (MCP) JSON-RPC 2.0',
      protocolVersion: SERVER_INFO.protocolVersion,
      server: SERVER_INFO,
      site: 'fokrulanthro16.atlassian.net',
      capabilities: {
        tools: { listChanged: false },
        resources: { subscribe: false, listChanged: false },
        prompts: { listChanged: false }
      },
      registeredToolsCount: MCP_TOOLS.length,
      tools: MCP_TOOLS.map(t => ({ name: t.name, description: t.description })),
      resources: MCP_RESOURCES,
      activePolicies: Object.keys(policies),
      sampleClientConfig: {
        mcpServers: {
          "chronos-atlassian": {
            command: "npx",
            args: ["-y", "mcp-remote-bridge", "--url", "REPLACE_WITH_LIVE_WEBTRIGGER_URL"]
          }
        }
      },
      message: 'ChronosMCP Atlassian MCP Bridge is fully operational. Send JSON-RPC 2.0 POST requests to invoke tools.'
    };

    return {
      statusCode: 200,
      headers: {
        'Content-Type': ['application/json'],
        'Access-Control-Allow-Origin': ['*'],
        'Access-Control-Allow-Methods': ['GET, POST, OPTIONS'],
        'Access-Control-Allow-Headers': ['Content-Type, Authorization']
      },
      body: JSON.stringify(diagnosticsPayload, null, 2)
    };
  }

  // Handle OPTIONS request for CORS preflight
  if (method === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: {
        'Access-Control-Allow-Origin': ['*'],
        'Access-Control-Allow-Methods': ['GET, POST, OPTIONS'],
        'Access-Control-Allow-Headers': ['Content-Type, Authorization']
      },
      body: ''
    };
  }

  // Handle POST request: MCP JSON-RPC 2.0
  let rpcBody;
  try {
    rpcBody = typeof request.body === 'string' ? JSON.parse(request.body) : request.body;
  } catch (err) {
    return {
      statusCode: 400,
      headers: { 'Content-Type': ['application/json'] },
      body: JSON.stringify({
        jsonrpc: '2.0',
        error: { code: -32700, message: 'Parse error: Invalid JSON' },
        id: null
      })
    };
  }

  const { jsonrpc, id, method: rpcMethod, params } = rpcBody || {};

  // Standard MCP JSON-RPC router
  switch (rpcMethod) {
    case 'initialize':
      return jsonRpcSuccess(id, {
        protocolVersion: SERVER_INFO.protocolVersion,
        capabilities: {
          tools: {},
          resources: {},
          prompts: {}
        },
        serverInfo: {
          name: SERVER_INFO.name,
          version: SERVER_INFO.version
        }
      });

    case 'tools/list':
      return jsonRpcSuccess(id, {
        tools: MCP_TOOLS
      });

    case 'resources/list':
      return jsonRpcSuccess(id, {
        resources: MCP_RESOURCES
      });

    case 'resources/read': {
      const uri = params ? params.uri : '';
      if (uri.includes('POL-402')) {
        const policies = (await kvs.get('enterprise_policies')) || {};
        return jsonRpcSuccess(id, {
          contents: [
            {
              uri,
              mimeType: 'application/json',
              text: JSON.stringify(policies['POL-402'] || {}, null, 2)
            }
          ]
        });
      }
      const graph = await buildTeamworkGraph('SCRUM-1');
      return jsonRpcSuccess(id, {
        contents: [
          {
            uri,
            mimeType: 'application/json',
            text: JSON.stringify(graph, null, 2)
          }
        ]
      });
    }

    case 'tools/call': {
      const toolName = params ? params.name : '';
      const toolArgs = (params ? params.arguments : {}) || {};

      try {
        if (toolName === 'simulate_issue_blast_radius') {
          const result = await simulateBlastRadius(toolArgs.issueKey || 'SCRUM-1', toolArgs.scenarioType || 'BREAKING_CONTRACT_DRIFT');
          return jsonRpcSuccess(id, {
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }
            ]
          });
        }

        if (toolName === 'get_teamwork_graph_context') {
          const result = await buildTeamworkGraph(toolArgs.issueKey || 'SCRUM-1');
          return jsonRpcSuccess(id, {
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }
            ]
          });
        }

        if (toolName === 'trigger_cross_team_alignment') {
          const result = await executeAutoRemediateSilos(toolArgs.issueKey || 'SCRUM-1');
          return jsonRpcSuccess(id, {
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }
            ]
          });
        }

        if (toolName === 'mint_cryptographic_receipt') {
          const result = await executeMintCryptographicReceipt(toolArgs.issueKey || 'SCRUM-1');
          return jsonRpcSuccess(id, {
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }
            ]
          });
        }

        if (toolName === 'verify_cryptographic_release_proof') {
          const receipts = await getReceiptHistory(toolArgs.issueKey || 'SCRUM-1');
          const targetHash = toolArgs.receiptHash || (receipts.length > 0 ? receipts[0].hash : null);
          if (!targetHash) {
            return jsonRpcSuccess(id, {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({ verified: false, message: 'No release receipts found for issue' })
                }
              ]
            });
          }
          const result = await verifyReceipt(targetHash, toolArgs.issueKey || 'SCRUM-1');
          return jsonRpcSuccess(id, {
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }
            ]
          });
        }

        return jsonRpcError(id, -32601, `Method tool '${toolName}' not found`);
      } catch (err) {
        return jsonRpcError(id, -32603, `Internal tool execution error: ${err.message}`);
      }
    }

    default:
      return jsonRpcError(id, -32601, `Unsupported MCP method '${rpcMethod}'`);
  }
}

function jsonRpcSuccess(id, result) {
  return {
    statusCode: 200,
    headers: {
      'Content-Type': ['application/json'],
      'Access-Control-Allow-Origin': ['*']
    },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: id || 1,
      result
    })
  };
}

function jsonRpcError(id, code, message) {
  return {
    statusCode: 200,
    headers: {
      'Content-Type': ['application/json'],
      'Access-Control-Allow-Origin': ['*']
    },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: id || null,
      error: { code, message }
    })
  };
}
