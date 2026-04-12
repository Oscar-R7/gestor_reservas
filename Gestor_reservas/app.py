import os
import csv
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

ruta_csv = 'registro.csv'
hab = 50
ocup = 0 
reser = 0
#funcion para calcular las habitaciones --------------------------------------------
def calcular_estado():
    total = 50
    ocupadas = 0

    if os.path.exists(ruta_csv):
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            next(reader, None)

            for _ in reader:
                ocupadas += 1

    disponibles = total - ocupadas

    return total, ocupadas, disponibles
#------------------------------------------------------------------------------------

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
        datos = {
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'telefono': request.form['telefono'],
            'entrada': request.form['entrada'],
            'salida': request.form['salida'],
            'huespedes': request.form['huespedes'],
            'habitacion': request.form['habitacion']
        }

        file_exists = os.path.isfile(ruta_csv)
        columnas = ['nombre', 'email', 'telefono', 'entrada', 'salida', 'huespedes', 'habitacion']

        with open(ruta_csv, mode='a', newline='', encoding='utf-8') as archivo:
            
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            if not file_exists:
                writer.writeheader()
            writer.writerow(datos)

        return redirect(url_for('reservas')) # Redirigir al panel principal

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

#AQUI ESTO INTENTANDO QUE SE GENERE LA TABLA EN LA PARTE DEL ADMIN---------------------------------------------------------
def obtener_reservas():
    lista_reservas = []
    
    if os.path.exists(ruta_csv):
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            next(reader, None)
            
            for i, fila in enumerate(reader):
                #fila.insert(0, i)
                lista_reservas.append(fila)
    
    return lista_reservas

@app.route('/admin')
def admin():
    total_habitaciones, ocupadas_hoy, disponibles = calcular_estado()
    todas_las_reservas = obtener_reservas()
    reser = len(todas_las_reservas)

    # LÓGICA DEL GRÁFICO DE TENDENCIA
    #Define el rango de días para el gráfico 
    hoy = datetime.now()
    fechas_grafico = []
    porcentajes_grafico = []

    for i in range(7):
        dia_evaluado = hoy + timedelta(days=i)
        fecha_str = dia_evaluado.strftime('%d %b') # Formato "12 Abr"
        fechas_grafico.append(fecha_str)

        #contador de reservas por dia
        habitaciones_ocupadas_este_dia = 0
        for reserva in todas_las_reservas:
            try:
                # reserva[3] es Entrada, reserva[4] es Salida (según tu lógica de confirmar_reserva)
                f_entrada = datetime.strptime(reserva[3], '%Y-%m-%d')
                f_salida = datetime.strptime(reserva[4], '%Y-%m-%d')
                
                # Si el día evaluado está dentro del rango de la reserva
                if f_entrada.date() <= dia_evaluado.date() < f_salida.date():
                    habitaciones_ocupadas_este_dia += 1
            except (ValueError, IndexError):
                continue

        #Calcula el porcentaje de ocupación 
        porcentaje = (habitaciones_ocupadas_este_dia / total_habitaciones) * 100
        porcentajes_grafico.append(round(porcentaje, 1))

    return render_template('admin.html', 
                           lista_reservas=todas_las_reservas,
                           hab=disponibles,
                           ocup=ocupadas_hoy,
                           reser=reser,
                           fechas_labels=fechas_grafico,
                           datos_valores=porcentajes_grafico)
#-----------------------------------------------------------------------------------------------------------------------------

@app.route('/eliminar_reserva/<int:id>')                                                    
def eliminar_reserva(id):
    return redirect(url_for('reservas'))



if __name__ == '__main__':
    app.run(debug=True)