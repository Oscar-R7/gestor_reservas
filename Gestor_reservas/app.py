import os
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

ruta_csv = 'registro.csv'

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
        
        # Captura de datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        f_entrada = request.form['entrada']
        f_salida = request.form['salida']
        huespedes = request.form['huespedes']
        habitacion = request.form['habitacion']

        # Verificamos si el archivo ya existe antes de escribir
        file_exists = os.path.isfile(ruta_csv)

        # Guardar en el archivo CSV
        with open(ruta_csv, mode='a', newline='', encoding='utf-8') as archivo:
            columnas = ['nombre', 'email', 'telefono', 'entrada', 'salida', 'huespedes', 'habitacion']
            
            
            writer = csv.DictWriter(archivo, fieldnames=columnas)

            # Si el archivo no existe, escribe la primera fila con los títulos
            if not file_exists:
                writer.writeheader()

            # datos del huesped
            writer.writerow({
                'nombre': nombre, 
                'email': email, 
                'telefono': telefono, 
                'entrada': f_entrada, 
                'salida': f_salida, 
                'huespedes': huespedes, 
                'habitacion': habitacion
            })

        # Redirigimos a la página de reservas
        return redirect(url_for('reservas', ))

@app.route('/reservas')
def reservas():
    lista_reservas = []
    #verificacion archivo existente
    if os.path.exists(ruta_csv):
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
            # Leemos el archivo y convertimos cada fila en una lista
            reader = csv.reader(archivo)
            next(reader, None)  # Saltamos la cabecera
            for i, fila in enumerate(reader):
           
           
                lista_reservas.append(fila)
    
    return render_template('reservas.html', lista_reservas=lista_reservas)

@app.route('/eliminar_reserva/<int:id>')

def eliminar_reserva(id):
    return redirect(url_for('reservas'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)