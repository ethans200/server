import tkinter as tk
from tkinter import ttk, messagebox
from base_datos.conexion import ConexionBD

class VentanaDetallePedido:
    def __init__(self, parent, id_pedido):
        self.win = tk.Toplevel(parent)
        self.win.title(f"Ticket #{id_pedido}")
        self.win.geometry("450x600")
        self.win.configure(bg="white")
        self.db = ConexionBD()
        
        info = self.db.obtener_datos("SELECT id_mesa, total, cocinero_nombre FROM Pedidos WHERE id_pedido=?", (id_pedido,))
        if not info: return
        id_mesa, total, cocinero = info[0]
        detalles = self.db.obtener_datos("SELECT p.nombre, d.cantidad, d.subtotal FROM DetallePedido d JOIN Productos p ON d.id_producto=p.id_producto WHERE d.id_pedido=?", (id_pedido,))

        tk.Label(self.win, text="RESUMEN DE COCINA", font=("Segoe UI", 14, "bold"), bg="white", pady=20).pack()
        caja = tk.Frame(self.win, bg="#F9F9F9", padx=25, pady=25, bd=1, relief="solid")
        caja.pack(fill="both", expand=True, padx=30, pady=10)

        tk.Label(caja, text=f"MESA: {id_mesa} | COCINERO: {cocinero}", font=("Arial", 10, "bold"), bg="#F9F9F9").pack(anchor="w")
        tk.Label(caja, text="-"*40, bg="#F9F9F9", fg="#DCDDE1").pack(pady=5)
        for d in detalles:
            tk.Label(caja, text=f"• {d[0]} (x{d[1]}) - ${d[2]:.2f}", bg="#F9F9F9", font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Label(caja, text="-"*40, bg="#F9F9F9", fg="#DCDDE1").pack(pady=5)
        tk.Label(caja, text=f"TOTAL: ${total:.2f}", font=("Arial", 12, "bold"), bg="#F9F9F9", fg="#27AE60").pack(pady=10)
        tk.Button(self.win, text="CERRAR", command=self.win.destroy, width=15).pack(pady=10)

class CocinaVista:
    def __init__(self, root, rol, nombre_usuario):
        self.win = tk.Toplevel(root)
        self.win.title("Dashboard de Cocina")
        self.win.geometry("1000x700")
        self.win.grab_set()
        self.db = ConexionBD()
        self.rol = rol
        self.nombre_usuario = nombre_usuario 

        header = tk.Frame(self.win, bg="#E67E22", pady=15)
        header.pack(fill="x")
        tk.Label(header, text=f"COCINA - USUARIO: {self.nombre_usuario.upper()}", font=("Segoe UI", 12, "bold"), bg="#E67E22", fg="white").pack()

        self.tree = ttk.Treeview(self.win, columns=("ID", "Mesa", "Estado", "Cocinero"), show="headings")
        self.tree.heading("ID", text="ID"); self.tree.heading("Mesa", text="Mesa"); self.tree.heading("Estado", text="Estado"); self.tree.heading("Cocinero", text="Asignado a")
        self.tree.tag_configure('En Espera', background='white')
        self.tree.tag_configure('En Proceso', background='#D6EAF8')
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        btn_f = tk.Frame(self.win, pady=10)
        btn_f.pack()

        if self.rol == "Cocinero":
            tk.Button(btn_f, text="⚡ ACEPTAR PEDIDO", bg="#3498DB", fg="white", font=("Arial", 10, "bold"), width=20, command=self.a_proceso).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="✅ PEDIDO LISTO", bg="#27AE60", fg="white", font=("Arial", 10, "bold"), width=20, command=self.terminar).pack(side="left", padx=5)
        tk.Button(btn_f, text="📋 INFO", bg="#F1C40F", width=10, font=("Arial", 10, "bold"), command=self.ver_info).pack(side="left", padx=5)

        self.actualizar()

    def actualizar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        pedidos = self.db.obtener_datos("SELECT id_pedido, id_mesa, estado, cocinero_nombre FROM Pedidos WHERE estado IN ('Pendiente', 'En Proceso') ORDER BY id_pedido ASC")
        for p in pedidos:
            est = "En Espera" if p[2] == "Pendiente" else p[2]
            self.tree.insert("", "end", values=(p[0], p[1], est, p[3]), tags=(est,))

    def a_proceso(self):
        chequeo = self.db.obtener_datos("SELECT count(*) FROM Pedidos WHERE cocinero_nombre=? AND estado='En Proceso'", (self.nombre_usuario,))
        if chequeo[0][0] > 0:
            messagebox.showwarning("Atención", "Ya tienes un pedido en proceso.")
            return
        sel = self.tree.selection()
        if not sel: return
        id_p, mesa, est, coc = self.tree.item(sel)['values']
        if est == "En Espera":
            self.db.ejecutar_consulta("UPDATE Pedidos SET estado='En Proceso', cocinero_nombre=? WHERE id_pedido=?", (self.nombre_usuario, id_p))
            self.actualizar()

    def terminar(self):
        sel = self.tree.selection()
        if not sel: return
        id_p, mesa, est, coc = self.tree.item(sel)['values']
        if est == "En Proceso":
            self.db.ejecutar_consulta("UPDATE Pedidos SET estado='Completada' WHERE id_pedido=?", (id_p,))
            # Auto-asignar el siguiente en espera
            sig = self.db.obtener_datos("SELECT id_pedido FROM Pedidos WHERE estado='Pendiente' ORDER BY id_pedido ASC LIMIT 1")
            if sig:
                self.db.ejecutar_consulta("UPDATE Pedidos SET estado='En Proceso', cocinero_nombre=? WHERE id_pedido=?", (self.nombre_usuario, sig[0][0]))
                messagebox.showinfo("Cola", f"Pedido #{id_p} Listo. Se te asignó el #{sig[0][0]} automáticamente.")
            self.actualizar()

    def ver_info(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un pedido")
            return
        id_p = self.tree.item(sel)['values'][0]
        VentanaDetallePedido(self.win, id_p)
