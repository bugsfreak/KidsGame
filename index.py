from curses import flash
import os
import pymongo
from flask import Flask, redirect, render_template, request,url_for
import mongo 




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

@app.route("/validacionE", methods=["POST","GET"])
def validarEstudiante():
    '''
    Función que valida que el estudiante ingresado exista
    '''

    
    return redirect(url_for('login'))


@app.route("/panelAdministrador")
def panelAdministrador():

    return render_template("layouts/panelAdministrador.html")


@app.route("/loginAdministrador")
def loginAdministrador():

    return render_template("layouts/loginAdministrador.html")


@app.route("/validacionA", methods=["POST","GET"])
def validarAdmin():
    if (request.method == "POST"):
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        rol = request.form['rol']
        
        validado = mongo.busquedaUsuario(usuario,contrasenia,rol)

        if(validado == True):
            redirect(url_for('panelAdministrador'))
        else:
            flash('Error de credenciales')
            redirect(url_for('loginAdministrador'))
            
        
        


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=9696)