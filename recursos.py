import requests

recursos = {
    "uf": ('uf', 'UFs', 'Valor UF'),
    "usd": ('dolar', 'Dolares', 'Valor dólar'),
    "tmc": ('tmc', 'TMCs', 'Valor TMC')
}

def url_datos_meses(nombre_recurso, fecha_inicio, fecha_fin):
    start_year  = fecha_inicio.strftime("%Y")
    start_month = fecha_inicio.strftime("%m")
    end_year  = fecha_fin.strftime("%Y")
    end_month = fecha_fin.strftime("%m")
    api_key = '195494a39a7ad98fd58e56ed59eaa3adccce7f44'
    url = f'http://api.sbif.cl/api-sbifv3/recursos_api/{nombre_recurso}/periodo/{start_year}/{start_month}/{end_year}/{end_month}?apikey={api_key}&formato=json&callback=despliegue'
    
    return url

def obtener_datos_en_rango_dias(nombre_recurso, datetime_inicio, datetime_fin, rango_dias):
    datos_en_rango_meses = datos_rango_meses(nombre_recurso, datetime_inicio, datetime_fin)
    return datos_rango_dias(datos_en_rango_meses, rango_dias)

def preparar_datos_uf_dolar(nombre_recurso, datos_en_rango_dias):
    valores = [transformar_numero(dato["Valor"]) for dato in datos_en_rango_dias]
    fechas = [dato["Fecha"] for dato in datos_en_rango_dias]
    minimo = min(valores)
    maximo = max(valores)
    promedio = promediar(valores)
    (_, _, nombre_grafico) = recursos[nombre_recurso]
    return (
        valores,
        fechas,
        minimo,
        maximo,
        promedio,
        nombre_grafico
    )

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

def promediar(array):
    return sum(array) / len(array)

def transformar_numero(numero):
    return float(numero.replace('.', '').replace(',', '.'))
