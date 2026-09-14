import glob

footer_scripts = """
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script src="/static/js/constellations.js"></script>
</body>
"""

for filepath in glob.glob("templates/*.html"):
    with open(filepath, 'r') as f:
        html = f.read()
    
    if '<script src="/static/js/constellations.js"></script>' not in html:
        html = html.replace('</body>', footer_scripts)
        with open(filepath, 'w') as f:
            f.write(html)

