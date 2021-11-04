from db.config import Connection


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

    def actualizarSaldo(self, saldo, id_usuario):
        sql = "UPDATE usuario SET saldo=? WHERE  id_usuario = ? and estado = 0"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql, saldo, id_usuario)
            cursor.commit()
            cursor.close()
            result = True
        except Exception as e:
            result = e
        return result
