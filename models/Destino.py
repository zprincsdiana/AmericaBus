from db.config import Connection


class Destino:

    def listDepartamentos(self):
        sql = "Exec ListarDepartamentos"
        try:
            #abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            result = "Error No coinciden"
        
        return result

    def listDestino(self):
        sql = "SELECT * FROM destino"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql)
            return cursor
            cursor.close()
        except Exception as e:
            result = e

        return result

    def getDestino(self, id):
        sql = "SELECT * FROM destino where id_destino = ?"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql,id)
            return cursor
            cursor.close()
        except Exception as e:
            result = e

        return result

    def getBus(self,id):
        sql = "SELECT * FROM destino D inner join bus B on D.id_destino=B.id_destino WHERE D.id_destino = ?"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql, id)
            return cursor
            cursor.close()
        except Exception as e:
            result = e

        return result

    def getReseñas(self,id):
        sql = "select v.resenia,v.puntaje,concat(u.nombre,' ',u.apellido_paterno) as 'usuario' " \
              "from venta v inner join usuario u on v.id_usuario = u.id_usuario where v.resenia is not null and id_destino = ?"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql, id)
            return cursor
            cursor.close()
        except Exception as e:
            result = e

        return result
