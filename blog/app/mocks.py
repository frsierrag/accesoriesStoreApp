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
        {"id":"acc-001", "name":"Sombrero", "quantity":15, "image":"img/accesorio_1.png"},
        {"id":"acc-002", "name":"Gafas Verdes", "quantity":10, "image":"img/accesorio_2.png"},
        {"id":"acc-003", "name":"Gafas", "quantity":12, "image":"img/accesorio_3.png"},
        {"id":"acc-004", "name":"Collar", "quantity":25, "image":"img/accesorio_4.png"},
    ]}
    productSearch = [accesory for accesory in accesories["products"] if name in accesory["name"]]
    if len(productSearch) > 0:
        print('Product: ' + ''.join(str(e) for e in productSearch))
        return productSearch
    return "1"

def is_authenticated(self):
	return True

def is_active(self):
	return True

def is_anonymous(self):
	return False

def get_id(self):
	return str(self.id)

def is_admin(self):
	return self.admin