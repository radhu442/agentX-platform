with open('static/js/constellations.js', 'r') as f:
    js = f.read()

new_js = js.replace('document.addEventListener("DOMContentLoaded", function() {', 'function initParticles() {')
new_js = new_js.replace('});', '}\nif(document.readyState === "loading") {\n  document.addEventListener("DOMContentLoaded", initParticles);\n} else {\n  initParticles();\n}')

with open('static/js/constellations.js', 'w') as f:
    f.write(new_js)
