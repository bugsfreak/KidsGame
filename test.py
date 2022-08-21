import mongo



x = mongo.Mongo()
permisos = x.mostrarPermisos()

print(permisos)
'''
listPermisos = []w

for idx in range(2):
    listPermisos.append(permisos[idx])
'''
