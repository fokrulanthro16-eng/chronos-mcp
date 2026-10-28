#!/usr/bin/env node

/**
 * ChronosMCP: Local Stdio-to-Forge WebTrigger MCP Bridge & Health Inspector
 *
 * Exposes a standard MCP stdio interface for Cursor, Claude Desktop, and Antigravity,
 * routing JSON-RPC 2.0 messages to the live Forge WebTrigger server.
 */

const https = require('https');
const readline = require('readline');

const DEFAULT_ENDPOINT = 'https://84d8afae-9ec0-47fc-8212-e27f79430216.hello.atlassian-dev.net/x1/6aHEWuegPcDuTaXG0bLOpPFUZ1Q';
const ENDPOINT_URL = process.env.CHRONOS_MCP_ENDPOINT_URL || DEFAULT_ENDPOINT;

// Forward JSON-RPC payload to Forge WebTrigger
function forwardToForge(payload) {
  return new Promise((resolve, reject) => {
    const url = new URL(ENDPOINT_URL);
    const bodyStr = JSON.stringify(payload);

    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
        'User-Agent': 'ChronosMCP-Stdio-Bridge/1.0'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed);
        } catch (e) {
          resolve({ jsonrpc: '2.0', id: payload.id || null, result: data });
        }
      });
    });

    req.on('error', (err) => {
      reject(err);
    });

    req.write(bodyStr);
    req.end();
  });
}

// Health check function for CLI inspection
async function runHealthCheck() {
  console.log(`[ChronosMCP Bridge] Connecting to: ${ENDPOINT_URL}`);
  try {
    const initPayload = {
      jsonrpc: '2.0',
      id: 1,
      method: 'initialize',
      params: { protocolVersion: '2024-11-05' }
    };
    const initRes = await forwardToForge(initPayload);
    console.log('[ChronosMCP Bridge] Server Initialized:', JSON.stringify(initRes.result, null, 2));

    const toolsPayload = {
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/list',
      params: {}
    };
    const toolsRes = await forwardToForge(toolsPayload);
    console.log(`[ChronosMCP Bridge] ${toolsRes.result.tools.length} Tools Available:`);
    toolsRes.result.tools.forEach(t => console.log(`  - ${t.name}: ${t.description}`));
    console.log('[ChronosMCP Bridge] Health Check: 100% OPERATIONAL');
  } catch (err) {
    console.error('[ChronosMCP Bridge] Health check failed:', err.message);
    process.exit(1);
  }
}

// Mode router: if argument is --check, run diagnostic; otherwise run stdio loop
if (process.argv.includes('--check') || process.argv.includes('check')) {
  runHealthCheck();
} else {
  // Stdio loop for MCP clients
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
  });

  rl.on('line', async (line) => {
    if (!line.trim()) return;
    try {
      const parsed = JSON.parse(line);
      const response = await forwardToForge(parsed);
      process.stdout.write(JSON.stringify(response) + '\n');
    } catch (err) {
      const errResponse = {
        jsonrpc: '2.0',
        id: null,
        error: { code: -32603, message: 'Bridge error: ' + err.message }
      };
      process.stdout.write(JSON.stringify(errResponse) + '\n');
    }
  });

  process.stderr.write(`[ChronosMCP] Bridge active on stdio. Forwarding to ${ENDPOINT_URL}\n`);
}
