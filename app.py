from flask import Flask, render_template, jsonify, request, make_response, send_file
import pyodbc

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.after_request
def add_header(r):
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r

@app.route('/buscarPasajeroPorId')
def buscarPasajeroPorId():

	HMA = pyodbc.connect('Driver={SQL Server};'
					 'Server=LAPTOP-2CUS2J3L;'
					 'Database=Prueba;'
					 'Trusted_Connection=True;')

	IdPasajero = request.args.get('IdPasajero')
	
	cursor = HMA.cursor()
	cursor.execute("PA_buscarPasajeroPorId ?",(IdPasajero))
	columns = [column[0] for column in cursor.description]
	result = []
	for row in cursor.fetchall():
		result.append(dict(zip(columns, row)))

	HMA.commit()
	cursor.close()

	return jsonify(result)

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
	cursor.execute("PA_GuardarPasajero ?,?",(IdPasajero, Idusu))
	

	HMA.commit()
	cursor.close()

	return IdPasajero

if __name__ == '__main__':
	app.run(port=4065,debug=True)