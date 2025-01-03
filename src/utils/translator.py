from deep_translator import GoogleTranslator

class TranslatorAPI:
    def __init__(self):
        self.translator = GoogleTranslator()

    def translate_text(self, text, target_language):
        """
        Traduce el texto dado al idioma especificado.
        
        :param text: Texto a traducir.
        :param target_language: Código de idioma al cual traducir el texto (e.g., 'en', 'fr', 'es').
        :return: Texto traducido.
        """
        try:
            return GoogleTranslator(source='auto', target=target_language).translate(text)
        except Exception as e:
            return f"Error al traducir: {str(e)}"

    def translate_interface_elements(self, language):
        """
        Traduce los elementos de la interfaz al idioma especificado.

        :param language: Códidgo de idioma al cual traducir los elementos de la interfaz.
        :return: Diccionario con los elementos traducidos.
        """
        interface_elements = {
        "title": "SapiensBot",  # No es necesario traducir el nombre del bot
        "description": "Welcome to SapiensBot. Ask me anything you want and I will help you with useful and accurate answers.",
        "input_placeholder": "Type your message here...",
        "button_text": "Send",
        "output_placeholder": "The response will appear here...",
        "video_recommended_label": "YouTube Recommended Video",  # Nuevo: Traducción para "Video YouTube Recomendado"
        "video_related_label": "Content Related Video",  # Nuevo: Traducción para "Video Relacionado al Contenido"
        "export_button": "Export to PDF",
        "input_label": "Input",  # Agregamos input_label si necesario
        "output_label": "Output",  # Agregamos output_label si necesario
    }

        # Traducir todos los valores excepto el título
        for key, value in interface_elements.items():
            if key != "title":
                interface_elements[key] = self.translate_text(value, language)

        return interface_elements
