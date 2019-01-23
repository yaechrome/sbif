from flask import Flask, jsonify, request, render_template
import requests
from datetime import datetime, timedelta
app = Flask(__name__)

from bonus import preparar_datos
import dateutil.parser
import json

def url_valor_recurso_meses(nombre_recurso, fechaInicio, fechaFin):
    start_year  = fechaInicio.strftime("%Y")
    start_month = fechaInicio.strftime("%m")
    end_year  = fechaFin.strftime("%Y")
    end_month = fechaFin.strftime("%m")
    api_key = '195494a39a7ad98fd58e56ed59eaa3adccce7f44'
    url = f'http://api.sbif.cl/api-sbifv3/recursos_api/{nombre_recurso}/periodo/{start_year}/{start_month}/{end_year}/{end_month}?apikey={api_key}&formato=json&callback=despliegue'
    
    return url

recursos = {
    "uf": ('uf', 'UFs', 'Valor UF'),
    "usd": ('dolar', 'Dolares', 'Valor dólar'),
    "tmc": ('tmc', 'TMCs', 'Valor TMC')
}

def valor_recurso_meses(nombre_recurso, fechaInicio, fechaFin):
    (url_recurso, llave_recurso, _) = recursos[nombre_recurso]
    url = url_valor_recurso_meses(url_recurso, fechaInicio, fechaFin)
    r = requests.get(url)
    return r.json().get(llave_recurso, [])

def valores_rango_dias(valores_rango_meses, rango_dias):
    return [x for x in valores_rango_meses if esta_en_rango(x, rango_dias)]
    
def esta_en_rango(fecha_valor, rango_dias):
    (dia_inicio, dia_fin) = rango_dias
    fecha = fecha_valor["Fecha"]
    return dia_inicio <= fecha and fecha <= dia_fin

@app.route("/recurso")
def recurso():
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    if fecha_fin < fecha_inicio:
        error = "Debe seleccionar rango de fecha válido"
        return render_template(
            'holamundo.html',
            error=error,
        )
    nombre_recurso = request.args.get('nombre_recurso', '')
    rango_dias = (fecha_inicio, fecha_fin)
    valores_rango_meses = valor_recurso_meses(nombre_recurso, dateutil.parser.parse(fecha_inicio), dateutil.parser.parse(fecha_fin))
    valores_por_dia = valores_rango_dias(valores_rango_meses, rango_dias)
    
    if not valores_por_dia:
        error = "No hay datos en el rango seleccionado"
        return render_template(
            'holamundo.html',
            error=error,
        )
        
    if nombre_recurso == 'tmc':
        datos_preparados = preparar_datos(valores_por_dia)
        return render_template(
            'resultados_tmc.html',
            fechas=json.dumps(datos_preparados["fechas"]),
            datasets=json.dumps(datos_preparados["datasets"]),
            datos_tabla=datos_preparados["datos_tabla"]
        )
        
    
    valores = [parse_chilean_number(x["Valor"]) for x in valores_por_dia]
    minimo = min(valores)
    maximo = max(valores)
    promedio = mean(valores)
    (_, _, nombre_grafico) = recursos[nombre_recurso]
    return render_template(
        'resultados.html',
        minimo=minimo,
        maximo=maximo,
        promedio=round(promedio,3),
        valores_por_dia=valores_por_dia,
        nombre_grafico=nombre_grafico,
        all_dates=[x["Fecha"] for x in valores_por_dia],
        all_values=valores
    )

def mean(array):
    return sum(array) / len(array)

def parse_chilean_number(x):
    return float(x.replace('.', '').replace(',', '.'))

@app.route("/")
def main():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    return render_template('holamundo.html', today=today.strftime("%Y-%m-%d"), last_week=last_week.strftime("%Y-%m-%d"))
