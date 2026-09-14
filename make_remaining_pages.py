import glob
import re

# 1. Update sidebars across all current HTML files
def update_sidebars():
    for filepath in glob.glob("templates/*.html"):
        if filepath in ['templates/index.html', 'templates/login.html', 'templates/register.html']:
            continue
        with open(filepath, 'r') as f:
            html = f.read()
        
        html = html.replace('href="#" class="nav-item">Freshworks Deployer', 'href="/freshworks" class="nav-item">Freshworks Deployer')
        html = html.replace('href="#" class="nav-item">Knowledge Graph', 'href="/knowledge_graph" class="nav-item">Knowledge Graph')
        html = html.replace('href="#" class="nav-item">Analytics', 'href="/analytics" class="nav-item">Analytics')
        html = html.replace('href="#" class="nav-item">API Keys', 'href="/api_keys" class="nav-item">API Keys')
        
        with open(filepath, 'w') as f:
            f.write(html)

update_sidebars()

# 2. Create the 4 new templates based on an existing one (e.g., dashboard.html)
with open('templates/dashboard.html', 'r') as f:
    base_html = f.read()

def create_page(filename, title, content):
    html = base_html
    # Remove active state from Dashboard
    html = html.replace('href="/dashboard" class="nav-item active"', 'href="/dashboard" class="nav-item"')
    # Add active state to this page
    if title == "Freshworks":
        html = html.replace('href="/freshworks" class="nav-item"', 'href="/freshworks" class="nav-item active"')
    elif title == "Knowledge Graph":
        html = html.replace('href="/knowledge_graph" class="nav-item"', 'href="/knowledge_graph" class="nav-item active"')
    elif title == "Analytics":
        html = html.replace('href="/analytics" class="nav-item"', 'href="/analytics" class="nav-item active"')
    elif title == "API Keys":
        html = html.replace('href="/api_keys" class="nav-item"', 'href="/api_keys" class="nav-item active"')

    # Replace content
    start = html.find('<div class="main-content">')
    end = html.find('<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js">', start)
    if end == -1:
        end = html.find('</body>', start)
    
    final_html = html[:start+26] + content + html[end:]
    
    with open(f'templates/{filename}', 'w') as f:
        f.write(final_html)

# Content for Freshworks
freshworks_html = """
    <div class="header">
      <h1>Freshworks Deployer</h1>
    </div>
    <div class="card" style="margin-bottom:2rem;">
        <h3 style="color:#fff;">Deploy Agent to Workspace</h3>
        <p style="color:var(--text-gray); margin-bottom:1rem;">Push your trained agent and its skills directly into your Freshdesk or Freshservice environment.</p>
        <div style="display:flex; flex-direction:column; gap:1rem; margin-top:1rem;">
            <select style="padding:10px; border-radius:6px; background:#111827; border:1px solid #3B82F6; color:white;">
                <option>Freshdesk (Customer Support)</option>
                <option>Freshservice (ITSM / EX)</option>
                <option>Freshsales (CRM)</option>
            </select>
            <input type="text" placeholder="Workspace Domain (e.g., acme.freshdesk.com)" style="padding:10px; border-radius:6px; background:#111827; border:1px solid #3B82F6; color:white;">
            <button class="btn btn-primary" onclick="this.innerText='Deploying...'; setTimeout(() => {this.innerText='Successfully Deployed ✅'; this.style.backgroundColor='#10B981';}, 1500)" style="width:200px;">Start Deployment 🚀</button>
        </div>
    </div>
"""

