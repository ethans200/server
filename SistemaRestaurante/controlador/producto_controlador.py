from base_datos.conexion import ConexionBD

class ProductoControlador:
    """
    Controlador encargado de la lógica de negocio para los productos.
    Implementa algoritmos de ordenamiento manual para cumplir con los
    requisitos académicos del Taller 13.
    """
    def __init__(self):
        self.db = ConexionBD()

    def obtener_todos(self):
        """
        Recupera los productos de la base de datos y los ordena manualmente
        utilizando el algoritmo de Burbuja (Bubble Sort).
        """
        # La consulta NO incluye ORDER BY para aplicar el algoritmo manualmente en Python
        query = """
            SELECT p.id_producto, p.nombre, p.precio, c.nombre 
            FROM Productos p 
            JOIN Categorias c ON p.id_categoria = c.id_categoria
        """
        # Obtenemos los registros (vienen como una lista de tuplas)
        datos = self.db.obtener_datos(query)
        
        # Convertimos a lista de listas porque las tuplas son inmutables 
        # y necesitamos intercambiar posiciones para el ordenamiento.
        lista_productos = [list(item) for item in datos]

        # --- IMPLEMENTACIÓN DEL ALGORITMO DE BURBUJA (Requisito Taller 13) ---
        n = len(lista_productos)
        for i in range(n):
            # El último i elemento ya está en su lugar
            for j in range(0, n - i - 1):
                # Comparamos el ID del producto (índice 0)
                if lista_productos[j][0] > lista_productos[j + 1][0]:
                    # Intercambio de posiciones (Swap)
                    lista_productos[j], lista_productos[j + 1] = lista_productos[j + 1], lista_productos[j]
        
        # Retornamos la lista ya ordenada por ID (1, 2, 3... 27)
        return lista_productos

    def actualizar_precio(self, id_prod, nuevo_precio):
        """
        Valida que el precio sea un número real positivo y 
        actualiza el registro en la base de datos.
        """
        try:
            # Validación de tipo de dato
            precio_float = float(nuevo_precio)
            
            if precio_float < 0:
                return False # No se permiten precios negativos
            
            # Ejecución de la actualización en la BD
            query = "UPDATE Productos SET precio = ? WHERE id_producto = ?"
            self.db.ejecutar_consulta(query, (precio_float, id_prod))
            return True
            
        except (ValueError, TypeError):
            # Retorna falso si el usuario ingresó letras o valores nulos
            return False

    def obtener_por_categoria(self, id_cat):
        """
        Obtiene productos filtrados y también aplica ordenamiento manual.
        """
        query = f"SELECT id_producto, nombre, precio FROM Productos WHERE id_categoria = {id_cat}"
        datos = self.db.obtener_datos(query)
        lista = [list(item) for item in datos]
        
        # Ordenamiento rápido para filtros
        n = len(lista)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista[j][0] > lista[j + 1][0]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        return lista
