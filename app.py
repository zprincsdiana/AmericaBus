from flask.helpers import flash

from models.AsientoBus import AsientoBus
from models.Destino import Destino
from flask.json import dump
from models.Login import Login
from flask import Flask, render_template, jsonify, request, redirect, session, url_for, flash, make_response, send_file
import pyodbc

from db.config import Connection
from models.Usuario import Usuario
from models.Venta import Venta
from validation.EditableForm import EditableForm
from validation.Login import LoginForm

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
        print(login)
        # comprobar si es de tipo lista
        if isinstance(login, pyodbc.Row):
            session['user'] = {
                'id_usuario': login.id_usuario,
                'nombre': login.nombre,
                'apellido_paterno': login.apellido_paterno,
                'saldo': login.saldo
            }
            if login.rol == 0:
                session['rol'] = login.rol
            return redirect(url_for('index'))
        elif isinstance(login, bool):
            flash("El correo no existe", "danger")
        else:
            flash("Las credenciales no coinciden", "danger")
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
    formulario = LoginForm()
    formulario.departamento.choices = (
        'undefined', 'Seleccione un departamento')
    values = [("undefined", "Seleccione un departamento")]
    for row in departamentos:
        values.append((row.id_departamento, row.nombre))
    formulario.departamento.choices = values
    return render_template('usuario/formulario.html', form=formulario)


@app.route("/register", methods=['POST'])
def register():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        apellidoP = form.apellidoP.data
        apellidoM = form.apellidoM.data
        fechaN = form.fechaNacimiento.data
        departamento = form.departamento.data
        direccion = form.direccion.data
        telefono = form.telefono.data
        contraseña = form.contraseña.data
        correo = form.correo.data
        dni = form.DNI.data

        try:
            login = Login().crearUsuario(nombre, apellidoP, apellidoM, telefono, departamento,
                                         fechaN, direccion, correo, contraseña, dni)
            # enviar mensaje flash
            if isinstance(login, bool):
                flash('Usuario registrado correctamente', "success")
                return redirect(url_for('login'))
            else:
                flash('Usuario no registrado', "danger")
        except Exception as e:
            flash('Usuario no registrado', "danger")
    return render_template('usuario/formulario.html', form=form)


# ACTAULIZAR USUARIO, CAMBIO SUS DATOS
@app.route("/actualizarUsuario", methods=['POST'])
def actualizar_user():
    form = EditableForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        apellidoP = form.apellidoP.data
        apellidoM = form.apellidoM.data
        fechaN = form.fechaNacimiento.data
        departamento = form.departamento.data
        direccion = form.direccion.data
        telefono = form.telefono.data
        # contraseña = form.contraseña.data
        correo = form.correo.data
        dni = form.DNI.data

        try:
            actualizar = Usuario().actualizarUsuario(nombre, apellidoP, apellidoM, telefono, departamento,
                                                     fechaN, direccion, correo, dni, session['user']['id_usuario'])

            # enviar mensaje flash
            if isinstance(actualizar, bool):
                flash('Usuario actualizado correctamente', "success")
            else:
                flash('Usuario no actualizado', "danger")
        except Exception as e:
            flash('Usuario no actualizado', "danger")
    return render_template('admin/formularioEditable.html', form=form)


@app.route('/americanbus/usuarios', methods=['GET'])
def usuariosList():
    data = []
    try:
        cursor = Connection().conexion().cursor()
        cursor.execute('SELECT * FROM usuario')
        # usuario = cursor.fetchall()

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
        # res = {'id': row[0], 'nombre': row[1], 'telefono': row[2], 'email': row[3]}
        # data.append(res)

        # opcion 2: sin indices
        # var = [list(row) for row in usuario]
        # data = var
        cursor.close()
        print(data)
    except Exception as e:
        data['mensaje'] = 'Error'
        # jsonify convierte un arreglo a json
    return jsonify(result)


