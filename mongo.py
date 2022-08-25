from email.policy import default
from itertools import permutations
from warnings import catch_warnings
import pymongo 
import bcrypt




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
            return 'Se ha insertado'
        except:
            return 'El id ya existe'

        #Se retorna un mensaje por la terminal
        print(insercion)



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

    def registrarAula(self, id, nombre, max):
        '''
        Función para regisrar un Aula
        '''


        coleccionAulas = self.baseDatos.aulas

        query = {"_id": id, "nombre": nombre, "max": max}

        insertado = coleccionAulas.insert_one(query)
        print(insertado)

    def desactivarUsuario(self, usuario):
        '''
        Función que permite desactivar un usuario

        Parametros:
            self (class)
            usuario (string): usuario registrado
        
        Returns:
            Boolean: True o False
        
        '''


        query = {"usuario": usuario}

        if(self.coleccionPersonas.find_one(query)):
            self.coleccionPersonas.find_one_and_update(query, {"$set": {"estado": "Inactivo"}})
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


    def idrol(self,rol):
        coleccionRoles = self.baseDatos.roles
        rolID = coleccionRoles.find_one({"$and":[{"descripcion": rol},{"estado": 'Activo'}]})
        return rolID


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

'''
if __name__ == '__main__':

    print("Hello world")
    mongo = Mongo()

    contra1 = input("Primera contraseña: ")
    contra2 = input("Segunda contraseña: ")
    
    mongo.probarHashed(contra1,contra2)
'''