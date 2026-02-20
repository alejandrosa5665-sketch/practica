import csv
from datetime import datetime

archivo = "transacciones.csv"

def registrar_transaccion(tipo, monto, descripcion):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(archivo, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([fecha, tipo, monto, descripcion])
    
    print("✅ Transacción registrada correctamente.")

def ver_transacciones():
    try:
        with open(archivo, mode='r') as file:
            reader = csv.reader(file)
            print("\n📋 Historial de transacciones:")
            for row in reader:
                print(f"Fecha: {row[0]} | Tipo: {row[1]} | Monto: {row[2]} | Descripción: {row[3]}")
    except FileNotFoundError:
        print("⚠ No hay transacciones registradas todavía.")

def menu():
    while True:
        print("\n--- CONTROL FINANCIERO ---")
        print("1. Registrar ingreso")
        print("2. Registrar gasto")
        print("3. Ver transacciones")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            monto = float(input("Ingrese el monto: "))
            descripcion = input("Descripción: ")
            registrar_transaccion("Ingreso", monto, descripcion)
        
        elif opcion == "2":
            monto = float(input("Ingrese el monto: "))
            descripcion = input("Descripción: ")
            registrar_transaccion("Gasto", monto, descripcion)
        
        elif opcion == "3":
            ver_transacciones()
        
        elif opcion == "4":
            print("👋 Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida.")

menu()