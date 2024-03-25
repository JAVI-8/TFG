import os
import sys
import PruebaGPT
import PruebaCohere
import resultados

def mostrar_menu():
    print("Menú:")
    print("1. Generar pregunta")
    print("2. Generar respuesta a las preguntas")
    print("3. Corregir las respuestas")
    print("4. Salir")

def mostrar_submenuTipo():
    print("Seleccione el tipo de pregunta:")
    print("1. Tipo respuesta corta")
    print("2. Tipo test con 3 opciones")
    print("3. Verdadero o falso")

def mostrar_submenuTema():
    print("Seleccione el tema de la pregunta:")
    print("1. Cultura general")
    print("2. Codigo")
    print("3. Operaciones matematicas")
    print("4. Traducción")
    print("5. Definiciones de palabras")



def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        print("\n")

        if opcion == "1":
            # Llamar a la función para generar pregunta de cultura general (desde pruebaGPT)
           mostrar_submenuTipo()
           opcion_subTipo = input("Seleccione el número: ")
           print("\n")
           mostrar_submenuTema()
           opcion_subTema = input("Seleccione el número: ")
           print("\n")
           PruebaGPT.generar_pregunta(int(opcion_subTipo),int(opcion_subTema))
        elif opcion == "2":
            PruebaCohere.responder_preguntas()
        elif opcion == "3":
            resultados.verificar_respuestas()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()