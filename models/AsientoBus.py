from db.config import Connection

class AsientoBus:

    def listarAsientos(self, id_bus):
        sql = "SELECT * FROM asientos where id_bus = ?"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql, id_bus)
            return cursor
            cursor.close()
        except Exception as e:
            result = e
        return result

    def asientosSeleccionados(self, ids_asientos, ):
        sql1 = f"UPDATE asientos SET estado = 1 where id_asiento in {ids_asientos}"

        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql1)
            cursor.commit()

            sql = f"SELECT numero_asiento FROM asientos where id_asiento in {ids_asientos}"
            result = cursor.execute(sql).fetchall()
            cursor.close()
        except Exception as e:
            result = e
        return result

    def crearDetalleVenta(self, id_venta,precio,cantidad_asientos,importe,estado,asientos):
        sql = "INSERT INTO detalle_venta(id_venta,precio,cantidad_asientos,importe,Registro,Estado,asientos) VALUES(?,?,?,?,getdate(),?,?)"
        try:
            # abrir conexion
            con = Connection().conexion()
            cursor = con.cursor()
            cursor.execute(sql, (id_venta,precio,cantidad_asientos,importe,estado,asientos))
            cursor.commit()
            cursor.close()
            result = True
        except Exception as e:
            result = e
        return result