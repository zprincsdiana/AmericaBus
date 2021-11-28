from flask.json import dump
from db.config import Connection
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph


class Login:

    def comprobarLogin(self, correo, contraseña):
        sql = "SELECT * FROM usuario WHERE correo = ?"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()

            row = cursor.execute(sql, correo)

            # comprobamos si encontró el usuario
            if row.rowcount == -1:
                value = checkph(cursor.fetchone().contraseña, contraseña)
                if value:
                    result = cursor.execute(sql, correo).fetchone()
                else:
                    result = "No coinciden las credenciales"
            else:
                result = False
            cursor.close()
        except Exception as e:
            result = "Error No coinciden"

        return result

    def crearUsuario(self, nombre, apellidoPaterno, apellidoMaterno, telefono, idDepartamento,
                     fechaNacimiento, direccion, correo, contraseña, dni):
        sql = "INSERT INTO usuario(id_departamento,dni,nombre,apellido_paterno," \
              "apellido_materno,correo,contraseña,telefono,direccion" \
              ",fecha_nacimiento,rol,estado,saldo) VALUES(?,?,?,?,?,?,?,?,?,?,2,0,0.0)"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql,
                               (idDepartamento, dni, nombre, apellidoPaterno, apellidoMaterno, correo, genph(contraseña)
                                , telefono, direccion, fechaNacimiento))
            cursor.commit()
            cursor.close()
            result = True
        except Exception as e:
            result = e

        return result
