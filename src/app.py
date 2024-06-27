from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

db = MySQL(app)


@app.route('/')
def index():
    session.pop('cart', None)  # Vaciar el carrito al acceder al sitio
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form['username']
        password = request.form['password']

        cur = db.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cur.execute(query, (username, password))
        user = cur.fetchone()
        cur.close()

        try:
            # Vereficar en la base de datos
            if user:
                # Inicio de sesion exitoso
                flash('¡Inicio de sesion exitoso!', 'success')
                return redirect(url_for('shop'))
            else:
                # Inicio de sesion fallido
                flash('No puede ingresar, intente nuevamente', 'danger')
                return redirect(url_for('index'))
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        neighborhood = request.form['neighborhood']

        try:
            # Insertar en la base de datos
            cur = db.connection.cursor()
            query = "INSERT INTO users (username, password, fullname, email, neighborhood) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, (username, password,
                        fullname, email, neighborhood))
            db.connection.commit()
            cur.close()
            flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar: {e}', 'danger')
            db.connection.rollback()

    return render_template('register.html')


@app.route('/shop')
def shop():
    products = [
        {"id": 1, "name": "Pizza Muzarella", "price": 5900,
            "image": "static/img/muzarella.jpg"},
        {"id": 2, "name": "Pizza Napolitana", "price": 6800,
            "image": "static/img/napolitana.jpg"},
        {"id": 3, "name": "Pizza Jamón y Morrón", "price": 7900,
            "image": "static/img/jamon_morron.jpg"},
        {"id": 4, "name": "Pizza Fugazeta", "price": 8650,
            "image": "static/img/fugazeta.jpg"},
        {"id": 5, "name": "Pizza Fugazeta con Jamón", "price": 15550,
            "image": "static/img/fugazeta_jamon.jpg"},
        {"id": 6, "name": "Pizza Calabresa", "price": 5900,
            "image": "static/img/calabresa.jpg"}
    ]
    return render_template('shop.html', products=products)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Obtener la lista de productos
    products = [
        {"id": 1, "name": "Pizza Muzarella", "price": 5900,
            "image": "static/img/muzarella.jpg"},
        {"id": 2, "name": "Pizza Napolitana", "price": 6800,
            "image": "static/img/napolitana.jpg"},
        {"id": 3, "name": "Pizza Jamón y Morrón", "price": 7900,
            "image": "static/img/jamon_morron.jpg"},
        {"id": 4, "name": "Pizza Fugazeta", "price": 8650,
            "image": "static/img/fugazeta.jpg"},
        {"id": 5, "name": "Pizza Fugazeta con Jamón", "price": 15550,
            "image": "static/img/fugazeta_jamon.jpg"},
        {"id": 6, "name": "Pizza Calabresa", "price": 5900,
            "image": "static/img/calabresa.jpg"}
    ]

    # Buscar el producto
    product = next((p for p in products if p["id"] == product_id), None)

    if product:
        # Obtener el carrito de la sesión o crear uno nuevo
        if 'cart' not in session:
            session['cart'] = []

        # Añadir el producto al carrito
        session['cart'].append(product)
        flash(f'{product["name"]} añadido al carrito.', 'success')
    else:
        flash('Producto no encontrado.', 'danger')

    return redirect(url_for('shop'))


@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    flash('Producto eliminado del carrito.', 'success')
    return redirect(url_for('cart'))


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
