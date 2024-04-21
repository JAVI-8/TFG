import os
import sys
import PruebaGPT
import PruebaCohere
from tkinter import Menu
import resultados
import tkinter as tk

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Creación de Preguntas")
        self.master.geometry("500x400")

        # Configurar el menú principal
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Menú para crear preguntas
        self.menu_preguntas = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Crear Pregunta", menu=self.menu_preguntas)
        self.menu_bar.add_command(label="Generar respuesta a las preguntas", command=PruebaCohere.responder_preguntas)
        self.menu_bar.add_command(label="Corregir las respuestas", command=resultados.verificar_respuestas)
        self.menu_bar.add_command(label="Salir", command=lambda: master.destroy)
        # Submenú para seleccionar el tipo de pregunta
        self.menu_tipo = Menu(self.menu_preguntas, tearoff=0)
        self.menu_preguntas.add_cascade(label="Seleccionar Tipo", menu=self.menu_tipo)

        # Opciones de tipo de pregunta
        self.menu_tipo.add_command(label="Tipo respuesta corta", command=lambda: self.seleccionar_tema(1))
        self.menu_tipo.add_command(label="Tipo test con 3 opciones", command=lambda: self.seleccionar_tema(2))
        self.menu_tipo.add_command(label="Verdadero o falso", command=lambda: self.seleccionar_tema(3))

    def seleccionar_tema(self, tipo):
        self.menu_tema = Menu(self.menu_bar, tearoff=0)
        self.master.config(menu=self.menu_tema)

        self.menu_tema.add_command(label="Cultura general", command=lambda: self.seleccionar_dificultad(tipo, 1))
        self.menu_tema.add_command(label="Codigo", command=lambda: self.seleccionar_dificultad(tipo, 2))
        self.menu_tema.add_command(label="Operaciones matematicas", command=lambda: self.seleccionar_dificultad(tipo, 3))
        self.menu_tema.add_command(label="Traducción", command=lambda: self.seleccionar_dificultad(tipo, 4))
        self.menu_tema.add_command(label="Definiciones de palabras", command=lambda: self.seleccionar_dificultad(tipo, 5))

        self.menu_tema.add_command(label="Volver", command=lambda: self.volver_a_tipo())

    def seleccionar_dificultad(self, tipo, tema):
        self.menu_dificultad = Menu(self.menu_bar, tearoff=0)
        self.master.config(menu=self.menu_dificultad)

        self.menu_dificultad.add_command(label="Fácil", command=lambda: self.finalizar_pregunta(tipo, tema, 1))
        self.menu_dificultad.add_command(label="Medio", command=lambda: self.finalizar_pregunta(tipo, tema, 2))
        self.menu_dificultad.add_command(label="Difícil", command=lambda: self.finalizar_pregunta(tipo, tema, 3))

        self.menu_dificultad.add_command(label="Volver", command=lambda: self.seleccionar_tema(tipo))

    def finalizar_pregunta(self, tipo, tema, dificultad):
        PruebaGPT.generar_pregunta(int(tipo),int(tema), int(dificultad))
        self.volver_a_tipo()

    def volver_a_tipo(self):
        self.master.config(menu=self.menu_bar)


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

def mostrar_submenuDificultad():
    print("Seleccione la dificultad de la pregunta:")
    print("1. Fácil")
    print("2. Medio")
    print("3. Difícil")



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
           mostrar_submenuDificultad()
           opcion_subDificultad = input("Seleccione el número: ")
           print("\n")
           PruebaGPT.generar_pregunta(int(opcion_subTipo),int(opcion_subTema), int(opcion_subDificultad))
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
    root = tk.Tk()
    app = App(root)
    root.mainloop()