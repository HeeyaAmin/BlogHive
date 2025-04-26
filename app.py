from flask import Flask, render_template, request, jsonify, send_file, session, redirect
import mysql.connector
import secrets
from match_keywords_langchain import match_keywords_userside
from tts import audios

# Flask app
app = Flask(__name__, static_url_path='/static')

# Secure session key
app.secret_key = secrets.token_hex(16)

# ✅ MySQL connection (update this if needed)
connection = mysql.connector.connect(
    host="localhost",
    port=8889,  # ✅ since you're using local instance 8889
    user="root",
    password="root",  # put your password here if you have one
    database="blogs"
)

# ----------------------------
# 🔐 Login route
# ----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['logged_in'] = True
            return redirect('/')
        else:
            return "<script>alert('Incorrect email or password'); window.location.href='/login';</script>"

    return render_template('login.html')

# ----------------------------
# 📝 Signup route
# ----------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, password)
        )
        connection.commit()
        cursor.close()
        return redirect('/login')

    return render_template('signup.html')

# ----------------------------
# 🎯 Home page: select keywords
# ----------------------------
@app.route('/', methods=['GET'])
def index():
    if not session.get('logged_in'):
        return redirect('/login')

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM keywords")
    keywords = cursor.fetchall()
    cursor.close()

    return render_template('indexo.html', data=keywords)

# ----------------------------
# 🔍 Match keywords (AJAX)
# ----------------------------
@app.route('/match_keywords', methods=['POST'])
def match_keywords():
    selected_keywords = request.json.get('selected_keywords', [])
    matched_titles, descriptions, image_urls = match_keywords_userside(selected_keywords)
    return jsonify(matched_entries=matched_titles, desc_title=descriptions, image_url=image_urls)

# ----------------------------
# 🔊 Generate and return audio paths
# ----------------------------
@app.route('/get_the_audios', methods=['POST'])
def get_the_audios():
    title = request.json.get('title')
    eng, fre, ger = audios(title)
    return jsonify(en=eng, fr=fre, ge=ger)

# ----------------------------
# 🎧 Download audio
# ----------------------------
@app.route('/download_mp3', methods=['POST'])
def download_mp3():
    path = request.json.get('mp3_file_path')
    return send_file(path, as_attachment=True)

# ----------------------------
# 🚀 Run the app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
