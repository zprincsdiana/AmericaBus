from flask.helpers import flash
from models.Destino import Destino
from flask.json import dump
from models.Login import Login
from flask import Flask, render_template, jsonify, request, redirect, session, url_for, flash, make_response, send_file
import pyodbc

from db.config import Connection

app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey'


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('usuario/login.html')


@app.route("/entrar", methods=['POST'])
def entrar():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        login = Login().comprobarLogin(correo, contraseña)
        print(type(login))
        #comprobar si es de tipo lista
        if isinstance(login, pyodbc.Row):
            session['user'] = f'{login.nombre} {login.apellido_paterno}'
            if login.rol == 0:
                session['rol'] = login.rol
            return redirect(url_for('index'))
        elif isinstance(login, bool):
            flash("El correo no existe","danger")
        else:
            flash("Las credenciales no coinciden","danger")
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    if 'rol' in session:
        session.pop('rol')

    return redirect(url_for('index'))


@app.route("/create")
def create():
    departamentos = Destino().listDepartamentos()

    return render_template('usuario/formulario.html', depas=departamentos)


@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoPaterno']
        apellidoM = request.form['apellidoPaterno']
        fechaN = request.form['fechaNacimiento']
        departamento = request.form['departamento']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        contraseña = request.form['contraseña']
        correo = request.form['correo']
        #print(nombre + apellidoP + apellidoM + fechaN + departamento + direccion + telefono + correo + contraseña)

        try:
            Login().crearUsuario(nombre, apellidoP, apellidoM, telefono, departamento,
                                 fechaN, direccion, correo, contraseña)
            # enviar mensaje flash
            flash('Usuario registrado correctamente')
        except Exception as e:
            flash('Usuario no registrado correctamente')
    return redirect(url_for('login'))


@app.route('/americanbus/usuarios', methods=['GET'])
def usuariosList():
    data = []
    try:
        cursor = Connection().conexion().cursor()
        cursor.execute('SELECT * FROM usuario')
        #usuario = cursor.fetchall()

        # opcion 3: como la opcion 1 pero mas simplificado
        columns = [column[0] for column in cursor.description]
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        # opcion 1: con nombre de los indices osea los campos
        # for row in usuario:
            # list convierte cualquier fila ya sea tupla en arreglo => [ ]
            # print(list(row))
            # append es como un push
            # data.append(list(row))
            #res = {'id': row[0], 'nombre': row[1], 'telefono': row[2], 'email': row[3]}
            # data.append(res)

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
