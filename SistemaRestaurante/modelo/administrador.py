from modelo.usuario import Usuario

class Administrador(Usuario):
    """Clase que representa a un Administrador, hereda de Usuario."""
    def __init__(self, id_usuario, nombre, username, password):
        super().__init__(id_usuario, nombre, username, password, "Administrador")

    def gestionar_usuarios(self):
        # Lógica para gestionar usuarios
        print("Accediendo a gestión de usuarios...")
