import os
from dotenv import load_dotenv
from openai import OpenAI
import json

#cargar claves desde .env
load_dotenv()

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)


def cargar_preguntas():
    # Cargar preguntas existentes si el archivo ya existe
    if os.path.exists("preguntas.json"):
        with open("preguntas.json", "r") as file:
            return json.load(file)
    else:
        return []

# Función para guardar las preguntas en un archivo JSON
def guardar_pregunta_en_json(pregunta_id, pregunta, tipo, tema, dificultad):
    preguntas = cargar_preguntas()
    # Agregar nueva pregunta al archivo JSON
    nueva_pregunta = {
        "id": pregunta_id,
        "pregunta": pregunta,
        "tipo": tipo,
        "tema" : tema,
        "dificultad": dificultad
    }
    preguntas.append(nueva_pregunta)

    # Guardar preguntas en el archivo JSON
    with open("preguntas.json", "w") as file:
        json.dump(preguntas, file, indent=4)




def generar_pregunta(tipo_pregunta, tema_pregunta, dificultad_pregunta):
    
    preguntas_generadas = []

    tipos = {
        1: "respuesta corta",
        2: "test con 3 opciones",
        3: "verdadero o falso"
    }

    temas = {
        1: "cultura general",
        2: "codigo",
        3: "operaciones matemáticas numericas",
        4: "traducción linguistica",
        5: "definiciones de palabras",
    }

    dificultades = {
        1: "fácil",
        2: "media",
        3: "difícil"
    }

    if tipo_pregunta not in tipos:
        print("Tipo de pregunta no válido.")
        return
    
    if tema_pregunta not in temas:
        print("Tema de la pregunta no válido.")
        return
    
    if dificultad_pregunta not in dificultades:
        print("Dificultad de la pregunta no válido.")
        return
    
    tipo = tipos[tipo_pregunta]
    tema = temas[tema_pregunta]
    dificultad = dificultades[dificultad_pregunta]

    for _ in range(5):

        pregunta=f"Crea una pregunta de tipo {tipo} sobre {tema} con un nivel de dificultad {dificultad}, sin poner la solución"


        if tema_pregunta == 2:
            pregunta = f"Crea una pregunta de examen de tipo {tipo} sobre codigo (puede ser cualquier codigo no solo python), donde se proporciona un codigo en cualquier lenguaje con un nivel de dificultad {dificultad} y que pregunta que hace el codigo (no digas escribe el codigo si lo has puesto). No des ninguna pista de lo que hace"
            if tipo_pregunta == 3:
                pregunta= f"Crea una pregunta de examen de tipo {tipo} sobre codigo (puede ser cualquier codigo no solo python), donde se proporciona un codigo en cualquier lenguaje con un nivel de dificultad {dificultad}. No des ninguna pista de lo que hace. No preguntes que hace el codigo (esperando una respuesta redactada, ya que solo debe responder verdadero o falso). No des la solucion."

        elif tema_pregunta == 4:
            if tipo_pregunta == 1:
                pregunta= f"genera una pregunta de traduccion en un idioma al azar de una frase con un nivel de dificultad {dificultad}, sin poner la solución"
            elif tipo_pregunta == 3:
                pregunta = f"genera una pregunta de tipo verdadero o falso de traduccion en un idioma al azar de una frase con un nivel de dificultad {dificultad}, sin poner la solución"
            else:
                pregunta = f"genera una pregunta de traduccion de tipo test, con 3 opciones, en un idioma al azar de una frase con un nivel de dificultad {dificultad}, sin poner la solución"

        elif tema_pregunta == 3:
            if tipo_pregunta == 2:
                pregunta = pregunta + " Haz bien el calculo y pon la solucion en una de las tres opciones del test, para que siempre haya una opcion correcta."
            if tipo_pregunta == 3:
                pregunta = pregunta + ". Que la pregunta sea con operaciones matematicas. "
        elif tema_pregunta == 5:
            if tipo_pregunta == 2:
                pregunta = pregunta + " crea solo una pregunta"
            

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
            {"role": "system", "content": pregunta}
            ]
        )
        pregunta_generada = completion.choices[0].message.content

        if tipo_pregunta == 3:
            pregunta_generada = pregunta_generada + " Responder únicamente con Verdadero o Falso"         

        #preguntas = cargar_preguntas()
        # Guardar la pregunta generada en el archivo JSON`.`
        #pregunta_id = len(preguntas) + 1 if os.path.exists("preguntas.json") else 1
        #guardar_pregunta_en_json(pregunta_id, pregunta_generada, tipo, tema, dificultad)
        #print("Pregunta guardada exitosamente en el archivo JSON.")
        preguntas_generadas.append({
            "pregunta": pregunta_generada,
            "tipo": tipo,
            "tema": tema,
            "dificultad": dificultad
        })
        print(pregunta_generada)
        print("\n")

    return preguntas_generadas

def guardar_preguntas_generadas(preguntasGeneradas):
        preguntas = cargar_preguntas()
        # Guardar la pregunta generada en el archivo JSON`.`
        pregunta_id = len(preguntas) + 1 if os.path.exists("preguntas.json") else 1

        for pregunta in preguntasGeneradas:
            guardar_pregunta_en_json(pregunta_id, pregunta["pregunta"], pregunta["tipo"], pregunta["tema"], pregunta["dificultad"])
            print("Pregunta guardada exitosamente en el archivo JSON.")
            pregunta_id += 1

def corregir(pregunta, respuesta):
    #texto = f"Pregunta: {pregunta}\nRespuesta: {respuesta}\n¿La respuesta es correcta?"
    texto = f"Pregunta: {pregunta}\nRespuesta: {respuesta}\nRespuesta: (responder unicamente 'correcto' o 'incorrecto')"
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=[
      {"role": "system", "content": texto}
      ],
      #max_tokens=2,  # Limitamos la cantidad de tokens para restringir la respuesta.
      temperature=0
    )
    respuesta_gpt = response.choices[0].message.content
    print(respuesta_gpt)
    
    if "incorrecto" in respuesta_gpt.lower():
        print("si")
        return False
    else:
        return True
    
    







