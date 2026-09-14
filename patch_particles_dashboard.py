with open('templates/dashboard.html', 'r') as f:
    html = f.read()

scripts = """
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script src="/static/js/constellations.js"></script>
</body>
"""

html = html.replace('</body>', scripts)

with open('templates/dashboard.html', 'w') as f:
    f.write(html)
