from flask.json import dump
from db.config import Connection
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph


class Usuario:
#siempre va el self
    def traerDatos(self, id):
        sql = "SELECT * FROM usuario WHERE id_usuario = ?"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            result = cursor.execute(sql, id).fetchone()
            cursor.close()
        except Exception as e:
            result = "ID incorrecto"
        return result

    def actualizarUsuario(self, nombre, apellidoPaterno, apellidoMaterno, telefono, idDepartamento,
                     fechaNacimiento, direccion, correo, dni, id):
        sql = "UPDATE usuario SET id_departamento=? ,dni=?, nombre=?, apellido_paterno=?," \
              "apellido_materno=?,correo=?,telefono=?,direccion=?" \
              ",fecha_nacimiento=? WHERE id_usuario = ?" 
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql,
                               (idDepartamento, dni, nombre, apellidoPaterno, apellidoMaterno, correo
                                , telefono, direccion, fechaNacimiento, id))
            cursor.commit()
            cursor.close()
            result = True
        except Exception as e:
            result = e

        return result
