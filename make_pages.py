with open('templates/dashboard.html', 'r') as f:
    base_html = f.read()

def inject_content(html, title, active_menu, new_content):
    # Fix Sidebar
    html = html.replace('href="#" class="nav-item active"', 'href="#" class="nav-item"')
    html = html.replace(f'href="#" class="nav-item">{active_menu}', f'href="#" class="nav-item active">{active_menu}')
    
    # Actually make sidebar links functional
    html = html.replace('class="nav-item">Dashboard', 'href="/dashboard" class="nav-item">Dashboard')
    html = html.replace('class="nav-item active">Dashboard', 'href="/dashboard" class="nav-item active">Dashboard')
    
    html = html.replace('class="nav-item">Skill Registry', 'href="/skills" class="nav-item">Skill Registry')
    html = html.replace('class="nav-item active">Skill Registry', 'href="/skills" class="nav-item active">Skill Registry')
    
    html = html.replace('class="nav-item">MCP Integrations', 'href="/mcp" class="nav-item">MCP Integrations')
    html = html.replace('class="nav-item active">MCP Integrations', 'href="/mcp" class="nav-item active">MCP Integrations')
    
    html = html.replace('class="nav-item">Agent Simulator', 'href="/simulator" class="nav-item">Agent Simulator')
    html = html.replace('class="nav-item active">Agent Simulator', 'href="/simulator" class="nav-item active">Agent Simulator')

    # Inject main content
    import re
    # Find the main-content div
    start = html.find('<div class="main-content">')
    # find the next </body>
    end = html.find('</body>', start)
    
    final = html[:start+26] + new_content + html[end:]
    return final

# 1. NEW DASHBOARD (Profile Page)
dash_content = """
    <div class="header" style="margin-bottom:2rem;">
      <h1>Welcome back, {{ user.name }}</h1>
    </div>
    
    <div style="display:flex; gap:2rem;">
        <div class="card" style="flex:1; text-align:center;">
            <img src="{{ url_for('static', filename='uploads/' + user.profile_pic) }}" onerror="this.src='https://ui-avatars.com/api/?name={{ user.name }}&background=0D8ABC&color=fff'" style="width:120px; height:120px; border-radius:50%; margin-bottom:1rem; border:3px solid #00f2fe; box-shadow: 0 0 15px rgba(0,242,254,0.5);">
            <h2 style="margin:0; color:#fff;">{{ user.name }}</h2>
            <p style="color:#00f2fe; margin-top:5px; font-weight:bold;">Rank: {{ user.role }}</p>
            <p style="color:var(--text-gray); font-size:0.9rem;">{{ user.email }}</p>
        </div>
        <div style="flex:2; display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;">
            <div class="card" style="display:flex; flex-direction:column; justify-content:center; align-items:center;">
                <h3 style="font-size:3rem; margin:0; background: linear-gradient(90deg, #00f2fe, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{{ skill_count }}</h3>
                <p>Agent Skills Built</p>
            </div>
            <div class="card" style="display:flex; flex-direction:column; justify-content:center; align-items:center;">
                <h3 style="font-size:3rem; margin:0; background: linear-gradient(90deg, #00f2fe, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{{ mcp_count }}</h3>
                <p>MCP Integrations</p>
            </div>
        </div>
    </div>
"""
with open('templates/dashboard.html', 'w') as f:
    f.write(inject_content(base_html, 'Dashboard', 'Dashboard', dash_content))

# 2. SKILL REGISTRY (CRUD)
skills_content = """
    <div class="header">
      <h1>Skill Registry</h1>
    </div>
    <div class="card" style="margin-bottom:2rem;">
        <h3 style="color:#fff;">Create New Skill</h3>
        <form method="POST" action="/skills" style="display:flex; flex-direction:column; gap:1rem; margin-top:1rem;">
            <input type="text" name="name" placeholder="Skill Name (e.g., Salesforce Lookup)" required style="padding:10px; border-radius:6px; background:#111827; border:1px solid #3B82F6; color:white;">
            <textarea name="description" placeholder="Skill Description..." required style="padding:10px; border-radius:6px; background:#111827; border:1px solid #3B82F6; color:white; min-height:80px;"></textarea>
            <button type="submit" class="btn btn-primary" style="width:200px;">Deploy Skill 🚀</button>
        </form>
    </div>
    <h3 style="color:var(--text-gray); margin-bottom:1rem;">Deployed Skills</h3>
    <div class="grid">
        {% for skill in skills %}
        <div class="card">
            <h3>{{ skill.name }}</h3>
            <p style="font-size:0.9rem;">{{ skill.description }}</p>
            <span style="display:inline-block; margin-top:10px; padding:4px 8px; background:rgba(16,185,129,0.2); color:#10B981; border-radius:4px; font-size:0.8rem;">Status: {{ skill.status }}</span>
        </div>
        {% else %}
        <p>No skills deployed yet. Create your first skill above!</p>
        {% endfor %}
    </div>
"""
with open('templates/skills.html', 'w') as f:
    f.write(inject_content(base_html, 'Skill Registry', 'Skill Registry', skills_content))

