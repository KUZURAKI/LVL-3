from flask import Flask, request, render_template
import sqlite3
import os

# ЗАПУСТИТЬ ФАЙЛ python app.py

# ПОСЛЕ ЕГО ЗАПУСКА В КОНСОЛИ (FLASK) ТАМ БУДЕТ ССЫЛКА. НА ЭТУ ССЫЛКУ НУЖНО НАЖАТЬ,
# И ОТКРОЕТСЯ САЙТ.

app = Flask(__name__, template_folder='../front/templates', static_folder='../front/static')

def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            about TEXT NOT NULL,
            avatar TEXT
        )''')
        conn.commit()
        conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        about = request.form.get('about')
        avatar = request.form.get('avatar')

        print(f"Login: {login}, Password: {password}, Confirm: {confirm_password}")

        if password != confirm_password:
            return "Пароли не совпадают!"

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''INSERT INTO users (login, password, full_name, email, phone, about, avatar)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (login, password, full_name, email, phone, about, avatar))
            conn.commit()
            conn.close()
        except Exception as e:
            return f"Ошибка при сохранении: {str(e)}"

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()

    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)