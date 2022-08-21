
from math import perm
import os
import pymongo
from flask import Flask, redirect, render_template, request,url_for
import mongo 

MONGO = mongo.Mongo()
permisos = []


app = Flask(__name__)

#mn es la variable con la que se instanciara la clase de mongo
mn = mongo.Mongo()

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




@app.route("/principal")
def principal():
    '''
    Función que retorna la página principal para el profesor
    '''

    return render_template("layouts/")

@app.route("/validacionE", methods=["POST","GET"])
def validarEstudiante():
    '''
    Función que valida que el estudiante ingresado exista
    '''

    
    return redirect(url_for('login'))



# ------------------------ PARTE PROFESOR --------------------------

@app.route("/loginProfesor")
def loginProfesor():
    '''
    Funciòn que renderiza la página para el login de los profesores
    '''
    return render_template("layouts/loginProfesor.html")

@app.route('/reporteNotas')
def registroPersona():

    return render_template("layouts/reporteNotas.html")  



# ------------------------ PARTE ADMINISTRADOR -------------------------

@app.route("/panelAdministrador")
def panelAdministrador():

    return render_template("layouts/panelAdministrador.html", permisos = permisos)


@app.route("/loginAdministrador")
def loginAdministrador():

    return render_template("layouts/loginAdministrador.html")


@app.route('/listaPermisos')
def listaPermisos():
    permisos = MONGO.mostrarPermisos()
    
    return render_template("layouts/listaPermisos.html", permisos = permisos)


@app.route('/registroPersona')
def registroPersona():

    return render_template("layouts/registroPersona.html")

 
@app.route("/validacionA", methods=["POST","GET"])
def validarAdmin():
    if (request.method == "POST"):
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        rol = request.form['rol']
        
        
        validado = mn.validarUsuario(usuario, contrasenia, rol)

        if(validado == True):
            redirect(url_for('panelAdministrador'))
        else:
            redirect(url_for('loginAdministrador'))
            
            
        
# --------------------- MAIN FLASK -----------------------        


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=9696)