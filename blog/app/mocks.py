def userValidate(user, password):
    usersRegistered = [
        {"user": "Admin", "email": "admin@gmail.com", "pass": 1234567890},
        {"user": "Julio", "email": "jcastanoc@uninorte.edu.co", "pass": 123},
        {"user": "Pepe", "email": "pepe@gmail.com", "pass": 567},
        {"user": "Elena", "email": "elena@outlook.com", "pass": 198},
        {"user": "Silvia", "email": "silvia@uninorte.edu.co", "pass": 456},
        {"user": "Fabian", "email": "fabiansierra@uninorte.edu.co", "pass": 000}
    ];

    userSearch = [registered for registered in usersRegistered if registered[0] == user]
    if len(userSearch) > 0:
        if userSearch.pass == password:
            return "Credenciales correctas. Bienvenido " + userSearch.user 
        return "Clave incorrecta"
    return "Usuario no registrado"
