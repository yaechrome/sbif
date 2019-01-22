colores = ['rgba(255,99,132,1)','rgba(54, 162, 235, 1)','rgba(255, 206, 86, 1)','rgba(75, 192, 192, 1)','rgba(153, 102, 255, 1)','rgba(255, 159, 64, 1)','rgba(255,150,134,1)','rgba(56, 60, 250, 1)','rgba(10, 255, 99, 1)','rgba(90, 200, 75, 1)','rgba(200, 102, 200, 1)','rgba(0, 30, 255, 1)']

def preparar_datos(x):
    fechas = fechas_unicas(x)
    d = agrupar_por_tipo(x)
    datasets = crear_datasets(d,fechas)
    return {
        "datasets": datasets,
        "fechas": fechas
    }

def agrupar_por_tipo(x):
    d = {}
    for dato in x:
        tipo = dato["Tipo"]
        valores = d.get(tipo, [])
        valores.append(dato)
        d[tipo] = valores
    return d

def crear_datasets(d, fechas):
    datasets = []
    for tipo, datos in d.items():
        porcentajes = porcentajes_por_tipo(datos, fechas)
        data = {
            "data":  porcentajes,
            "texto": [titulo(dato) for dato in datos],
            "label":  "Tipo " + tipo,
            "borderColor":  colores[0],
            "fill": False,
        }
        colores.append(colores.pop(0))
        datasets.append(data)
        
    return datasets

def titulo(dato):
    titulo = dato["Titulo"]
    subtitulo = dato["SubTitulo"]
    arreglo = []
    if titulo:
        arreglo.append(titulo)
    if subtitulo:
        arreglo.append(subtitulo)
    return " - ".join(arreglo)

def fechas_unicas(x):
    fechas = [dato["Fecha"] for dato in x]
    return sorted(set(fechas))

def porcentajes_por_tipo(datos_por_tipo, fechas):
    porcentajes = []
    for fecha in fechas:
        valor = obtener_valor(datos_por_tipo, fecha)
        porcentajes.append(valor)
    return porcentajes

def obtener_valor(datos, fecha):
    for dato in datos:
        if dato["Fecha"] == fecha:
            return dato["Valor"]
    return None
