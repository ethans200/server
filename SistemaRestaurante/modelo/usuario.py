class Usuario:
    def __init__(self, id_u, nombre, user, clave, rol):
        self.__id = id_u
        self.__nombre = nombre
        self.__username = user
        self.__contrasena = clave
        self.__rol = rol

    def get_rol(self): return self.__rol
    def get_nombre(self): return self.__nombre

class Administrador(Usuario):
    def __init__(self, id_u, nombre, user, clave):
        super().__init__(id_u, nombre, user, clave, "Administrador")

class Mesero(Usuario):
    def __init__(self, id_u, nombre, user, clave):
        super().__init__(id_u, nombre, user, clave, "Mesero")

class Cocinero(Usuario):
    def __init__(self, id_u, nombre, user, clave):
        super().__init__(id_u, nombre, user, clave, "Cocinero")
