import glob
import re

for filepath in glob.glob("templates/*.html"):
    if filepath == 'templates/index.html' or filepath == 'templates/login.html' or filepath == 'templates/register.html':
        continue
        
    with open(filepath, 'r') as f:
        html = f.read()
    
    # 1. Clean up double hrefs
    html = re.sub(r'href="#"\s+href="(/.*?)"', r'href="\1"', html)
    html = re.sub(r'href="(/.*?)"\s+href="#"', r'href="\1"', html)
    
    # If there are still href="#" for the ones we mapped, fix them:
    html = html.replace('href="#" class="nav-item active">Dashboard', 'href="/dashboard" class="nav-item active">Dashboard')
    html = html.replace('href="#" class="nav-item">Dashboard', 'href="/dashboard" class="nav-item">Dashboard')
    
    html = html.replace('href="#" class="nav-item active">Skill Registry', 'href="/skills" class="nav-item active">Skill Registry')
    html = html.replace('href="#" class="nav-item">Skill Registry', 'href="/skills" class="nav-item">Skill Registry')
    
    html = html.replace('href="#" class="nav-item active">MCP Integrations', 'href="/mcp" class="nav-item active">MCP Integrations')
    html = html.replace('href="#" class="nav-item">MCP Integrations', 'href="/mcp" class="nav-item">MCP Integrations')
    
    html = html.replace('href="#" class="nav-item active">Agent Simulator', 'href="/simulator" class="nav-item active">Agent Simulator')
    html = html.replace('href="#" class="nav-item">Agent Simulator', 'href="/simulator" class="nav-item">Agent Simulator')
    
    html = html.replace('href="#" class="nav-item">Logout', 'href="/logout" class="nav-item">Logout')

    # 2. Remove the e.preventDefault() JS block that breaks navigation
    html = re.sub(r'// Fix Sidebar interactions.*?\}\);', '', html, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(html)
