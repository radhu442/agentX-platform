import re

with open('templates/index.html', 'r') as f:
    html = f.read()

# Remove the old canvas element
html = html.replace('<canvas id="canvas-bg"></canvas>', '')

# Remove the old canvas CSS
html = re.sub(r'/\*\s*Ambient Canvas Particle Network Background\s*\*/.*?\}', '', html, flags=re.DOTALL | re.IGNORECASE)

# Remove the old canvas JS
html = re.sub(r'// ==========================================\s*// 2\. AMBIENT BACKGROUND ANIMATION\s*// ==========================================.*?// ==========================================', '// ==========================================', html, flags=re.DOTALL)

# Ensure the body background doesn't interfere
html = html.replace('background-color: var(--bg-primary);', 'background-color: transparent;')

with open('templates/index.html', 'w') as f:
    f.write(html)
