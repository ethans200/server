import tkinter as tk
from tkinter import ttk, messagebox
from controlador.producto_controlador import ProductoControlador

class GestionProductosVista:
    def __init__(self, root, rol):
        self.win = tk.Toplevel(root)
        self.win.title("Gestión de Menú")
        self.win.geometry("600x500")
        self.win.grab_set() # Mantiene la ventana al frente
        self.ctrl = ProductoControlador()

        tk.Label(self.win, text="CATÁLOGO DE PRODUCTOS", font=("Arial", 12, "bold")).pack(pady=10)

        # Configuración de la tabla
        self.tree = ttk.Treeview(self.win, columns=("ID", "Nom", "Pre", "Cat"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nombre")
        self.tree.heading("Pre", text="Precio ($)")
        self.tree.heading("Cat", text="Categoría")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nom", width=200)
        self.tree.pack(fill="both", expand=True, padx=20)

        # Panel de edición
        f_edit = tk.Frame(self.win, pady=20)
        f_edit.pack()
        tk.Label(f_edit, text="Nuevo Precio: $").pack(side="left")
        self.ent_p = tk.Entry(f_edit, width=10)
        self.ent_p.pack(side="left", padx=5)
        
        self.btn_upd = tk.Button(f_edit, text="ACTUALIZAR", bg="#2980B9", fg="white", command=self.upd)
        self.btn_upd.pack(side="left")
        
        # Seguridad por rol
        if rol != "Administrador":
            self.btn_upd.config(state="disabled")
            tk.Label(self.win, text="* Solo lectura para Meseros/Cocineros", fg="red").pack()

        self.cargar()

    def cargar(self):
        """Limpia y recarga la tabla desde el controlador."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.ctrl.obtener_todos():
            self.tree.insert("", "end", values=p)

    def upd(self):
        """Lógica para actualizar el precio."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un producto")
            return
        
        id_p = self.tree.item(sel)['values'][0]
        nuevo_p = self.ent_p.get()
        
        if self.ctrl.actualizar_precio(id_p, nuevo_p):
            messagebox.showinfo("Éxito", "Precio Actualizado")
            self.ent_p.delete(0, tk.END)
            self.cargar()
        else:
            messagebox.showerror("Error", "Precio no válido")
