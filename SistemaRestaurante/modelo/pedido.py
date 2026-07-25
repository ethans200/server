class Pedido:
    """Representa un pedido realizado en una mesa."""
    def __init__(self, id_pedido, id_mesa, id_usuario, fecha, total, estado="Pendiente"):
        self.__id_pedido = id_pedido
        self.__id_mesa = id_mesa
        self.__id_usuario = id_usuario
        self.__fecha = fecha
        self.__total = total
        self.__estado = estado

    def get_id_pedido(self): return self.__id_pedido
    def get_estado(self): return self.__estado
    def set_estado(self, estado): self.__estado = estado
    
    def __str__(self):
        return f"Pedido #{self.__id_pedido} - Mesa {self.__id_mesa} - Status: {self.__estado}"
