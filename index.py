
import os
import pymongo
from flask import Flask, redirect, render_template, request,url_for

MONGOHOST = "localhost"
MONGOPORT = "27017"
MONGO_TIEMPO_FUERA = 1000

MONGO_URI = "mongodb://" + MONGOHOST + ":" + MONGOPORT + "/"

MONGO_BASEDATOS = "proyectoweb"
PROFECOLLECTION = "profesor"
ESTUCOLLECTION = "estudiante"

cliente = pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos = cliente[MONGO_BASEDATOS]
coleccionProfesor = baseDatos[PROFECOLLECTION]
coleccionEstudiante = baseDatos[ESTUCOLLECTION]



app = Flask(__name__)

app._static_folder = os.path.abspath("templates/static/")

@app.route("/")
def index():
    '''
    Función que retorna la página de inicio para el login
    '''
    return render_template("layouts/login.html")


@app.route("/loginEstudiante")
def loginEstudiante():
    '''
    Función que retorna la página de login para los estudiantes
    '''
    return render_template("layouts/loginEstudiante.html")


@app.route("/loginProfesor")
def loginProfesor():
    '''
    Funciòn que renderiza la página para el login de los profesores
    '''
    return render_template("layouts/loginProfesor.html")

@app.route("/principal")
def principal():
    '''
    Función que retorna la página principal para el profesor
    '''

    return render_template("layouts/")

@app.route("/validacion", methods=["POST","GET"])
def validarProfesor():
    if (request.method == "POST"):
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        
        if((coleccionProfesor.find_one({"usuario": usuario})) and (coleccionProfesor.find_one({"contraseña": contrasenia}))):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('loginProfesor'))


    return redirect(url_for('loginProfesor'))

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=9696)