import tkinter as tk
from vistas.gestion_productos import GestionProductosVista
from vistas.gestion_mesas import GestionMesasVista
from vistas.gestion_pedidos import GestionPedidosVista
from vistas.cocina_vista import CocinaVista
from vistas.monitor_mesero_vista import MonitorMeseroVista

class MenuPrincipalVista:
    def __init__(self, root, nombre, rol):
        self.root = root
        self.rol = rol
        self.nombre = nombre
        
        # 1. Limpiar pantalla
        for w in self.root.winfo_children():
            w.destroy()

        self.root.geometry("1000x750") # Ventana más amplia
        self.root.title(f"Panel Principal - {rol}")
        self.root.configure(bg="#F5F6FA")

        # --- BARRA SUPERIOR (HEADER) ---
        header = tk.Frame(root, bg="#2C3E50", height=80)
        header.pack(fill="x", side="top")
        
        tk.Label(header, text="🍽️ SISTEMA RESTAURANTE", 
                 font=("Segoe UI", 16, "bold"), bg="#2C3E50", fg="white").pack(side="left", padx=30, pady=20)
        
        user_info = tk.Frame(header, bg="#2C3E50")
        user_info.pack(side="right", padx=30)
        tk.Label(user_info, text=nombre.upper(), font=("Segoe UI", 10, "bold"), bg="#2C3E50", fg="white").pack()
        tk.Label(user_info, text=f"Perfil: {rol}", font=("Segoe UI", 9), bg="#2C3E50", fg="#BDC3C7").pack()

        # --- PIE DE PÁGINA (Reserva el espacio inferior primero) ---
        footer = tk.Frame(root, bg="#F5F6FA", pady=20)
        footer.pack(side="bottom", fill="x")
        tk.Button(footer, text="❌ CERRAR SESIÓN Y SALIR", font=("Segoe UI", 10, "bold"), 
                  fg="#C0392B", bg="white", relief="solid", bd=1, padx=20, pady=10,
                  cursor="hand2", command=self.salir).pack()

        # --- CUERPO PRINCIPAL (CONTENEDOR DE TARJETAS) ---
        self.body = tk.Frame(root, bg="#F5F6FA")
        self.body.pack(expand=True)

        self.configurar_modulos()

    def configurar_modulos(self):
        # Admin: 3 columnas para que no crezca mucho hacia abajo
        if self.rol == "Administrador":
            self.crear_card("GESTIÓN PRODUCTOS", "⚙️", "#2980B9", self.abrir_productos, 0, 0)
            self.crear_card("MONITOR DE MESAS", "🪑", "#8E44AD", self.abrir_mesas, 0, 1)
            self.crear_card("REGISTRAR PEDIDO", "🛒", "#27AE60", self.abrir_pedidos, 0, 2)
            self.crear_card("DASHBOARD COCINA", "👨‍🍳", "#E67E22", self.abrir_cocina, 1, 0)
            self.crear_card("SEGUIMIENTO PEDIDOS", "📋", "#16A085", self.abrir_seguimiento, 1, 1)

        elif self.rol == "Mesero":
            self.crear_card("MONITOR DE MESAS", "🪑", "#8E44AD", self.abrir_mesas, 0, 0)
            self.crear_card("REGISTRAR PEDIDO", "🛒", "#27AE60", self.abrir_pedidos, 0, 1)
            self.crear_card("SEGUIMIENTO PEDIDOS", "📋", "#16A085", self.abrir_seguimiento, 1, 0)
            
        elif self.rol == "Cocinero":
            self.crear_card("DASHBOARD COCINA", "👨‍🍳", "#E67E22", self.abrir_cocina, 0, 0)

    def crear_card(self, texto, icono, color, comando, fila, col):
        card_frame = tk.Frame(self.body, bg="white", highlightbackground="#DCDDE1", highlightthickness=1)
        card_frame.grid(row=fila, column=col, padx=20, pady=20)
        btn = tk.Button(card_frame, text=f"{icono}\n\n{texto}", font=("Segoe UI", 10, "bold"), bg="white", fg=color,
                        width=25, height=7, bd=0, cursor="hand2", command=comando, relief="flat")
        btn.pack()

    def abrir_productos(self): GestionProductosVista(self.root, self.rol)
    def abrir_mesas(self): GestionMesasVista(self.root)
    def abrir_pedidos(self): GestionPedidosVista(self.root)
    def abrir_cocina(self): CocinaVista(self.root, self.rol, self.nombre)
    def abrir_seguimiento(self): MonitorMeseroVista(self.root)

    def salir(self):
        import sys, os
        python = sys.executable
        os.execl(python, python, *sys.argv)