# 3. MCP INTEGRATIONS (CRUD)
mcp_content = """
    <div class="header">
      <h1>MCP Gateway Connections</h1>
    </div>
    <div class="card" style="margin-bottom:2rem;">
        <h3 style="color:#fff;">Add New Integration</h3>
        <form method="POST" action="/mcp" style="display:flex; flex-direction:column; gap:1rem; margin-top:1rem;">
            <input type="text" name="provider" placeholder="Provider Name (e.g., Freshdesk, GitHub, Postgres)" required style="padding:10px; border-radius:6px; background:#111827; border:1px solid #3B82F6; color:white;">
            <input type="password" name="api_key" placeholder="API Key / Auth Token" required style="padding:10px; border-radius:6px; background:#111827; border:1px solid #3B82F6; color:white;">
            <button type="submit" class="btn btn-primary" style="width:200px;">Connect MCP ⚡</button>
        </form>
    </div>
    <h3 style="color:var(--text-gray); margin-bottom:1rem;">Active Connections</h3>
    <div style="display:flex; flex-direction:column; gap:1rem;">
        {% for mcp in mcps %}
        <div class="card" style="display:flex; justify-content:space-between; align-items:center; padding:1rem 1.5rem;">
            <div>
                <h3 style="margin:0; margin-bottom:5px;">{{ mcp.provider }}</h3>
                <code style="color:var(--text-muted);">Key: ••••••••••••</code>
            </div>
            <span style="padding:4px 12px; background:rgba(16,185,129,0.2); color:#10B981; border-radius:20px; font-weight:bold;">{{ mcp.status }}</span>
        </div>
        {% else %}
        <p>No integrations configured.</p>
        {% endfor %}
    </div>
"""
with open('templates/mcp.html', 'w') as f:
    f.write(inject_content(base_html, 'MCP Integrations', 'MCP Integrations', mcp_content))

# 4. AGENT SIMULATOR
sim_content = """
    <div class="header">
      <h1>Agent Sandbox Simulator</h1>
    </div>
    <div class="card" style="display:flex; flex-direction:column; height: 60vh;">
        <div id="chat-box" style="flex:1; background:#0F172A; border-radius:8px; padding:1rem; overflow-y:auto; margin-bottom:1rem; border:1px solid rgba(255,255,255,0.1);">
            <div style="margin-bottom:1rem; color:var(--text-gray);"><span style="color:#00f2fe; font-weight:bold;">System:</span> Agent Simulator initialized. Sandbox environment ready. All skills loaded.</div>
        </div>
        <div style="display:flex; gap:10px;">
            <input type="text" id="sim-input" placeholder="Give your agent a command..." style="flex:1; padding:10px 15px; border-radius:8px; background:#111827; border:1px solid #3B82F6; color:white;">
            <button class="btn btn-primary" onclick="simulateCommand()">Execute</button>
        </div>
    </div>
    <script>
      function simulateCommand() {
          const input = document.getElementById('sim-input');
          const box = document.getElementById('chat-box');
          if(!input.value.trim()) return;
          
          box.innerHTML += `<div style="margin-bottom:1rem; text-align:right;"><span style="background:#3B82F6; padding:8px 12px; border-radius:12px; display:inline-block; color:white;">${input.value}</span></div>`;
          
          setTimeout(() => {
              box.innerHTML += `<div style="margin-bottom:1rem; text-align:left;"><span style="color:#f093fb; font-weight:bold;">AgentX:</span> <span style="background:rgba(255,255,255,0.05); padding:8px 12px; border-radius:12px; display:inline-block; border:1px solid rgba(240,147,251,0.3);"><br>Evaluating intent...<br>➜ Triggering MCP Context...<br>➜ Skill Executed Successfully.</span></div>`;
              box.scrollTop = box.scrollHeight;
          }, 600);
          
          input.value = '';
      }
    </script>
"""
with open('templates/simulator.html', 'w') as f:
    f.write(inject_content(base_html, 'Agent Simulator', 'Agent Simulator', sim_content))

