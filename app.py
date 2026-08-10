from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/author')
def author():
    return render_template('author.html')


@app.route('/planner')
def planner():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, created_at FROM tasks')
    all_tasks = cursor.fetchall()
    conn.close()
    return render_template('planner.html', tasks=all_tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description, created_at) VALUES (?, ?, ?)', (title, description, created_at))
    conn.commit()
    conn.close()

    return redirect('/planner')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

    return redirect('/planner')


if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

    app.run(debug=True)