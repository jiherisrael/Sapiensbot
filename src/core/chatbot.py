from openai import OpenAI
import gradio as gr
import os
import signal
import sys
from src.api.youtube import YouTubeAPI  # Importamos YouTubeAPI desde el archivo separado
from src.utils.translator import TranslatorAPI  # Importamos TranslatorAPI desde el archivo separado

# Inicializar el cliente OpenAI con tu clave de API
client = OpenAI(api_key="tu_api_key")  # Asegúrate de reemplazar "tu_api_key" con tu clave correcta

# Inicializar la clase YouTubeAPI con la clave de API de YouTube
youtube_client = YouTubeAPI(api_key="tu_api_key_youtube")  # Asegúrate de reemplazar "tu_api_key_youtube" con tu clave correctaCA

# Inicializar el traductor
translator_client = TranslatorAPI()

def chat_with_gpt_and_youtube(prompt, language='es'):
    try:
        # Crear la solicitud de chat completion
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.3
        )
        # Acceder al contenido del mensaje correctamente
        message_content = completion.choices[0].message.content

        # Buscar un video relacionado en YouTube usando la clase YouTubeAPI
        youtube_video_link = youtube_client.search_video(prompt)

        # Mensaje adicional para el usuario
        additional_message = "Below, I show you a video that may help you with your request if necessary."
        
        # Traducir el mensaje adicional al idioma del usuario
        translated_message = translator_client.translate_text(additional_message, language)

        # Combinar la respuesta del chatbot con el enlace al video de YouTube y el mensaje adicional traducido
        full_response = f"{message_content}\n\n{translated_message}\n\nVideo relacionado: {youtube_video_link}"
        return full_response
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

# Crear la interfaz Gradio personalizada usando gr.Blocks
def create_interface():
    with gr.Blocks() as demo:

        # Crear un dropdown para seleccionar el idioma
        language_selector = gr.Dropdown(
            label="Selecciona el idioma",
            choices=["es", "en", "fr", "de", "it", "pt", "zh-cn", "ja"],
            value="es",
            interactive=True
        )

        # Obtener las traducciones iniciales para la interfaz
        interface_elements = translator_client.translate_interface_elements(language_selector.value)

        # Crear componentes de la interfaz con los textos traducidos
        title = gr.Markdown(f"## {interface_elements['title']}")
        description = gr.Markdown(interface_elements["description"])

        user_input = gr.Textbox(
            label="",  # Eliminamos la etiqueta para dejarlo vacío
            placeholder=interface_elements["input_placeholder"],
            lines=6
        )
        submit_btn = gr.Button(interface_elements["button_text"], variant="primary")
        output_text = gr.Textbox(
            label="",  # Eliminamos la etiqueta para dejarlo vacío
            placeholder=interface_elements["output_placeholder"],
            lines=10
        )

        # Los ejemplos no se actualizarán dinámicamente, pero se mostrarán traducidos inicialmente
        gr.Examples(
            examples=["Photosynthesis", "Fernando Alonso F1", "World War II"],  # Ejemplos estáticos
            inputs=user_input,
            label=interface_elements["examples_label"]
        )

        # Función para actualizar la interfaz según el idioma seleccionado
        def update_interface(language):
            interface_elements = translator_client.translate_interface_elements(language)
            return (
                f"## {interface_elements['title']}",
                interface_elements["description"],
                interface_elements["input_placeholder"],
                interface_elements["output_placeholder"],
                interface_elements["button_text"]
            )

        # Actualizar la interfaz cuando se cambia el idioma, excepto los ejemplos
        language_selector.change(
            fn=update_interface,
            inputs=language_selector,
            outputs=[title, description, user_input, output_text, submit_btn]
        )

        # Llamar al chatbot con los datos de entrada
        def chatbot_interface(user_input, language):
            return chat_with_gpt_and_youtube(user_input, language)

        submit_btn.click(fn=chatbot_interface, inputs=[user_input, language_selector], outputs=output_text)

    return demo

# Registrar el manejador de señal para poder cerrar el servidor con CTRL + C
def signal_handler(sig, frame):
    print("Cerrando servidor...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Ejecutar la interfaz
if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
