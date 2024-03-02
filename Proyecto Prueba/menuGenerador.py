import os
import sys
import PruebaGPT

def mostrar_menu():
    print("Menú:")
    print("1. Generar pregunta")
    print("2. Generar respuesta a las preguntas")
    print("3. Salir")

def mostrar_submenu():
    print("Seleccione el tipo de pregunta:")
    print("1. Cultura general")
    print("2. Tipo test")
    print("3. Preguntas lógicas")
    print("4. Verdadero o falso")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Llamar a la función para generar pregunta de cultura general (desde pruebaGPT)
           mostrar_submenu()
           opcion_sub = input("Seleccione el tipo de pregunta: ")
           PruebaGPT.generar_pregunta(int(opcion_sub))
        elif opcion == "2":
            # Llamar a la función para generar otro tipo de pregunta
            print("Aún no implementado")
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()