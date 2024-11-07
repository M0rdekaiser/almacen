from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "my_secret_key"

def get_db_connection():
    conn = sqlite3.connect('almacen.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/add', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        if not descripcion or not cantidad or not precio:
            flash('Por favor, completa todos los campos')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)',
                         (descripcion, cantidad, float(precio)))
            conn.commit()
            conn.close()
            flash('Producto agregado exitosamente')
            return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_product(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        if not descripcion or not cantidad or not precio:
            flash('Por favor, completa todos los campos')
        else:
            conn.execute('UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?',
                         (descripcion, cantidad, float(precio), id))
            conn.commit()
            conn.close()
            flash('Producto actualizado exitosamente')
            return redirect(url_for('index'))

    conn.close()
    return render_template('edit_product.html', producto=producto)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM producto WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Producto eliminado exitosamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
