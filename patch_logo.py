import re

with open('templates/index.html', 'r') as f:
    content = f.read()

# Replace brand logo CSS
new_css = """    .brand-logo span {
      font-size: 1.5rem;
      font-weight: 800;
      letter-spacing: 0.5px;
      background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #f093fb 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 0 20px rgba(79, 172, 254, 0.6);
      animation: neonPulse 2s infinite alternate;
    }

    @keyframes neonPulse {
      from { filter: drop-shadow(0 0 2px rgba(0,242,254,0.5)) drop-shadow(0 0 10px rgba(0,242,254,0.3)); }
      to { filter: drop-shadow(0 0 5px rgba(240,147,251,0.8)) drop-shadow(0 0 20px rgba(240,147,251,0.5)); }
    }
    
    .brand-logo svg {
      width: 38px;
      height: 38px;
      filter: drop-shadow(0 0 8px rgba(79, 172, 254, 0.8));
    }
"""

content = re.sub(
    r'\.brand-logo span \{.*?-webkit-text-fill-color: transparent;\s*\}', 
    new_css, 
    content, 
    flags=re.DOTALL
)

# Also make buttons more attractive
button_css = """    .btn-primary {
      background: linear-gradient(45deg, #00f2fe, #4facfe, #f093fb);
      background-size: 200% auto;
      color: #FFFFFF;
      box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4), 0 0 20px rgba(240, 147, 251, 0.2);
      border: 1px solid rgba(255,255,255,0.2);
      animation: gradientShift 3s ease infinite;
    }
    @keyframes gradientShift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    .btn-primary:hover {
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 8px 25px rgba(79, 172, 254, 0.6), 0 0 30px rgba(240, 147, 251, 0.4);
    }"""

content = re.sub(
    r'\.btn-primary \{.*\.btn-primary:active \{[^\}]*\}',
    button_css,
    content,
    flags=re.DOTALL
)

with open('templates/index.html', 'w') as f:
    f.write(content)