@app.route("/asientos", methods=['POST'])
def asientos():
    if request.method == 'POST':
        id_destino = request.form['id_destino']
        id_bus = request.form['id_bus'].split(sep=',')
        id_usuario = request.form['id_usuario']

        try:
            # retorna el id de la venta creada
            id_venta = Venta().crearVenta(id_usuario, id_bus[0], id_destino)
            print(id_venta[0])
            session['detalle_venta'] = {
                'id_venta': id_venta[0],
                'precio': id_bus[1],
                'cantidad_asientos': 0,
                'importe': 0,
                'estado': 0,
                'asientos': [0, 0, 0]
            }
            asiento = AsientoBus().listarAsientos(id_bus[0])
            print(asiento)
            columns = [column[0] for column in asiento.description]
            data = []
            for row in asiento.fetchall():
                data.append(dict(zip(columns, row)))
            print(data)
        except Exception as e:
            print(e)
    return render_template('asistencia/asientos.html', data=data)


@app.route("/listaReservas", methods=['GET', 'POST'])
def listaReservas():
    if request.method == 'POST':
        asientos = (request.form.getlist('check'))
        # pasar los id a int
        ids_asientos = [int(row) for row in request.form.getlist('check')]
        # convertir de una arreglo a tupla
        ids_asientitos = str(tuple(ids_asientos))
        asientos_select = AsientoBus().asientosSeleccionados(ids_asientitos)

        asientoss = []
        # convertir en un solo arreglo los numeros de asientos
        for row in asientos_select:
            asientoss.append(list(row))

        asientoss = str(asientoss).replace('[', '')
        asientoss = str(asientoss).replace(']', '')
        session['detalle_venta']['cantidad_asientos'] = len(asientos)
        session['detalle_venta']['importe'] = len(
            asientos) * float(session['detalle_venta']['precio'])
        session['detalle_venta']['asientos'] = asientoss

        asientos_select = AsientoBus().crearDetalleVenta(session['detalle_venta']['id_venta'],
                                                         session['detalle_venta']['precio'],
                                                         session['detalle_venta']['cantidad_asientos'],
                                                         session['detalle_venta']['importe'],
                                                         session['detalle_venta']['estado'],
                                                         session['detalle_venta']['asientos'])

        print(asientos_select)

    reservas = Venta().listReservas(session['user']['id_usuario'])
    columns = [column[0] for column in reservas.description]
    data = []
    for row in reservas.fetchall():
        data.append(dict(zip(columns, row)))
    print(data)
    return render_template('reserva/listaReservas.html', data=data)


@app.route("/destinos")
def destinos():
    destino = Destino().listDestino()
    columns = [column[0] for column in destino.description]
    data = []
    for row in destino.fetchall():
        data.append(dict(zip(columns, row)))
    print(data)
    return render_template('destinos/destinos.html', data=data)


@app.route("/asistencia")
def asistencia():
    return render_template('asistencia/asistencia.html')


@app.route("/estadisticas")
def estadistica():
    return render_template('estadisticas/estadisticas.html')


@app.route("/pago")
def pago():
    return render_template('pago/pago.html')


@app.route("/detalle/<id>")
def detalle(id):
    destino = Destino().getDestino(id)
    columns = [column[0] for column in destino.description]
    for row in destino.fetchall():
        data = (dict(zip(columns, row)))
    return render_template('destinos/DestinosDetallados.html', data=data)


@app.route("/administrar")
def administrar():
    return render_template('admin/administrar.html')


