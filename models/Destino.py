from db.config import Connection


class Destino:

    def listDepartamentos(self):
        sql = "SELECT * FROM departamento"
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
