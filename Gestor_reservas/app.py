from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/detalle_estandar')
def detalle_estandar():
    return render_template('detalle-estandar.html')

@app.route('/detalle_deluxe')
def detalle_deluxe():
    return render_template('detalle-deluxe.html')

@app.route('/detalle_suite')
def detalle_suite():
    return render_template('detalle-suite.html')

@app.route('/detalle_presidencial')
def detalle_presidencial():
    return render_template('detalle-presidencial.html')

@app.route('/confirmar-reserva', methods=['POST'])
def confirmar_reserva():
    if request.method == 'POST':
        # Los nombres en [] deben coincidir exactamente con el 'name' del HTML
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        f_entrada = request.form['entrada']
        f_salida = request.form['salida']
        huespedes = request.form['huespedes']
        habitacion = request.form['habitacion']


        return redirect(url_for('reservas'))

@app.route('/reservas')
def reservas():
    return render_template('reservas.html')

@app.route('/eliminar_reserva/<int:id>')

def eliminar_reserva(id):
    return redirect(url_for('reservas'))

if __name__ == '__main__':
    app.run(debug=True)