@app.route("/generarReserva/<id>")
def generarReserva(id):
    bus = Destino().getBus(id)
    columns = [column[0] for column in bus.description]
    data = []
    for row in bus.fetchall():
        data.append(dict(zip(columns, row)))
    print(data)
    if 'user' in session:
        return render_template('reserva/generarReserva.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route("/realizarResenia")
def realizarResenia():
    return render_template('usuario/realizarResenia.html')


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


# MODIFICAR
@app.route("/modificable/<id>")
def modificable(id):
    # instanciando
    usuario = Usuario().traerDatos(id)
    departamentos = Destino().listDepartamentos()
    formUsuario = EditableForm()
    formUsuario.departamento.default = usuario.id_departamento
    # este procees es para que le default sirva
    formUsuario.process()
    formUsuario.nombre.data = usuario.nombre
    formUsuario.apellidoM.data = usuario.apellido_materno
    formUsuario.apellidoP.data = usuario.apellido_paterno
    formUsuario.correo.data = usuario.correo
    formUsuario.telefono.data = usuario.telefono
    formUsuario.direccion.data = usuario.direccion
    formUsuario.fechaNacimiento.data = usuario.fecha_nacimiento
    formUsuario.DNI.data = usuario.dni
    formUsuario.departamento.choices = (
        'undefined', 'Seleccione un departamento')
    values = [("undefined", "Seleccione un departamento")]
    for row in departamentos:
        values.append((row.id_departamento, row.nombre))
    formUsuario.departamento.choices = values
    return render_template('admin/formularioEditable.html', form=formUsuario)


############################

# Viajes
@app.route("/viajes")
def viajes():
    return render_template('usuario/DestinosDetallados.html')


############################

# Mi cronograma
@app.route("/cronograma", methods=['GET', 'POST'])
def cronograma():

    if request.method == 'POST' or request.method == 'GET' :

        saldo = float(session['user']['saldo'])
        total = float(request.form['total'])

        print(saldo)
        print(total)

        if total <= saldo:
            #restamos el total a pagar al saldo actual
            session['user']['saldo'] = saldo - total
            # llamamos al la funcion para que Actualice el registro
            Usuario().actualizarSaldo(session['user']['saldo'],session['user']['id_usuario'])
            # ejecuto la transaccion de pago
            pagado = Venta().pagarVenta(session['user']['id_usuario'])
            print(pagado)
            if pagado:
                flash('Viaje pagado', "success")
        else:
            flash('Saldo insuficiente', "danger")
            return redirect(url_for('listaReservas'))

    return render_template('usuario/cronograma.html')


############################

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

@app.route('/ListarUsuarios', methods=['GET'])
def ListarUsuarios():
    data = []
    try:
        ses = session['user']['id_usuario']
        print(ses)
        cursor = Connection().conexion().cursor()
        cursor.execute('ListarUsuarios ?', ses)
        #usuario = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))
        cursor.close()
    except Exception as e:
        data['mensaje'] = 'Error'
        # jsonify convierte un arreglo a json
    return jsonify(result)

@app.route('/ListarUsuarioPorNombreDni', methods=['GET'])
def ListarUsuarioPorNombreDni():
    data = []
    try:
        ses = session['user']['id_usuario']
        nombre = request.args.get('nombre')
        dni = request.args.get('dni')
        opt = request.args.get('opt')
        cursor = Connection().conexion().cursor()
        cursor.execute('ListarUsuarioPorNombreDni ?,?,?,?',(nombre, dni,opt,ses))
        #usuario = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        result = []
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))
        cursor.close()
        print(data)
    except Exception as e:
        data['mensaje'] = 'Error'
        # jsonify convierte un arreglo a json
    return jsonify(result)

@app.route('/EliminarUsuarioPorId', methods=['GET'])
def EliminarUsuarioPorId():
    data = []
    try:
        id_usuario = request.args.get('id_usuario')
        print("raaaaa"+id_usuario)
        cursor = Connection().conexion().cursor()
        cursor.execute('EliminarUsuarioPorId ?',(id_usuario))
        cursor.commit()
        cursor.close()
    except Exception as e:
        data['mensaje'] = 'Error'
        # jsonify convierte un arreglo a json
    return jsonify(data)


# para verificar si el archivo es la principal
if __name__ == '__main__':
    # asignar puerto, el debug hace los cambios automaticos
    app.run(port=3000, debug=True)
