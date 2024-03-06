import json
import PruebaGPT
def cargar_resultados():
    try:
        with open("resultados.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def guardar_resultados(resultados):
    with open("resultados.json", "w") as file:
        json.dump(resultados, file, indent=4)

def cargar_preguntas():
    with open("preguntas.json", "r") as file:
        return json.load(file)

def cargar_respuestas():
    with open("respuestas.json", "r") as file:
        return json.load(file)

def verificar_respuestas():
    preguntas = cargar_preguntas()
    respuestas = cargar_respuestas()

    resultados = cargar_resultados()

    # Obtener el ID de la última pregunta verificada
    ultimo_id_verificado = resultados[-1]["id_pregunta"] if resultados else 0

    nuevos_resultados = []

    for pregunta in preguntas:

        if pregunta["id"] <= ultimo_id_verificado:
            continue

        pregunta_id = pregunta["id"]

        # Encontrar la respuesta correspondiente a la pregunta actual
        respuesta = next((r for r in respuestas if r["id_pregunta"] == pregunta_id), None)
        print(pregunta["pregunta"])
        print(respuesta["respuesta"])
        if PruebaGPT.corregir(pregunta["pregunta"], respuesta["respuesta"]):
            resultado = {
                    "id_pregunta": pregunta_id,
                    "id_respuesta": respuesta["id_respuesta"],
                    "resultado": "correcto"}
        else:
            resultado = {
                    "id_pregunta": pregunta_id,
                    "id_respuesta": respuesta["id_respuesta"],
                    "resultado": "incorrecto"}
        nuevos_resultados.append(resultado)    
    guardar_resultados(nuevos_resultados)
        