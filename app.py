from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Base de datos inicial
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']  # Recibe el rol

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password, role)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password, role))
            conn.commit()
            conn.close()

            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username or email already exists!")
            return redirect(url_for('register'))
    return render_template('register.html')

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[4]

            flash(f"Welcome back, {user[1]}!")

            # Redirigir según el rol
            if user[4] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user[4] == 'printer':
                return redirect(url_for('printer_dashboard'))
            elif user[4] == 'client':
                return redirect(url_for('client_dashboard'))
        else:
            flash("Invalid credentials!")
            return redirect(url_for('login'))
    return render_template('login.html')

# Ruta de cierre de sesión
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for('index'))

# Rutas específicas para cada rol
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        flash("Access denied!")
        return redirect(url_for('login'))

@app.route('/printer-dashboard')
def printer_dashboard():
    if 'user_id' in session and session['role'] == 'printer':
        return render_template('printer_dashboard.html')
    else:
        flash("Access denied!")
        return redirect(url_for('login'))

@app.route('/client-dashboard')
def client_dashboard():
    if 'user_id' in session and session['role'] == 'client':
        return render_template('client_dashboard.html')
    else:
        flash("Access denied!")
        return redirect(url_for('login'))
    
@app.route('/approve-printer/<int:printer_id>', methods=['POST', 'GET'])
def approve_printer(printer_id):
    if 'user_id' in session and session['role'] == 'admin':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Actualizar el estado de la solicitud a "approved"
        cursor.execute('UPDATE printer_requests SET status = "approved" WHERE id = ?', (printer_id,))
        conn.commit()
        conn.close()

        flash("Printer request approved successfully!")
        return redirect(url_for('admin_panel'))
    else:
        flash("Access denied!")
        return redirect(url_for('login'))
    
    

@app.route('/approve-client/<int:client_id>', methods=['POST', 'GET'])
def approve_client(client_id):
    if 'user_id' in session and session['role'] == 'admin':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Actualizar el estado de la solicitud a "approved"
        cursor.execute('UPDATE client_requests SET status = "approved" WHERE id = ?', (client_id,))
        conn.commit()
        conn.close()

        flash("Client request approved successfully!")
        return redirect(url_for('admin_panel'))
    else:
        flash("Access denied!")
        return redirect(url_for('login'))

    

@app.route('/submit-printer-request', methods=['GET', 'POST'])
def submit_printer_request():
    if 'user_id' in session and session['role'] == 'printer':
        if request.method == 'POST':
            user_id = session['user_id']
            characteristics = request.form['characteristics']
            community = request.form['community']
            province = request.form['province']

            # Procesar materiales seleccionados
            main_material = request.form['main_material']
            sub_material = request.form.get('sub_material', '')
            other_material = request.form.get('other_material', '')

            # Determinar el material final
            if main_material == "Other":
                materials = other_material
            else:
                materials = sub_material or main_material

            if not materials:
                flash("You must select or specify at least one material.")
                return redirect(url_for('submit_printer_request'))

            # Guardar en la base de datos
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO printer_requests (user_id, characteristics, community, province, materials, status)
                VALUES (?, ?, ?, ?, ?, "pending")
            ''', (user_id, characteristics, community, province, materials))
            conn.commit()
            conn.close()

            flash("Your printer request has been submitted successfully!")
            return redirect(url_for('printer_dashboard'))

        return render_template('submit_printer_request.html')
    else:
        flash("Access denied!")
        return redirect(url_for('login'))




    
@app.route('/admin-panel')
def admin_panel():
    if 'user_id' in session and session['role'] == 'admin':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Consultar solicitudes de printers
        cursor.execute('''
            SELECT pr.id, pr.characteristics, pr.materials, 
                   pr.community || ', ' || pr.province AS location, 
                   pr.status, u.email
            FROM printer_requests pr
            JOIN users u ON pr.user_id = u.id
        ''')
        printer_requests = cursor.fetchall()

        # Consultar solicitudes de clientes
        cursor.execute('''
            SELECT cr.id, cr.requirements, cr.budget, 
                   cr.community || ', ' || cr.province AS location, 
                   cr.status, u.email
            FROM client_requests cr
            JOIN users u ON cr.user_id = u.id
        ''')
        client_requests = cursor.fetchall()

        conn.close()

        # Revisar solicitudes de printers para validar datos
        for printer_request in printer_requests:
            if not printer_request[2]:  # Si materials está vacío
                flash(f"Printer request ID {printer_request[0]} has no materials specified.")

        return render_template('admin_panel.html', printer_requests=printer_requests, client_requests=client_requests)
    else:
        flash("Access denied!")
        return redirect(url_for('login'))






@app.route('/submit-client-request', methods=['GET', 'POST'])
def submit_client_request():
    if 'user_id' in session and session['role'] == 'client':
        if request.method == 'POST':
            user_id = session['user_id']
            requirements = request.form['requirements']
            budget = request.form['budget']
            community = request.form['community']
            province = request.form['province']

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO client_requests (user_id, requirements, budget, community, province, status)
                VALUES (?, ?, ?, ?, ?, "pending")
            ''', (user_id, requirements, budget, community, province))
            conn.commit()
            conn.close()

            flash("Your request has been submitted successfully!")
            return redirect(url_for('client_dashboard'))
        return render_template('submit_client_request.html')
    else:
        flash("Access denied!")
        return redirect(url_for('login'))
    


@app.route('/reject-printer/<int:request_id>')
def reject_printer(request_id):
    if 'user_id' in session and session['role'] == 'admin':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE printer_requests SET status = "rejected" WHERE id = ?', (request_id,))
        conn.commit()
        conn.close()
        flash("Printer request rejected.")
        return redirect(url_for('admin_panel'))
    else:
        flash("Access denied!")
        return redirect(url_for('login'))


@app.route('/reject-client/<int:request_id>')
def reject_client(request_id):
    if 'user_id' in session and session['role'] == 'admin':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE client_requests SET status = "rejected" WHERE id = ?', (request_id,))
        conn.commit()
        conn.close()
        flash("Client request rejected.")
        return redirect(url_for('admin_panel'))
    else:
        flash("Access denied!")
        return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
