import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
# In production, set SECRET_KEY env var. For development, this is fine:
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Database file
DATABASE = 'database.db'

# DB schema
init_schema = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    word_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # enable check_same_thread to False is not required for simple dev usage,
        # but keep default sqlite connection settings for simplicity
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_database():
    """Always ensure schema exists (idempotent)."""
    with app.app_context():
        db = get_db()
        db.cursor().executescript(init_schema)
        db.commit()

# initialize DB (safe to call every start)
init_database()

# set g.user for templates
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        if user:
            g.user = user

# ---------------- Routes ----------------

@app.route('/')
def index():
    if g.user:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        db = get_db()
        try:
            hashed_password = generate_password_hash(password)
            db.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
            db.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('An account with that email already exists.', 'danger')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not g.user:
        flash('Please log in to view your dashboard.', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    stories = db.execute(
        'SELECT * FROM stories WHERE user_id = ? ORDER BY created_at DESC',
        (g.user['id'],)
    ).fetchall()

    return render_template('dashboard.html', stories=stories)

@app.route('/new_story', methods=['GET', 'POST'])
def new_story():
    if not g.user:
        flash('Please log in to write a story.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        word_count = len(content.split())
        db = get_db()
        db.execute(
            'INSERT INTO stories (user_id, title, content, word_count) VALUES (?, ?, ?, ?)',
            (g.user['id'], title, content, word_count)
        )
        db.commit()
        flash('Story saved successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('new_story.html', story=None)

@app.route('/edit_story/<int:story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    if not g.user:
        flash('Please log in to edit a story.', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    story = db.execute(
        'SELECT * FROM stories WHERE id = ? AND user_id = ?',
        (story_id, g.user['id'])
    ).fetchone()

    if not story:
        flash('Story not found or you do not have permission to edit it.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        word_count = len(content.split())
        db.execute(
            'UPDATE stories SET title = ?, content = ?, word_count = ? WHERE id = ?',
            (title, content, word_count, story_id)
        )
        db.commit()
        flash('Story updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('new_story.html', story=story)

@app.route('/confirm_delete/<int:story_id>', methods=['GET', 'POST'])
def confirm_delete(story_id):
    """Server-side confirmation page (no JS)."""
    if not g.user:
        flash('Please log in to delete a story.', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    story = db.execute(
        'SELECT * FROM stories WHERE id = ? AND user_id = ?',
        (story_id, g.user['id'])
    ).fetchone()

    if not story:
        flash('Story not found or you do not have permission to delete it.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        db.execute('DELETE FROM stories WHERE id = ? AND user_id = ?', (story_id, g.user['id']))
        db.commit()
        flash('Story deleted successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('confirm_delete.html', story=story)

# keep original delete endpoint (optional; not used by dashboard now)
@app.route('/delete_story/<int:story_id>', methods=['POST'])
def delete_story(story_id):
    if not g.user:
        flash('Please log in to delete a story.', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    db.execute(
        'DELETE FROM stories WHERE id = ? AND user_id = ?',
        (story_id, g.user['id'])
    )
    db.commit()
    flash('Story deleted successfully.', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
