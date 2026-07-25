class Categoria:
    """Representa las categorías de los productos (Bebidas, Platos Fuertes, etc.)."""
    def __init__(self, id_categoria, nombre):
        self.__id_categoria = id_categoria
        self.__nombre = nombre

    def get_id_categoria(self): return self.__id_categoria
    def get_nombre(self): return self.__nombre
    def set_nombre(self, nombre): self.__nombre = nombre
