from db.config import Connection


class Venta:

    def crearVenta(self, id_usuario, id_bus, id_destino):
        sql = "INSERT INTO venta(id_usuario,id_bus,id_destino,Registro,asistencia) VALUES(?,?,?,getdate(),0)"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql, (id_usuario, id_bus, id_destino))
            cursor.commit()

            sql = "SELECT max(id_venta) as 'id_venta' FROM venta"
            result = cursor.execute(sql).fetchone()
            cursor.close()
        except Exception as e:
            result = e
        return result

    def listReservas(self,id_usuario):
        sql = "SELECT d.titulo, dv.importe, v.Registro FROM detalle_venta dv " \
              "INNER JOIN venta v ON dv.id_venta=v.id_venta " \
              "INNER JOIN destino d ON d.id_destino=v.id_destino where v.id_usuario = ?"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql,id_usuario)
            return cursor
            cursor.close()
        except Exception as e:
            result = e

        return result
