import pyodbc


class Connection:
    # datos de la bd
    server = 'hsac1530553.database.windows.net'
    bd = 'AmericanBus'
    user = 'harold'
    password = 'Lo$t1998'

    def conexion(self):
        try:
            conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER=' + self.server + ';DATABASE=' +
                                      self.bd + ';UID=' + self.user + ';PWD=' + self.password)
        except Exception as e:
            print(f'Ha sucedido un error: {e}')
        return conexion
