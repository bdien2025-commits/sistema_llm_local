import os
import datetime
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1", 
    api_key="ollama" 
)

def get_system_prompt(user_role):
    # Si el usuario es el admin, carga el prompt peligroso
    if user_role.lower() == "admin":
        ruta = "prompts/admin_unrestricted.txt"
        logging = False # El admin no espiamos
    else:
        # Cualquier otro nombre es alumno
        ruta = "prompts/student_education.txt"
        logging = True # Espiamos a los alumnos para enseñar ética
    
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read(), logging
    return "Eres un asistente.", False

def log_interaction(user_name, message):
    # Guardar en logs/historial_aula.txt
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] - Usuario: {user_name} | Intento: {message}\n"
    
    with open("logs/historial_aula.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

def chatear():
    print("--- SISTEMA DE LABORATORIO IA LOCAL ---")
    user_name = input("Ingresa tu nombre o ID (o 'admin' para profesor): ").strip()
    
    # Cargar el prompt correcto según el usuario
    system_prompt, must_log = get_system_prompt(user_name)
    
    if user_name.lower() == "admin":
        print(f"\n[!] MODO ADMINISTRADOR ACTIVADO. Restricciones desactivadas.")
    else:
        print(f"\n[?] Modo Alumno: {user_name}. Las interacciones serán registradas para fines educativos.")
        print(f"[!] Toda interacción será loggeada en logs/historial_aula.txt")

    print("-" * 40)

    while True:
        try:
            user_input = input(f"\n{user_name}: ")
            
            if user_input.lower() == "salir":
                print("Desconectando...")
                break

            # Si es alumno, guardamos su intento ANTES de enviarlo a la IA
            if must_log:
                log_interaction(user_name, user_input)

            print(f"IA ({user_name}): ", end="", flush=True)
            
            # Usamos el modelo Qwen 2.5 7B que acabamos de descargar
                        # ... código anterior ...
            print(f"IA ({user_name}): ", end="", flush=True)
            
            # CONFIGURACIÓN DE PARÁMETROS (Temperatura)
            if user_name.lower() == "admin":
                # Admin: Alta temperatura (0.7 - 1.0) para eludir filtros y ser creativo
                temp_val = 0.9
            else:
                # Alumno: Baja temperatura (0.1 - 0.3) para respuestas estables y educativas
                temp_val = 0.2

            response = client.chat.completions.create(
                model="qwen2.5:7b", 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                stream=True,
                temperature=temp_val  # Aplicamos la temperatura
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            print()
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            print() 

        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    chatear()
