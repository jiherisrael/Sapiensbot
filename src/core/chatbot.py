from openai import OpenAI
import gradio as gr
import os
import signal
import sys
import re  # Para extraer el ID del video de YouTube
from src.api.youtube import YouTubeAPI
from src.utils.translator import TranslatorAPI
from src.utils.content_exporter import ContentExporter

# Inicializar el cliente OpenAI con tu clave de API
client = OpenAI(api_key="tu_api_key")

# Inicializar la clase YouTubeAPI con la clave de API de YouTube
youtube_client = YouTubeAPI(api_key="tu_api_key_youtube")

# Inicializar el traductor
translator_client = TranslatorAPI()

# Inicializar el exportador de contenido
content_exporter = ContentExporter()

# Variables globales para la conversación actual
current_user_input = ""
current_bot_response = ""
current_youtube_link = ""
current_language = "es"

# Clase FeedbackLoop
class FeedbackLoop:
    def __init__(self):
        self.feedback_given = False

    def process_feedback(self, feedback, user_input, language):
        """
        Procesar el feedback del usuario.
        :param feedback: 👍 (True) o 👎 (False)
        :param user_input: Consulta del usuario
        :return: Prompt ajustado si es necesario.
        """
        self.feedback_given = True
        if feedback:  # Si el feedback es positivo, no hacemos nada adicional
            return None
        else:  # Si el feedback es negativo, ajustamos el prompt
            print("Feedbackloop negativo")
            print(user_input)
            message = "Can you be more accurate?"
            translated_message = translator_client.translate_text(message, language)
            print(translated_message)
            return f"{user_input}. {translated_message}"

feedback_loop = FeedbackLoop()

def chat_with_gpt_and_youtube(prompt):
    global current_user_input, current_bot_response, current_youtube_link

    def validate_video_link(video_link):
        """Valida que el video esté disponible."""
        return video_link and "youtube.com/watch" in video_link

    try:

        language = current_language  # Usar el idioma actual

        # Llamada al modelo de OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant question solver. You only answer questions with text, and with links to youtube videos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.3
        )
        message_content = completion.choices[0].message.content

        # Buscar el video recomendado
        youtube_video_link = youtube_client.search_video_with_validation(prompt)
        attempts_recommended = 3  # Máximo 3 intentos para validar el video
        while not validate_video_link(youtube_video_link) and attempts_recommended > 0:
            youtube_video_link = youtube_client.search_video_with_validation(prompt)
            attempts_recommended -= 1

        # Buscar el video relacionado
        related_video_link = youtube_client.search_video_with_validation(f"{prompt} related")
        attempts_related = 3  # Máximo 3 intentos para validar y evitar duplicados
        while (not validate_video_link(related_video_link) or related_video_link == youtube_video_link) and attempts_related > 0:
            related_video_link = youtube_client.search_video_with_validation(f"{prompt} related")
            attempts_related -= 1

        # Verificar que los videos sean diferentes después del bucle
        if related_video_link == youtube_video_link:
            related_video_link = "No se encontró un video relacionado diferente."

        # Traducir el contenido del mensaje al idioma seleccionado
        translated_message_content = translator_client.translate_text(message_content, language)
        print(language)

        # Traducir mensaje adicional
        additional_message = "Below, I show you a video that may help you with your request if necessary."
        translated_message = translator_client.translate_text(additional_message, language)

        full_response = (
            f"{message_content}\n\n{translated_message}\n\n"
            f"Video recomendado: {youtube_video_link}\n"
            f"Video relacionado: {related_video_link}"
        )

        # Traducir etiquetas de los videos
        video_recommended_label = translator_client.translate_text("Video recommended", language)
        video_related_label = translator_client.translate_text("Related video", language)

        # Construir la respuesta completa traducida
        full_response = (
            f"{translated_message_content}\n\n{translated_message}\n\n"
            f"{video_recommended_label}: {youtube_video_link}\n"
            f"{video_related_label}: {related_video_link}"
        )

        # Actualizamos las variables globales
        current_user_input = prompt
        current_bot_response = message_content
        current_youtube_link = youtube_video_link

        return full_response, youtube_video_link, related_video_link
    except Exception as e:
        return f"Ocurrió un error: {str(e)}", "", ""

def extract_youtube_id(url):
    """
    Extraer el ID del video de YouTube desde la URL.
    """
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    return video_id_match.group(1) if video_id_match else ""

def export_conversation():
    return content_exporter.export_to_pdf(
        current_user_input,  # Pregunta actual del usuario
        current_bot_response,  # Respuesta actual del bot
        current_youtube_link  # Enlace al video actual
    )
