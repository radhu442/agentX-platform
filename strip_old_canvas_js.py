import re

with open('templates/index.html', 'r') as f:
    html = f.read()

# Just remove the whole script block that contains it, or replace the function bodies
html = re.sub(r'const canvas = document\.getElementById\(''canvas-bg''\);.*?requestAnimationFrame\([^)]+\);\s*\}', '', html, flags=re.DOTALL)
html = html.replace("initCanvas();", "")

with open('templates/index.html', 'w') as f:
    f.write(html)
