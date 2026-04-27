from flask import Flask, request, render_template_string, redirect
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "notesdb")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def index():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM notes ORDER BY id DESC")
        notes = cur.fetchall()
    conn.close()

    return render_template_string("""
    <h1>Student Notes App</h1>

    <form method="POST" action="/add">
        <input name="note" placeholder="Enter note" required>
        <button type="submit">Add Note</button>
    </form>

    <hr>

    {% for note in notes %}
        <p>{{ note.id }}. {{ note.content }}</p>
    {% endfor %}
    """, notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    note = request.form["note"]

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO notes(content) VALUES(%s)", (note,))
        conn.commit()
    conn.close()

    return redirect("/")

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)