from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime, timedelta
app = Flask(__name__)

from bonus import preparar_datos
from recursos import obtener_datos_en_rango_dias, preparar_datos_uf_dolar
import dateutil.parser
import json

@app.route("/")
def index():
    today = datetime.now()
    last_week = today - timedelta(days = 7)
    error = request.args.get('error')
    return render_template(
        'index.html', 
        today = today.strftime("%Y-%m-%d"), 
        last_week = last_week.strftime("%Y-%m-%d"),
        error = error
    )


@app.route("/recurso")
def recurso():
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    if fecha_fin < fecha_inicio:
        error = "Debe seleccionar rango de fecha válido"
        return redirect(url_for('.index', error = error))
        
    try:
        datetime_inicio = dateutil.parser.parse(fecha_inicio)
        datetime_fin = dateutil.parser.parse(fecha_fin)
    except:
        error = "Debe ingresar fecha en formato YYYY-MM-DD"
        return redirect(url_for('.index', error = error))
    
    nombre_recurso = request.args.get('nombre_recurso', '')
    rango_dias = (fecha_inicio, fecha_fin)

    datos_en_rango_dias = obtener_datos_en_rango_dias(nombre_recurso, datetime_inicio, datetime_fin, rango_dias)
    
    if not datos_en_rango_dias:
        error = "No hay datos en el rango seleccionado"
        return redirect(url_for('.index', error = error))
        
    if nombre_recurso == 'tmc':
        (fechas, datasets, datos_tabla) = preparar_datos(datos_en_rango_dias)
        return render_template(
            'resultados_tmc.html',
            fechas = json.dumps(fechas),
            datasets = json.dumps(datasets),
            datos_tabla = datos_tabla
        )
    else:
        (valores, fechas, minimo, maximo, promedio, nombre_grafico) = preparar_datos_uf_dolar(nombre_recurso, datos_en_rango_dias)
        return render_template(
            'resultados.html',
            minimo = minimo,
            maximo = maximo,
            promedio = round(promedio, 3),
            datos = datos_en_rango_dias,
            nombre_grafico = nombre_grafico,
            all_dates = fechas,
            all_values = valores
        )
