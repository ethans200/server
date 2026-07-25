class Producto:
    """Representa un producto del menú."""
    def __init__(self, id_producto, nombre, precio, id_categoria):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__precio = precio
        self.__id_categoria = id_categoria

    # Getters y Setters
    def get_id_producto(self): return self.__id_producto
    def get_nombre(self): return self.__nombre
    def set_nombre(self, nombre): self.__nombre = nombre
    def get_precio(self): return self.__precio
    def set_precio(self, precio): self.__precio = precio
    def get_id_categoria(self): return self.__id_categoria
