from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Database connection function
def get_db_connection():
    conn = sqlite3.connect('testimonials.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


# Route to display the landing page
@app.route('/')
def landing():
    conn = get_db_connection()
    testimonials = conn.execute('SELECT * FROM testimonials').fetchall()
    conn.close()
    return render_template('landing.html', testimonials=testimonials)


# Route to handle new testimonials submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    opinion = request.form['opinion']

    if name and opinion:
        conn = get_db_connection()
        conn.execute('INSERT INTO testimonials (name, opinion) VALUES (?, ?)', (name, opinion))
        conn.commit()
        conn.close()
    return redirect(url_for('landing'))


if __name__ == '__main__':
    app.run(debug=True)
