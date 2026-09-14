html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AgentX Platform</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0F172A;
      --bg-secondary: #111827;
      --card-bg: #1E293B;
      --accent-primary: #3B82F6;
      --accent-ai: #8B5CF6;
      --text-main: #FFFFFF;
      --text-gray: #D1D5DB;
      --border-color: rgba(255, 255, 255, 0.08);
      --font-family: 'Poppins', sans-serif;
    }
    body {
      margin: 0;
      font-family: var(--font-family);
      background-color: var(--bg-primary);
      color: var(--text-main);
      overflow-x: hidden;
    }
    /* Constellations will override background to transparent and put a deep space bg behind */
    
    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1.5rem 4rem;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border-color);
      position: fixed;
      top: 0; width: 100%; box-sizing: border-box;
      z-index: 100;
    }
    .logo {
      font-size: 1.5rem;
      font-weight: 700;
      color: #fff;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      animation: neonPulse 2s infinite alternate;
      filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.8));
    }
    @keyframes neonPulse {
      0% { filter: drop-shadow(0 0 5px rgba(0, 242, 254, 0.5)); }
      100% { filter: drop-shadow(0 0 20px rgba(0, 242, 254, 1)) drop-shadow(0 0 40px rgba(240, 147, 251, 0.6)); }
    }
    .nav-links a {
      color: var(--text-gray);
      text-decoration: none;
      margin-left: 2rem;
      font-weight: 500;
      transition: color 0.3s;
    }
    .nav-links a:hover {
      color: var(--accent-primary);
    }
    .btn {
      padding: 0.6rem 1.5rem;
      border-radius: 8px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.3s;
      display: inline-block;
      cursor: pointer;
      border: none;
    }
    .btn-primary {
      background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
      color: #000;
      box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
    }
    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 242, 254, 0.6);
    }
    .btn-outline {
      background: transparent;
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: white;
    }
    .btn-outline:hover {
      background: rgba(255, 255, 255, 0.05);
    }
    
    .hero {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 0 2rem;
      position: relative;
    }
    .hero-badge {
      background: rgba(139, 92, 246, 0.15);
      border: 1px solid rgba(139, 92, 246, 0.3);
      color: #b490ff;
      padding: 0.4rem 1rem;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 1.5rem;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
    }
    .hero h1 {
      font-size: 3.5rem;
      font-weight: 700;
      margin: 0 0 1rem 0;
      line-height: 1.2;
    }
    .gradient-text {
      background: linear-gradient(135deg, #00f2fe 0%, #f093fb 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero p {
      font-size: 1.1rem;
      color: var(--text-gray);
      max-width: 600px;
      line-height: 1.6;
      margin-bottom: 2.5rem;
    }
    .cta-group {
      display: flex;
      gap: 1rem;
      justify-content: center;
    }
  </style>
</head>
<body>

  <header class="navbar">
    <a href="/" class="logo">⚡ AgentX Platform</a>
    <div class="nav-links">
      <a href="#about">About</a>
      <a href="#skills">Reusable Skills</a>
      <a href="#mcp">MCP Integrations</a>
      <a href="/login" class="btn btn-outline" style="margin-left: 2rem;">Login</a>
      <a href="/register" class="btn btn-primary" style="margin-left: 1rem;">Register</a>
    </div>
  </header>

  <main class="hero">
    <div class="hero-badge">
      🚀 Platform Agent Skills & Knowledge
    </div>
    <h1>
      Empower Agents with<br>
      <span class="gradient-text">Freshworks Platform</span>
    </h1>
    <p>
      The definitive platform for building reusable skills, orchestrating MCP integrations, and deploying context-aware AI on the Freshworks developer platform.
    </p>
    <div class="cta-group">
      <a href="/register" class="btn btn-primary">Start Building</a>
      <a href="#capabilities" class="btn btn-outline">Explore Capabilities</a>
    </div>
  </main>

  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script src="/static/js/constellations.js"></script>
</body>
</html>
"""

with open('templates/index.html', 'w') as f:
    f.write(html_content)
