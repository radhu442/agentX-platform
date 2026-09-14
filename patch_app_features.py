import re

with open('app.py', 'r') as f:
    app_code = f.read()

new_routes = """
import os
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('full_name', 'User')
        if not name:
            name = request.form.get('name', 'User')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'Agent Developer')
        
        filename = 'default.png'
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, password, role, profile_pic) VALUES (?, ?, ?, ?, ?)', (name, email, password, role, filename))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'Email already exists'}), 400
        conn.close()
        return jsonify({'message': 'Registration successful'})
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    skill_count = conn.execute('SELECT COUNT(*) FROM skills WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    mcp_count = conn.execute('SELECT COUNT(*) FROM mcp WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    conn.close()
    
    return render_template('dashboard.html', user=user, skill_count=skill_count, mcp_count=mcp_count)

@app.route('/skills', methods=['GET', 'POST'])
def skills():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('description')
        conn.execute('INSERT INTO skills (user_id, name, description) VALUES (?, ?, ?)', (session['user_id'], name, desc))
        conn.commit()
        return redirect(url_for('skills'))
        
    user_skills = conn.execute('SELECT * FROM skills WHERE user_id = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('skills.html', skills=user_skills, user=user)

@app.route('/mcp', methods=['GET', 'POST'])
def mcp():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    if request.method == 'POST':
        provider = request.form.get('provider')
        api_key = request.form.get('api_key')
        conn.execute('INSERT INTO mcp (user_id, provider, api_key) VALUES (?, ?, ?)', (session['user_id'], provider, api_key))
        conn.commit()
        return redirect(url_for('mcp'))
        
    user_mcp = conn.execute('SELECT * FROM mcp WHERE user_id = ?', (session['user_id'],)).fetchall()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('mcp.html', mcps=user_mcp, user=user)

@app.route('/simulator')
def simulator():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('simulator.html', user=user)

"""

# Replace register and dashboard
app_code = re.sub(r'@app\.route\(''/register''.*?return render_template\(''register\.html''\)', '', app_code, flags=re.DOTALL)
app_code = re.sub(r'@app\.route\(''/dashboard''.*?return render_template\(''dashboard\.html'', name=session\.get\(''name''\)\)', '', app_code, flags=re.DOTALL)

# Insert new routes before @app.route('/logout')
app_code = app_code.replace("@app.route('/logout')", new_routes + "\n@app.route('/logout')")
# Add os import if missing
if 'from werkzeug.utils import secure_filename' not in app_code:
    app_code = app_code.replace("import os", "import os\nfrom werkzeug.utils import secure_filename")

with open('app.py', 'w') as f:
    f.write(app_code)

