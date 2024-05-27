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

    #ultimo id
    ultimo_id_verificado = resultados[-1]["id_pregunta"] if resultados else 0

    for pregunta in preguntas:

        if pregunta["id"] <= ultimo_id_verificado:
            continue

        pregunta_id = pregunta["id"]

        #unir id y pregunta
        respuesta = next((r for r in respuestas if r["id_pregunta"] == pregunta_id), None)
        print(pregunta["pregunta"])
        print(respuesta["respuesta"])
        #verificar pregunta
        if PruebaGPT.corregir(pregunta["pregunta"], respuesta["respuesta"]):
            resultado = {
                    "id_pregunta": pregunta_id,
                    "id_respuesta": respuesta["id_respuesta"],
                    "resultado": "correcto",
                    "revision":""
                    }
        else:
            resultado = {
                    "id_pregunta": pregunta_id,
                    "id_respuesta": respuesta["id_respuesta"],
                    "resultado": "incorrecto",
                    "revision":""
                    }
        resultados.append(resultado) 
    guardar_resultados(resultados)
        