# Traducir textos de la interfaz según el idioma seleccionado
def update_interface_texts(language):
    """
    Actualiza los textos de la interfaz al idioma seleccionado.
    """
    translations = translator_client.translate_interface_elements(language)
    return (
        f"## {translations['title']}",  # Título del bot
        translations["description"],  # Descripción del bot
        gr.update(placeholder=translations["input_placeholder"]),  # Placeholder del input
        gr.update(placeholder=translations["output_placeholder"]),  # Placeholder del output
        gr.update(label=translations["button_text"]),  # Texto del botón Enviar
        gr.update(label=translations["export_button"])  # Texto del botón Exportar
    )

# Crear la interfaz de Gradio
def create_interface():
    with gr.Blocks(css="""
        /* Fondo y estilos generales */
        body, html {
            background-color: #000000 !important; /* Fondo negro */
            color: #ffffff !important; /* Texto blanco */
            font-family: 'Roboto Mono', monospace; /* Fuente robótica */
            margin: 0;
            padding: 0;
            height: 100%;
            overflow-x: hidden;
        }

        /* Contenedor general */
        .gradio-container {
            background-color: #000000 !important; /* Fondo negro */
            color: #ffffff !important; /* Texto blanco */
            font-family: 'Roboto Mono', monospace;
            max-width: 100% !important;
            margin: 0 auto;
            border: 2px solid #00ff00 !important; /* Bordes verdes claros */
        }

        /* Textbox */
        textarea {
            background-color: transparent !important; /* Fondo transparente */
            color: #ffffff !important; /* Texto blanco */
            border: 2px solid #00ff00 !important; /* Bordes verdes claros */
            border-radius: 8px !important;
            padding: 10px;
        }

        textarea:focus {
            border-color: #00cc00 !important; /* Verde más oscuro al enfocar */
            outline: none !important;
        }

        /* Dropdown (selector) */
        select, .gr-dropdown select {
            background-color: #000000 !important; /* Fondo negro */
            border: 2px solid #00ff00 !important; /* Bordes verdes claros */
            color: #ffffff !important; /* Texto blanco */
            font-family: 'Roboto Mono', monospace;
            border-radius: 8px !important; /* Bordes redondeados */
            padding: 5px;
            height: 40px; /* Altura personalizada */
        }

        select:focus, .gr-dropdown select:focus {
            outline: none !important;
            border-color: #00cc00 !important; /* Borde más oscuro al enfocar */
        }

        .gr-dropdown {
            border: 2px solid #00ff00 !important; /* Bordes verdes claros */
            border-radius: 8px !important;
        }

        /* Botones */
        .gr-button {
            background-color: #000000 !important; /* Fondo negro */
            color: #ffffff !important; /* Texto blanco */
            border: 2px solid #00ff00 !important; /* Bordes verdes claros */
            border-radius: 8px !important;
            padding: 10px 20px;
            font-size: 16px;
        }

        .gr-button:hover {
            border-color: #00cc00 !important; /* Hover bordes verde oscuro */
        }

        /* Bloques y contenedores */
        .gr-block, .gr-box, .gr-container {
            border: 2px solid #00ff00 !important; /* Bordes verdes claros */
            border-radius: 8px !important;
            padding: 10px;
        }
                   
        /* Ocultar label predeterminado de gr.Examples */
        .gr-examples > label {
            display: none !important;
        }
        
        /* Videos y frames */
        .gr-html iframe {
            border: 2px solid #00ff00 !important; /* Bordes verdes claros para los videos */
            border-radius: 10px; /* Bordes redondeados */
        }
    """) as demo:
        # Agregar el logo de SapiensBot
        gr.Image(value="src/assets/sapiensbotlogo.png", show_label=False, interactive=False, width=200, height=200)

        # Selector de idioma
        language_selector = gr.Dropdown(
            label="|🇪🇸||🇺🇸||🇫🇷||🇩🇪||🇮🇹||🇵🇹|",
            choices=["es", "en", "fr", "de", "it", "pt"],
            value="es",
            interactive=True
        )

        # Inicializar traducciones iniciales
        initial_translations = translator_client.translate_interface_elements(language_selector.value)

        # Título y descripción de SapiensBot
        gr.Markdown("## 🤖SapiensBot")
        description = gr.Markdown(initial_translations["description"])

        # Textbox de entrada (Input)
        user_input = gr.Textbox(
            label="Input",
            placeholder="Escriba su mensaje aquí...",
            lines=6
        )

        # Botón de enviar
        submit_btn = gr.Button(value="Enviar", variant="primary")

        # Textbox de salida (Output)
        output_text = gr.Textbox(
            label="Output",
            placeholder="La respuesta aparecerá aquí...",
            lines=10
        )

        # Botones de feedback
        with gr.Row(visible=False) as feedback_buttons:  # Inicialmente ocultos
            feedback_valid = gr.Button("👍🏼")
            feedback_invalid = gr.Button("👎🏼")

        # Botón para exportar PDF (deshabilitado por defecto)
        export_btn = gr.Button(value="Exportar a PDF", interactive=False)

        # Función para traducir la interfaz al cambiar el idioma
        def on_language_change(language):
            global current_language 
            current_language = language
            translations = translator_client.translate_interface_elements(language)
            return (
                translations["description"],  # Descripción traducida
                gr.update(placeholder=translations["input_placeholder"]),  # Actualizar input
                gr.update(placeholder=translations["output_placeholder"]),  # Actualizar output
                gr.update(value=translations["button_text"]),  # Actualizar texto del botón Enviar
                gr.update(value=translations["export_button"]),  # Actualizar texto del botón Exportar
                translations["video_recommended_label"],  # Traducción para "Video YouTube Recomendado"
                translations["video_related_label"]  # Traducción para "Video Relacionado al Contenido"
            )

        # Ejemplos de entrada
        # Ejemplos de entrada
        gr.Examples(
            examples=[
                "Rick & Morty",
                "Fernando Alonso F1",
                "World War II",
            ],
            inputs=user_input,
        )

        # Videos recomendados
        with gr.Row():  
            with gr.Column(scale=1):
                video_recommended_label = gr.Markdown("### Video YouTube Recomendado")  # Etiqueta del video recomendado
                video_html_left = gr.HTML()  # Espacio para el contenido del video recomendado

            with gr.Column(scale=1):
                video_related_label = gr.Markdown("### Video Relacionado al Contenido")  # Etiqueta del video relacionado
                video_html_right = gr.HTML()  # Espacio para el contenido del video relacionado
                
        # Conectar el botón de exportar PDF a la función de exportación
        export_btn.click(
            fn=export_conversation,
            inputs=[],
            outputs=gr.File()
        )

        # Conectar el selector de idioma a la función de cambio
        language_selector.change(
            fn=on_language_change,
            inputs=[language_selector],
            outputs=[
                description,  # Descripción
                user_input,  # Textbox de entrada
                output_text,  # Textbox de salida
                submit_btn,  # Botón Enviar
                export_btn,  # Botón Exportar
                video_recommended_label,  # Texto para "Video YouTube Recomendado"
                video_related_label  # Texto para "Video Relacionado al Contenido"
            ]
        )

        # Función para manejar la consulta
        def chatbot_interface(user_input, language=None):

            full_response, video_link, related_video_link = chat_with_gpt_and_youtube(user_input)
            
            # Video recomendado
            video_id_main = extract_youtube_id(video_link)
            embed_link_main = f"https://www.youtube.com/embed/{video_id_main}" if video_id_main else ""
            video_html_main = (
                f'<iframe src="{embed_link_main}" frameborder="0" '
                'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
                if video_id_main else "No video found."
            )
            
            # Video relacionado
            video_id_related = extract_youtube_id(related_video_link)
            embed_link_related = f"https://www.youtube.com/embed/{video_id_related}" if video_id_related else ""
            video_html_related = (
                f'<iframe src="{embed_link_related}" frameborder="0" '
                'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
                if video_id_related else "No related video found."
            )
            
            return full_response, video_html_main, video_html_related

        submit_btn.click(
            fn=chatbot_interface,
            inputs=[user_input],
            outputs=[output_text, video_html_left, video_html_right]
        )

        # Actualizar la visibilidad de los botones de feedback por separado
        submit_btn.click(
            fn=lambda: gr.update(visible=True),  # Hacer visibles los botones de feedback
            inputs=[],
            outputs=[feedback_buttons]
        )

        # Hacer visibles los botones de feedback y habilitar exportar PDF tras consulta
        submit_btn.click(
            fn=lambda: gr.update(interactive=True),  # Hacer interactivo el botón Exportar a PDF
            inputs=[],
            outputs=[export_btn]
        )

        # Acción al hacer clic en "Respuesta válida"
        feedback_valid.click(
            lambda: feedback_buttons.update(visible=False),  # Ocultar botones
            inputs=[],
            outputs=[feedback_buttons]
        )

        # Acción al hacer clic en "Respuesta no válida"
        feedback_invalid.click(
            fn=lambda: chatbot_interface(
                feedback_loop.process_feedback(
                    feedback=False,  # Feedback negativo
                    user_input=current_user_input,  # Usar el input del usuario actual
                    language=current_language  # Pasar el idioma seleccionado
                ),
            ),
            inputs=[],
            outputs=[output_text, video_html_left, video_html_right]
        )

    return demo

# Manejar señales
def signal_handler(sig, frame):
    print("Cerrando servidor...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Ejecutar la interfaz
if __name__ == "__main__":
    demo = create_interface()
    demo.launch()