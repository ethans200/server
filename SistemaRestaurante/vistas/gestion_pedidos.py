import tkinter as tk
from tkinter import ttk, messagebox
from base_datos.conexion import ConexionBD
from datetime import datetime

class GestionPedidosVista:
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Terminal Punto de Venta - Catálogo Visual")
        self.win.geometry("1250x850")
        self.win.grab_set()
        self.db = ConexionBD()
        
        # Diccionarios para rastrear el pedido en memoria
        self.cantidades_vars = {} 
        self.carrito = {}        

        # --- ENCABEZADO ---
        header = tk.Frame(self.win, bg="#2C3E50", pady=15)
        header.pack(fill="x")
        
        tk.Label(header, text="🍽️ PUNTO DE VENTA", font=("Segoe UI", 18, "bold"), bg="#2C3E50", fg="white").pack(side="left", padx=30)
        
        mesa_frame = tk.Frame(header, bg="#2C3E50")
        mesa_frame.pack(side="right", padx=30)
        tk.Label(mesa_frame, text="MESA SELECCIONADA:", font=("Segoe UI", 10, "bold"), bg="#2C3E50", fg="#BDC3C7").pack(side="left")
        
        mesas = [m[0] for m in self.db.obtener_datos("SELECT numero FROM Mesas WHERE estado='Disponible'")]
        self.cb_mesa = ttk.Combobox(mesa_frame, values=mesas, state="readonly", width=8, font=("Arial", 12))
        self.cb_mesa.pack(side="left", padx=10)

        # --- CUERPO PRINCIPAL ---
        cuerpo = tk.Frame(self.win, bg="#F5F6FA")
        cuerpo.pack(fill="both", expand=True)

        # IZQUIERDA: CATÁLOGO DE PRODUCTOS (Scrollable)
        self.contenedor_izq = tk.Frame(cuerpo, bg="#F5F6FA", padx=15, pady=15)
        self.contenedor_izq.pack(side="left", fill="both", expand=True)

        # Pestañas de Categoría en línea recta
        tabs_frame = tk.Frame(self.contenedor_izq, bg="#F5F6FA", pady=5)
        tabs_frame.pack(fill="x")
        
        categorias = [("TODOS", "#7F8C8D", "Todos"), ("ENTRADAS", "#3498DB", "Entradas"), 
                      ("PLATOS FUERTES", "#E67E22", "Platos Fuertes"), ("BEBIDAS", "#9B59B6", "Bebidas")]
        
        for texto, color, cat in categorias:
            tk.Button(tabs_frame, text=texto, bg=color, fg="white", font=("Segoe UI", 9, "bold"),
                      relief="flat", padx=20, pady=10, cursor="hand2",
                      command=lambda c=cat: self.dibujar_catalogo(c)).pack(side="left", padx=5)

        # Área de Scroll
        self.canvas = tk.Canvas(self.contenedor_izq, bg="#F5F6FA", highlightthickness=0)
        self.scroll_y = ttk.Scrollbar(self.contenedor_izq, orient="vertical", command=self.canvas.yview)
        self.grid_productos = tk.Frame(self.canvas, bg="#F5F6FA")

        self.canvas.create_window((0, 0), window=self.grid_productos, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # DERECHA: HOJA DE PEDIDO (Ticket Fijo)
        self.der = tk.Frame(cuerpo, width=400, bg="white", highlightthickness=1, highlightbackground="#DCDDE1")
        self.der.pack(side="right", fill="y", padx=15, pady=15)
        self.der.pack_propagate(False)

        tk.Label(self.der, text="HOJA DE PEDIDO", font=("Segoe UI", 12, "bold"), bg="white", pady=15).pack(side="top")

        # Footer del Ticket (Botón e Info fija abajo)
        self.footer = tk.Frame(self.der, bg="white", pady=10)
        self.footer.pack(side="bottom", fill="x")

        self.lbl_total = tk.Label(self.footer, text="TOTAL: $0.00", font=("Segoe UI", 22, "bold"), fg="#27AE60", bg="white")
        self.lbl_total.pack(pady=10)

        tk.Button(self.footer, text="📋 REVISAR Y ENVIAR", bg="#27AE60", fg="white", font=("Segoe UI", 12, "bold"),
                  height=3, cursor="hand2", command=self.abrir_confirmacion).pack(fill="x", padx=15, pady=10)

        # Tabla del Ticket (En el centro)
        self.tree_ticket = ttk.Treeview(self.der, columns=("N", "C", "S"), show="headings")
        self.tree_ticket.heading("N", text="Item"); self.tree_ticket.heading("C", text="Cant"); self.tree_ticket.heading("S", text="Sub")
        self.tree_ticket.column("N", width=180); self.tree_ticket.column("C", width=50, anchor="center"); self.tree_ticket.column("S", width=80, anchor="e")
        self.tree_ticket.pack(side="top", fill="both", expand=True, padx=10)

        self.dibujar_catalogo("Todos")

    def dibujar_catalogo(self, categoria):
        for widget in self.grid_productos.winfo_children(): widget.destroy()
        query = "SELECT id_producto, nombre, precio FROM Productos"
        if categoria != "Todos":
            cat_id = {"Entradas": 1, "Platos Fuertes": 2, "Bebidas": 3}[categoria]
            query += f" WHERE id_categoria = {cat_id}"
        
        productos = self.db.obtener_datos(query)
        columnas = 4
        for index, p in enumerate(productos):
            id_p, nombre, precio = p
            card = tk.Frame(self.grid_productos, bg="white", bd=1, relief="solid", padx=15, pady=15, width=190, height=160)
            card.grid(row=index//columnas, column=index%columnas, padx=8, pady=8)
            card.grid_propagate(False)
            
            if id_p not in self.cantidades_vars: self.cantidades_vars[id_p] = tk.IntVar(value=0)
            
            # Selector de cantidad arriba
            tk.Spinbox(card, from_=0, to=99, textvariable=self.cantidades_vars[id_p], width=5, font=("Arial", 14, "bold"), 
                       justify="center", bg="#F1F2F6", command=lambda i=id_p, n=nombre, pr=precio: self.actualizar_pedido(i, n, pr)).pack(pady=(0, 10))
            tk.Label(card, text=nombre.upper(), font=("Segoe UI", 8, "bold"), bg="white", wraplength=150).pack()
            tk.Label(card, text=f"${precio:.2f}", font=("Segoe UI", 9), bg="white", fg="#2980B9").pack(pady=5)

        self.grid_productos.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def actualizar_pedido(self, id_p, nombre, precio):
        if not self.cb_mesa.get():
            self.cantidades_vars[id_p].set(0)
            messagebox.showwarning("Atención", "Seleccione la Mesa primero.")
            return
        cant = self.cantidades_vars[id_p].get()
        self.cb_mesa.config(state="disabled")
        if cant > 0: self.carrito[id_p] = {'nom': nombre, 'cant': cant, 'sub': cant * float(precio), 'precio': precio}
        else:
            if id_p in self.carrito: del self.carrito[id_p]
        self.refrescar_ticket()

    def refrescar_ticket(self):
        for i in self.tree_ticket.get_children(): self.tree_ticket.delete(i)
        total = sum(i['sub'] for i in self.carrito.values())
        for item in self.carrito.values():
            self.tree_ticket.insert("", "end", values=(item['nom'], item['cant'], f"${item['sub']:.2f}"))
        self.lbl_total.config(text=f"TOTAL: ${total:.2f}")

    def abrir_confirmacion(self):
        if not self.carrito:
            messagebox.showerror("Error", "No hay productos seleccionados.")
            return

        self.conf_win = tk.Toplevel(self.win)
        self.conf_win.title("Confirmar Pedido")
        self.conf_win.geometry("500x600")
        self.conf_win.configure(bg="white")
        self.conf_win.grab_set()

        tk.Label(self.conf_win, text="RESUMEN DEL PEDIDO", font=("Segoe UI", 14, "bold"), bg="white", pady=20).pack()
        caja = tk.Frame(self.conf_win, bg="#F9F9F9", padx=20, pady=20, bd=1, relief="solid")
        caja.pack(fill="both", expand=True, padx=30)

        tk.Label(caja, text=f"MESA: {self.cb_mesa.get()}", font=("Arial", 11, "bold"), bg="#F9F9F9").pack(anchor="w")
        tk.Label(caja, text="-"*45, bg="#F9F9F9", fg="#DCDDE1").pack(pady=10)

        total = 0
        for item in self.carrito.values():
            tk.Label(caja, text=f"{item['nom']} (x{item['cant']}) - ${item['sub']:.2f}", bg="#F9F9F9", font=("Arial", 10)).pack(anchor="w", pady=2)
            total += item['sub']

        tk.Label(caja, text="-"*45, bg="#F9F9F9", fg="#DCDDE1").pack(pady=10)
        tk.Label(caja, text=f"TOTAL A PAGAR: ${total:.2f}", font=("Arial", 14, "bold"), bg="#F9F9F9", fg="#27AE60").pack(pady=10)

        btn_f = tk.Frame(self.conf_win, bg="white", pady=20)
        btn_f.pack(fill="x", padx=30)
        tk.Button(btn_f, text="⬅️ EDITAR", bg="#7F8C8D", fg="white", font=("bold"), height=2, command=self.conf_win.destroy).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(btn_f, text="🚀 ENVIAR", bg="#27AE60", fg="white", font=("bold"), height=2, command=self.guardar_final).pack(side="right", fill="x", expand=True, padx=5)

    def guardar_final(self):
        # LÓGICA DE AUTO-ASIGNACIÓN A COCINERO LIBRE
        query_libres = """
            SELECT nombre FROM Usuarios 
            WHERE rol='Cocinero' 
            AND nombre NOT IN (SELECT cocinero_nombre FROM Pedidos WHERE estado='En Proceso')
            ORDER BY nombre ASC
        """
        libres = self.db.obtener_datos(query_libres)
        
        if libres:
            asignado_a = libres[0][0]
            estado_ini = 'En Proceso'
        else:
            asignado_a = 'N/A'
            estado_ini = 'Pendiente'

        total_final = sum(i['sub'] for i in self.carrito.values())
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        id_p = self.db.ejecutar_consulta(
            "INSERT INTO Pedidos (id_mesa, total, fechaHora, estado, cocinero_nombre) VALUES (?,?,?,?,?)",
            (self.cb_mesa.get(), total_final, fecha, estado_ini, asignado_a)
        )
        
        for id_prod, d in self.carrito.items():
            self.db.ejecutar_consulta("INSERT INTO DetallePedido (id_pedido, id_producto, cantidad, subtotal) VALUES (?,?,?,?)", (id_p, id_prod, d['cant'], d['sub']))
            
        self.db.ejecutar_consulta("UPDATE Mesas SET estado='Ocupada' WHERE numero=?", (self.cb_mesa.get(),))
        
        msg = f"PEDIDO #{id_p} ENVIADO.\n" + (f"Asignado a: {asignado_a}" if asignado_a != 'N/A' else "Estado: En Espera")
        messagebox.showinfo("Éxito", msg)
        self.conf_win.destroy()
        self.win.destroy()
