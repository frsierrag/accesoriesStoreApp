def userValidate(user, password):
    usersRegistered = [
        {"user": "Admin", "email": "admin@gmail.com", "password": "1234567890"},
        {"user": "Julio", "email": "jcastanoc@uninorte.edu.co", "password": "123"},
        {"user": "Pepe", "email": "pepe@gmail.com", "password": "567"},
        {"user": "Elena", "email": "elena@outlook.com", "password": "198"},
        {"user": "Silvia", "email": "silvia@uninorte.edu.co", "password": "456"},
        {"user": "Fabian", "email": "fabiansierra@uninorte.edu.co", "password": "000"}
    ]
    userSearch = [registered for registered in usersRegistered if registered["user"] == user]
    if len(userSearch) > 0:
        if userSearch[0]["password"] == password:
            return  userSearch[0]["user"]
        return "1"
    return "2"

def listAccesories(name):
    accesories = {"products":[
        {"id":"acc-001", "name":"Gafas Azules", "quantity":15, "image":"D:\image\exem2.png"},
        {"id":"acc-002", "name":"Gafas Verdes", "quantity":10, "image":"D:\image\exem2.png"},
        {"id":"acc-003", "name":"Gafas", "quantity":12, "image":"D:\image\exem2.png"},
        {"id":"acc-004", "name":"Gafas Negras", "quantity":25, "image":"D:\image\exem2.png"},
    ]}
    productSearch = [accesory for accesory in accesories["products"] if accesory["name"] == name]
    if len(productSearch) > 0:
        return productSearch[0]
    return "Accesorio no encontrado"