# Content for Knowledge Graph
kg_html = """
    <div class="header">
      <h1>Knowledge Graph</h1>
    </div>
    <div class="card" style="margin-bottom:2rem;">
        <h3 style="color:#fff;">Semantic Context Engine</h3>
        <p style="color:var(--text-gray); margin-bottom:1rem;">Visualize and manage the enterprise entities your agent has learned.</p>
        <div style="display:flex; gap:10px; margin-bottom:1rem;">
            <input type="text" placeholder="Search entities (e.g., 'Refund Policy')..." style="flex:1; padding:10px; border-radius:6px; background:#111827; border:1px solid #3B82F6; color:white;">
            <button class="btn btn-outline">Search</button>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:1rem;">
            <div style="padding:1rem; border:1px solid rgba(0,242,254,0.3); border-radius:8px; background:rgba(0,0,0,0.2);">
                <h4 style="color:#00f2fe; margin-top:0;">Customer</h4>
                <p style="font-size:0.8rem; color:#aaa;">Connected to: Tickets, Orders, Sentiment</p>
            </div>
            <div style="padding:1rem; border:1px solid rgba(240,147,251,0.3); border-radius:8px; background:rgba(0,0,0,0.2);">
                <h4 style="color:#f093fb; margin-top:0;">Employee</h4>
                <p style="font-size:0.8rem; color:#aaa;">Connected to: Assets, HR Tickets, Departments</p>
            </div>
            <div style="padding:1rem; border:1px solid rgba(16,185,129,0.3); border-radius:8px; background:rgba(0,0,0,0.2);">
                <h4 style="color:#10B981; margin-top:0;">IT Asset</h4>
                <p style="font-size:0.8rem; color:#aaa;">Connected to: Employee, Procurement, Software</p>
            </div>
        </div>
    </div>
"""

# Content for Analytics
analytics_html = """
    <div class="header">
      <h1>Analytics Engine</h1>
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1.5rem; margin-bottom:2rem;">
        <div class="card" style="text-align:center;">
            <h3 style="font-size:2.5rem; margin:0; color:#00f2fe;">1.2M</h3>
            <p style="color:var(--text-gray);">Tokens Processed</p>
        </div>
        <div class="card" style="text-align:center;">
            <h3 style="font-size:2.5rem; margin:0; color:#f093fb;">98.4%</h3>
            <p style="color:var(--text-gray);">Task Success Rate</p>
        </div>
        <div class="card" style="text-align:center;">
            <h3 style="font-size:2.5rem; margin:0; color:#10B981;">320ms</h3>
            <p style="color:var(--text-gray);">Avg Latency</p>
        </div>
    </div>
    <div class="card">
        <h3 style="color:#fff;">Recent Activity Log</h3>
        <p style="font-family:monospace; color:#aaa; font-size:0.9rem; line-height:1.8;">
            [10:42:01] Skill 'Refund Lookup' executed successfully (20ms).<br>
            [10:41:15] MCP Connection 'Freshdesk' synchronized 140 tickets.<br>
            [10:35:22] Agent Simulator session ended.<br>
            [10:20:00] New user profile created.
        </p>
    </div>
"""

# Content for API Keys
api_keys_html = """
    <div class="header">
      <h1>API Key Manager</h1>
    </div>
    <div class="card" style="margin-bottom:2rem;">
        <h3 style="color:#fff;">Generate New Agent Key</h3>
        <p style="color:var(--text-gray); margin-bottom:1rem;">Create secure credentials for your external applications to call your custom agents.</p>
        <div style="display:flex; gap:1rem;">
            <input type="text" placeholder="Key Name (e.g., Production App)" style="flex:1; padding:10px; border-radius:6px; background:#111827; border:1px solid #3B82F6; color:white;">
            <button class="btn btn-primary" onclick="this.innerText='Key Generated ✅'; setTimeout(() => this.innerText='Generate Key', 2000)">Generate Key</button>
        </div>
    </div>
    <div class="card">
        <h3 style="color:#fff; margin-bottom:1rem;">Active Keys</h3>
        <div style="display:flex; justify-content:space-between; padding:1rem; border-bottom:1px solid rgba(255,255,255,0.1);">
            <div><strong style="color:white;">Development Key</strong> <br><span style="color:#aaa; font-size:0.8rem;">Created: Today</span></div>
            <code style="color:#00f2fe;">agx_dev_••••••••••••</code>
        </div>
        <div style="display:flex; justify-content:space-between; padding:1rem;">
            <div><strong style="color:white;">Freshworks Webhook</strong> <br><span style="color:#aaa; font-size:0.8rem;">Created: Yesterday</span></div>
            <code style="color:#00f2fe;">agx_fw_••••••••••••</code>
        </div>
    </div>
"""

create_page('freshworks.html', 'Freshworks', freshworks_html)
create_page('knowledge_graph.html', 'Knowledge Graph', kg_html)
create_page('analytics.html', 'Analytics', analytics_html)
create_page('api_keys.html', 'API Keys', api_keys_html)

