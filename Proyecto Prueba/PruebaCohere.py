import os
import cohere
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

co = cohere.Client(
    api_key=os.environ.get("COHERE_API_KEY"),
)

response = co.generate(
  prompt='Respuesta muy corta ¿Cómo se llama el actual rey de España?',
  temperature = 0.0,
  num_generations=1,
)

print(response)