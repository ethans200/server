class Mesa:
    """Representa una mesa del restaurante."""
    def __init__(self, id_mesa, numero, capacidad, estado="Disponible"):
        self.__id_mesa = id_mesa
        self.__numero = numero
        self.__capacidad = capacidad
        self.__estado = estado # Disponible, Ocupada, Reservada

    def get_id_mesa(self): return self.__id_mesa
    def get_numero(self): return self.__numero
    def get_estado(self): return self.__estado
    def set_estado(self, estado): self.__estado = estado
