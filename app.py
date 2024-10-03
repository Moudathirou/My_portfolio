"""from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from connexion import authenticate
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mouda'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
csrf = CSRFProtect(app)

# Assurez-vous que le dossier d'upload existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('portfolio.db')
    conn.row_factory = sqlite3.Row
    return conn

# Créez la table des projets si elle n'existe pas
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, title TEXT, photo TEXT, github TEXT)')
    conn.close()

init_db()

@app.route('/')
def home():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return render_template('index.html', projects=projects)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if authenticate(username, password):
                return jsonify({'success': True})
            else:
                return jsonify({'success': False}), 401
        else:
            return jsonify({'error': 'Request must be JSON'}), 400
    
    return render_template('admin.html')

@app.route('/admin/update_profile', methods=['POST'])
def update_profile():
    if 'photo' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile.jpg'))
        return jsonify({'success': True})

@app.route('/admin/add_project', methods=['POST'])
def add_project():
    title = request.form['title']
    github = request.form['github']
    if 'photo' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = get_db_connection()
        conn.execute('INSERT INTO projects (title, photo, github) VALUES (?, ?, ?)',
                     (title, filename, github))
        conn.commit()
        project_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return jsonify({'success': True, 'project': {'id': project_id, 'title': title, 'photo': filename, 'github': github}})

@app.route('/admin/get_projects')
def get_projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return jsonify([dict(project) for project in projects])

if __name__ == '__main__':
    app.run(debug=True)"""


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
import os
from auth import authenticate, create_user
from database import init_db, get_db_connection
from werkzeug.security import generate_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mouda'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
csrf = CSRFProtect(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

init_db()

@app.route('/')
def home():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    experiences = conn.execute('SELECT * FROM experiences ORDER BY start_date DESC').fetchall()
    skills = conn.execute('SELECT * FROM skills').fetchall()
    conn.close()
    return render_template('index.html', projects=projects, experiences=experiences, skills=skills)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if authenticate(username, password):
                return jsonify({'success': True})
            else:
                return jsonify({'success': False}), 401
        else:
            return jsonify({'error': 'Request must be JSON'}), 400
    
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    experiences = conn.execute('SELECT * FROM experiences ORDER BY start_date DESC').fetchall()
    skills = conn.execute('SELECT * FROM skills').fetchall()
    conn.close()
    return render_template('admin.html', projects=projects, experiences=experiences, skills=skills)

@app.route('/create_admin', methods=['POST'])
def create_admin():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if create_user(username, password):
            return jsonify({'success': True, 'message': 'Admin user created successfully'})
        else:
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

@app.route('/admin/update_profile', methods=['POST'])
def update_profile():
    if 'photo' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile.jpg'))
        return jsonify({'success': True})

@app.route('/admin/add_project', methods=['POST'])
def add_project():
    title = request.form['title']
    github = request.form['github']
    if 'photo' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = get_db_connection()
        conn.execute('INSERT INTO projects (title, photo, github) VALUES (?, ?, ?)',
                     (title, filename, github))
        conn.commit()
        project_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return jsonify({'success': True, 'project': {'id': project_id, 'title': title, 'photo': filename, 'github': github}})

@app.route('/admin/add_experience', methods=['POST'])
def add_experience():
    title = request.form['title']
    company = request.form['company']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    description = request.form['description']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO experiences (title, company, start_date, end_date, description) VALUES (?, ?, ?, ?, ?)',
                 (title, company, start_date, end_date, description))
    conn.commit()
    experience_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    
    return jsonify({'success': True, 'experience': {'id': experience_id, 'title': title, 'company': company, 'start_date': start_date, 'end_date': end_date, 'description': description}})

@app.route('/admin/add_skill', methods=['POST'])
def add_skill():
    name = request.form['name']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO skills (name) VALUES (?)', (name,))
    conn.commit()
    skill_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    
    return jsonify({'success': True, 'skill': {'id': skill_id, 'name': name}})

@app.route('/admin/get_projects')
def get_projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return jsonify([dict(project) for project in projects])

@app.route('/admin/get_experiences')
def get_experiences():
    conn = get_db_connection()
    experiences = conn.execute('SELECT * FROM experiences ORDER BY start_date DESC').fetchall()
    conn.close()
    return jsonify([dict(experience) for experience in experiences])

@app.route('/admin/get_skills')
def get_skills():
    conn = get_db_connection()
    skills = conn.execute('SELECT * FROM skills').fetchall()
    conn.close()
    return jsonify([dict(skill) for skill in skills])

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class AdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


@app.route('/setup_admin', methods=['GET', 'POST'])
def setup_admin():
    form = AdminForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('setup_admin'))
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                         (username, generate_password_hash(password)))
            conn.commit()
            flash('Admin user created successfully.')
            return redirect(url_for('home'))  # ou une autre page appropriée
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()
    
    return render_template('setup_admin.html', form=form)



@app.route('/admin/delete_project', methods=['POST'])
def delete_project():
    project_id = request.form['id']
    conn = get_db_connection()
    conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/admin/delete_experience', methods=['POST'])
def delete_experience():
    experience_id = request.form['id']
    conn = get_db_connection()
    conn.execute('DELETE FROM experiences WHERE id = ?', (experience_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/admin/delete_skill', methods=['POST'])
def delete_skill():
    skill_id = request.form['id']
    conn = get_db_connection()
    conn.execute('DELETE FROM skills WHERE id = ?', (skill_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})





if __name__ == '__main__':
    app.run(debug=True)














