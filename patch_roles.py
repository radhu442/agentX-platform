import re

# Patch Register HTML
with open('templates/register.html', 'r') as f:
    html = f.read()

# Replace roles
html = html.replace('<option value="Participant">Participant</option>', '<option value="Developer">Agent Developer</option>')
html = html.replace('<option value="Mentor">Mentor</option>', '<option value="Prompt Engineer">Prompt Engineer</option>')
html = html.replace('<option value="Judge">Judge</option>', '<option value="Admin">Platform Admin</option>')
html = html.replace('<option value="Organizer">Organizer</option>', '<option value="Integration">Integration Specialist</option>')
html = html.replace('<option value="Sponsor">Sponsor</option>', '')
html = html.replace('<option value="Admin">Admin</option>', '')
html = html.replace('Choose your station...', 'Choose your role...')
html = html.replace('Register to join the AgentX Platform platform platform.', 'Register to join the Platform Agent Skills network.')
html = html.replace('AgentX Platform', 'Agent Skills Platform')

with open('templates/register.html', 'w') as f:
    f.write(html)
