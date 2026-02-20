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

def cargar_transacciones(filtro_tipo=None, fecha_inicio=None, fecha_fin=None):
    for item in tree.get_children():
        tree.delete(item)

    try:
        with open(archivo, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            for row in reader:
                fecha_row, tipo_row, monto_row, desc_row = row
                # Filtrado por tipo
                if filtro_tipo and tipo_row != filtro_tipo:
                    continue
                # Filtrado por fecha
                if fecha_inicio and fecha_fin:
                    if not (fecha_inicio <= fecha_row <= fecha_fin):
                        continue
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

def aplicar_filtros():
    filtro_tipo = filtro_tipo_var.get()
    inicio = entry_fecha_inicio.get()
    fin = entry_fecha_fin.get()
    fecha_inicio = inicio + " 00:00:00" if inicio else None
    fecha_fin = fin + " 23:59:59" if fin else None

    if (inicio and not fin) or (fin and not inicio):
        messagebox.showwarning("Advertencia", "Debe ingresar ambas fechas para filtrar por rango")
        return

    cargar_transacciones(
        filtro_tipo=filtro_tipo if filtro_tipo != "Todos" else None,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    actualizar_balance()

def limpiar_filtros():
    filtro_tipo_var.set("Todos")
    entry_fecha_inicio.delete(0, tk.END)
    entry_fecha_fin.delete(0, tk.END)
    cargar_transacciones()
    actualizar_balance()

# ----------------- INTERFAZ -----------------

root = tk.Tk()
root.title("Control Financiero")
root.geometry("850x550")

# Variables
tipo_var = tk.StringVar(value="Ingreso")
filtro_tipo_var = tk.StringVar(value="Todos")

# Frame superior: Registro
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Tipo:").grid(row=0, column=0)
combo_tipo = ttk.Combobox(
    frame_top, textvariable=tipo_var,
    values=["Ingreso", "Gasto"], width=10, state="readonly"
)
combo_tipo.grid(row=0, column=1)

tk.Label(frame_top, text="Monto:").grid(row=0, column=2)
entry_monto = tk.Entry(frame_top)
entry_monto.grid(row=0, column=3)

tk.Label(frame_top, text="Descripción:").grid(row=0, column=4)
entry_desc = tk.Entry(frame_top)
entry_desc.grid(row=0, column=5)

boton = tk.Button(frame_top, text="Registrar", command=boton_registrar)
boton.grid(row=0, column=6, padx=10)

# Frame filtros
frame_filtros = tk.Frame(root)
frame_filtros.pack(pady=10)

tk.Label(frame_filtros, text="Filtrar por tipo:").grid(row=0, column=0)
combo_filtro_tipo = ttk.Combobox(
    frame_filtros, textvariable=filtro_tipo_var,
    values=["Todos", "Ingreso", "Gasto"], width=10, state="readonly"
)
combo_filtro_tipo.grid(row=0, column=1)

tk.Label(frame_filtros, text="Fecha inicio (YYYY-MM-DD):").grid(row=0, column=2)
entry_fecha_inicio = tk.Entry(frame_filtros, width=12)
entry_fecha_inicio.grid(row=0, column=3)

tk.Label(frame_filtros, text="Fecha fin (YYYY-MM-DD):").grid(row=0, column=4)
entry_fecha_fin = tk.Entry(frame_filtros, width=12)
entry_fecha_fin.grid(row=0, column=5)

boton_filtrar = tk.Button(frame_filtros, text="Aplicar filtros", command=aplicar_filtros)
boton_filtrar.grid(row=0, column=6, padx=5)

boton_limpiar = tk.Button(frame_filtros, text="Limpiar filtros", command=limpiar_filtros)
boton_limpiar.grid(row=0, column=7, padx=5)

# Tabla
columns = ("Fecha", "Tipo", "Monto", "Descripción")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)
tree.pack(pady=20, fill="both", expand=True)

# Balance
label_balance = tk.Label(root, text="Balance: $0.00", font=("Arial", 14))
label_balance.pack(pady=10)

# Cargar datos al iniciar
cargar_transacciones()
actualizar_balance()

root.mainloop()