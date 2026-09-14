with open('templates/index.html', 'r') as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if "const canvas = document.getElementById('canvas-bg');" in line:
        skip = True
    if skip and "initCanvas();" in line:
        skip = False
        continue
        
    if not skip:
        out.append(line)

with open('templates/index.html', 'w') as f:
    f.writelines(out)
