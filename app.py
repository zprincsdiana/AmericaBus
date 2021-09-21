from flask import Flask, render_template, jsonify, request, make_response, send_file
import pyodbc

from db.config import Connection

app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey'


@app.route("/")
def index():
    return render_template('index.html')


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/americanbus/usuarios', methods=['GET'])
def usuariosList():
    data = []
    try:
        conn = Connection()
        cursor = conn.conexion().cursor()
        cursor.execute('SELECT * FROM usuario')
        #usuario = cursor.fetchall()

        # opcion 3: como la opcion 1 pero mas simplificado
        columns = [column[0] for column in cursor.description]
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        # opcion 1: con nombre de los indices osea los campos
        #for row in usuario:
            # list convierte cualquier fila ya sea tupla en arreglo => [ ]
            #print(list(row))
            # append es como un push
            # data.append(list(row))
            #res = {'id': row[0], 'nombre': row[1], 'telefono': row[2], 'email': row[3]}
            #data.append(res)

        # opcion 2: sin indices
        #var = [list(row) for row in usuario]
        #data = var
        cursor.close()
        print(data)
    except Exception as e:
        data['mensaje'] = 'Error'
        # jsonify convierte un arreglo a json
    return jsonify(result)


@app.route('/buscarPasajeroPorId')
def buscarPasajeroPorId():
    HMA = pyodbc.connect('Driver={SQL Server};'
                         'Server=LAPTOP-2CUS2J3L;'
                         'Database=Prueba;'
                         'Trusted_Connection=True;')

    IdPasajero = request.args.get('IdPasajero')

    cursor = HMA.cursor()
    cursor.execute("PA_buscarPasajeroPorId ?", (IdPasajero))
    columns = [column[0] for column in cursor.description]
    result = []
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row)))

    HMA.commit()
    cursor.close()

    return jsonify(result)


@app.route('/guardarHistorialPasajero')
def guardarHistorialPasajero():
    HMA = pyodbc.connect('Driver={SQL Server};'
                         'Server=LAPTOP-2CUS2J3L;'
                         'Database=Prueba;'
                         'UID=LAPTOP-2CUS2J3L\gabri;'
                         'PWD=;')

    IdPasajero = request.args.get('IdPasajero')
    Idusu = request.args.get('Idusu')

    cursor = HMA.cursor()
    cursor.execute("PA_GuardarPasajero ?,?", (IdPasajero, Idusu))

    HMA.commit()
    cursor.close()

    return IdPasajero


# para verificar si el archivo es la principal
if __name__ == '__main__':
    # asignar puerto, el debug hace los cambios automaticos
    app.run(port=3000, debug=True)
