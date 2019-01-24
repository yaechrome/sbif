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

colores = ['rgba(255,99,132,1)','rgba(54, 162, 235, 1)','rgba(255, 206, 86, 1)','rgba(75, 192, 192, 1)','rgba(153, 102, 255, 1)','rgba(255, 159, 64, 1)','rgba(255,150,134,1)','rgba(50, 90, 200, 1)','rgba(10, 255, 99, 1)','rgba(90, 200, 75, 1)','rgba(200, 102, 200, 1)','rgba(0, 30, 255, 1)']
def siguiente_color():
    color = colores.pop(0)
    colores.append(color)
    return color

def crear_datasets(datos_por_tipo, fechas):
    datasets = []
    
    for tipo, datos in datos_por_tipo.items():
        valores = valores_para_cada_fecha(datos, fechas)
        maximo_valor = max([valor for valor in valores if valor is not None])
        color = siguiente_color()
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
