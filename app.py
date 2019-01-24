from flask import Flask, jsonify, request, render_template
import requests
from datetime import datetime, timedelta
app = Flask(__name__)

from bonus import preparar_datos
import dateutil.parser
import json

def url_datos_meses(nombre_recurso, fecha_inicio, fecha_fin):
    start_year  = fecha_inicio.strftime("%Y")
    start_month = fecha_inicio.strftime("%m")
    end_year  = fecha_fin.strftime("%Y")
    end_month = fecha_fin.strftime("%m")
    api_key = '195494a39a7ad98fd58e56ed59eaa3adccce7f44'
    url = f'http://api.sbif.cl/api-sbifv3/recursos_api/{nombre_recurso}/periodo/{start_year}/{start_month}/{end_year}/{end_month}?apikey={api_key}&formato=json&callback=despliegue'
    
    return url

recursos = {
    "uf": ('uf', 'UFs', 'Valor UF'),
    "usd": ('dolar', 'Dolares', 'Valor dólar'),
    "tmc": ('tmc', 'TMCs', 'Valor TMC')
}

def datos_rango_meses(nombre_recurso, fecha_inicio, fecha_fin):
    (url_recurso, llave_recurso, _) = recursos[nombre_recurso]
    url = url_datos_meses(url_recurso, fecha_inicio, fecha_fin)
    r = requests.get(url)
    return r.json().get(llave_recurso, [])

def datos_rango_dias(datos_en_rango_meses, rango_dias):
    return [dato for dato in datos_en_rango_meses if esta_en_rango(dato, rango_dias)]
    
def esta_en_rango(dato, rango_dias):
    (dia_inicio, dia_fin) = rango_dias
    fecha = dato["Fecha"]
    return dia_inicio <= fecha and fecha <= dia_fin

@app.route("/recurso")
def recurso():
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    if fecha_fin < fecha_inicio:
        error = "Debe seleccionar rango de fecha válido"
        return render_template(
            'index.html',
            error = error,
        )
    nombre_recurso = request.args.get('nombre_recurso', '')
    rango_dias = (fecha_inicio, fecha_fin)
    datos_en_rango_meses = datos_rango_meses(nombre_recurso, dateutil.parser.parse(fecha_inicio), dateutil.parser.parse(fecha_fin))
    datos_en_rango_dias = datos_rango_dias(datos_en_rango_meses, rango_dias)
    
    if not datos_en_rango_dias:
        error = "No hay datos en el rango seleccionado"
        return render_template(
            'index.html',
            error = error,
        )
        
    if nombre_recurso == 'tmc':
        (fechas, datasets, datos_tabla) = preparar_datos(datos_en_rango_dias)
        return render_template(
            'resultados_tmc.html',
            fechas = json.dumps(fechas),
            datasets = json.dumps(datasets),
            datos_tabla = datos_tabla
        )
        
    
    valores = [transformar_numero(dato["Valor"]) for dato in datos_en_rango_dias]
    minimo = min(valores)
    maximo = max(valores)
    promedio = promediar(valores)
    (_, _, nombre_grafico) = recursos[nombre_recurso]
    return render_template(
        'resultados.html',
        minimo = minimo,
        maximo = maximo,
        promedio = round(promedio, 3),
        datos = datos_en_rango_dias,
        nombre_grafico = nombre_grafico,
        all_dates = [dato["Fecha"] for dato in datos_en_rango_dias],
        all_values = valores
    )

def promediar(array):
    return sum(array) / len(array)

def transformar_numero(numero):
    return float(numero.replace('.', '').replace(',', '.'))

@app.route("/")
def index():
    today = datetime.now()
    last_week = today - timedelta(days = 7)
    return render_template(
        'index.html', 
        today = today.strftime("%Y-%m-%d"), 
        last_week = last_week.strftime("%Y-%m-%d")
    )
