import tkinter as tk
from tkinter import ttk, messagebox
from base_datos.conexion import ConexionBD

class GestionMesasVista:
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Monitor de Mesas")
        self.win.geometry("400x450")
        self.win.grab_set()
        self.db = ConexionBD()

        tk.Label(self.win, text="ESTADO DE MESAS", font=("Arial", 12, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self.win, columns=("N", "C", "E"), show="headings")
        self.tree.heading("N", text="Mesa #"); self.tree.heading("C", text="Capacidad"); self.tree.heading("E", text="Estado")
        self.tree.pack(fill="both", expand=True, padx=20)

        tk.Button(self.win, text="ALTERNAR ESTADO", bg="#8E44AD", fg="white", command=self.toggle).pack(pady=20)
        self.cargar()

    def cargar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for m in self.db.obtener_datos("SELECT numero, capacidad, estado FROM Mesas"):
            self.tree.insert("", "end", values=m)

    def toggle(self):
        sel = self.tree.selection()
        if not sel: return
        num, _, est = self.tree.item(sel)['values']
        nuevo = "Ocupada" if est == "Disponible" else "Disponible"
        self.db.ejecutar_consulta("UPDATE Mesas SET estado=? WHERE numero=?", (nuevo, num))
        self.cargar()
