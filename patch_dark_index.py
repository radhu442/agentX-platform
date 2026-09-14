import re

with open('templates/index.html', 'r') as f:
    html = f.read()

# 1. Text Replacements
html = html.replace('HackOps AI', 'Agent Skills Platform')
html = html.replace('/login-page', '/login')
html = html.replace('/register-page', '/register')
html = html.replace("window.location.href='/login-page'", "window.location.href='/login'")
html = html.replace("window.location.href='/register-page'", "window.location.href='/register'")
html = html.replace("window.location.href = '/login-page'", "window.location.href = '/login'")
html = html.replace("window.location.href = '/register-page'", "window.location.href = '/register'")

# 2. Add Neon Logo CSS
neon_css = """
<style>
  .logo, .agentx-logo {
      animation: neonPulse 2s infinite alternate !important;
      filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.8)) !important;
  }
  @keyframes neonPulse {
      0% { filter: drop-shadow(0 0 5px rgba(0, 242, 254, 0.5)); }
      100% { filter: drop-shadow(0 0 20px rgba(0, 242, 254, 1)) drop-shadow(0 0 40px rgba(240, 147, 251, 0.6)); }
  }
</style>
</head>
"""
html = html.replace('</head>', neon_css)

# 3. Add Constellations
constellations_scripts = """
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script src="/static/js/constellations.js"></script>
</body>
"""
html = html.replace('</body>', constellations_scripts)

with open('templates/index.html', 'w') as f:
    f.write(html)
