import tkinter as tk
from tkinter import messagebox, ttk
from base_datos.conexion import ConexionBD

class LoginVista:
    def __init__(self, root, al_exito):
        self.root = root
        self.al_exito = al_exito
        for w in self.root.winfo_children(): w.destroy()

        self.root.geometry("400x450")
        self.root.title("Acceso - Restaurante")
        self.root.configure(bg="#F5F6FA") # Fondo claro

        # Contenedor central (Estilo Tarjeta)
        card = tk.Frame(root, bg="white", padx=40, pady=40, highlightbackground="#DCDDE1", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Icono y Título
        tk.Label(card, text="👤", font=("Arial", 50), bg="white", fg="#2F3640").pack()
        tk.Label(card, text="BIENVENIDO", font=("Segoe UI", 18, "bold"), bg="white", fg="#2F3640").pack(pady=(10, 30))

        # Campos de entrada
        tk.Label(card, text="USUARIO", font=("Segoe UI", 9, "bold"), bg="white", fg="#7F8C8D").pack(anchor="w")
        self.u = tk.Entry(card, font=("Segoe UI", 12), bd=0, bg="#F1F2F6", highlightthickness=1, highlightbackground="#DCDDE1")
        self.u.pack(fill="x", pady=(5, 15), ipady=5)
        self.u.insert(0, "admin")

        tk.Label(card, text="CONTRASEÑA", font=("Segoe UI", 9, "bold"), bg="white", fg="#7F8C8D").pack(anchor="w")
        self.p = tk.Entry(card, show="*", font=("Segoe UI", 12), bd=0, bg="#F1F2F6", highlightthickness=1, highlightbackground="#DCDDE1")
        self.p.pack(fill="x", pady=(5, 30), ipady=5)
        self.p.insert(0, "1234")

        # Botón estilizado
        btn = tk.Button(card, text="INGRESAR AL SISTEMA", bg="#27AE60", fg="white", font=("Segoe UI", 10, "bold"), 
                        bd=0, cursor="hand2", command=self.validar, activebackground="#219150", activeforeground="white")
        btn.pack(fill="x", ipady=10)

    def validar(self):
        res = ConexionBD().obtener_datos("SELECT nombre, rol FROM Usuarios WHERE username=? AND contrasena=?", (self.u.get(), self.p.get()))
        if res:
            self.al_exito(res[0][0], res[0][1])
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
