import os
import cohere
from dotenv import load_dotenv
import json

# Carga las variables de entorno del archivo .env
load_dotenv()

def cargar_preguntas():
    if os.path.exists("preguntas.json"):
        with open("preguntas.json", "r") as file:
            return json.load(file)
    else:
        return []
    
def cargar_respuestas():
    if os.path.exists("respuestas.json"):
        with open("respuestas.json", "r") as file:
            return json.load(file)
    else:
        return []

    
def guardar_respuestas(respuestas):
    with open("respuestas.json", "w") as file:
        json.dump(respuestas, file, indent=4)


def responder_preguntas():
    co = cohere.Client(
        api_key=os.environ.get("COHERE_API_KEY"),
        )
    preguntas = cargar_preguntas()
    respuestas = cargar_respuestas()
    indice_inicio = len(respuestas)  # Último índice de respuesta


    for pregunta in preguntas[indice_inicio:]:
        prompt = "respuesta muy directa y corta " + pregunta['pregunta']
        response = co.generate(
                prompt=prompt,
                temperature=0.0,
                num_generations=1,
                end_sequences=["."],
            )
        respuesta_generada = response[0].text
        respuestas.append({
                "id_respuesta": len(respuestas) + 1,
                "respuesta": respuesta_generada,
                "id_pregunta": pregunta["id"]
            })
    guardar_respuestas(respuestas)

    #solo muestra la ultima respuesta
    print(respuesta_generada)




