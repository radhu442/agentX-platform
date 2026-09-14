with open('templates/index.html', 'r') as f:
    html = f.read()

import re
# Find where const canvas = document.getElementById('canvas-bg'); starts
start = html.find("const canvas = document.getElementById('canvas-bg');")
if start != -1:
    end = html.find("initCanvas();", start)
    if end != -1:
        # Remove it all
        html = html[:start] + html[end + 13:]

with open('templates/index.html', 'w') as f:
    f.write(html)
