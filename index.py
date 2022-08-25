
import os
import pymongo
from flask import Flask, redirect, render_template, request,url_for,Markup, flash
import mongo 

MONGO = mongo.Mongo()
permisos = []


app = Flask(__name__)

#mn es la variable con la que se instanciara la clase de mongo
mn = mongo.Mongo()

app._static_folder = os.path.abspath("templates/static/")

Rol_logeado = ''

# --------------- PARTE GENERAL Y ESTUDIANTE -------------------


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

    return render_template("layouts/login.html")

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
    '''
    Dirige a la página principal del administrador
    '''
    if(Rol_logeado == ""):
        return render_template("layouts/panelAdministrador.html")
    else:
        return redirect(url_for("loginAdministrador"))
    


@app.route("/loginAdministrador")
def loginAdministrador():
    '''
    Se dirige al login del administrador
    '''
    return render_template("layouts/loginAdministrador.html")

@app.route("/validarA", methods=["POST"])
def validarA():
    if(request.method == "POST"):
        usuario = request.form["usuario"]
        contrasenia = request.form["contrasenia"]
        rol = "Administrador"
        val_ingreso = MONGO.validarUsuario(usuario,contrasenia,rol)
        if(val_ingreso == True):
            Rol_logeado = "Administrador"
            return redirect(url_for('panelAdministrador'))
        else:
            return redirect(url_for('loginAdministrador'))


@app.route('/listaPermisos')
def listaPermisos():
    permisos = MONGO.mostrarPermisos()
    return render_template("layouts/tablaPermisos.html", permisos = permisos)

@app.route('/listaRoles')
def listaRoles():
    roles = MONGO.mostrarRoles()
    return render_template("layouts/tablaRoles.html", roles = roles)


@app.route('/registroPersona')
def registro():

    return render_template("layouts/registroPersona.html")


@app.route('/registroAula')
def registroAula():

    return render_template("layouts/registroAulas.html")

@app.route('/regA')
def regA():

    return redirect(url_for('registroAula'))


@app.route('/matricularEstudiante')
def matricularEstudiante():

    return render_template("layours/matriculacion.html")

@app.route('/matricular', methods=["POST"])
def matricular():
    if(request.method == "POST"):


        return redirect(url_for('matricularEstudiante'))



@app.route('/ingreso', methods=['POST'])
def ingreso():

    if(request.method == "POST"):
        id = request.form['id']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        f_nac = request.form['f_nac']  
        telefono = request.form['telefono']
        email = request.form['email']
        usuario = request.form['usuario']  
        contrasenia = request.form['contrasenia']
        rol = request.form['rol']
        try:
            MONGO.creacionUsuario(id,nombre,apellido,f_nac,telefono,email,usuario,contrasenia,rol)
            return redirect(url_for('registro'))
        except:
            flash("Existe un inconveniente, y no se pudo ingresar")
            print("No se pudo ingresar")
        
            

        
# --------------------- MAIN FLASK -----------------------        


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=9696)