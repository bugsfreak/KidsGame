import os
import pymongo
from flask import Flask, redirect, render_template, request,url_for,Markup, flash
import mongo 
from datetime import date

MONGO = mongo.Mongo()
permisos = []


app = Flask(__name__)
app.secret_key = "super secret key"

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

#Renderización de los juegos
@app.route("/juego1")
def juego1():

    return render_template('layouts/figuras.html')

@app.route("/juego2")
def juego2():

    return render_template('layouts/adivinar.html')



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

#Página principal para el administrador
@app.route("/panelAdministrador")
def panelAdministrador():
    '''
    Dirige a la página principal del administrador
    '''
    if(Rol_logeado == ""):
        return render_template("layouts/panelAdministrador.html")
    else:
        return redirect(url_for("loginAdministrador"))
    

#Ingreso para el administrador
@app.route("/loginAdministrador")
def loginAdministrador():
    '''
    Se dirige al login del administrador
    '''
    return render_template("layouts/loginAdministrador.html")

#Ruta y función para validar el admministrador
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


#Lista de los permisos
@app.route('/listaPermisos')
def listaPermisos():
    permisos = MONGO.mostrarPermisos()
    return render_template("layouts/tablaPermisos.html", permisos = permisos)


#Lista de los roles
@app.route('/listaRoles')
def listaRoles():
    roles = MONGO.mostrarRoles()
    return render_template("layouts/tablaRoles.html", roles = roles)


#Página de registro de persona
@app.route('/registroPersona')
def registro():
    roles  = MONGO.mostrarRoles()
    return render_template("layouts/registroPersona.html", roles = roles)


#REGISTRO DE AULA
@app.route('/registroAula')
def registroAula():

    return render_template("layouts/registroAulas.html")

@app.route('/regA', methods=["POST"])
def regA():
    if(request.method == "POST"):
        id = request.form["id"]
        nombre = request.form["nombre"]
        max = request.form["max"]
        if (id == "" or nombre == "" or max == ""):
            flash("Hay campos vacios")
            return redirect(url_for('registroAula'))
        else:
            MONGO.registrarAula(id,nombre,max)
            return redirect(url_for('registroAula'))
    

# MATRICULACIÓN

@app.route('/matricularEstudiante')
def matricularEstudiante():
    personas = MONGO.mostrarPersonas()
    aulas = MONGO.mostrarAulas()
    return render_template("layouts/matriculacion.html", personas = personas, aulas = aulas)



@app.route('/matricular', methods=["POST"])
def matricular():
    if(request.method == "POST"):
        id = request.form["id"]
        aula = request.form["aula"]
        fechaHoy = date.today()
        f_matricula = fechaHoy.strftime("%d/%m/%Y")


        return redirect(url_for('matricularEstudiante'))


#CREACION USUARIO

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
            if(id == "" or nombre == "" or apellido == "" or f_nac == "" or email == "" or usuario == "" or contrasenia == ""):
                MONGO.creacionUsuario(id,nombre,apellido,f_nac,telefono,email,usuario,contrasenia,rol)
                return redirect(url_for('registro'))
            else:
                flash("Existen campos vacíos")
                return redirect(url_for('registro'))
        except:
            flash("Existe un inconveniente, y no se pudo ingresar")
            print("No se pudo ingresar")
            return redirect(url_for('registro'))

        
#REGISTRO AÑO LECTIVO

@app.route('/registroAnioLectivo')
def registroAnioLectivo():

    return render_template('layouts/registroAnioLectivo.html')


@app.route('/registroAL', methods=["POST"])
def registroAL():
    if(request.method == "POST"):
        id = request.form["id"]
        nombre = request.form["nombre"]
        f_inicio = request.form["f_inicio"]
        f_fin = request.form["f_fin"]
        try:
            if(id == "" or nombre == "" or f_inicio == "" or f_fin == ""):
                flash("Hay campos vacios")
            else:    
                MONGO.registroAnioLectivo(id,nombre,f_inicio,f_fin)
                return redirect(url_for('registroAnioLectivo'))
        except:
            flash("Existe un inconveniente y no se pudo ingresar")
            return redirect(url_for('registoAnioLectivo'))


    


        
# --------------------- MAIN FLASK -----------------------        


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=9696)