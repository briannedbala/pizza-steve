from flask import Flask, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

db = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = db.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cur.execute(query, (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            flash('Bienvenido', 'success')
            return redirect(url_for('shop'))
        else:
            flash('No puede ingresar', 'danger')
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['full-name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        neighborhood = request.form['neighborhood']

        cur = db.connection.cursor()
        cur.execute("INSERT INTO users (username, password, fullname, email, neighborhood) VALUES (%s, %s, %s, %s, %s,)",
                    (username, password, fullname, email, neighborhood))
        db.connection.commit()
        cur.close()

        flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
