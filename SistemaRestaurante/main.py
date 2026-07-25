import tkinter as tk
from tkinter import ttk
from vistas.login import LoginVista
from vistas.menu_principal import MenuPrincipalVista

class SistemaRestauranteApp:
    def __init__(self):
        # 1. Configuración de la Ventana Raíz
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Restaurante v1.0")
        self.root.geometry("400x450")
        self.root.configure(bg="#F5F6FA") # Fondo gris claro moderno

        # 2. Configuración de Estilos Globales (UI/UX)
        # Esto hace que todas las tablas y botones del sistema se vean modernos
        self.configurar_estilos_globales()

        # 3. Iniciar con la pantalla de Login
        self.mostrar_login()
        
        # Mantener la aplicación abierta
        self.root.mainloop()

    def configurar_estilos_globales(self):
        """Define el aspecto visual de las tablas y componentes del sistema."""
        style = ttk.Style()
        style.theme_use("clam") # Tema base que permite personalización de colores

        # Estilo para todas las Tablas (Treeview) del proyecto
        style.configure("Treeview", 
                        background="#FFFFFF", 
                        foreground="#2F3640", 
                        rowheight=35,           # Filas más altas para mejor lectura
                        fieldbackground="#FFFFFF",
                        font=("Segoe UI", 10))  # Fuente profesional

        # Estilo para los encabezados de las tablas (N°, Producto, Precio...)
        style.configure("Treeview.Heading", 
                        background="#DCDDE1", 
                        foreground="#2F3640", 
                        font=("Segoe UI", 10, "bold"), 
                        relief="flat")
        
        # Color azul cuando seleccionas una fila en cualquier tabla
        style.map("Treeview", 
                  background=[('selected', '#3498DB')],
                  foreground=[('selected', '#FFFFFF')])

        # Estilo para los menús desplegables (Combobox)
        style.configure("TCombobox", padding=5)

    def mostrar_login(self):
        """Carga la interfaz de inicio de sesión."""
        # Se le pasa self.iniciar_menu como 'callback' para que se ejecute al entrar
        LoginVista(self.root, self.iniciar_menu)

    def iniciar_menu(self, nombre, rol):
        """
        Esta función se activa automáticamente cuando el Login es exitoso.
        Limpia la pantalla y construye el Menú Principal según el rol.
        """
        # Redimensionar la ventana para el Dashboard principal
        self.root.geometry("950x700")
        
        # Centrar la ventana en la pantalla
        self.root.update_idletasks()
        
        # Cargar el Menú Principal pasando nombre y rol para los permisos
        MenuPrincipalVista(self.root, nombre, rol)

if __name__ == "__main__":
    # Arrancar la aplicación
    app = SistemaRestauranteApp()
