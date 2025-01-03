from fpdf import FPDF

class ContentExporter:
    def __init__(self):
        pass  # Eliminar la inicialización del PDF aquí

    def export_to_pdf(self, user_question, bot_response, youtube_link, file_path="output.pdf"):
        """
        Exporta el contenido a un archivo PDF.

        :param user_question: La pregunta hecha por el usuario.
        :param bot_response: La respuesta del chatbot.
        :param youtube_link: El enlace al video de YouTube relacionado.
        :param file_path: Ruta donde se guardará el PDF (default es "output.pdf").
        :return: La ruta del archivo PDF creado.
        """
        # Crear una nueva instancia de FPDF cada vez que se llama al método
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(200, 10, txt="SapiensBot Interaction Summary", ln=True, align='C')

        # Pregunta del usuario
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, txt="User Question:", ln=True)
        pdf.multi_cell(0, 10, txt=user_question)

        # Respuesta del chatbot
        pdf.ln(10)
        pdf.cell(200, 10, txt="SapiensBot Response:", ln=True)
        pdf.multi_cell(0, 10, txt=bot_response)

        # Enlace del video de YouTube
        if youtube_link:
            pdf.ln(10)
            pdf.cell(200, 10, txt="Recommended YouTube Video:", ln=True)
            pdf.multi_cell(0, 10, txt=youtube_link)

        # Guardar el PDF
        pdf.output(file_path)
        return file_path