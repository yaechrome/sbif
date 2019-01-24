from colorsys import hls_to_rgb

def preparar_datos(datos):
    fechas = fechas_unicas(datos)
    datos_por_tipo = agrupar_por_tipo(datos)
    datasets = crear_datasets(datos_por_tipo, fechas)
    datos_tabla = sorted(datos, key=lambda dato: dato['Tipo'])
    
    return (fechas, datasets, datos_tabla)

def agrupar_por_tipo(datos):
    d = {}
    for dato in datos:
        tipo = dato["Tipo"]
        datos_del_tipo = d.get(tipo, [])
        datos_del_tipo.append(dato)
        d[tipo] = datos_del_tipo
    return d

def siguiente_color(angulo_anterior):
    # Este angulo viene del "golden ratio" o número áureo
    # (razón entre números de la serie de fibonacci)
    # Al sumar esta cantidad de grados, nos dan siempre ángulos distintos
    # y bien separados entre sí.
    # En este caso ocupamos esos ángulos como el "matiz" (hue) de un color
    # manteniendo la saturación y luminocidad fijas.
    angulo_aureo = 137.5
    # Se transforma el color en RGB, porque la librería chart.js no soporta
    # colores en el formato hsl(…).
    (_r, _g, _b) = hls_to_rgb(angulo_anterior / 360, 0.7, 1.0)
    r = round(_r * 255)
    g = round(_g * 255)
    b = round(_b * 255)
    color = f'rgb({r}, {g}, {b})'
    angulo_nuevo = (angulo_anterior + angulo_aureo) % 360
    return (color, angulo_nuevo)

def crear_datasets(datos_por_tipo, fechas):
    datasets = []
    
    angulo_color = 235
    for tipo, datos in datos_por_tipo.items():
        valores = valores_para_cada_fecha(datos, fechas)
        maximo_valor = max([valor for valor in valores if valor is not None])
        (color, angulo_color) = siguiente_color(angulo_color)
        radios_puntos = [radio_punto(valor, maximo_valor) for valor in valores]
        
        datasets.append({
            "data":  valores,
            "texto": [titulo(dato) for dato in datos],
            "label":  "Tipo " + tipo,
            "borderColor": color,
            "fill": False,
            "tension": 0,
            "pointRadius": radios_puntos,
            "pointHoverRadius": radios_puntos,
            "pointBackgroundColor": color
        })
        
    return datasets
    
def radio_punto(valor, maximo):
    # para destacar el punto,
    # se usa un radio mayor si es el con maximo valor
    if valor == maximo:
        return 8
    else:
        return 2

def titulo(dato):
    titulo = dato["Titulo"]
    subtitulo = dato["SubTitulo"]
    
    arreglo = []
    if titulo:
        arreglo.append(titulo)
    if subtitulo:
        arreglo.append(subtitulo)
    return " - ".join(arreglo)

def fechas_unicas(datos):
    fechas = [dato["Fecha"] for dato in datos]
    return sorted(set(fechas))

def valores_para_cada_fecha(dato, fechas):
    valores = []
    for fecha in fechas:
        valor = valor_para_una_fecha(dato, fecha)
        valores.append(valor)
    return valores

def valor_para_una_fecha(datos, fecha):
    for dato in datos:
        if dato["Fecha"] == fecha:
            return float(dato["Valor"])
    return None
