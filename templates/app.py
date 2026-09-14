import os
import sqlite3
import secrets
import json

# Load .env if python-dotenv is installed (optional, not required)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
from db import get_db_connection, init_db

app = Flask(__name__)

# Secret key: read from environment, fall back to a generated dev key
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ── Initialise DB on startup (safe: uses IF NOT EXISTS) ───────────────────────
init_db()


def check_is_admin(role_str):
    if not role_str:
        return False
    r = role_str.lower().strip()
    return any(k in r for k in ['admin', 'platform admin', 'administrator', 'system admin', 'sysadmin'])


def get_role_category(role_str):
    if not role_str:
        return 'developer'
    r = role_str.lower().strip()
    if check_is_admin(r):
        return 'admin'
    elif 'prompt' in r or 'ai' in r or 'architect' in r:
        return 'prompt'
    elif 'integration' in r or 'mcp' in r or 'gateway' in r:
        return 'integration'
    return 'developer'


# ── AI helper ─────────────────────────────────────────────────────────────────
def get_ai_response(command: str, user_name: str) -> str:
    """
    Try Gemini first, then OpenAI, then a smart rule-based fallback.
    Returns a text response string.
    """
    cmd_lower = command.lower().strip()

    # ── 1. Gemini (google-generativeai) ──────────────────────────────────────
    gemini_key = os.environ.get('GEMINI_API_KEY', '')
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            system = (
                f"You are AgentX, an intelligent AI agent assistant for {user_name}. "
                "You help with tasks like Freshworks CRM, customer support automation, "
                "MCP tool orchestration, and agent skill building. "
                "Keep responses concise (2-3 sentences max), practical and helpful."
            )
            resp = model.generate_content(f"{system}\n\nUser: {command}")
            return resp.text.strip()
        except Exception:
            pass  # fall through to next option

    # ── 2. OpenAI ────────────────────────────────────────────────────────────
    openai_key = os.environ.get('OPENAI_API_KEY', '')
    if openai_key:
        try:
            import openai
            openai.api_key = openai_key
            resp = openai.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': (
                        f"You are AgentX, an intelligent AI agent assistant for {user_name}. "
                        "Help with Freshworks, CRM, MCP integrations and agent skills. "
                        "Keep replies concise and practical."
                    )},
                    {'role': 'user', 'content': command}
                ],
                max_tokens=200
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            pass  # fall through to fallback

    # ── 3. Smart rule-based fallback ─────────────────────────────────────────
    if any(k in cmd_lower for k in ['hello', 'hi', 'hey', 'greet']):
        return f"Hello, {user_name}! AgentX sandbox is ready. You can test MCP commands, skill executions, or ask about Freshworks deployments."

    if any(k in cmd_lower for k in ['skill', 'deploy skill', 'create skill']):
        return "⚙️ Skill execution pipeline initiated → Parsing intent → Matching registered skills → Sandbox execution complete. Navigate to Skill Registry to manage your skills."

    if any(k in cmd_lower for k in ['mcp', 'tool', 'connect', 'bridge']):
        return "🔗 MCP context provider queried → Tool registry scanned → Bridge handshake successful. Your MCP integrations are active and responsive."

    if any(k in cmd_lower for k in ['freshwork', 'freshdesk', 'freshservice', 'deploy', 'push']):
        return "🚀 Freshworks deployment pipeline triggered → Agent configuration validated → Workspace target identified. Head to Freshworks Deployer to confirm the push."

    if any(k in cmd_lower for k in ['analytic', 'metric', 'stat', 'report', 'log']):
        return "📊 Analytics module active → Pulling telemetry from persistent store → All systems nominal. Check the Analytics page for live counters."

    if any(k in cmd_lower for k in ['api', 'key', 'token', 'auth']):
        return "🔑 Authorization context scanned → API key vault queried → Token integrity verified. Manage your keys on the API Keys page."

    if any(k in cmd_lower for k in ['help', '?', 'what', 'how']):
        return (
            "AgentX supports: skill deployment, MCP orchestration, Freshworks integration, "
            "analytics, and API key management. Try commands like 'deploy skill', "
            "'connect MCP', or 'run analytics'."
        )

    if any(k in cmd_lower for k in ['status', 'health', 'ping', 'check']):
        return "✅ All systems operational → Database: connected → MCP gateway: ready → Skill engine: standby → Freshworks bridge: active."

    if any(k in cmd_lower for k in ['error', 'fail', 'issue', 'bug', 'problem']):
        return "🔍 Diagnostic scan initiated → Reviewing recent execution logs → No critical failures detected in sandbox. Check Analytics for detailed audit trail."

    # Generic catch-all
    return (
        f"⚡ Command received: '{command[:60]}{'...' if len(command) > 60 else ''}' → "
        "Intent parsed → MCP context loaded → Skill engine engaged → "
        "Execution completed and logged to database."
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            return jsonify({'error': 'Please provide both email and password.'}), 400

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE LOWER(email) = LOWER(?) AND password = ?',
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            session['role'] = user['role']
            return jsonify({
                'message': 'Login successful',
                'redirect': '/dashboard',
                'user': {
                    'email': user['email'],
                    'full_name': user['name'],
                    'role': user['role'],
                    'phone': user['phone'] if 'phone' in user.keys() else '',
                    'organization': user['organization'] if 'organization' in user.keys() else '',
                    'profile_image': user['profile_pic']
                },
                'token': secrets.token_hex(16)
            })
        else:
            return jsonify({'error': 'Invalid email or passphrase. Check your credentials.'}), 401

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('full_name', '').strip()
        if not name:
            name = request.form.get('name', 'Agent Developer').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'Agent Developer').strip()
        phone = request.form.get('phone', '').strip()
        organization = request.form.get('organization', '').strip()

        if not email or not password:
            return jsonify({'error': 'Email and passphrase are required.'}), 400

        filename = 'default.png'
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '':
                filename = secure_filename(f"{secrets.token_hex(4)}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (name, email, password, role, profile_pic, phone, organization) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (name, email, password, role, filename, phone, organization)
            )
            conn.commit()

            new_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            session['user_id'] = new_user['id']
            session['name'] = new_user['name']
            session['email'] = new_user['email']
            session['role'] = new_user['role']

        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'An account with this email address already exists.'}), 409
        except Exception as e:
            conn.close()
            return jsonify({'error': f'Database error: {str(e)}'}), 500

        conn.close()
        return jsonify({'message': 'Registration successful and sealed in database!', 'redirect': '/dashboard'})

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not user:
        conn.close()
        session.clear()
        return redirect(url_for('login'))

    user_role = user['role'] or ''
    is_admin = check_is_admin(user_role)
    role_category = get_role_category(user_role)

    # Personal counters
    skill_count = conn.execute('SELECT COUNT(*) FROM skills WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    mcp_count = conn.execute('SELECT COUNT(*) FROM mcp WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    deployment_count = conn.execute('SELECT COUNT(*) FROM deployments WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    sim_count = conn.execute('SELECT COUNT(*) FROM simulator_logs WHERE user_id = ?', (session['user_id'],)).fetchone()[0]

    recent_skills = conn.execute(
        'SELECT * FROM skills WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
        (session['user_id'],)
    ).fetchall()

    user_mcps = conn.execute(
        'SELECT * FROM mcp WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
        (session['user_id'],)
    ).fetchall()

    user_deployments = conn.execute(
        'SELECT * FROM deployments WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
        (session['user_id'],)
    ).fetchall()

    # System-wide metrics (for Admin and system summary)
    all_users = conn.execute('SELECT id, name, email, role, organization, created_at FROM users ORDER BY id DESC').fetchall()
    total_users_count = len(all_users)
    global_skill_count = conn.execute('SELECT COUNT(*) FROM skills').fetchone()[0]
    global_mcp_count = conn.execute('SELECT COUNT(*) FROM mcp').fetchone()[0]
    all_system_skills = conn.execute(
        'SELECT skills.*, users.name as user_name FROM skills JOIN users ON skills.user_id = users.id ORDER BY skills.created_at DESC LIMIT 10'
    ).fetchall()

    ai_provider = 'Rule Engine'
    if os.environ.get('GEMINI_API_KEY'):
        ai_provider = 'Gemini 1.5 Flash'
    elif os.environ.get('OPENAI_API_KEY'):
        ai_provider = 'OpenAI GPT-3.5'

    conn.close()

    return render_template(
        'dashboard.html',
        user=user,
        is_admin=is_admin,
        role_category=role_category,
        skill_count=skill_count,
        mcp_count=mcp_count,
        deployment_count=deployment_count,
        sim_count=sim_count,
        recent_skills=recent_skills,
        user_mcps=user_mcps,
        user_deployments=user_deployments,
        all_users=all_users,
        total_users_count=total_users_count,
        global_skill_count=global_skill_count,
        global_mcp_count=global_mcp_count,
        all_system_skills=all_system_skills,
        ai_provider=ai_provider
    )


@app.route('/skills', methods=['GET', 'POST'])
def skills():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    is_admin = check_is_admin(user['role'] if user else '')

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        desc = request.form.get('description', '').strip()
        if name and desc:
            conn.execute(
                'INSERT INTO skills (user_id, name, description) VALUES (?, ?, ?)',
                (session['user_id'], name, desc)
            )
            conn.commit()
        conn.close()
        return redirect(url_for('skills'))

    user_skills = conn.execute(
        'SELECT * FROM skills WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()

    all_system_skills = []
    if is_admin:
        all_system_skills = conn.execute(
            'SELECT skills.*, users.name as user_name, users.email as user_email FROM skills JOIN users ON skills.user_id = users.id ORDER BY skills.created_at DESC'
        ).fetchall()

    conn.close()
    return render_template('skills.html', skills=user_skills, all_system_skills=all_system_skills, user=user, is_admin=is_admin)


@app.route('/mcp', methods=['GET', 'POST'])
def mcp():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    is_admin = check_is_admin(user['role'] if user else '')

    if request.method == 'POST':
        provider = request.form.get('provider', '').strip()
        api_key = request.form.get('api_key', '').strip()
        if provider and api_key:
            conn.execute(
                'INSERT INTO mcp (user_id, provider, api_key) VALUES (?, ?, ?)',
                (session['user_id'], provider, api_key)
            )
            conn.commit()
        conn.close()
        return redirect(url_for('mcp'))

    user_mcp = conn.execute(
        'SELECT * FROM mcp WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()

    all_system_mcps = []
    if is_admin:
        all_system_mcps = conn.execute(
            'SELECT mcp.*, users.name as user_name FROM mcp JOIN users ON mcp.user_id = users.id ORDER BY mcp.created_at DESC'
        ).fetchall()

    conn.close()
    return render_template('mcp.html', mcps=user_mcp, all_system_mcps=all_system_mcps, user=user, is_admin=is_admin)


@app.route('/freshworks', methods=['GET', 'POST'])
def freshworks():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    is_admin = check_is_admin(user['role'] if user else '')

    if request.method == 'POST':
        ws_type = request.form.get('workspace_type', 'Freshdesk')
        domain = request.form.get('domain', '').strip()
        if domain:
            conn.execute(
                'INSERT INTO deployments (user_id, workspace_type, domain) VALUES (?, ?, ?)',
                (session['user_id'], ws_type, domain)
            )
            conn.commit()
        conn.close()
        return redirect(url_for('freshworks'))

    deployments = conn.execute(
        'SELECT * FROM deployments WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()

    all_deployments = []
    if is_admin:
        all_deployments = conn.execute(
            'SELECT deployments.*, users.name as user_name FROM deployments JOIN users ON deployments.user_id = users.id ORDER BY deployments.created_at DESC'
        ).fetchall()

    conn.close()
    return render_template('freshworks.html', user=user, deployments=deployments, all_deployments=all_deployments, is_admin=is_admin)


@app.route('/knowledge_graph')
def knowledge_graph():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    is_admin = check_is_admin(user['role'] if user else '')

    skills = conn.execute('SELECT * FROM skills WHERE user_id = ?', (session['user_id'],)).fetchall()
    mcps = conn.execute('SELECT * FROM mcp WHERE user_id = ?', (session['user_id'],)).fetchall()
    all_users = []
    if is_admin:
        all_users = conn.execute('SELECT id, name, email, role, organization FROM users').fetchall()

    conn.close()
    return render_template('knowledge_graph.html', user=user, skills=skills, mcps=mcps, all_users=all_users, is_admin=is_admin)


@app.route('/simulator', methods=['GET', 'POST'])
def simulator():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    is_admin = check_is_admin(user['role'] if user else '')

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        cmd = data.get('command', '') or request.form.get('command', '')
        cmd = cmd.strip()

        if cmd:
            user_name = session.get('name', 'Agent')
            resp = get_ai_response(cmd, user_name)
            conn.execute(
                'INSERT INTO simulator_logs (user_id, command, response) VALUES (?, ?, ?)',
                (session['user_id'], cmd, resp)
            )
            conn.commit()
            conn.close()
            return jsonify({'response': resp})
        else:
            conn.close()
            return jsonify({'error': 'Empty command'}), 400

    logs = conn.execute(
        'SELECT * FROM simulator_logs WHERE user_id = ? ORDER BY created_at ASC',
        (session['user_id'],)
    ).fetchall()

    ai_provider = None
    if os.environ.get('GEMINI_API_KEY'):
        ai_provider = 'Gemini'
    elif os.environ.get('OPENAI_API_KEY'):
        ai_provider = 'OpenAI'

    conn.close()
    return render_template('simulator.html', user=user, logs=logs, ai_provider=ai_provider, is_admin=is_admin)


@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    is_admin = check_is_admin(user['role'] if user else '')

    skill_count = conn.execute('SELECT COUNT(*) FROM skills WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    mcp_count = conn.execute('SELECT COUNT(*) FROM mcp WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    sim_count = conn.execute('SELECT COUNT(*) FROM simulator_logs WHERE user_id = ?', (session['user_id'],)).fetchone()[0]

    role_distribution = []
    total_users = 0
    total_system_skills = 0
    total_system_mcps = 0

    if is_admin:
        role_distribution = conn.execute('SELECT role, COUNT(*) as count FROM users GROUP BY role').fetchall()
        total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        total_system_skills = conn.execute('SELECT COUNT(*) FROM skills').fetchone()[0]
        total_system_mcps = conn.execute('SELECT COUNT(*) FROM mcp').fetchone()[0]

    conn.close()
    return render_template(
        'analytics.html',
        user=user,
        is_admin=is_admin,
        skill_count=skill_count,
        mcp_count=mcp_count,
        sim_count=sim_count,
        role_distribution=role_distribution,
        total_users=total_users,
        total_system_skills=total_system_skills,
        total_system_mcps=total_system_mcps
    )


@app.route('/api_keys', methods=['GET', 'POST'])
def api_keys():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    is_admin = check_is_admin(user['role'] if user else '')

    if request.method == 'POST':
        name = request.form.get('name', 'Default Key').strip()
        new_key = f"agx_{secrets.token_urlsafe(16)}"
        conn.execute(
            'INSERT INTO api_keys (user_id, name, key_value) VALUES (?, ?, ?)',
            (session['user_id'], name, new_key)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('api_keys'))

    keys = conn.execute(
        'SELECT * FROM api_keys WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()

    all_keys = []
    if is_admin:
        all_keys = conn.execute(
            'SELECT api_keys.*, users.name as user_name FROM api_keys JOIN users ON api_keys.user_id = users.id ORDER BY api_keys.created_at DESC'
        ).fetchall()

    conn.close()
    return render_template('api_keys.html', user=user, keys=keys, all_keys=all_keys, is_admin=is_admin)


@app.route('/admin/add_user', methods=['POST'])
def admin_add_user():
    """Admin-only: create a new platform user account."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    conn = get_db_connection()
    me = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not me or not check_is_admin(me['role']):
        conn.close()
        return jsonify({'error': 'Admin privileges required'}), 403

    name         = request.form.get('name', '').strip()
    email        = request.form.get('email', '').strip()
    password     = request.form.get('password', '').strip()
    role         = request.form.get('role', 'Developer').strip()
    organization = request.form.get('organization', '').strip()

    if not name or not email or not password:
        conn.close()
        return jsonify({'error': 'Name, email and password are required'}), 400

    try:
        conn.execute(
            'INSERT INTO users (name, email, password, role, profile_pic, phone, organization) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, email, password, role, 'default.png', '', organization)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': f'An account with email "{email}" already exists'}), 409
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

    conn.close()
    return jsonify({'message': f'User "{name}" created successfully', 'redirect': '/dashboard'})


@app.route('/admin/delete_user/<int:target_id>', methods=['POST'])
def admin_delete_user(target_id):
    """Admin-only: permanently delete a platform user account."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    conn = get_db_connection()
    me = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not me or not check_is_admin(me['role']):
        conn.close()
        return jsonify({'error': 'Admin privileges required'}), 403

    if target_id == session['user_id']:
        conn.close()
        return jsonify({'error': 'You cannot delete your own account'}), 400

    target = conn.execute('SELECT * FROM users WHERE id = ?', (target_id,)).fetchone()
    if not target:
        conn.close()
        return jsonify({'error': 'User not found'}), 404

    # Cascade-delete related records
    conn.execute('DELETE FROM skills WHERE user_id = ?', (target_id,))
    conn.execute('DELETE FROM mcp WHERE user_id = ?', (target_id,))
    conn.execute('DELETE FROM deployments WHERE user_id = ?', (target_id,))
    conn.execute('DELETE FROM simulator_logs WHERE user_id = ?', (target_id,))
    conn.execute('DELETE FROM api_keys WHERE user_id = ?', (target_id,))
    conn.execute('DELETE FROM users WHERE id = ?', (target_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': f'User "{target["name"]}" deleted successfully', 'redirect': '/dashboard'})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/data')
def api_data():
    return jsonify({"status": "success", "data": []})


if __name__ == '__main__':
    app.run(port=3000, debug=True)

