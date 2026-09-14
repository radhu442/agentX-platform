import glob

script_tags = """
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script src="/static/js/constellations.js"></script>
</body>
"""

for filepath in glob.glob("templates/*.html"):
    with open(filepath, 'r') as f:
        html = f.read()
    
    html = html.replace('</body>', script_tags)
    
    # Remove any old hackathon stuff if present
    html = html.replace('Mentor', 'Agent Engineer')
    html = html.replace('Prizes', 'Capabilities')
    html = html.replace('Hackers', 'Agents')
    
    with open(filepath, 'w') as f:
        f.write(html)
