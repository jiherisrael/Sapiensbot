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

        :param language: Código de idioma al cual traducir los elementos de la interfaz.
        :return: Diccionario con los elementos traducidos.
        """
        return {
            "title": self.translate_text("🤖 SapiensBot", language),
            "description": self.translate_text("Welcome to this chatbot based on GPT-3.5 Turbo. Ask me anything and I will help you with useful and accurate answers.", language),
            "input_label": self.translate_text("Input", language),
            "input_placeholder": self.translate_text("Type your message here...", language),
            "button_text": self.translate_text("Send", language),
            "output_label": self.translate_text("Output", language),
            "output_placeholder": self.translate_text("The response will appear here...", language),
            "examples_label": self.translate_text("Ex", language),
        }
