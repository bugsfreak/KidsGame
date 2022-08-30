from email.policy import default
from itertools import permutations
from warnings import catch_warnings
import pymongo 
import bcrypt
import basehash
from cryptography.fernet import Fernet



class Mongo():

    '''
    Clase que permite la conexion con MongoDB

    '''

    #Se define el host, puerto y tiempo fuera para la conexion a mongo
    MONGOHOST = "localhost"
    MONGOPORT = "27017"
    MONGO_TIEMPO_FUERA = 1000

    #Se establece la direccion para conectar a mongo
    MONGO_URI = "mongodb://" + MONGOHOST + ":" + MONGOPORT + "/"

    #Se escoge la base de datos a la que deseamos conectarnos
    MONGO_BASEDATOS = "Unidad_Educativa"
    COL_PERSONAS = "personas"
    COL_ROLES = "roles"
    COL_PERMISOS = "permisos"
    
    #Se establece el cliente con la funcion de MongoClient
    cliente = pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    #Se selecciona la base de datos
    baseDatos = cliente[MONGO_BASEDATOS]
    #La coleccion de personas para esta ocasion
    coleccionPersonas = baseDatos[COL_PERSONAS]
    coleccionRoles = baseDatos[COL_ROLES]
    coleccionPermisos = baseDatos[COL_PERMISOS]

    #Se obtiene la salt generada por bcrypt
    salt = bcrypt.gensalt()
  
    # -------------------------- CREACIÒN -----------------------------
    
    def creacionUsuario(self,id,nombre,apellido,f_nac,telefono, email,usuario,contrasenia, rol):
        '''
        Funcion que es usada para ingresar nuevos profesores a la base de datos

        Parametros:
            self (class):
            id (int): Id del profesor
            nombre (string): Nombre del profesor
            apellido (string): Apellido del profesor
            f_nac (string): Fecha de nacimiento del profesor
            usuario (string): Usuario asignado para el profesor
            contrasenia (string): Contraseña asignada para el profesor
            rol (string): El rol puede ser estudiante, profesor o administrador
        Returns:
            none
        
        '''
        coleccionPersonas = self.baseDatos.personas
        coleccionRoles = self.baseDatos.roles

        #Encode a la contraseña en base a utf-8
        byteContrasenia = contrasenia.encode('utf-8')
        
        #Se realiza el hashed a la contraseña
        hashed_contrasenia = bcrypt.hashpw(byteContrasenia, self.salt)
        
        #Se obtiene el id del rol
        rolID = coleccionRoles.find_one({"$and":[{"descripcion": rol},{"estado": 'Activo'}]})

        #Documento con la estructura
        persona = {"_id": id, 'info_personal': {"nombre": nombre, "apellido": apellido, "f_nac": f_nac, "telefono": telefono, "email": email},
                    "usuario": usuario, "contrasenia": hashed_contrasenia, "rol_id": rolID["_id"], "estado": 'Inactivo'}
        
        #Se inserta dentro de la coleccion
        try:
            insercion = coleccionPersonas.insert_one(persona)
        except:
            return 'El id ya existe'

        #Se retorna un mensaje por la terminal
        print(insercion)

    def registrarAula(self, id, nombre, max):
        """
        Función para registrar el aula

        Args:
            id (int): id del aula
            nombre (string): nombre del aula
            max (int): capacidad del aula
        """


        coleccionAulas = self.baseDatos.aulas

        query = {"_id": id, "nombre": nombre, "max": max}

        insertado = coleccionAulas.insert_one(query)
        print(insertado)
    

    def registroAnioLectivo(self, id, nombre, fechaInicio, fechaFin):
        """
        Función para la creación de un año lectivo

        Args:
            id (int): _description_
            fechaInicio (date): fecha de inicio del año lectivo
            fechaFin (date): fecha de final del año lectivo

        Returns:
            insercion: none
        """
        coleccionAnio = self.baseDatos.aniolectivo
        query = {"_id": id,"nombre": nombre,"fechaInicio": fechaInicio, "fechaFin": fechaFin, "estado": "Activo"}
        insercion = coleccionAnio.insert_one(query)
        
        return insercion


    def registroMateria(self, id, descripcion):
        """
        Función para la creación de una materia del aplicativo

        Args:
            id (int): id de la materia
            descripcion (string): nombre de la materia

        Returns:
            insercion: none
        """
        coleccionMateria = self.baseDatos.materias
        query = {"_id": id, "descripcion":descripcion}
        insercion = coleccionMateria.insert_one(query)

        return insercion

    def registroRangoNotas(self,id,notaMin,notaMax):
        """
        Función que permite el registro de las notas, la nota minima y máxima, estarán establecidas en el año lectivo

        Args:
            id (int): id escogido por el administrador
            notaMin (float): Nota mínima
            notaMax (float): Nota máxima

        Returns:
            insercion: none
        """
        coleccionRangoNotas = self.baseDatos.rangonotas
        query = {"_id": id, "notaMin": notaMin, "notaMax": notaMax, "estado": "Activo"}
        insercion = coleccionRangoNotas.insert_one(query)

        return insercion


    def registroMatricula(self,id_alumno,id_aula,f_matricula):
        """
        Función que se usa para matricular a un estudiante

        Args:
            id_alumno (_type_): _description_
            id_aula (_type_): _description_
            f_matricula (_type_): _description_

        Returns:
            _type_: _description_
        """


        coleccionMatriculas = self.baseDatos.matriculas
        query = {"id_alumno": id_alumno, "id_aula": id_aula, "f_matricula": f_matricula}
        restado = self.restarCapacidad(id_aula)
        if(restado == True):
            insercion = coleccionMatriculas.insert_one(query)
            return insercion
        else:
            return "No existe aula"

        

    #--------------------- VALIDACIÓN -----------------------

    def validarUsuario(self, usuario, contrasenia,rol):

        '''
        Función que permite la busqueda del usuario en la base de datos en Mongodb

        Parametros:
            self (class)
            usuario (string): usario registrado
            contrasenia (string): contraseña del usuario registrado
        
        Returns:
            Boolean: True o False
        
        '''
        coleccionPersonas = self.baseDatos.personas
        coleccionRoles = self.baseDatos.roles

        encodedContrasenia = contrasenia.encode('utf-8')
        comprobarHashed = bcrypt.hashpw(encodedContrasenia, self.salt)
        print(comprobarHashed)
        rolID = coleccionRoles.find_one({"$and":[{"descripcion": rol},{"estado": 'Activo'}]})
        query1 = {"usuario": usuario}

        cons = coleccionPersonas.find_one(query1)
        hash = cons["contrasenia"]
        print(hash)
        query = {"$and":[{"usuario": usuario},{"contrasenia": comprobarHashed},{"rol_id": rolID["_id"]},{"estado": "Activo"}]}
        
        if (coleccionPersonas.find_one(query)):
            return True
        else:
            return False

    
    def desactivarUsuario(self, usuario):
        '''
        Función que permite desactivar un usuario

        Parametros:
            self (class)
            usuario (string): usuario registrado
        
        Returns:
            Boolean: True o False
        
        '''
        coleccionPersonas = self.baseDatos.personas

        query = {"usuario": usuario}

        if(coleccionPersonas.find_one(query)):
            coleccionPersonas.find_one_and_update(query, {"$set": {"estado": "Inactivo"}})
            return True
        else:
            return False


    def restarCapacidad(self,idAula):
        '''
        Función para ir restando la capacidad del aula
        '''

        coleccionAulas = self.baseDatos.aulas
        query = {"_id": idAula}

        if(coleccionAulas.find_one(query)):
            aula = coleccionAulas.find_one(query)
            capacidad = aula["max"]
            capacidad -= 1
            coleccionAulas.find_one_and_update(query,{"$set": {"max": capacidad}})
            return True
        else:
            return False

        
    def mostrarRoles(self):
        '''
        Función que retorna la colección de roles 
        
        Parametros:
            self (class)
        
        Returns:
            roles (list)
        '''
        coleccion = self.baseDatos.roles
        roles = list(coleccion.find())
        return roles


    def mostrarPermisos(self):
        '''
        Función que retorna la colección de permisos

        Parametros:
            self (class)
        
        Returns:
            permisos (list)
        '''   
        coleccion = self.baseDatos.permisos
        permisos = list(coleccion.find())

        return permisos

    def mostrarPersonas(self):
        """
        Función para mostrar personas

        Returns:
            personas: Lista de las personas extraidas de mongo
        """

        coleccion = self.baseDatos.personas
        personas = list(coleccion.find())

        return personas

    def mostrarAulas(self):
        """
        Función que retorna la lista de aulas

        Returns:
            aulas:  Lista de las aulas extraidas de mongo
        """


        coleccion = self.baseDatos.aulas
        aulas = list(coleccion.find())

        return aulas

    def buscarAula(self,nombre):
        """
        Función que busca el aula

        Args:
            nombre (string): Nombre del aula

        Returns:
            idAula: retorna el id del aula
        """
        coleccion = self.baseDatos.aulas
        idAula = list(coleccion.find_one({"nombre": nombre}))
        idAula = idAula["_id"]
        return idAula

    def idrol(self,rol):
        '''
        Función que retorna el id del rol
        '''
        coleccionRoles = self.baseDatos.roles
        rolID = coleccionRoles.find_one({"$and":[{"descripcion": rol},{"estado": 'Activo'}]})
        return rolID

    
    def desactivarAnioLectivo(self,id):
        """
        Función para desactivar el año lectivo 

        Args:
            id (int): id del año lectivo
        
        Returns:
            actualizacion: none
        """

        coleccionAnio = self.baseDatos.aniolectivo
        query = {"_id":id}
        query2 = {"$set":{"estado":"Inactivo"}}
        actualizacion = coleccionAnio.find_one_and_update(query,query2)

        return actualizacion

    def desactivarNotas(self,id):
        """
        Función para desactivar el rango de notas

        Args:
            id (int): id del rango de notas

        Returns:
            actualizacion: none
        """

        coleccionNotas = self.baseDatos.rangonotas
        query = {"_id":id}
        query2 = {"$set":{"estado":"Inactivo"}}
        actualizacion = coleccionNotas.find_one_and_update(query,query2)

        return actualizacion
    
    


    # Código de prueba para el hash
    def probarHashed (self, contra1, contra2):
        encod1 = contra1.encode('utf-8')
        encod2 = contra2.encode('utf-8')

        hash1 = bcrypt.hashpw(encod1,self.salt)
        hash2 = bcrypt.hashpw(encod2,self.salt)

        print(hash1)
        print(hash2)

        if(hash1 == hash2):
            print("Son iguales")


    def getKey(self):
        key = Fernet.generate_key()
        return key

   


'''
if __name__ == '__main__':

    print("Hello world")
    mongo = Mongo()

    contra1 = input("Primera contraseña: ")
    contra2 = input("Segunda contraseña: ")
    
    mongo.probarHashed(contra1,contra2)
'''