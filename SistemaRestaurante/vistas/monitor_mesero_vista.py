import tkinter as tk
from tkinter import ttk, messagebox
from base_datos.conexion import ConexionBD

class VentanaDetallePedido:
    def __init__(self, parent, id_pedido):
        self.win = tk.Toplevel(parent)
        self.win.title(f"Detalle Ticket #{id_pedido}")
        self.win.geometry("450x650")
        self.win.configure(bg="white")
        self.db = ConexionBD()
        
        info = self.db.obtener_datos("SELECT id_mesa, total, cocinero_nombre FROM Pedidos WHERE id_pedido=?", (id_pedido,))
        if not info: return
        id_mesa, total, cocinero = info[0]
        detalles = self.db.obtener_datos("SELECT p.nombre, d.cantidad, d.subtotal FROM DetallePedido d JOIN Productos p ON d.id_producto=p.id_producto WHERE d.id_pedido=?", (id_pedido,))

        tk.Label(self.win, text="DETALLE DEL PEDIDO", font=("Segoe UI", 14, "bold"), bg="white", pady=20).pack()
        caja = tk.Frame(self.win, bg="#F9F9F9", padx=25, pady=25, bd=1, relief="solid")
        caja.pack(fill="both", expand=True, padx=30)

        tk.Label(caja, text=f"MESA: {id_mesa} | COCINERO: {cocinero}", font=("Arial", 10, "bold"), bg="#F9F9F9").pack(anchor="w")
        tk.Label(caja, text="-"*40, bg="#F9F9F9", fg="#DCDDE1").pack(pady=5)
        for d in detalles:
            tk.Label(caja, text=f"• {d[0]} (x{d[1]}) - ${d[2]:.2f}", bg="#F9F9F9", font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Label(caja, text="-"*40, bg="#F9F9F9", fg="#DCDDE1").pack(pady=5)
        tk.Label(caja, text=f"TOTAL: ${total:.2f}", font=("Arial", 14, "bold"), bg="#F9F9F9", fg="#27AE60").pack(pady=10)
        tk.Button(self.win, text="CERRAR", command=self.win.destroy, width=15).pack(pady=10)

class MonitorMeseroVista:
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Seguimiento Meseros")
        self.win.geometry("1000x700")
        self.win.grab_set()
        self.db = ConexionBD()

        header = tk.Frame(self.win, bg="#16A085", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="📋 SEGUIMIENTO DE ÓRDENES", font=("Segoe UI", 14, "bold"), bg="#16A085", fg="white").pack()

        # Botones abajo
        self.footer = tk.Frame(self.win, bg="#F5F6FA", pady=20)
        self.footer.pack(side="bottom", fill="x")

        tk.Button(self.footer, text="ℹ️ VER INFO PEDIDO", bg="#3498DB", fg="white", font=("Arial", 11, "bold"), width=25, command=self.ver_info).pack(side="left", padx=50)
        tk.Button(self.footer, text="🍽️ MARCAR SERVIDO", bg="#27AE60", fg="white", font=("Arial", 11, "bold"), width=25, command=self.marcar_servido).pack(side="right", padx=50)

        self.tree = ttk.Treeview(self.win, columns=("ID", "Mesa", "Estado", "Cocinero"), show="headings")
        self.tree.heading("ID", text="ID"); self.tree.heading("Mesa", text="Mesa"); self.tree.heading("Estado", text="Estado"); self.tree.heading("Cocinero", text="Cocinero")
        self.tree.tag_configure('Pedido Listo', background='#ABEBC6')
        self.tree.tag_configure('En Proceso', background='#FAD7A0')
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.actualizar()

    def actualizar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        pedidos = self.db.obtener_datos("SELECT id_pedido, id_mesa, estado, cocinero_nombre FROM Pedidos WHERE estado != 'Servido' ORDER BY id_pedido ASC")
        for p in pedidos:
            est = "En Espera" if p[2] == "Pendiente" else p[2]
            est = "Pedido Listo" if est == "Completada" else est
            self.tree.insert("", "end", values=(p[0], p[1], est, p[3]), tags=(est,))

    def ver_info(self):
        sel = self.tree.selection()
        if not sel: return
        id_p = self.tree.item(sel)['values'][0]
        VentanaDetallePedido(self.win, id_p)

    def marcar_servido(self):
        sel = self.tree.selection()
        if not sel: return
        id_p, mesa, est, coc = self.tree.item(sel)['values']
        if est == "Pedido Listo":
            self.db.ejecutar_consulta("UPDATE Pedidos SET estado='Servido' WHERE id_pedido=?", (id_p,))
            self.db.ejecutar_consulta("UPDATE Mesas SET estado='Disponible' WHERE numero=?", (mesa,))
            self.actualizar()
        else:
            messagebox.showwarning("Atención", "El pedido no está listo.")
