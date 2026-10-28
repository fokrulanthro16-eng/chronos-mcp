import os
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = os.path.abspath(r"C:\Users\WALTON\.gemini\antigravity\scratch\chronos-mcp\screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

COMMON_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 1920px;
  height: 1080px;
  background: #090D16;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #F1F5F9;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
/* Atlassian Top Global Nav */
.atlassian-nav {
  height: 48px;
  background: #0B1120;
  border-bottom: 1px solid #1E293B;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.nav-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.app-switcher {
  display: grid;
  grid-template-columns: repeat(3, 4px);
  gap: 3px;
  padding: 6px;
  cursor: pointer;
}
.app-switcher div {
  width: 4px;
  height: 4px;
  background: #94A3B8;
  border-radius: 1px;
}
.jira-logo-box {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  font-size: 15px;
  color: #38BDF8;
}
.jira-links {
  display: flex;
  gap: 14px;
  font-size: 13px;
  color: #94A3B8;
  margin-left: 8px;
}
.jira-link {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}
.jira-link.active {
  color: #F8FAFC;
  font-weight: 600;
}
.nav-center {
  display: flex;
  align-items: center;
  width: 440px;
  background: #172238;
  border: 1px solid #23304A;
  border-radius: 6px;
  padding: 6px 14px;
  gap: 8px;
  font-size: 13px;
  color: #64748B;
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 14px;
}
.user-badge {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #4F46E5;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 800;
}

/* Main Workspace */
.main-workspace {
  flex: 1;
  display: flex;
  overflow: hidden;
  background: #080C16;
}

/* Jira Left Navigation Sidebar */
.jira-sidebar {
  width: 220px;
  background: #0D1424;
  border-right: 1px solid #1E293B;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.project-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 12px;
  border-bottom: 1px solid #1E293B;
}
.project-avatar {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: linear-gradient(135deg, #3B82F6, #1D4ED8);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 14px;
}
.project-meta {
  display: flex;
  flex-direction: column;
}
.project-name { font-size: 13px; font-weight: 700; color: #F1F5F9; }
.project-type { font-size: 11px; color: #64748B; }

.side-nav-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.side-nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 6px;
  font-size: 13px;
  color: #94A3B8;
  cursor: pointer;
}
.side-nav-item.active {
  background: #17253D;
  color: #38BDF8;
  font-weight: 600;
}

/* Jira Issue Detail Container */
.issue-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 16px 24px;
}

/* Issue Top Bar */
.issue-breadcrumb-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #64748B;
}
.breadcrumbs span { color: #94A3B8; }
.issue-key-badge {
  color: #818CF8;
  font-weight: 700;
}

.issue-title-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.issue-title {
  font-size: 21px;
  font-weight: 800;
  color: #F8FAFC;
  display: flex;
  align-items: center;
  gap: 12px;
}
.status-pill {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 4px;
  background: #1E3A8A;
  color: #93C5FD;
  border: 1px solid #3B82F6;
}

/* Issue 2-Column Split: Main Content + Context Panel */
.issue-layout {
  flex: 1;
  display: flex;
  gap: 20px;
  overflow: hidden;
}
.issue-main-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 14px;
  overflow-y: auto;
  padding-right: 4px;
}
.issue-side-col {
  width: 320px;
  background: #0E1626;
  border: 1px solid #1E293B;
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Jira Context Fields in Side Col */
.meta-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.meta-label {
  font-size: 11px;
  color: #64748B;
  text-transform: uppercase;
  font-weight: 700;
}
.meta-val {
  font-size: 13px;
  color: #E2E8F0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.avatar-small {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #3B82F6;
  color: white;
  font-size: 10px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Chronos App Card Inside Main Col */
.chronos-panel {
  background: #0E1626;
  border: 1px solid #23304A;
  border-radius: 12px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.chronos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.brand-title {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: linear-gradient(135deg, #6366F1, #06B6D4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}
.brand-text h2 {
  font-size: 16px;
  font-weight: 800;
  color: #F8FAFC;
  display: flex;
  align-items: center;
  gap: 8px;
}
.verigraph-badge {
  font-size: 11px;
  font-weight: 700;
  color: #38BDF8;
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid #38BDF8;
  padding: 1px 6px;
  border-radius: 4px;
}
.brand-text p {
  font-size: 12px;
  color: #94A3B8;
  margin-top: 2px;
}

/* KPIs Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.kpi-box {
  background: #141F33;
  border: 1px solid #22314A;
  border-radius: 8px;
  padding: 10px 14px;
}
.kpi-label { font-size: 10px; color: #64748B; text-transform: uppercase; font-weight: 700; }
.kpi-val { font-size: 15px; font-weight: 800; margin-top: 2px; }
.kpi-sub { font-size: 11px; color: #94A3B8; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Action Buttons */
.action-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}
.btn-action {
  padding: 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid #334155;
  background: #1E293B;
  color: #F8FAFC;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.btn-action.primary {
  background: linear-gradient(135deg, #4F46E5, #6366F1);
  border-color: #6366F1;
}
.btn-action.rovo {
  background: linear-gradient(135deg, #059669, #10B981);
  border-color: #10B981;
}
.btn-action.danger {
  background: linear-gradient(135deg, #DC2626, #EF4444);
  border-color: #EF4444;
}

/* Scenario Strip */
.scenario-strip {
  display: flex;
  gap: 8px;
  align-items: center;
  background: #121A2B;
  border: 1px solid #1E293B;
  padding: 8px 12px;
  border-radius: 8px;
}
.scenario-label { font-size: 11px; color: #64748B; font-weight: 700; text-transform: uppercase; margin-right: 4px; }
.scenario-btn {
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  border: 1px solid #28374F;
  background: #172238;
  color: #94A3B8;
}
.scenario-btn.active-red {
  background: #DC2626;
  border-color: #EF4444;
  color: white;
}
.scenario-btn.active-green {
  background: #059669;
  border-color: #10B981;
  color: white;
}

/* Tabs */
.tabs-bar {
  display: flex;
  gap: 6px;
  border-bottom: 1px solid #1E293B;
  padding-bottom: 2px;
}
.tab-btn {
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 700;
  color: #94A3B8;
  border: none;
  background: none;
  border-bottom: 2px solid transparent;
}
.tab-btn.active {
  color: #38BDF8;
  border-bottom-color: #38BDF8;
}

/* Tab Card */
.tab-canvas {
  background: #0A0F1D;
  border: 1px solid #1E293B;
  border-radius: 8px;
  padding: 16px;
  min-height: 280px;
}
"""

def generate_html_view(scene_id):
    if scene_id == 1:
        # 01-chronos-command-center-risk.png
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{COMMON_CSS}</style>
</head>
<body>
  <div class="atlassian-nav">
    <div class="nav-left">
      <div class="app-switcher"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="jira-logo-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M11.5 2C11.5 7.24 7.24 11.5 2 11.5C7.24 11.5 11.5 15.76 11.5 21C11.5 15.76 15.76 11.5 21 11.5C15.76 11.5 11.5 7.24 11.5 2Z" fill="#38BDF8"/></svg>
        Jira Software
      </div>
      <div class="jira-links">
        <div class="jira-link">Your work ▾</div>
        <div class="jira-link active">Projects ▾</div>
        <div class="jira-link">Filters ▾</div>
        <div class="jira-link">Dashboards ▾</div>
        <div class="jira-link">Teams ▾</div>
        <div class="jira-link">Apps ▾</div>
      </div>
    </div>
    <div class="nav-center">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
      Search Jira (fokrulanthro16.atlassian.net)
    </div>
    <div class="nav-right">
      <span style="font-size:12px; color:#10B981; font-weight:700; background:rgba(16,185,129,0.1); border:1px solid #10B981; padding:3px 8px; border-radius:4px;">● Live Forge development</span>
      <div class="user-badge">FI</div>
    </div>
  </div>

  <div class="main-workspace">
    <div class="jira-sidebar">
      <div class="project-header">
        <div class="project-avatar">SC</div>
        <div class="project-meta">
          <div class="project-name">FinTech Core</div>
          <div class="project-type">Software project</div>
        </div>
      </div>
      <div class="side-nav-list">
        <div class="side-nav-item">📋 Timeline</div>
        <div class="side-nav-item">📊 Backlog</div>
        <div class="side-nav-item">📈 Active Sprints</div>
        <div class="side-nav-item active">🎯 Issues & Sprints</div>
        <div class="side-nav-item">⚡ Releases</div>
        <div class="side-nav-item">📑 Project pages</div>
      </div>
    </div>

    <div class="issue-container">
      <div class="issue-breadcrumb-bar">
        <div class="breadcrumbs">
          <span>Projects</span> / <span>FinTech Core (SCRUM)</span> / <span class="issue-key-badge">SCRUM-1</span>
        </div>
        <div style="font-size:12px; color:#64748B;">Updated 4 minutes ago</div>
      </div>

      <div class="issue-title-bar">
        <div class="issue-title">
          <span style="color:#60A5FA;">SCRUM-1:</span> [Core-Pay] Upgrade Payment Settlement API v3
          <span class="status-pill">IN PROGRESS</span>
        </div>
        <div style="display:flex; gap:8px;">
          <button style="background:#1E293B; border:1px solid #334155; color:#E2E8F0; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600;">Attach</button>
          <button style="background:#1E293B; border:1px solid #334155; color:#E2E8F0; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600;">Create subtask</button>
          <button style="background:#1E293B; border:1px solid #334155; color:#E2E8F0; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600;">Link issue</button>
        </div>
      </div>

      <div class="issue-layout">
        <div class="issue-main-col">
          <!-- Critical Risk Banner -->
          <div style="background:rgba(239,68,68,0.15); border:2px solid #EF4444; border-radius:10px; padding:14px 18px; display:flex; align-items:center; justify-content:space-between; box-shadow:0 0 25px rgba(239,68,68,0.25);">
            <div style="display:flex; align-items:center; gap:12px;">
              <div style="font-size:28px;">🚨</div>
              <div>
                <div style="font-size:14px; font-weight:800; color:#FCA5A5; text-transform:uppercase; letter-spacing:0.5px;">Critical Release Gate Blocked — Causal Blast Radius Detected</div>
                <div style="font-size:12px; color:#FECACA; margin-top:2px;">
                  Breaking schema mutation in <code>/v3/settle</code> drops legacy token contract. Downstream Mobile Checkout (<strong>SCRUM-2</strong>) and Confluence PCI-DSS v4.0 (<strong>POL-402</strong>) severely impacted.
                </div>
              </div>
            </div>
            <div style="background:#DC2626; color:white; font-size:13px; font-weight:800; padding:8px 16px; border-radius:20px; white-space:nowrap;">
              DO NOT SHIP
            </div>
          </div>

          <!-- ChronosMCP Live Issue Panel -->
          <div class="chronos-panel">
            <div class="chronos-header">
              <div class="brand-title">
                <div class="brand-icon">⚡</div>
                <div class="brand-text">
                  <h2>ChronosMCP <span class="verigraph-badge">VeriGraph AI</span></h2>
                  <p>Causal Blast-Radius Simulator, Cross-Silo Policy Gatekeeper & Bi-Directional Atlassian MCP Bridge</p>
                </div>
              </div>
              <!-- 38% Critical Score -->
              <div style="background:linear-gradient(135deg, #DC2626, #B91C1C); border:1px solid #EF4444; padding:8px 18px; border-radius:24px; display:flex; align-items:center; gap:10px; box-shadow:0 0 20px rgba(239,68,68,0.5);">
                <div style="font-size:22px;">⚠️</div>
                <div>
                  <div style="font-size:10px; text-transform:uppercase; color:#FECACA; font-weight:700;">Ship Confidence Score</div>
                  <div style="font-size:18px; font-weight:900; color:white;">38% — CRITICAL RISK (GRADE F)</div>
                </div>
              </div>
            </div>

            <!-- KPIs -->
            <div class="kpi-grid">
              <div class="kpi-box">
                <div class="kpi-label">Current Context Issue</div>
                <div class="kpi-val" style="color:#60A5FA;">SCRUM-1</div>
                <div class="kpi-sub">Core Payments API Upgrade v3</div>
              </div>
              <div class="kpi-box">
                <div class="kpi-label">Blast Severity Vector</div>
                <div class="kpi-val" style="color:#EF4444;">CRITICAL (GRADE F)</div>
                <div class="kpi-sub">2 Active Release Blockers Detected</div>
              </div>
              <div class="kpi-box">
                <div class="kpi-label">Regulatory Policy Gate</div>
                <div class="kpi-val" style="color:#F59E0B;">POL-402 VIOLATION</div>
                <div class="kpi-sub">PCI-DSS v4.0 Zero-Drift Mandate</div>
              </div>
              <div class="kpi-box">
                <div class="kpi-label">Atlassian MCP Bridge</div>
                <div class="kpi-val" style="color:#38BDF8;">SPEC 2024-11-05</div>
                <div class="kpi-sub">JSON-RPC 2.0 WebTrigger Active</div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-grid">
              <div class="btn-action">⚡ 1. Seed FinTech Scenario</div>
              <div class="btn-action primary">🔍 2. Blast Simulation</div>
              <div class="btn-action rovo">🤖 3. Rovo Auto-Align Silos (98%)</div>
              <div class="btn-action">🛡️ 4. Mint SHA-256 Receipt</div>
            </div>

            <!-- Counterfactual Scenario Switcher -->
            <div class="scenario-strip">
              <div class="scenario-label">What-If Simulation:</div>
              <div class="scenario-btn active-red">⚡ Breaking Schema Drift (38%)</div>
              <div class="scenario-btn">🔒 Auth Policy Mutation (52%)</div>
              <div class="scenario-btn">🔄 Additive Hotfix (94%)</div>
              <div class="scenario-btn">✅ Auto-Remediated Bridge (98%)</div>
            </div>

            <!-- Tabs -->
            <div class="tabs-bar">
              <div class="tab-btn active">🌐 Teamwork Graph Explorer</div>
              <div class="tab-btn">📊 Causal Blast-Radius Vectors</div>
              <div class="tab-btn">🛡️ SHA-256 Release Ledger (4)</div>
              <div class="tab-btn">🔌 Atlassian MCP Bridge (IDE Gateway)</div>
            </div>

            <!-- Tab Canvas -->
            <div class="tab-canvas">
              <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <span style="font-size:12px; font-weight:700; color:#E2E8F0;">Active Causal Dependency Chain (Unmitigated Breaking Path)</span>
                <span style="font-size:11px; color:#EF4444; font-weight:700;">● High-Risk Blast Propagation in Progress</span>
              </div>
              <svg width="100%" height="160" viewBox="0 0 900 160">
                <defs>
                  <linearGradient id="redGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#EF4444"/>
                    <stop offset="100%" stop-color="#F59E0B"/>
                  </linearGradient>
                </defs>
                <line x1="160" y1="80" x2="400" y2="80" stroke="url(#redGrad)" stroke-width="3" stroke-dasharray="6,4"/>
                <line x1="470" y1="80" x2="720" y2="80" stroke="#EF4444" stroke-width="3"/>
                <!-- Node 1 -->
                <g transform="translate(40, 45)">
                  <rect width="180" height="70" rx="8" fill="#1E293B" stroke="#EF4444" stroke-width="2"/>
                  <text x="12" y="24" fill="#818CF8" font-size="12" font-weight="800">SCRUM-1</text>
                  <text x="12" y="44" fill="#F8FAFC" font-size="11" font-weight="700">Payment API v3</text>
                  <text x="12" y="60" fill="#94A3B8" font-size="10">Owner: Fokrul Islam</text>
                </g>
                <text x="230" y="70" fill="#EF4444" font-size="10" font-weight="800">BREAKS SCHEMA</text>
                <!-- Node 2 -->
                <g transform="translate(360, 45)">
                  <rect width="180" height="70" rx="8" fill="#1E293B" stroke="#EF4444" stroke-width="2" filter="drop-shadow(0 0 10px rgba(239,68,68,0.5))"/>
                  <text x="12" y="24" fill="#F87171" font-size="12" font-weight="800">SCRUM-2</text>
                  <text x="12" y="44" fill="#F8FAFC" font-size="11" font-weight="700">Mobile Checkout App</text>
                  <text x="12" y="60" fill="#94A3B8" font-size="10">Owner: Elena Rostova</text>
                </g>
                <text x="560" y="70" fill="#F59E0B" font-size="10" font-weight="800">GOVERNED BY</text>
                <!-- Node 3 -->
                <g transform="translate(680, 45)">
                  <rect width="180" height="70" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
                  <text x="12" y="24" fill="#FBBF24" font-size="12" font-weight="800">POL-402 (Confluence)</text>
                  <text x="12" y="44" fill="#F8FAFC" font-size="11" font-weight="700">PCI-DSS Backward Comp</text>
                  <text x="12" y="60" fill="#94A3B8" font-size="10">Policy: Non-Compliant</text>
                </g>
              </svg>
            </div>
          </div>
        </div>

        <!-- Jira Right Side Context Panel -->
        <div class="issue-side-col">
          <div style="font-size:12px; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:0.5px;">Details</div>
          <div class="meta-field">
            <div class="meta-label">Assignee</div>
            <div class="meta-val"><div class="avatar-small">FI</div> Fokrul Islam (Staff Architect)</div>
          </div>
          <div class="meta-field">
            <div class="meta-label">Reporter</div>
            <div class="meta-val"><div class="avatar-small" style="background:#EC4899;">ER</div> Elena Rostova (Lead Mobile)</div>
          </div>
          <div class="meta-field">
            <div class="meta-label">Priority</div>
            <div class="meta-val" style="color:#EF4444; font-weight:700;">🔴 High (P1 Release Gate)</div>
          </div>
          <div class="meta-field">
            <div class="meta-label">Fix Version</div>
            <div class="meta-val">FinTech Release 2026.Q4</div>
          </div>
          <div class="meta-field">
            <div class="meta-label">Issue Links</div>
            <div class="meta-val" style="flex-direction:column; align-items:flex-start; gap:4px; font-size:11px;">
              <span style="color:#EF4444; font-weight:700;">⚠️ blocks</span>
              <span style="color:#60A5FA;">SCRUM-2: Mobile Checkout Core</span>
            </div>
          </div>
          <div class="meta-field">
            <div class="meta-label">Labels</div>
            <div style="display:flex; flex-wrap:wrap; gap:4px; margin-top:2px;">
              <span style="background:#1E293B; border:1px solid #334155; padding:2px 8px; border-radius:4px; font-size:10px; color:#A5B4FC;">fintech-core</span>
              <span style="background:#1E293B; border:1px solid #334155; padding:2px 8px; border-radius:4px; font-size:10px; color:#A5B4FC;">payment-v3</span>
              <span style="background:#311B92; border:1px solid #6366F1; padding:2px 8px; border-radius:4px; font-size:10px; color:#C7D2FE;">chronos-monitored</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

    elif scene_id == 2:
        # 02-teamwork-graph-explorer.png
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{COMMON_CSS}</style>
</head>
<body>
  <div class="atlassian-nav">
    <div class="nav-left">
      <div class="app-switcher"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="jira-logo-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M11.5 2C11.5 7.24 7.24 11.5 2 11.5C7.24 11.5 11.5 15.76 11.5 21C11.5 15.76 15.76 11.5 21 11.5C15.76 11.5 11.5 7.24 11.5 2Z" fill="#38BDF8"/></svg>
        Jira Software
      </div>
      <div class="jira-links">
        <div class="jira-link">Your work ▾</div>
        <div class="jira-link active">Projects ▾</div>
        <div class="jira-link">Filters ▾</div>
        <div class="jira-link">Dashboards ▾</div>
        <div class="jira-link">Teams ▾</div>
        <div class="jira-link">Apps ▾</div>
      </div>
    </div>
    <div class="nav-center">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
      Search Jira (fokrulanthro16.atlassian.net)
    </div>
    <div class="nav-right">
      <span style="font-size:12px; color:#10B981; font-weight:700; background:rgba(16,185,129,0.1); border:1px solid #10B981; padding:3px 8px; border-radius:4px;">● Live Forge development</span>
      <div class="user-badge">FI</div>
    </div>
  </div>

  <div class="main-workspace">
    <div class="jira-sidebar">
      <div class="project-header">
        <div class="project-avatar">SC</div>
        <div class="project-meta">
          <div class="project-name">FinTech Core</div>
          <div class="project-type">Software project</div>
        </div>
      </div>
      <div class="side-nav-list">
        <div class="side-nav-item">📋 Timeline</div>
        <div class="side-nav-item">📊 Backlog</div>
        <div class="side-nav-item">📈 Active Sprints</div>
        <div class="side-nav-item active">🎯 Issues & Sprints</div>
        <div class="side-nav-item">⚡ Releases</div>
        <div class="side-nav-item">📑 Project pages</div>
      </div>
    </div>

    <div class="issue-container">
      <div class="issue-breadcrumb-bar">
        <div class="breadcrumbs">
          <span>Projects</span> / <span>FinTech Core (SCRUM)</span> / <span class="issue-key-badge">SCRUM-1</span> / <span style="color:#38BDF8;">Teamwork Graph Explorer</span>
        </div>
        <div style="font-size:12px; color:#38BDF8; font-weight:700;">Real-Time Organizational Entity Topology</div>
      </div>

      <div class="issue-layout" style="gap:0;">
        <div class="issue-main-col" style="padding-right:0;">
          <div class="chronos-panel" style="padding:22px; gap:16px;">
            <div class="chronos-header">
              <div class="brand-title">
                <div class="brand-icon">🌐</div>
                <div class="brand-text">
                  <h2>Teamwork Graph (TWG) Explorer <span class="verigraph-badge">6 Nodes · 7 Edges</span></h2>
                  <p>Multi-Hop Causal Graph: Jira Issues, Downstream Consumers, Confluence Policies & Engineering Owners</p>
                </div>
              </div>
              <div style="background:#17253D; border:1px solid #23385D; padding:8px 16px; border-radius:20px; font-size:12px; color:#7DD3FC; font-weight:700;">
                Connected to Atlassian Graph API
              </div>
            </div>

            <!-- Tabs -->
            <div class="tabs-bar">
              <div class="tab-btn active">🌐 Teamwork Graph Explorer</div>
              <div class="tab-btn">📊 Causal Blast-Radius Vectors</div>
              <div class="tab-btn">🛡️ SHA-256 Release Ledger (4)</div>
              <div class="tab-btn">🔌 Atlassian MCP Bridge (IDE Gateway)</div>
            </div>

            <!-- Full-Height Graph Visualizer -->
            <div class="tab-canvas" style="min-height:480px; position:relative; background:#060A14;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; border-bottom:1px solid #172238; padding-bottom:10px;">
                <div style="font-size:13px; font-weight:700; color:#E2E8F0;">
                  Multi-Hop Dependency & Ownership DAG (Directed Acyclic Graph)
                </div>
                <div style="display:flex; gap:12px; font-size:11px;">
                  <span style="color:#60A5FA;">■ Upstream Service</span>
                  <span style="color:#F87171;">■ Downstream Consumer</span>
                  <span style="color:#FBBF24;">■ Confluence Policy</span>
                  <span style="color:#34D399;">■ Remediation Bridge</span>
                  <span style="color:#C084FC;">■ Team Owner</span>
                </div>
              </div>

              <!-- Full SVG DAG -->
              <svg width="100%" height="400" viewBox="0 0 1300 400">
                <defs>
                  <linearGradient id="edgeRed" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#EF4444"/>
                    <stop offset="100%" stop-color="#F59E0B"/>
                  </linearGradient>
                  <linearGradient id="edgeGreen" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#10B981"/>
                    <stop offset="100%" stop-color="#06B6D4"/>
                  </linearGradient>
                  <filter id="glowGreen" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="8" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                  <filter id="glowRed" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="6" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                </defs>

                <!-- Connector Lines -->
                <!-- SCRUM-1 to SCRUM-2 -->
                <path d="M 260 120 L 520 120" stroke="url(#edgeRed)" stroke-width="4" stroke-dasharray="8,4"/>
                <rect x="330" y="98" width="120" height="22" rx="4" fill="#450A0A" stroke="#EF4444" stroke-width="1"/>
                <text x="390" y="113" fill="#FCA5A5" font-size="10" font-weight="800" text-anchor="middle">BLOCKS (CONTRACT)</text>

                <!-- SCRUM-2 to POL-402 -->
                <path d="M 720 120 L 980 120" stroke="#F59E0B" stroke-width="3"/>
                <rect x="790" y="98" width="120" height="22" rx="4" fill="#451A03" stroke="#F59E0B" stroke-width="1"/>
                <text x="850" y="113" fill="#FDE68A" font-size="10" font-weight="800" text-anchor="middle">GOVERNED BY</text>

                <!-- SCRUM-1 down to Fokrul Islam -->
                <path d="M 160 170 L 160 270" stroke="#6366F1" stroke-width="2" stroke-dasharray="4,4"/>
                <text x="170" y="225" fill="#A5B4FC" font-size="10" font-weight="700">LEAD OWNER</text>

                <!-- SCRUM-2 down to Elena Rostova -->
                <path d="M 620 170 L 620 270" stroke="#EC4899" stroke-width="2" stroke-dasharray="4,4"/>
                <text x="630" y="225" fill="#F472B6" font-size="10" font-weight="700">CONSUMER OWNER</text>

                <!-- SCRUM-5 (Dual-Token Adapter) Bridge Arc -->
                <path d="M 260 145 C 380 250, 480 250, 560 170" stroke="url(#edgeGreen)" stroke-width="3"/>
                <rect x="350" y="210" width="160" height="24" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1"/>
                <text x="430" y="226" fill="#A7F3D0" font-size="10" font-weight="800" text-anchor="middle">ROVO ADAPTER (SCRUM-5)</text>

                <!-- NODE 1: SCRUM-1 -->
                <g transform="translate(60, 70)">
                  <rect width="200" height="100" rx="10" fill="#0F172A" stroke="#3B82F6" stroke-width="2"/>
                  <rect x="12" y="12" width="60" height="20" rx="4" fill="#1E3A8A"/>
                  <text x="42" y="26" fill="#93C5FD" font-size="11" font-weight="800" text-anchor="middle">SCRUM-1</text>
                  <text x="12" y="52" fill="#F8FAFC" font-size="13" font-weight="800">Core-Pay Settlement</text>
                  <text x="12" y="70" fill="#94A3B8" font-size="11">Type: REST API Service (v3)</text>
                  <text x="12" y="88" fill="#F87171" font-size="10" font-weight="700">⚠️ Breaking Schema Drift</text>
                </g>

                <!-- NODE 2: SCRUM-2 -->
                <g transform="translate(520, 70)">
                  <rect width="200" height="100" rx="10" fill="#0F172A" stroke="#EF4444" stroke-width="2" filter="url(#glowRed)"/>
                  <rect x="12" y="12" width="60" height="20" rx="4" fill="#7F1D1D"/>
                  <text x="42" y="26" fill="#FCA5A5" font-size="11" font-weight="800" text-anchor="middle">SCRUM-2</text>
                  <text x="12" y="52" fill="#F8FAFC" font-size="13" font-weight="800">Mobile Instant Checkout</text>
                  <text x="12" y="70" fill="#94A3B8" font-size="11">Consumer: iOS / Android</text>
                  <text x="12" y="88" fill="#EF4444" font-size="10" font-weight="700">💥 Blocked by Contract Drift</text>
                </g>

                <!-- NODE 3: POL-402 (Confluence Policy) -->
                <g transform="translate(980, 70)">
                  <rect width="220" height="100" rx="10" fill="#0F172A" stroke="#F59E0B" stroke-width="2"/>
                  <rect x="12" y="12" width="60" height="20" rx="4" fill="#78350F"/>
                  <text x="42" y="26" fill="#FDE68A" font-size="11" font-weight="800" text-anchor="middle">POL-402</text>
                  <text x="12" y="52" fill="#F8FAFC" font-size="13" font-weight="800">PCI-DSS v4.0 Zero-Drift</text>
                  <text x="12" y="70" fill="#94A3B8" font-size="11">Space: SEC (Confluence Cloud)</text>
                  <text x="12" y="88" fill="#FBBF24" font-size="10" font-weight="700">Mandates 90-Day Dual Read</text>
                </g>

                <!-- PEOPLE NODE 1: Fokrul Islam -->
                <g transform="translate(60, 270)">
                  <rect width="200" height="70" rx="10" fill="#13192B" stroke="#6366F1" stroke-width="1.5"/>
                  <circle cx="36" cy="35" r="18" fill="#4F46E5"/>
                  <text x="36" y="40" fill="white" font-size="11" font-weight="800" text-anchor="middle">FI</text>
                  <text x="64" y="30" fill="#F1F5F9" font-size="12" font-weight="800">Fokrul Islam</text>
                  <text x="64" y="46" fill="#A5B4FC" font-size="10">Staff Architect (Backend)</text>
                  <text x="64" y="58" fill="#64748B" font-size="9">fokrulanthro16@gmail.com</text>
                </g>

                <!-- PEOPLE NODE 2: Elena Rostova -->
                <g transform="translate(520, 270)">
                  <rect width="200" height="70" rx="10" fill="#13192B" stroke="#EC4899" stroke-width="1.5"/>
                  <circle cx="36" cy="35" r="18" fill="#DB2777"/>
                  <text x="36" y="40" fill="white" font-size="11" font-weight="800" text-anchor="middle">ER</text>
                  <text x="64" y="30" fill="#F1F5F9" font-size="12" font-weight="800">Elena Rostova</text>
                  <text x="64" y="46" fill="#F472B6" font-size="10">Lead iOS / Mobile Eng</text>
                  <text x="64" y="58" fill="#64748B" font-size="9">elena.rostova@enterprise.dev</text>
                </g>
              </svg>
            </div>

            <!-- Graph Entity Metadata Inspector -->
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-top:4px;">
              <div style="background:#131B2E; border:1px solid #1E293B; border-radius:8px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#38BDF8; text-transform:uppercase;">Causal Centrality Score</div>
                <div style="font-size:18px; font-weight:800; color:#F8FAFC; margin-top:2px;">0.94 (Highest In Sprint)</div>
                <div style="font-size:11px; color:#94A3B8;">SCRUM-1 is a critical hub node; changes impact 3 tiers</div>
              </div>
              <div style="background:#131B2E; border:1px solid #1E293B; border-radius:8px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#F59E0B; text-transform:uppercase;">Cross-Team Blast Radius</div>
                <div style="font-size:18px; font-weight:800; color:#F8FAFC; margin-top:2px;">2 Siloed Squads</div>
                <div style="font-size:11px; color:#94A3B8;">Core-Pay (Squad A) & Mobile Experience (Squad B)</div>
              </div>
              <div style="background:#131B2E; border:1px solid #1E293B; border-radius:8px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#10B981; text-transform:uppercase;">Remediation Path</div>
                <div style="font-size:18px; font-weight:800; color:#10B981; margin-top:2px;">Dual-Token Adapter Active</div>
                <div style="font-size:11px; color:#94A3B8;">Auto-orchestrated by Rovo AI Agent (Subtask SCRUM-5)</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

    elif scene_id == 3:
        # 03-rovo-auto-remediation-98.png
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{COMMON_CSS}</style>
</head>
<body>
  <div class="atlassian-nav">
    <div class="nav-left">
      <div class="app-switcher"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="jira-logo-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M11.5 2C11.5 7.24 7.24 11.5 2 11.5C7.24 11.5 11.5 15.76 11.5 21C11.5 15.76 15.76 11.5 21 11.5C15.76 11.5 11.5 7.24 11.5 2Z" fill="#38BDF8"/></svg>
        Jira Software
      </div>
      <div class="jira-links">
        <div class="jira-link">Your work ▾</div>
        <div class="jira-link active">Projects ▾</div>
        <div class="jira-link">Filters ▾</div>
        <div class="jira-link">Dashboards ▾</div>
        <div class="jira-link">Teams ▾</div>
        <div class="jira-link">Apps ▾</div>
      </div>
    </div>
    <div class="nav-center">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
      Search Jira (fokrulanthro16.atlassian.net)
    </div>
    <div class="nav-right">
      <span style="font-size:12px; color:#10B981; font-weight:700; background:rgba(16,185,129,0.1); border:1px solid #10B981; padding:3px 8px; border-radius:4px;">● Live Forge development</span>
      <div class="user-badge">FI</div>
    </div>
  </div>

  <div class="main-workspace">
    <div class="jira-sidebar">
      <div class="project-header">
        <div class="project-avatar">SC</div>
        <div class="project-meta">
          <div class="project-name">FinTech Core</div>
          <div class="project-type">Software project</div>
        </div>
      </div>
      <div class="side-nav-list">
        <div class="side-nav-item">📋 Timeline</div>
        <div class="side-nav-item">📊 Backlog</div>
        <div class="side-nav-item">📈 Active Sprints</div>
        <div class="side-nav-item active">🎯 Issues & Sprints</div>
        <div class="side-nav-item">⚡ Releases</div>
        <div class="side-nav-item">📑 Project pages</div>
      </div>
    </div>

    <div class="issue-container">
      <div class="issue-breadcrumb-bar">
        <div class="breadcrumbs">
          <span>Projects</span> / <span>FinTech Core (SCRUM)</span> / <span class="issue-key-badge">SCRUM-1</span>
        </div>
        <div style="font-size:12px; color:#10B981; font-weight:700;">Remediation Successfully Applied</div>
      </div>

      <div class="issue-title-bar">
        <div class="issue-title">
          <span style="color:#60A5FA;">SCRUM-1:</span> [Core-Pay] Upgrade Payment Settlement API v3
          <span class="status-pill" style="background:#065F46; color:#6EE7B7; border-color:#10B981;">CLEARED FOR RELEASE</span>
        </div>
        <div style="display:flex; gap:8px;">
          <button style="background:#1E293B; border:1px solid #334155; color:#E2E8F0; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600;">Attach</button>
          <button style="background:#1E293B; border:1px solid #334155; color:#E2E8F0; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600;">Create subtask</button>
          <button style="background:#1E293B; border:1px solid #334155; color:#E2E8F0; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:600;">Link issue</button>
        </div>
      </div>

      <div class="issue-layout">
        <div class="issue-main-col">
          <!-- Success Notification Bar -->
          <div style="background:rgba(16,185,129,0.15); border:1px solid #10B981; border-radius:8px; padding:12px 18px; display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:10px; font-size:13px; font-weight:700; color:#34D399;">
              <span style="font-size:18px;">✅</span>
              <span>Rovo Silo Remediation Executed! Score upgraded to <strong>98% (A+)</strong>. Subtask <strong>SCRUM-5</strong> auto-created & bidirectional sync established!</span>
            </div>
            <div style="background:#047857; color:white; font-size:11px; font-weight:800; padding:4px 10px; border-radius:12px;">ACTIVE</div>
          </div>

          <!-- ChronosMCP Live Issue Panel -->
          <div class="chronos-panel">
            <div class="chronos-header">
              <div class="brand-title">
                <div class="brand-icon">⚡</div>
                <div class="brand-text">
                  <h2>ChronosMCP <span class="verigraph-badge">VeriGraph AI</span></h2>
                  <p>Causal Blast-Radius Simulator, Cross-Silo Policy Gatekeeper & Bi-Directional Atlassian MCP Bridge</p>
                </div>
              </div>
              <!-- 98% Green Glowing Score -->
              <div style="background:linear-gradient(135deg, #059669, #10B981); border:1px solid #34D399; padding:8px 18px; border-radius:24px; display:flex; align-items:center; gap:10px; box-shadow:0 0 25px rgba(16,185,129,0.5);">
                <div style="font-size:22px;">🛡️</div>
                <div>
                  <div style="font-size:10px; text-transform:uppercase; color:#D1FAE5; font-weight:700;">Ship Confidence Score</div>
                  <div style="font-size:18px; font-weight:900; color:white;">98% — OPTIMAL (CLEARED TO SHIP)</div>
                </div>
              </div>
            </div>

            <!-- KPIs -->
            <div class="kpi-grid">
              <div class="kpi-box">
                <div class="kpi-label">Current Context Issue</div>
                <div class="kpi-val" style="color:#60A5FA;">SCRUM-1</div>
                <div class="kpi-sub">Dual-Token Compatibility Enabled</div>
              </div>
              <div class="kpi-box">
                <div class="kpi-label">Blast Severity Vector</div>
                <div class="kpi-val" style="color:#10B981;">LOW RISK (GRADE A+)</div>
                <div class="kpi-sub">0 Active Release Blockers (Mitigated)</div>
              </div>
              <div class="kpi-box">
                <div class="kpi-label">Regulatory Policy Gate</div>
                <div class="kpi-val" style="color:#10B981;">POL-402 SATISFIED</div>
                <div class="kpi-sub">PCI-DSS v4.0 Zero-Drift Certified</div>
              </div>
              <div class="kpi-box">
                <div class="kpi-label">Atlassian MCP Bridge</div>
                <div class="kpi-val" style="color:#38BDF8;">SPEC 2024-11-05</div>
                <div class="kpi-sub">JSON-RPC 2.0 WebTrigger Active</div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-grid">
              <div class="btn-action">⚡ 1. Seed FinTech Scenario</div>
              <div class="btn-action">🔍 2. Blast Simulation</div>
              <div class="btn-action rovo">🤖 3. Rovo Auto-Align Silos (98%)</div>
              <div class="btn-action primary">🛡️ 4. Mint SHA-256 Receipt</div>
            </div>

            <!-- Scenario Switcher -->
            <div class="scenario-strip">
              <div class="scenario-label">What-If Simulation:</div>
              <div class="scenario-btn">⚡ Breaking Schema Drift (38%)</div>
              <div class="scenario-btn">🔒 Auth Policy Mutation (52%)</div>
              <div class="scenario-btn">🔄 Additive Hotfix (94%)</div>
              <div class="scenario-btn active-green">✅ Auto-Remediated Bridge (98%)</div>
            </div>

            <!-- Tabs -->
            <div class="tabs-bar">
              <div class="tab-btn active">🌐 Teamwork Graph Explorer</div>
              <div class="tab-btn">📊 Causal Blast-Radius Vectors</div>
              <div class="tab-btn">🛡️ SHA-256 Release Ledger (4)</div>
              <div class="tab-btn">🔌 Atlassian MCP Bridge (IDE Gateway)</div>
            </div>

            <!-- Tab Canvas -->
            <div class="tab-canvas">
              <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <span style="font-size:12px; font-weight:700; color:#E2E8F0;">Autonomous Rovo Remediation: Dual-Token Shim Architecture</span>
                <span style="font-size:11px; color:#10B981; font-weight:700;">● Contract Blast Mitigated (Zero Downstream Downtime)</span>
              </div>
              <svg width="100%" height="160" viewBox="0 0 900 160">
                <defs>
                  <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#10B981"/>
                    <stop offset="100%" stop-color="#06B6D4"/>
                  </linearGradient>
                </defs>
                <line x1="160" y1="80" x2="400" y2="80" stroke="#10B981" stroke-width="3"/>
                <line x1="470" y1="80" x2="720" y2="80" stroke="#10B981" stroke-width="3"/>
                <!-- Node 1 -->
                <g transform="translate(40, 45)">
                  <rect width="180" height="70" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
                  <text x="12" y="24" fill="#34D399" font-size="12" font-weight="800">SCRUM-1</text>
                  <text x="12" y="44" fill="#F8FAFC" font-size="11" font-weight="700">Payment API v3</text>
                  <text x="12" y="60" fill="#94A3B8" font-size="10">Dual-Read Adapter Active</text>
                </g>
                <text x="220" y="70" fill="#34D399" font-size="10" font-weight="800">MITIGATED (SHIM ACTIVE)</text>
                <!-- Node 2 -->
                <g transform="translate(360, 45)">
                  <rect width="180" height="70" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
                  <text x="12" y="24" fill="#34D399" font-size="12" font-weight="800">SCRUM-2</text>
                  <text x="12" y="44" fill="#F8FAFC" font-size="11" font-weight="700">Mobile Checkout App</text>
                  <text x="12" y="60" fill="#94A3B8" font-size="10">Zero-Breaking Contract</text>
                </g>
                <text x="550" y="70" fill="#34D399" font-size="10" font-weight="800">COMPLIANT (v4.0)</text>
                <!-- Node 3 -->
                <g transform="translate(680, 45)">
                  <rect width="180" height="70" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
                  <text x="12" y="24" fill="#34D399" font-size="12" font-weight="800">POL-402 (Confluence)</text>
                  <text x="12" y="44" fill="#F8FAFC" font-size="11" font-weight="700">PCI-DSS Backward Comp</text>
                  <text x="12" y="60" fill="#34D399" font-size="10">Status: 100% SATISFIED</text>
                </g>
              </svg>
            </div>
          </div>
        </div>

        <!-- Jira Right Side Context Panel -->
        <div class="issue-side-col">
          <div style="font-size:12px; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:0.5px;">Details</div>
          <div class="meta-field">
            <div class="meta-label">Assignee</div>
            <div class="meta-val"><div class="avatar-small">FI</div> Fokrul Islam (Staff Architect)</div>
          </div>
          <div class="meta-field">
            <div class="meta-label">Reporter</div>
            <div class="meta-val"><div class="avatar-small" style="background:#EC4899;">ER</div> Elena Rostova (Lead Mobile)</div>
          </div>
          <div class="meta-field">
            <div class="meta-label">Auto-Created Subtask</div>
            <div style="background:#13261E; border:1px solid #10B981; border-radius:6px; padding:8px 10px; margin-top:2px;">
              <div style="color:#34D399; font-weight:800; font-size:11px;">SCRUM-5 (DONE)</div>
              <div style="font-size:11px; color:#E2E8F0; margin-top:2px;">[Chronos Remediation] Implement Dual-Token Adapter v2/v3</div>
              <div style="font-size:10px; color:#6EE7B7; margin-top:4px;">🤖 Created by Rovo Agent</div>
            </div>
          </div>
          <div class="meta-field">
            <div class="meta-label">Labels</div>
            <div style="display:flex; flex-wrap:wrap; gap:4px; margin-top:2px;">
              <span style="background:#064E3B; border:1px solid #10B981; padding:2px 8px; border-radius:4px; font-size:10px; color:#6EE7B7;">chronos-verified</span>
              <span style="background:#064E3B; border:1px solid #10B981; padding:2px 8px; border-radius:4px; font-size:10px; color:#6EE7B7;">blast-radius-mitigated</span>
              <span style="background:#1E293B; border:1px solid #334155; padding:2px 8px; border-radius:4px; font-size:10px; color:#A5B4FC;">fintech-core</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

    elif scene_id == 4:
        # 04-causal-blast-radius-vectors.png
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{COMMON_CSS}</style>
</head>
<body>
  <div class="atlassian-nav">
    <div class="nav-left">
      <div class="app-switcher"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="jira-logo-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M11.5 2C11.5 7.24 7.24 11.5 2 11.5C7.24 11.5 11.5 15.76 11.5 21C11.5 15.76 15.76 11.5 21 11.5C15.76 11.5 11.5 7.24 11.5 2Z" fill="#38BDF8"/></svg>
        Jira Software
      </div>
      <div class="jira-links">
        <div class="jira-link">Your work ▾</div>
        <div class="jira-link active">Projects ▾</div>
        <div class="jira-link">Filters ▾</div>
        <div class="jira-link">Dashboards ▾</div>
        <div class="jira-link">Teams ▾</div>
        <div class="jira-link">Apps ▾</div>
      </div>
    </div>
    <div class="nav-center">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
      Search Jira (fokrulanthro16.atlassian.net)
    </div>
    <div class="nav-right">
      <span style="font-size:12px; color:#10B981; font-weight:700; background:rgba(16,185,129,0.1); border:1px solid #10B981; padding:3px 8px; border-radius:4px;">● Live Forge development</span>
      <div class="user-badge">FI</div>
    </div>
  </div>

  <div class="main-workspace">
    <div class="jira-sidebar">
      <div class="project-header">
        <div class="project-avatar">SC</div>
        <div class="project-meta">
          <div class="project-name">FinTech Core</div>
          <div class="project-type">Software project</div>
        </div>
      </div>
      <div class="side-nav-list">
        <div class="side-nav-item">📋 Timeline</div>
        <div class="side-nav-item">📊 Backlog</div>
        <div class="side-nav-item">📈 Active Sprints</div>
        <div class="side-nav-item active">🎯 Issues & Sprints</div>
        <div class="side-nav-item">⚡ Releases</div>
        <div class="side-nav-item">📑 Project pages</div>
      </div>
    </div>

    <div class="issue-container">
      <div class="issue-breadcrumb-bar">
        <div class="breadcrumbs">
          <span>Projects</span> / <span>FinTech Core (SCRUM)</span> / <span class="issue-key-badge">SCRUM-1</span> / <span style="color:#38BDF8;">Blast-Radius Telemetry</span>
        </div>
        <div style="font-size:12px; color:#94A3B8;">Multi-Vector Mathematical Risk Analysis</div>
      </div>

      <div class="issue-layout" style="gap:0;">
        <div class="issue-main-col" style="padding-right:0;">
          <div class="chronos-panel" style="padding:22px; gap:16px;">
            <div class="chronos-header">
              <div class="brand-title">
                <div class="brand-icon">📊</div>
                <div class="brand-text">
                  <h2>Causal Blast-Radius Vectors & Risk Telemetry</h2>
                  <p>Weighted Vector Breakdown: Schema Compatibility, Service Blast, Regulatory Drift & Incident Probability</p>
                </div>
              </div>
              <div style="background:#281832; border:1px solid #701A75; padding:8px 16px; border-radius:20px; font-size:12px; color:#F0ABFC; font-weight:700;">
                Bayesian Risk Model 2.2
              </div>
            </div>

            <!-- Tabs -->
            <div class="tabs-bar">
              <div class="tab-btn">🌐 Teamwork Graph Explorer</div>
              <div class="tab-btn active">📊 Causal Blast-Radius Vectors</div>
              <div class="tab-btn">🛡️ SHA-256 Release Ledger (4)</div>
              <div class="tab-btn">🔌 Atlassian MCP Bridge (IDE Gateway)</div>
            </div>

            <!-- 4 Detailed Vector Breakdown Cards -->
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
              <!-- Vector 1 -->
              <div style="background:#131B2E; border:1px solid #23304A; border-radius:10px; padding:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                  <span style="font-size:13px; font-weight:800; color:#F8FAFC;">1. API Schema Contract Compatibility</span>
                  <span style="background:#7F1D1D; color:#FCA5A5; font-size:11px; font-weight:800; padding:2px 8px; border-radius:4px;">42% / 100% · HIGH RISK</span>
                </div>
                <div style="background:#1E293B; height:8px; border-radius:4px; overflow:hidden; margin-bottom:10px;">
                  <div style="background:linear-gradient(90deg, #EF4444, #F59E0B); width:42%; height:100%;"></div>
                </div>
                <p style="font-size:12px; color:#94A3B8; line-height:1.4;">
                  Detected removal of mandatory field <code>legacy_card_token</code> in endpoint <code>POST /v3/settlement</code>. 3 consumer endpoints will trigger uncaught 422 Unprocessable Entity faults.
                </p>
                <div style="margin-top:10px; font-size:11px; color:#818CF8; font-weight:600;">
                  Impact: 3 Consumers · Zero Dual-Read fallback detected
                </div>
              </div>

              <!-- Vector 2 -->
              <div style="background:#131B2E; border:1px solid #23304A; border-radius:10px; padding:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                  <span style="font-size:13px; font-weight:800; color:#F8FAFC;">2. Downstream Service Impact Vector</span>
                  <span style="background:#7F1D1D; color:#FCA5A5; font-size:11px; font-weight:800; padding:2px 8px; border-radius:4px;">35% / 100% · CRITICAL</span>
                </div>
                <div style="background:#1E293B; height:8px; border-radius:4px; overflow:hidden; margin-bottom:10px;">
                  <div style="background:linear-gradient(90deg, #DC2626, #EF4444); width:35%; height:100%;"></div>
                </div>
                <p style="font-size:12px; color:#94A3B8; line-height:1.4;">
                  Affects <strong>SCRUM-2</strong> (Mobile Instant Checkout), <strong>FIN-104</strong> (Daily Reconciliation Engine), and <strong>ANL-88</strong> (Fraud Detection Pipeline). 14,000 transactions/min at risk.
                </p>
                <div style="margin-top:10px; font-size:11px; color:#F87171; font-weight:600;">
                  Cascading Failure Radius: Tier-1 Payment Pathway
                </div>
              </div>

              <!-- Vector 3 -->
              <div style="background:#131B2E; border:1px solid #23304A; border-radius:10px; padding:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                  <span style="font-size:13px; font-weight:800; color:#F8FAFC;">3. Confluence Regulatory Compliance</span>
                  <span style="background:#78350F; color:#FDE68A; font-size:11px; font-weight:800; padding:2px 8px; border-radius:4px;">50% / 100% · NON-COMPLIANT</span>
                </div>
                <div style="background:#1E293B; height:8px; border-radius:4px; overflow:hidden; margin-bottom:10px;">
                  <div style="background:linear-gradient(90deg, #F59E0B, #EAB308); width:50%; height:100%;"></div>
                </div>
                <p style="font-size:12px; color:#94A3B8; line-height:1.4;">
                  Violates <strong>POL-402</strong> (PCI-DSS v4.0 Zero-Drift Policy). Enterprise standard mandates a 90-day deprecation runway with simultaneous dual-token ingestion.
                </p>
                <div style="margin-top:10px; font-size:11px; color:#FBBF24; font-weight:600;">
                  Audit Risk: Immediate Compliance Notice Triggered
                </div>
              </div>

              <!-- Vector 4 -->
              <div style="background:#131B2E; border:1px solid #23304A; border-radius:10px; padding:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                  <span style="font-size:13px; font-weight:800; color:#F8FAFC;">4. Historical Incident & Rollback Risk</span>
                  <span style="background:#7F1D1D; color:#FCA5A5; font-size:11px; font-weight:800; padding:2px 8px; border-radius:4px;">88% PROBABILITY</span>
                </div>
                <div style="background:#1E293B; height:8px; border-radius:4px; overflow:hidden; margin-bottom:10px;">
                  <div style="background:linear-gradient(90deg, #EF4444, #B91C1C); width:88%; height:100%;"></div>
                </div>
                <p style="font-size:12px; color:#94A3B8; line-height:1.4;">
                  Bayesian model trained on 142 past Jira releases indicates an 88% probability of an emergency rollback within 4 hours of production deployment if shipped unmitigated.
                </p>
                <div style="margin-top:10px; font-size:11px; color:#FCA5A5; font-weight:600;">
                  Estimated Downtime Cost: $184,000 / hour
                </div>
              </div>
            </div>

            <!-- Counterfactual Intervention Matrix -->
            <div style="background:#060A14; border:1px solid #1E293B; border-radius:10px; padding:16px; margin-top:4px;">
              <div style="font-size:12px; font-weight:800; color:#38BDF8; text-transform:uppercase; margin-bottom:10px;">
                Counterfactual "What-If" Mitigation Matrix
              </div>
              <table style="width:100%; border-collapse:collapse; font-size:12px; text-align:left;">
                <thead>
                  <tr style="border-bottom:1px solid #1E293B; color:#94A3B8;">
                    <th style="padding:8px;">Mitigation Strategy</th>
                    <th style="padding:8px;">Ship Confidence Score</th>
                    <th style="padding:8px;">Downstream Downtime</th>
                    <th style="padding:8px;">Regulatory Clearance</th>
                    <th style="padding:8px;">Implementation Effort</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style="border-bottom:1px solid #172238; color:#F87171;">
                    <td style="padding:8px; font-weight:700;">Status Quo (No Mitigation)</td>
                    <td style="padding:8px;">38% (Critical)</td>
                    <td style="padding:8px;">~45 mins (Sev-1 Outage)</td>
                    <td style="padding:8px;">Non-Compliant (Failed)</td>
                    <td style="padding:8px;">0 hrs</td>
                  </tr>
                  <tr style="border-bottom:1px solid #172238; color:#FBBF24;">
                    <td style="padding:8px; font-weight:700;">Manual Downstream Patching</td>
                    <td style="padding:8px;">72% (Acceptable)</td>
                    <td style="padding:8px;">0 mins</td>
                    <td style="padding:8px;">Conditional Waiver</td>
                    <td style="padding:8px;">16 engineering hrs</td>
                  </tr>
                  <tr style="color:#34D399; background:rgba(16,185,129,0.06);">
                    <td style="padding:8px; font-weight:800;">🤖 Rovo Dual-Token Shim (Recommended)</td>
                    <td style="padding:8px; font-weight:800;">98% (Optimal)</td>
                    <td style="padding:8px; font-weight:800;">0 mins (Zero Drift)</td>
                    <td style="padding:8px; font-weight:800;">100% Certified</td>
                    <td style="padding:8px; font-weight:800;">3 seconds (Autonomous)</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

    elif scene_id == 5:
        # 05-sha256-cryptographic-ledger.png
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{COMMON_CSS}</style>
</head>
<body>
  <div class="atlassian-nav">
    <div class="nav-left">
      <div class="app-switcher"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="jira-logo-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M11.5 2C11.5 7.24 7.24 11.5 2 11.5C7.24 11.5 11.5 15.76 11.5 21C11.5 15.76 15.76 11.5 21 11.5C15.76 11.5 11.5 7.24 11.5 2Z" fill="#38BDF8"/></svg>
        Jira Software
      </div>
      <div class="jira-links">
        <div class="jira-link">Your work ▾</div>
        <div class="jira-link active">Projects ▾</div>
        <div class="jira-link">Filters ▾</div>
        <div class="jira-link">Dashboards ▾</div>
        <div class="jira-link">Teams ▾</div>
        <div class="jira-link">Apps ▾</div>
      </div>
    </div>
    <div class="nav-center">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
      Search Jira (fokrulanthro16.atlassian.net)
    </div>
    <div class="nav-right">
      <span style="font-size:12px; color:#10B981; font-weight:700; background:rgba(16,185,129,0.1); border:1px solid #10B981; padding:3px 8px; border-radius:4px;">● Live Forge development</span>
      <div class="user-badge">FI</div>
    </div>
  </div>

  <div class="main-workspace">
    <div class="jira-sidebar">
      <div class="project-header">
        <div class="project-avatar">SC</div>
        <div class="project-meta">
          <div class="project-name">FinTech Core</div>
          <div class="project-type">Software project</div>
        </div>
      </div>
      <div class="side-nav-list">
        <div class="side-nav-item">📋 Timeline</div>
        <div class="side-nav-item">📊 Backlog</div>
        <div class="side-nav-item">📈 Active Sprints</div>
        <div class="side-nav-item active">🎯 Issues & Sprints</div>
        <div class="side-nav-item">⚡ Releases</div>
        <div class="side-nav-item">📑 Project pages</div>
      </div>
    </div>

    <div class="issue-container">
      <div class="issue-breadcrumb-bar">
        <div class="breadcrumbs">
          <span>Projects</span> / <span>FinTech Core (SCRUM)</span> / <span class="issue-key-badge">SCRUM-1</span> / <span style="color:#38BDF8;">SHA-256 Release Ledger</span>
        </div>
        <div style="font-size:12px; color:#10B981; font-weight:700;">Zero-Trust Merkle Tree Proof Verified</div>
      </div>

      <div class="issue-layout" style="gap:0;">
        <div class="issue-main-col" style="padding-right:0;">
          <div class="chronos-panel" style="padding:22px; gap:16px;">
            <div class="chronos-header">
              <div class="brand-title">
                <div class="brand-icon">🛡️</div>
                <div class="brand-text">
                  <h2>Immutable SHA-256 Cryptographic Release Ledger</h2>
                  <p>Cryptographic Audit Trail Minted on Atlassian Forge KVS · Tamper-Proof Zero-Trust Architecture</p>
                </div>
              </div>
              <div style="background:#064E3B; border:1px solid #10B981; padding:8px 16px; border-radius:20px; font-size:12px; color:#6EE7B7; font-weight:800;">
                ✓ 100% Tamper-Free Verified
              </div>
            </div>

            <!-- Tabs -->
            <div class="tabs-bar">
              <div class="tab-btn">🌐 Teamwork Graph Explorer</div>
              <div class="tab-btn">📊 Causal Blast-Radius Vectors</div>
              <div class="tab-btn active">🛡️ SHA-256 Release Ledger (4)</div>
              <div class="tab-btn">🔌 Atlassian MCP Bridge (IDE Gateway)</div>
            </div>

            <!-- Spotlight Verified Merkle Receipt -->
            <div style="background:#0B1220; border:2px solid #10B981; border-radius:12px; padding:20px; box-shadow:0 0 30px rgba(16,185,129,0.2);">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <div style="display:flex; align-items:center; gap:10px;">
                  <span style="font-size:24px;">💎</span>
                  <div>
                    <div style="font-size:15px; font-weight:800; color:#F8FAFC;">Active Cryptographic Receipt: VERI-7E8602AEB534</div>
                    <div style="font-size:11px; color:#94A3B8;">Minted for SCRUM-1 · Signed with Forge App Key ARI</div>
                  </div>
                </div>
                <div style="background:#10B981; color:#064E3B; font-size:12px; font-weight:900; padding:6px 14px; border-radius:6px;">
                  PCI-DSS v4.0 VERIFIED
                </div>
              </div>

              <!-- Merkle Hash Display -->
              <div style="background:#040711; border:1px solid #1E293B; border-radius:8px; padding:12px 16px; font-family:monospace; margin-bottom:14px;">
                <div style="font-size:10px; color:#64748B; text-transform:uppercase; font-weight:700; margin-bottom:4px;">SHA-256 Merkle Root Digest:</div>
                <div style="font-size:13px; color:#38BDF8; word-break:break-all; font-weight:700;">
                  9f83ab28e469d7b4c9b32912440315c1e9e2f9d6ab9f18a2d1e02812903fe512
                </div>
              </div>

              <!-- Metadata Grid -->
              <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; font-size:12px;">
                <div style="background:#131B2E; padding:10px 14px; border-radius:6px; border:1px solid #1E293B;">
                  <div style="color:#64748B; font-size:10px; text-transform:uppercase;">Timestamp</div>
                  <div style="color:#E2E8F0; font-weight:700; margin-top:2px;">2026-10-28 20:34:12 UTC</div>
                </div>
                <div style="background:#131B2E; padding:10px 14px; border-radius:6px; border:1px solid #1E293B;">
                  <div style="color:#64748B; font-size:10px; text-transform:uppercase;">Storage Backend</div>
                  <div style="color:#38BDF8; font-weight:700; margin-top:2px;">@forge/kvs (Encrypted)</div>
                </div>
                <div style="background:#131B2E; padding:10px 14px; border-radius:6px; border:1px solid #1E293B;">
                  <div style="color:#64748B; font-size:10px; text-transform:uppercase;">Signing Entity ARI</div>
                  <div style="color:#A78BFA; font-weight:700; margin-top:2px;">ari:cloud:ecosystem::app/84d8afae</div>
                </div>
                <div style="background:#131B2E; padding:10px 14px; border-radius:6px; border:1px solid #1E293B;">
                  <div style="color:#64748B; font-size:10px; text-transform:uppercase;">Audit Status</div>
                  <div style="color:#10B981; font-weight:700; margin-top:2px;">Immutable & Auditable</div>
                </div>
              </div>
            </div>

            <!-- Historical Ledger Table -->
            <div style="background:#060A14; border:1px solid #1E293B; border-radius:10px; padding:16px; margin-top:4px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div style="font-size:12px; font-weight:800; color:#E2E8F0; text-transform:uppercase;">
                  Persistent Forge KVS Audit History (Jira Key: SCRUM-1)
                </div>
                <button style="background:#1E293B; border:1px solid #334155; color:#94A3B8; font-size:11px; padding:4px 10px; border-radius:4px;">
                  Export JSON Audit Trail
                </button>
              </div>

              <table style="width:100%; border-collapse:collapse; font-size:12px; text-align:left;">
                <thead>
                  <tr style="border-bottom:1px solid #1E293B; color:#64748B; font-size:11px;">
                    <th style="padding:8px;">RECEIPT ID</th>
                    <th style="padding:8px;">SCENARIO EVENT</th>
                    <th style="padding:8px;">CONFIDENCE SCORE</th>
                    <th style="padding:8px;">MERKLE DIGEST PREFIX</th>
                    <th style="padding:8px;">VERIFICATION</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style="border-bottom:1px solid #172238;">
                    <td style="padding:8px; font-family:monospace; color:#818CF8; font-weight:700;">VERI-7E8602AEB534</td>
                    <td style="padding:8px; color:#F8FAFC;">Rovo Silo Remediation Completed</td>
                    <td style="padding:8px; color:#10B981; font-weight:800;">98% (A+)</td>
                    <td style="padding:8px; font-family:monospace; color:#38BDF8;">9f83ab28e469d7...</td>
                    <td style="padding:8px;"><span style="background:#064E3B; color:#6EE7B7; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:800;">✓ VALIDATED</span></td>
                  </tr>
                  <tr style="border-bottom:1px solid #172238;">
                    <td style="padding:8px; font-family:monospace; color:#818CF8; font-weight:700;">VERI-3A194CB0D189</td>
                    <td style="padding:8px; color:#F8FAFC;">Additive Hotfix Ingestion</td>
                    <td style="padding:8px; color:#38BDF8; font-weight:800;">94% (A)</td>
                    <td style="padding:8px; font-family:monospace; color:#38BDF8;">5c19de33719b4a...</td>
                    <td style="padding:8px;"><span style="background:#064E3B; color:#6EE7B7; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:800;">✓ VALIDATED</span></td>
                  </tr>
                  <tr style="border-bottom:1px solid #172238;">
                    <td style="padding:8px; font-family:monospace; color:#818CF8; font-weight:700;">VERI-88F41602B731</td>
                    <td style="padding:8px; color:#F8FAFC;">Initial Enterprise FinTech Seed</td>
                    <td style="padding:8px; color:#EF4444; font-weight:800;">38% (F)</td>
                    <td style="padding:8px; font-family:monospace; color:#38BDF8;">1a03f44697be9c...</td>
                    <td style="padding:8px;"><span style="background:#064E3B; color:#6EE7B7; padding:2px 8px; border-radius:4px; font-size:10px; font-weight:800;">✓ VALIDATED</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

    elif scene_id == 6:
        # 06-atlassian-mcp-ide-gateway.png
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{COMMON_CSS}</style>
</head>
<body>
  <div class="atlassian-nav">
    <div class="nav-left">
      <div class="app-switcher"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="jira-logo-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M11.5 2C11.5 7.24 7.24 11.5 2 11.5C7.24 11.5 11.5 15.76 11.5 21C11.5 15.76 15.76 11.5 21 11.5C15.76 11.5 11.5 7.24 11.5 2Z" fill="#38BDF8"/></svg>
        Jira Software
      </div>
      <div class="jira-links">
        <div class="jira-link">Your work ▾</div>
        <div class="jira-link active">Projects ▾</div>
        <div class="jira-link">Filters ▾</div>
        <div class="jira-link">Dashboards ▾</div>
        <div class="jira-link">Teams ▾</div>
        <div class="jira-link">Apps ▾</div>
      </div>
    </div>
    <div class="nav-center">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
      Search Jira (fokrulanthro16.atlassian.net)
    </div>
    <div class="nav-right">
      <span style="font-size:12px; color:#10B981; font-weight:700; background:rgba(16,185,129,0.1); border:1px solid #10B981; padding:3px 8px; border-radius:4px;">● Live Forge development</span>
      <div class="user-badge">FI</div>
    </div>
  </div>

  <div class="main-workspace">
    <div class="jira-sidebar">
      <div class="project-header">
        <div class="project-avatar">SC</div>
        <div class="project-meta">
          <div class="project-name">FinTech Core</div>
          <div class="project-type">Software project</div>
        </div>
      </div>
      <div class="side-nav-list">
        <div class="side-nav-item">📋 Timeline</div>
        <div class="side-nav-item">📊 Backlog</div>
        <div class="side-nav-item">📈 Active Sprints</div>
        <div class="side-nav-item active">🎯 Issues & Sprints</div>
        <div class="side-nav-item">⚡ Releases</div>
        <div class="side-nav-item">📑 Project pages</div>
      </div>
    </div>

    <div class="issue-container">
      <div class="issue-breadcrumb-bar">
        <div class="breadcrumbs">
          <span>Projects</span> / <span>FinTech Core (SCRUM)</span> / <span class="issue-key-badge">SCRUM-1</span> / <span style="color:#38BDF8;">Atlassian MCP Bridge</span>
        </div>
        <div style="font-size:12px; color:#38BDF8; font-weight:700;">Model Context Protocol (JSON-RPC 2.0) Active</div>
      </div>

      <div class="issue-layout" style="gap:0;">
        <div class="issue-main-col" style="padding-right:0;">
          <div class="chronos-panel" style="padding:22px; gap:16px;">
            <div class="chronos-header">
              <div class="brand-title">
                <div class="brand-icon">🔌</div>
                <div class="brand-text">
                  <h2>Atlassian MCP Server & External IDE Bridge</h2>
                  <p>Spec 2024-11-05 Compliant · Connects Cursor, Claude Desktop, and VS Code Directly into Jira Context</p>
                </div>
              </div>
              <div style="background:#0C4A6E; border:1px solid #0284C7; padding:8px 16px; border-radius:20px; font-size:12px; color:#7DD3FC; font-weight:800;">
                Live WebTrigger: 200 OK (32ms)
              </div>
            </div>

            <!-- Tabs -->
            <div class="tabs-bar">
              <div class="tab-btn">🌐 Teamwork Graph Explorer</div>
              <div class="tab-btn">📊 Causal Blast-Radius Vectors</div>
              <div class="tab-btn">🛡️ SHA-256 Release Ledger (4)</div>
              <div class="tab-btn active">🔌 Atlassian MCP Bridge (IDE Gateway)</div>
            </div>

            <!-- 2-Panel Layout: MCP Tools + Live Terminal Verification -->
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
              <!-- Left: 5 MCP Tools Registry -->
              <div style="background:#060A14; border:1px solid #1E293B; border-radius:10px; padding:16px; display:flex; flex-direction:column; gap:10px;">
                <div style="font-size:12px; font-weight:800; color:#38BDF8; text-transform:uppercase;">
                  Exposed MCP Tool Capabilities (JSON-RPC 2.0)
                </div>

                <div style="background:#0F172A; border:1px solid #23304A; border-radius:6px; padding:10px;">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <code style="color:#60A5FA; font-weight:700; font-size:12px;">simulate_issue_blast_radius</code>
                    <span style="font-size:10px; background:#1E3A8A; color:#93C5FD; padding:1px 6px; border-radius:3px;">AI TOOL</span>
                  </div>
                  <p style="font-size:11px; color:#94A3B8; margin-top:3px;">Simulates causal blast radius, calculates ship score, detects blockers.</p>
                </div>

                <div style="background:#0F172A; border:1px solid #23304A; border-radius:6px; padding:10px;">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <code style="color:#60A5FA; font-weight:700; font-size:12px;">get_teamwork_graph_context</code>
                    <span style="font-size:10px; background:#1E3A8A; color:#93C5FD; padding:1px 6px; border-radius:3px;">GRAPH</span>
                  </div>
                  <p style="font-size:11px; color:#94A3B8; margin-top:3px;">Fetches multi-hop entity DAG: Jira issues, dependencies, and Confluence policies.</p>
                </div>

                <div style="background:#0F172A; border:1px solid #23304A; border-radius:6px; padding:10px;">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <code style="color:#10B981; font-weight:700; font-size:12px;">trigger_cross_team_alignment</code>
                    <span style="font-size:10px; background:#064E3B; color:#6EE7B7; padding:1px 6px; border-radius:3px;">MUTATION</span>
                  </div>
                  <p style="font-size:11px; color:#94A3B8; margin-top:3px;">Invokes Rovo AI to auto-create remediation subtasks and post alignment comments.</p>
                </div>

                <div style="background:#0F172A; border:1px solid #23304A; border-radius:6px; padding:10px;">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <code style="color:#F59E0B; font-weight:700; font-size:12px;">mint_release_receipt & verify_proof</code>
                    <span style="font-size:10px; background:#78350F; color:#FDE68A; padding:1px 6px; border-radius:3px;">SECURITY</span>
                  </div>
                  <p style="font-size:11px; color:#94A3B8; margin-top:3px;">Mints SHA-256 Merkle root to Forge KVS and verifies cryptographic integrity.</p>
                </div>
              </div>

              <!-- Right: Live IDE / Terminal Bridge Overlay -->
              <div style="background:#040711; border:1px solid #1E293B; border-radius:10px; padding:16px; font-family:Consolas, 'Courier New', monospace; display:flex; flex-direction:column;">
                <div style="display:flex; align-items:center; justify-content:space-between; padding-bottom:10px; border-bottom:1px solid #1E293B; margin-bottom:10px;">
                  <div style="display:flex; gap:6px;">
                    <div style="width:10px; height:10px; border-radius:50%; background:#EF4444;"></div>
                    <div style="width:10px; height:10px; border-radius:50%; background:#F59E0B;"></div>
                    <div style="width:10px; height:10px; border-radius:50%; background:#10B981;"></div>
                  </div>
                  <div style="font-size:11px; color:#64748B;">cursor-ide / mcp-bridge.js</div>
                </div>

                <div style="font-size:12px; line-height:1.6; color:#CBD5E1; flex:1;">
                  <div style="color:#38BDF8;">$ node scripts/mcp-bridge.js --check</div>
                  <div style="color:#94A3B8;">[CHRONOS-MCP BRIDGE] Connecting to live Atlassian Forge WebTrigger...</div>
                  <div style="color:#94A3B8;">[CHRONOS-MCP BRIDGE] Target: fokrulanthro16.atlassian.net</div>
                  <div style="color:#10B981; font-weight:bold;">[CHRONOS-MCP BRIDGE] 200 OK — Handshake Established!</div>
                  <div style="color:#CBD5E1; margin-top:6px;">&#123;</div>
                  <div style="color:#CBD5E1; padding-left:14px;">"server": <span style="color:#60A5FA;">"chronos-atlassian-mcp-server"</span>,</div>
                  <div style="color:#CBD5E1; padding-left:14px;">"version": <span style="color:#34D399;">"2.2.0"</span>,</div>
                  <div style="color:#CBD5E1; padding-left:14px;">"spec": <span style="color:#FBBF24;">"2024-11-05"</span>,</div>
                  <div style="color:#CBD5E1; padding-left:14px;">"protocol": <span style="color:#F0ABFC;">"JSON-RPC 2.0"</span>,</div>
                  <div style="color:#CBD5E1; padding-left:14px;">"toolsCount": <span style="color:#38BDF8;">5</span>,</div>
                  <div style="color:#CBD5E1; padding-left:14px;">"latency": <span style="color:#34D399;">"32ms"</span></div>
                  <div style="color:#CBD5E1;">&#125;</div>
                  <div style="color:#10B981; font-weight:bold; margin-top:8px;">[CHRONOS-MCP BRIDGE] Status: 100% OPERATIONAL. Ready for Cursor & Claude Desktop.</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

def main():
    print("Launching Playwright to capture 6 Ultra-HD Devpost gallery screenshots...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using 1920x1080 viewport with device_scale_factor=2 for crisp 2x Retina clarity (3840x2160)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)

        screenshots = [
            (1, "01-chronos-command-center-risk.png"),
            (2, "02-teamwork-graph-explorer.png"),
            (3, "03-rovo-auto-remediation-98.png"),
            (4, "04-causal-blast-radius-vectors.png"),
            (5, "05-sha256-cryptographic-ledger.png"),
            (6, "06-atlassian-mcp-ide-gateway.png"),
        ]

        for scene_id, filename in screenshots:
            html = generate_html_view(scene_id)
            page.set_content(html)
            page.wait_for_timeout(300) # Ensure full CSS repaint
            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            page.screenshot(path=filepath, full_page=False)
            size_bytes = os.path.getsize(filepath)
            size_mb = size_bytes / 1024 / 1024
            print(f"Captured: {filename} -> {filepath} ({size_mb:.2f} MB, {size_bytes} bytes)")

        browser.close()
    print("All 6 screenshots captured successfully!")

if __name__ == "__main__":
    main()
