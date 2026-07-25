from modelo.usuario import Usuario

class Mesero(Usuario):
    """Clase que representa a un Mesero, hereda de Usuario."""
    def __init__(self, id_usuario, nombre, username, password):
        super().__init__(id_usuario, nombre, username, password, "Mesero")

    def tomar_pedido(self):
        # Lógica para tomar pedidos
        print("Tomando nuevo pedido...")
