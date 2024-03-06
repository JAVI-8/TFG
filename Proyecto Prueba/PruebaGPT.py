import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Carga las variables de entorno del archivo .env
load_dotenv()

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
   #api_key = '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',
)


def cargar_preguntas():
    # Cargar preguntas existentes si el archivo ya existe
    if os.path.exists("preguntas.json"):
        with open("preguntas.json", "r") as file:
            return json.load(file)
    else:
        return []

# Función para guardar las preguntas en un archivo JSON
def guardar_pregunta_en_json(pregunta_id, pregunta, tipo):
    preguntas = cargar_preguntas()
    # Agregar nueva pregunta al archivo JSON
    nueva_pregunta = {
        "id": pregunta_id,
        "pregunta": pregunta,
        "tipo": tipo
    }
    preguntas.append(nueva_pregunta)

    # Guardar preguntas en el archivo JSON
    with open("preguntas.json", "w") as file:
        json.dump(preguntas, file, indent=4)




def generar_pregunta(tipo_pregunta):
    
    tipos = {
        1: "cultura general",
        2: "tipo test con 3 opciones",
        3: "tipo lógica",
        4: "verdadero o falso"
    }

    if tipo_pregunta not in tipos:
        print("Tipo de pregunta no válido.")
        return
    
    tipo = tipos[tipo_pregunta]

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=[
      {"role": "system", "content": f"Crea una pregunta de {tipo}"}
      ]
    )
    pregunta_generada = completion.choices[0].message.content
    preguntas = cargar_preguntas()
    # Guardar la pregunta generada en el archivo JSON`.`
    pregunta_id = len(preguntas) + 1 if os.path.exists("preguntas.json") else 1
    guardar_pregunta_en_json(pregunta_id, pregunta_generada, "cultura general")
    print("Pregunta guardada exitosamente en el archivo JSON.")
    print(completion.choices[0].message.content)


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
    
    







