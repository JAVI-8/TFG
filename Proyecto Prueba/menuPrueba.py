import time
import tkinter as tk
from tkinter import Scrollbar, Text, Toplevel, ttk, messagebox
import estadisticas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PruebaGPT
import PruebaCohere
import resultados
import json
import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y, END
from tkinter import ttk

class App:
    def __init__(self, master):

        self.hora_inicio = time.time()
        self.master = master
        self.master.title("Interfaz")
        self.master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth() - 10, master.winfo_screenheight()))

        # Crear el menú en la esquina
        self.menu_frame = tk.Frame(master, bg="white", width=200, height=600)
        self.menu_frame.grid(row=0, column=0, sticky="ns")

        # Crear los botones del menú con más margen
        button_texts = ["Generador de preguntas", "Visualización de estadísticas"]
        self.buttons = []
        for i, text in enumerate(button_texts):
            button = tk.Button(self.menu_frame, text=text, padx=10, pady=5, bg="white", relief="flat", borderwidth=1)
            button.grid(row=i, column=0, sticky="ew", padx=20, pady=(10, 0))
            button.bind("<Enter>", self.change_color)
            button.bind("<Leave>", self.restore_color)
            button.bind("<Button-1>", lambda e, btn=button: self.show_content(btn))
            self.buttons.append(button)

        # Crear el área central para mostrar contenido con barra de desplazamiento
        self.content_frame = tk.Frame(master, bg="lightgray")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.canvas = tk.Canvas(self.content_frame, bg="lightgray")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollable_frame = tk.Frame(self.canvas, bg="lightgray")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.stat_buttons = None

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def change_color(self, event):
        event.widget.config(bg="lightgray")

    def restore_color(self, event):
        event.widget.config(bg="white")

    def change_colorStat(self, event):
        event.widget.config(bg="lightgray")

    def restore_colorStat(self, event):
        event.widget.config(bg="lightblue")

    def show_content(self, button):
        if button["text"] == "Generador de preguntas":
            self.mostrar_generador()
        elif button["text"] == "Visualización de estadísticas":
            if not self.stat_buttons:
                self.create_stat_buttons()
            else:
                self.toggle_stat_buttons()

    def mostrar_generador(self):
        # Ocultar los botones principales y mostrar el formulario cuando se selecciona "Generar pregunta"
        self.hora_inicio = time.time()
        try:
            with open('hora.txt', 'r') as f:
                ultima_hora = float(f.read())
        except FileNotFoundError:
            ultima_hora = 0

        if ultima_hora == 0 or self.hora_inicio - ultima_hora > 60:
            self.clear_content_frame()

            self.generator_frame = tk.Frame(self.scrollable_frame, bg="white")
            self.generator_frame.pack(fill="both", expand=True)

            # Crear el generador de preguntas
            self.generator = AppGenerador(self.generator_frame)
        else:
            messagebox.showerror("Error", "Por favor, espere un minuto antes de volver a intentarlo")
            return

    def clear_content_frame(self):
        self.hora_inicio = time.time()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def create_stat_buttons(self):
        self.stat_buttons = tk.Frame(self.menu_frame, bg="white")
        self.stat_buttons.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 0))

        r = estadisticas.cargar()
        categories = ["cultura general", "operaciones matemáticas numericas",
                      "traducción linguistica", "codigo", "logica con trampa, para adivinar", "definiciones de palabras"]

        for i, category in enumerate(categories):
            button = tk.Button(self.stat_buttons, text=category, padx=10, pady=5, bg="lightblue", fg="black", relief="flat", borderwidth=1, anchor="w")
            button.grid(row=i, column=0, sticky="ew", padx=20, pady=5)
            button.bind("<Enter>", self.change_colorStat)
            button.bind("<Leave>", self.restore_colorStat)
            button.bind("<Button-1>", lambda e, cat=category: self.show_statistics(cat))
        self.toggle_stat_buttons()

    def toggle_stat_buttons(self):
        if self.stat_buttons.winfo_ismapped():
            self.stat_buttons.grid_forget()
        else:
            self.stat_buttons.grid()

    def show_statistics(self, category):
        r = estadisticas.cargar()
        fig = estadisticas.resultados_categorias(r, category)

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        fig.set_figwidth(13)

        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


