# SBIF 👌🏻
Esta aplicación es para poder ver los valores de la UF, Dólar y TMC (Tasa Máxima Convencional) desde la api de la SBIF (Superintendencia de Bancos e Instituciones Financieras)

## Requerimientos

 - Python 3.6
 - Flask 1.0.2
 - py-dateutil 2.2
 - requests 2.21.0
 - gunicorn 19.9.0 (opcional, para subir a Heroku)

## Instalación

```Bash
pip install -r requirements.txt
```

## Ejecución

Para correr en modo desarrollo:
```Bash
FLASK_APP=app.py FLASK_DEBUG=1 flask run
```

Si tienes instalado Heroku, se puede correr en modo producción así:
```Bash
heroku local
