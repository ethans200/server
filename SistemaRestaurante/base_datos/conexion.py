import sqlite3
import os

class ConexionBD:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.ruta_db = os.path.join(self.base_dir, "restaurante.db")
        self.inicializar_bd()

    def conectar(self):
        return sqlite3.connect(self.ruta_db)

    def inicializar_bd(self):
        con = self.conectar()
        cursor = con.cursor()
        
        # Crear Tablas
        cursor.execute('CREATE TABLE IF NOT EXISTS Usuarios (id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, username TEXT UNIQUE, contrasena TEXT, rol TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS Pedidos (id_pedido INTEGER PRIMARY KEY AUTOINCREMENT, id_mesa INTEGER, total REAL, fechaHora TEXT, estado TEXT DEFAULT "Pendiente", cocinero_nombre TEXT DEFAULT "N/A")')
        cursor.execute('CREATE TABLE IF NOT EXISTS DetallePedido (id_detalle INTEGER PRIMARY KEY AUTOINCREMENT, id_pedido INTEGER, id_producto INTEGER, cantidad INTEGER, subtotal REAL)')
        cursor.execute('CREATE TABLE IF NOT EXISTS Productos (id_producto INTEGER PRIMARY KEY, nombre TEXT, precio REAL, id_categoria INTEGER)')
        cursor.execute('CREATE TABLE IF NOT EXISTS Mesas (id_mesa INTEGER PRIMARY KEY AUTOINCREMENT, numero INTEGER, capacidad INTEGER, estado TEXT DEFAULT "Disponible")')
        cursor.execute('CREATE TABLE IF NOT EXISTS Categorias (id_categoria INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT)')

        # LIMPIEZA: Borrar cualquier usuario "Chef" o antiguo
        cursor.execute("DELETE FROM Usuarios WHERE nombre LIKE '%Chef%' OR username='cocina'")

        # INSERTAR LOS 4 USUARIOS OFICIALES
        usuarios = [
            ('Administrador', 'admin', '1234', 'Administrador'),
            ('Mesero', 'mesero', '1234', 'Mesero'),
            ('Cocinero 1', 'cocinero1', '1234', 'Cocinero'),
            ('Cocinero 2', 'cocinero2', '1234', 'Cocinero')
        ]
        for nom, user, clave, rol in usuarios:
            cursor.execute("SELECT id_usuario FROM Usuarios WHERE username=?", (user,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO Usuarios (nombre, username, contrasena, rol) VALUES (?,?,?,?)", (nom, user, clave, rol))

        con.commit()
        con.close()

    def obtener_datos(self, consulta, parametros=()):
        con = self.conectar(); c = con.cursor(); c.execute(consulta, parametros); r = c.fetchall(); con.close(); return r

    def ejecutar_consulta(self, consulta, parametros=()):
        con = self.conectar(); c = con.cursor(); c.execute(consulta, parametros); lid = c.lastrowid; con.commit(); con.close(); return lid
