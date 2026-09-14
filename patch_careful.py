import re

with open('templates/index.html', 'r') as f:
    html = f.read()

# 1. Strip the canvas element completely
html = html.replace('<canvas id="canvas-bg"></canvas>', '')

# 2. Add Constellations Scripts right before </body>
scripts = """
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script src="/static/js/constellations.js"></script>
</body>
"""
html = html.replace('</body>', scripts)

# 3. Fix the routes
html = html.replace('HackOps AI', 'Agent Skills Platform')
html = html.replace('/login-page', '/login')
html = html.replace('/register-page', '/register')
html = html.replace("window.location.href='/login-page'", "window.location.href='/login'")
html = html.replace("window.location.href='/register-page'", "window.location.href='/register'")
html = html.replace("window.location.href = '/login-page'", "window.location.href = '/login'")
html = html.replace("window.location.href = '/register-page'", "window.location.href = '/register'")

# 4. Disable the native canvas background logic so it doesn't crash or draw over
# I will just redefine the initCanvas function to do nothing, or catch the error.
# Actually, the simplest way is to inject a dummy canvas element with display:none so the JS doesn't crash!
html = html.replace('<body>', '<body>\n<canvas id="canvas-bg" style="display:none;"></canvas>')

with open('templates/index.html', 'w') as f:
    f.write(html)
