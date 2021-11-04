from db.config import Connection


class Venta:

    def crearVenta(self, id_usuario, id_bus, id_destino):
        sql = "INSERT INTO venta(id_usuario,id_bus,id_destino,Registro,asistencia,tipo,Estado) VALUES(?,?,?,getdate(),0,0,0)"
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

    def listReservas(self, id_usuario):
        sql = "SELECT d.titulo, dv.importe, v.Registro, dv.asientos, (SELECT sum(dev.importe) from detalle_venta dev inner join venta ven on dev.id_venta = ven.id_venta where ven.id_usuario = 2 ) as 'total_pagar' FROM detalle_venta dv INNER JOIN venta v ON dv.id_venta=v.id_venta INNER JOIN destino d ON d.id_destino=v.id_destino WHERE v.id_usuario = ? GROUP BY dv.importe,d.titulo,v.Registro, dv.asientos"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql, id_usuario)
            return cursor
            cursor.close()
        except Exception as e:
            result = e

        return result
