import re

with open('app.py', 'r') as f:
    content = f.read()

new_login = """
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            return jsonify({'user': {'email': user['email'], 'full_name': user['name'], 'role': 'user'}})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    return render_template('login.html')
"""

content = re.sub(r'@app\.route\(''/login''.*?return render_template\(''login\.html''\)', new_login.strip(), content, flags=re.DOTALL)

new_register = """
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('full_name', 'User')
        if not name:
             name = request.form.get('name', 'User')
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'Email already exists'}), 400
        conn.close()
        return jsonify({'message': 'success'})
    return render_template('register.html')
"""

content = re.sub(r'@app\.route\(''/register''.*?return render_template\(''register\.html''\)', new_register.strip(), content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(content)
