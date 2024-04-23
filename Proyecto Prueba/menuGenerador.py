import json
import os
import PruebaGPT
import PruebaCohere
import resultados
import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y, END
from tkinter import ttk
import time

class App:
    def __init__(self, master):

        self.hora_inicio = time.time()

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
        self.hora_inicio = time.time()
        try:
            with open('hora.txt', 'r') as f:
                ultima_hora = float(f.read())
        except FileNotFoundError:
            ultima_hora = 0

        if ultima_hora == 0 or self.hora_inicio - ultima_hora > 60:
            self.buttons_frame.pack_forget()
            self.form_frame.pack()
        else:
            messagebox.showerror("Error", "Por favor, espere un minuto antes de volver a intentarlo")
            return

    def ocultar_formulario(self):
        # Mostrar los botones principales y ocultar el formulario cuando se selecciona "Volver"
        self.form_frame.pack_forget()
        self.buttons_frame.pack(pady=50)
        self.hora_inicio = time.time()

    def generar_pregunta(self):
        # Crear ventana para mostrar el mensaje de espera
        wait_window = tk.Toplevel()
        wait_window.title("Generando, respondiendo y corrigiendo")

        wait_label = tk.Label(wait_window, text="Espera unos segundos mientras serealiza el proceso...")
        wait_label.pack(padx=20, pady=20)

        # Forzar la actualización de la interfaz gráfica para mostrar el mensaje
        wait_window.update()

        # guardar horas.txt
        with open('hora.txt', 'w') as f:
            f.write(str(time.time()))

        tipo = self.tipo_var.get()
        tema = self.tema_var.get()
        dificultad = self.dificultad_var.get()

        if tipo == "" or tema == "" or dificultad == "":
            messagebox.showerror("Error", "Por favor, seleccione todas las opciones.")
            return

        tipo_int = self.opciones_tipo[tipo]
        tema_int = self.opciones_tema[tema]
        dificultad_int = self.opciones_dificultad[dificultad]

        print(f"Generando pregunta de tipo {tipo}, tema {tema}, dificultad {dificultad}")
        for _ in range(5):
            PruebaGPT.generar_pregunta(tipo_int, tema_int, dificultad_int)

        PruebaCohere.responder_preguntas()
        resultados.verificar_respuestas()

        wait_window.destroy()

        self.ocultar_formulario()
        self.mostrar_preguntas()


    def mostrar_preguntas(self):
        # Create a new window
        resultadosVentana = Toplevel(self.master)
        resultadosVentana.title("Resumen de las preguntas generadas")

        texto = Text(resultadosVentana, wrap='word')  # wrap='word' will wrap text at word boundaries
        scrollbar = Scrollbar(resultadosVentana, command=texto.yview)
        texto.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        texto.pack(fill='both', expand=True)

        with open("preguntas.json", 'r') as f:
            preguntas = json.load(f)[-5:]  # Obtener las últimas 5 preguntas

        with open("respuestas.json", 'r') as f:
            respuestas = json.load(f)[-5:]  # Obtener las últimas 5 respuestas

        with open("resultados.json", 'r') as f:
            resultados = json.load(f)[-5:]  # Obtener los últimos 5 resultados

        # Mostrar preguntas, respuestas y resultados
        for pregunta, respuesta, resultado in zip(preguntas, respuestas, resultados):
            texto.insert(END, "Pregunta: {}\n".format(pregunta['pregunta']))
            texto.insert(END, "Respuesta: {}\n".format(respuesta['respuesta']))
            texto.insert(END, "Resultado: {}\n\n".format(resultado['resultado']))            

            texto.insert(END, "\n\n")

        # Scroll back to the top
        texto.yview_moveto(0)
        resultadosVentana.mainloop()

    def ver_estadisticas(self):
        print("")

def main():
   
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()