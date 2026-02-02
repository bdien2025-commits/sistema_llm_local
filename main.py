import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Cargar variables de entorno (por si en el futuro usas claves)
load_dotenv()

# 2. Configuración del Cliente (Apuntando a futuro local)
# NOTA: Para ahora mismo funcionará, pero necesitas un modelo corriendo (ej: Ollama o LM Studio).
client = OpenAI(
    base_url="http://localhost:1234/v1", # URL estándar para servidores locales (LM Studio)
    api_key="no-es-necesario-por-el-momento"
)

# 3. Cargar el System Prompt Leak desde la carpeta
def get_system_prompt():
    ruta = os.path.join("prompts", "coding_assistant.txt")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Eres un asistente útil."

# 4. Función principal de chat
def chatear():
    system_prompt = get_system_prompt()
    print("--- Sistema LLM Local Iniciado ---")
    print(f"Prompt del sistema cargado: {system_prompt[:30]}...\n")

    # Simulación de petición (comentada para que no falle si no tienes servidor local aún)
    # user_input = input("Tú: ")
    # try:
    #     response = client.chat.completions.create(
    #         model="local-model", # Nombre del modelo en tu servidor local
    #         messages=[
    #             {"role": "system", "content": system_prompt},
    #             {"role": "user", "content": user_input}
    #         ]
    #     )
    #     print(f"IA: {response.choices[0].message.content}")
    # except Exception as e:
    #     print(f"Error: Asegúrate de tener tu servidor local corriendo. ({e})")
    
    print("Configuración lista. Próximo paso: Instalar Ollama o LM Studio.")

if __name__ == "__main__":
    chatear()
