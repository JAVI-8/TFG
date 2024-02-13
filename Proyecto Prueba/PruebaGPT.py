import os
from dotenv import load_dotenv
from openai import OpenAI

# Carga las variables de entorno del archivo .env
load_dotenv()

client = OpenAI(
   api_key=os.environ.get("OPENAI_API_KEY"),
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  messages=[
    {"role": "system", "content": "Crea una pregunta concreta de cultura general"}
  ]
)

print(completion.choices[0].message.content)
