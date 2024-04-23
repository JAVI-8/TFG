import os
import sys
import PruebaGPT
import PruebaCohere
from tkinter import Menu
import resultados
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Creación de Preguntas")
        self.master.geometry("400x400")  # Cambiar el tamaño de la ventana

        # Configuración de estilos
        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=("Helvetica", 12))
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", font=("Helvetica", 14))

        # Contenedor principal
        self.container = ttk.Frame(self.master)
        self.container.pack(fill="both", expand=True)

        # Frame para los botones principales
        self.buttons_frame = ttk.Frame(self.container)
        self.buttons_frame.pack(pady=50)  # Ajustar el relleno vertical para centrar los botones

        # Botones principales
        self.generate_button = ttk.Button(self.buttons_frame, text="Generar pregunta", command=self.mostrar_formulario)
        self.generate_button.pack(fill="x", pady=5)

        self.response_button = ttk.Button(self.buttons_frame, text="Ver estadisticas", command=self.ver_estadisticas)
        self.response_button.pack(fill="x", pady=5)

        self.exit_button = ttk.Button(self.buttons_frame, text="Salir", command=self.master.destroy)
        self.exit_button.pack(fill="x", pady=5)

        # Frame para el formulario
        self.form_frame = ttk.Frame(self.container)

        # Variables para opciones seleccionadas
        self.tipo_var = tk.StringVar()
        self.tema_var = tk.StringVar()
        self.dificultad_var = tk.StringVar()

        self.opciones_tipo = {"Tipo respuesta corta": 1, "Tipo test con 3 opciones": 2, "Verdadero o falso": 3}
        self.opciones_tema = {"Cultura general": 1, "Codigo": 2, "Operaciones matematicas": 3, "Traducción": 4, "Definiciones de palabras": 5}
        self.opciones_dificultad = {"Fácil": 1, "Medio": 2, "Difícil": 3}

        self.interaction_times = []  # Lista para almacenar los tiempos de interacción
        self.generate_button_state = "enabled"  # Estado inicial del botón "Aceptar"

        self.formulario()

    def formulario(self):
        # Etiqueta de título
        self.title_label = ttk.Label(self.form_frame, text="Crear Pregunta")
        self.title_label.pack(pady=10)

        # Selector de tipo de pregunta
        self.tipo_label = ttk.Label(self.form_frame, text="Tipo de pregunta:")
        self.tipo_label.pack(anchor="w", padx=10)

        self.tipo_option_menu = ttk.OptionMenu(self.form_frame, self.tipo_var, "", "Tipo respuesta corta", "Tipo test con 3 opciones", "Verdadero o falso")
        self.tipo_option_menu.pack(pady=5, padx=10)

        # Selector de tema
        self.tema_label = ttk.Label(self.form_frame, text="Tema de la pregunta:")
        self.tema_label.pack(anchor="w", padx=10)

        self.tema_option_menu = ttk.OptionMenu(self.form_frame, self.tema_var, "", "Cultura general", "Codigo", "Operaciones matematicas", "Traducción", "Definiciones de palabras")
        self.tema_option_menu.pack(pady=5, padx=10)

        # Selector de dificultad
        self.dificultad_label = ttk.Label(self.form_frame, text="Dificultad:")
        self.dificultad_label.pack(anchor="w", padx=10)

        self.dificultad_option_menu = ttk.OptionMenu(self.form_frame, self.dificultad_var, "", "Fácil", "Medio", "Difícil")
        self.dificultad_option_menu.pack(pady=5, padx=10)

        # Selector de cantidad de preguntas
        self.cantidad_label = ttk.Label(self.form_frame, text="Cantidad de preguntas:")
        self.cantidad_label.pack(anchor="w", padx=10)

        self.cantidad_var = tk.StringVar()
        self.cantidad_var.set("1")  # Establecer valor inicial en 1

        self.cantidad_option_menu = ttk.OptionMenu(self.form_frame, self.cantidad_var, "1", "1", "2", "3", "4", "5")
        self.cantidad_option_menu.pack(pady=5, padx=10)

        # Botón para generar pregunta
        self.generate_button = ttk.Button(self.form_frame, text="Aceptar", command=self.generar_pregunta)
        self.generate_button.pack(pady=10)

        # Botón para volver
        self.back_button = ttk.Button(self.form_frame, text="Volver", command=self.ocultar_formulario)
        self.back_button.pack(pady=10)

        # Ocultar el formulario al inicio
        self.form_frame.pack_forget()

    def mostrar_formulario(self):
        # Ocultar los botones principales y mostrar el formulario cuando se selecciona "Generar pregunta"
        self.buttons_frame.pack_forget()
        self.form_frame.pack()

    def ocultar_formulario(self):
        # Mostrar los botones principales y ocultar el formulario cuando se selecciona "Volver"
        self.form_frame.pack_forget()
        self.buttons_frame.pack(pady=50)

    def generar_pregunta(self):
        tipo = self.tipo_var.get()
        tema = self.tema_var.get()
        dificultad = self.dificultad_var.get()
        cantidad = self.cantidad_var.get()
        # Obtén el tiempo actual
        current_time = time.time()

        # Agrega el tiempo actual a la lista de tiempos de interacción
        self.interaction_times.append(current_time)

        # Elimina los tiempos que ocurrieron hace más de un minuto
        self.interaction_times = [t for t in self.interaction_times if current_time - t <= 60]

        # Verifica si se ha excedido el límite de interacciones en el último minuto
        if len(self.interaction_times) > 5:
            self.generate_button.config(state="disabled")  # Deshabilita el botón "Aceptar"
            messagebox.showerror("Error", "Se ha excedido el límite de interacciones por minuto.")
            return
        
         # Restaura el botón "Aceptar" si no se ha excedido el límite de interacciones
        self.generate_button.config(state="enabled")


        if tipo == "" or tema == "" or dificultad == "":
            messagebox.showerror("Error", "Por favor, seleccione todas las opciones.")
            return

        tipo_int = self.opciones_tipo[tipo]
        tema_int = self.opciones_tema[tema]
        dificultad_int = self.opciones_dificultad[dificultad]
        cantidad_int = int(cantidad)

        print(f"Generando pregunta de tipo {tipo}, tema {tema}, dificultad {dificultad}")
        for _ in range(cantidad_int):
            PruebaGPT.generar_pregunta(tipo_int, tema_int, dificultad_int)

        PruebaCohere.responder_preguntas()
        resultados.verificar_respuestas()

    def ver_estadisticas(self):
        print("")

def main():
   
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()