import re

# Update login.html
with open('templates/login.html', 'r') as f:
    content = f.read()

new_css = """    .eyebrow {
      font-family: 'Fira Code', monospace;
      color: #00f2fe;
      font-size: 0.9rem;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 1rem;
      text-align: center;
      text-shadow: 0 0 15px rgba(0,242,254,0.8);
      animation: pulseText 2s infinite alternate;
    }
    @keyframes pulseText {
      from { text-shadow: 0 0 10px rgba(0,242,254,0.5); }
      to { text-shadow: 0 0 20px rgba(0,242,254,1), 0 0 30px rgba(240,147,251,0.6); }
    }
"""

content = re.sub(
    r'\.eyebrow \{[^\}]*\}',
    new_css,
    content,
    flags=re.DOTALL
)

with open('templates/login.html', 'w') as f:
    f.write(content)

# Update dashboard.html
with open('templates/dashboard.html', 'r') as f:
    dash = f.read()

dash_css = """    .logo {
      font-size: 1.8rem;
      font-weight: 800;
      margin-bottom: 2rem;
      text-align: center;
      background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #f093fb 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 0 20px rgba(79, 172, 254, 0.6);
      animation: neonPulse 2s infinite alternate;
    }
    @keyframes neonPulse {
      from { filter: drop-shadow(0 0 2px rgba(0,242,254,0.5)) drop-shadow(0 0 10px rgba(0,242,254,0.3)); }
      to { filter: drop-shadow(0 0 5px rgba(240,147,251,0.8)) drop-shadow(0 0 20px rgba(240,147,251,0.5)); }
    }
"""

dash = re.sub(
    r'\.logo \{.*text-align: center;\s*\}',
    dash_css,
    dash,
    flags=re.DOTALL
)

with open('templates/dashboard.html', 'w') as f:
    f.write(dash)