class AppGenerador:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="lightgray")

        self.tipo_var = tk.StringVar()
        self.tema_var = tk.StringVar()
        self.dificultad_var = tk.StringVar()

        self.opciones_tipo = {"Tipo respuesta corta": 1, "Tipo test con 3 opciones": 2, "Verdadero o falso": 3}
        self.opciones_tema = {"Cultura general": 1, "Codigo": 2, "Operaciones matematicas": 3, "Traducción": 4, "Definiciones de palabras": 5, "Preguntas lógicas":6}
        self.opciones_dificultad = {"Fácil": 1, "Medio": 2, "Difícil": 3}

        self.form_frame = tk.Frame(self.master, bg="lightgray", width=800, height=500)
        self.form_frame.pack_propagate(False)  # No dejar que el frame se ajuste automáticamente al tamaño de sus widgets
        self.form_frame.pack(pady=200, padx = 350)

        self.formulario()

    def formulario(self):
        # Etiqueta del título
        self.title_label = tk.Label(self.form_frame, text="Generar pregunta", bg="lightgray", font=("Helvetica", 40, "bold"))
        self.title_label.pack(anchor="w", padx=100, pady=(0, 15))

        # Etiqueta y menú de selección para el tipo de pregunta
        self.tipo_label = tk.Label(self.form_frame, text="Tipo de pregunta:", bg="lightgray", font=("Helvetica", 14))
        self.tipo_label.pack(anchor="w", padx=250, pady=(0, 5))

        # Variable de control para el tipo de pregunta
        self.tipo_var = tk.StringVar(self.form_frame)

        # Establecer la primera opción como predeterminada para el tipo de pregunta
        first_tipo_option = list(self.opciones_tipo.keys())[0]
        self.tipo_var.set(first_tipo_option)

        self.tipo_option_menu = ttk.OptionMenu(self.form_frame, self.tipo_var, first_tipo_option, *self.opciones_tipo.keys())
        self.tipo_option_menu.pack(anchor="w", padx=250, pady=(0, 5))

        # Etiqueta y menú de selección para el tema de la pregunta
        self.tema_label = tk.Label(self.form_frame, text="Tema de la pregunta:", bg="lightgray", font=("Helvetica", 14))
        self.tema_label.pack(anchor="w", padx=250, pady=(50, 5))

        # Variable de control para el tema de la pregunta
        self.tema_var = tk.StringVar(self.form_frame)

        # Establecer la primera opción como predeterminada para el tema de la pregunta
        first_tema_option = list(self.opciones_tema.keys())[0]
        self.tema_var.set(first_tema_option)

        self.tema_option_menu = ttk.OptionMenu(self.form_frame, self.tema_var, first_tema_option, *self.opciones_tema.keys())
        self.tema_option_menu.pack(anchor="w", padx=250, pady=(0, 5))

        # Etiqueta y menú de selección para la dificultad
        self.dificultad_label = tk.Label(self.form_frame, text="Dificultad:", bg="lightgray", font=("Helvetica", 14))
        self.dificultad_label.pack(anchor="w", padx=250, pady=(50, 5))

        # Variable de control para la dificultad
        self.dificultad_var = tk.StringVar(self.form_frame)

        # Establecer la primera opción como predeterminada para la dificultad
        first_dificultad_option = list(self.opciones_dificultad.keys())[0]
        self.dificultad_var.set(first_dificultad_option)

        self.dificultad_option_menu = ttk.OptionMenu(self.form_frame, self.dificultad_var, first_dificultad_option, *self.opciones_dificultad.keys())
        self.dificultad_option_menu.pack(anchor="w", padx=250, pady=(0, 5))

        style = ttk.Style()
        style.configure("Large.TButton", font=("Helvetica", 14))

        # Botón para generar la pregunta
        self.generate_button = ttk.Button(self.form_frame, text="Generar Pregunta", command=self.generar_pregunta, style="Large.TButton")
        self.generate_button.pack(anchor="w", padx=250, pady=(60, 10))


    def generar_pregunta(self):
        tipo = self.tipo_var.get()
        tema = self.tema_var.get()
        dificultad = self.dificultad_var.get()

        if tipo == "" or tema == "" or dificultad == "":
            messagebox.showerror("Error", "Por favor, seleccione todas las opciones.")
            return

        tipo_int = self.opciones_tipo[tipo]
        tema_int = self.opciones_tema[tema]
        dificultad_int = self.opciones_dificultad[dificultad]

        
        preguntas_generadas = PruebaGPT.generar_pregunta(tipo_int, tema_int, dificultad_int)

        self.mostrar_preguntasPreview(preguntas_generadas)

        #PruebaCohere.responder_preguntas()
        #resultados.verificar_respuestas()

        #messagebox.showinfo("Generación completada", "Preguntas generadas y respondidas exitosamente.")
        #self.mostrar_preguntas()

    def mostrar_preguntasPreview(self, preguntas_generadas):
        self.preguntas_window = Toplevel(self.master)
        self.preguntas_window.title("Preguntas Generadas")

        # Mostrar cada pregunta generada con botones de eliminar y modificar
        for pregunta in preguntas_generadas:
            pregunta_frame = tk.Frame(self.preguntas_window, bg="white", padx=20, pady=10)
            pregunta_frame.pack(pady=10, padx=10, fill="both", expand=True)

            # Obtener solo el texto de la pregunta
            pregunta_texto = pregunta['pregunta']

            # Etiqueta de la pregunta
            pregunta_label = tk.Label(pregunta_frame, text=pregunta_texto, bg="white", font=("Helvetica", 12))
            pregunta_label.pack(side="top", fill="both", expand=True)

            # Frame para contener los botones de eliminar y modificar
            botones_frame = tk.Frame(pregunta_frame, bg="white")
            botones_frame.pack(side="bottom", pady=5)

            # Botones de eliminar y modificar centrados
            eliminar_button = tk.Button(botones_frame, text="Eliminar", command=lambda p=pregunta: self.eliminar_pregunta(p))
            eliminar_button.pack(side="left", padx=5)

            modificar_button = tk.Button(botones_frame, text="Modificar", command=lambda p=pregunta: self.modificar_pregunta(p))
            modificar_button.pack(side="left", padx=5)

        # Botón de aceptar para enviar las preguntas a la corrección de Cohere
        aceptar_button = tk.Button(self.preguntas_window, text="Aceptar", command=self.enviar_a_cohere)
        aceptar_button.pack(pady=10)

    def enviar_a_cohere(self):
        # Método vacío para evitar el error
        pass

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


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()