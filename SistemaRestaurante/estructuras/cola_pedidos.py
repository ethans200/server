class Nodo:
    def __init__(self, pedido):
        self.pedido = pedido
        self.siguiente = None

class ColaPedidos:
    def __init__(self):
        self.__frente = None
        self.__final = None

    def esta_vacia(self):
        return self.__frente is None

    def enqueue(self, pedido):
        nuevo = Nodo(pedido)
        if self.esta_vacia():
            self.__frente = nuevo
        else:
            self.__final.siguiente = nuevo
        self.__final = nuevo

    def dequeue(self):
        if self.esta_vacia(): return None
        aux = self.__frente
        self.__frente = self.__frente.siguiente
        return aux.pedido
