usersRegistered = [
    {"user": "Admin", "email": "admin@gmail.com", "password": "1234567890"},
    {"user": "Julio", "email": "jcastanoc@uninorte.edu.co", "password": "123"},
    {"user": "Pepe", "email": "pepe@gmail.com", "password": "567"},
    {"user": "Elena", "email": "elena@outlook.com", "password": "198"},
    {"user": "Silvia", "email": "silvia@uninorte.edu.co", "password": "456"},
    {"user": "Fabian", "email": "fabiansierra@uninorte.edu.co", "password": "000"}
]

accesories = {"products":[
    {"id":"acc-001", "name":"Sombrero", "quantity":15, "image":"img/accesorio_1.png"},
    {"id":"acc-002", "name":"Gafas Verdes", "quantity":10, "image":"img/accesorio_2.png"},
    {"id":"acc-003", "name":"Gafas", "quantity":12, "image":"img/accesorio_3.png"},
    {"id":"acc-004", "name":"Collar", "quantity":25, "image":"img/accesorio_4.png"},
]}


def userValidate(user, password):
    userSearch = [registered for registered in usersRegistered if registered["user"] == user]
    if len(userSearch) > 0:
        if userSearch[0]["password"] == password:
            return  userSearch[0]["user"]
        return "1"
    return "2"


def createAccesories(form):
    newProduct = {"id":"acc-005", "name":form.productName.data, 
        "quantity":form.quantity.data, "image":"img/" + form.image.data.filename}
    accesories["products"].append(newProduct)
    print('CREACIÓN DE ACCESORIO EXITOSO')
    print(accesories)


def listAccesories(name):
    productSearch = [accesory for accesory in accesories["products"] if name in accesory["name"]]
    if len(productSearch) > 0:
        print('Product: ' + ''.join(str(e) for e in productSearch))
        print('LISTADO DE ACCESORIOS EXITOSO')
        return productSearch
    return ""


def updateAccesories(form):
    updateProduct = [accesory for accesory in accesories["products"] if accesory["id"] == form.idReference.data]
    if len(updateProduct) > 0:
        updateProduct[0]["name"] = form.productName.data
        updateProduct[0]["quantity"] = form.quantity.data
        updateProduct[0]["image"] = "img/" + form.image.data.filename
        print('ACTUALIZACIÓN DE ACCESORIOS EXITOSO')
        return accesories
    return "1"


def deleteAccesory(id):
    deleteProduct = [accesory for accesory in accesories["products"] if accesory["id"] == id]
    if len(deleteProduct) > 0:
        accesories["products"].remove(deleteProduct[0])
        print('ELIMINACIÓN DE ACCESORIOS EXITOSO')
        return accesories
    return "1"