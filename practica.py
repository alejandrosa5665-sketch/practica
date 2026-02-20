import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import os

archivo = "transacciones.csv"

# Crear archivo si no existe
if not os.path.exists(archivo):
    with open(archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Tipo", "Monto", "Descripción"])

def registrar_transaccion(tipo, monto, descripcion):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(archivo, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([fecha, tipo, monto, descripcion])
    
    cargar_transacciones()
    actualizar_balance()

def cargar_transacciones():
    for item in tree.get_children():
        tree.delete(item)

    try:
        with open(archivo, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            for row in reader:
                tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass

def actualizar_balance():
    total = 0
    for row in tree.get_children():
        valores = tree.item(row)["values"]
        if valores[1] == "Ingreso":
            total += float(valores[2])
        else:
            total -= float(valores[2])

    label_balance.config(text=f"Balance: ${total:.2f}")

def boton_registrar():
    tipo = tipo_var.get()
    descripcion = entry_desc.get()

    try:
        monto = float(entry_monto.get())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un monto válido")
        return

    registrar_transaccion(tipo, monto, descripcion)

    entry_monto.delete(0, tk.END)
    entry_desc.delete(0, tk.END)

# ----------------- INTERFAZ -----------------

root = tk.Tk()
root.title("Control Financiero")
root.geometry("750x500")

tipo_var = tk.StringVar(value="Ingreso")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Tipo:").grid(row=0, column=0)

combo_tipo = ttk.Combobox(
    frame_top,
    textvariable=tipo_var,
    values=["Ingreso", "Gasto"],
    width=10,
    state="readonly"
)
combo_tipo.grid(row=0, column=1)

tk.Label(frame_top, text="Monto:").grid(row=0, column=2)
entry_monto = tk.Entry(frame_top)
entry_monto.grid(row=0, column=3)

tk.Label(frame_top, text="Descripción:").grid(row=0, column=4)
entry_desc = tk.Entry(frame_top)
entry_desc.grid(row=0, column=5)

# 🔥 Botón corregido (sin la barra \)
boton = tk.Button(frame_top, text="Registrar", command=boton_registrar)
boton.grid(row=0, column=6, padx=10)

# Tabla
columns = ("Fecha", "Tipo", "Monto", "Descripción")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=170)

tree.pack(pady=20, fill="both", expand=True)

# Balance
label_balance = tk.Label(root, text="Balance: $0.00", font=("Arial", 14))
label_balance.pack(pady=10)

# Cargar datos al iniciar
cargar_transacciones()
actualizar_balance()

root.mainloop()