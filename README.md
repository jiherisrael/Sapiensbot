# SapiensBot

## Descripción
Este proyecto es un chatbot académico diseñado para ayudar a los estudiantes con sus preguntas académicas utilizando tecnologías de inteligencia artificial. El chatbot está construido con Python y utiliza Gradio para la interfaz, GPT-3.5-turbo para la generación de texto, la API de YouTube para proporcionar recursos de video relevantes, y la API de Google Translator para la traducción y facilidad del contenido proporcionado.

## Características
- Genera respuestas académicas interactivas.
- Recomienda videos educativos relacionados con las consultas del usuario.
- Interfaz amigable basada en Gradio.

## Requisitos Previos
Para ejecutar este proyecto, necesitas tener instalado Python 3.8 o superior y pip. Es recomendable también tener git instalado para clonar el repositorio.

## Configuración del Entorno
Sigue estos pasos para configurar el entorno de desarrollo:

### Clonar el Repositorio
Para obtener una copia del proyecto, clona el repositorio a tu máquina local usando:

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### Crear y Activar el Entorno Virtual

#### En Windows, ejecuta:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### En macOS y Linux, ejecuta:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Uso
Para iniciar el chatbot, navega al directorio del proyecto y ejecuta el script principal:

```bash
python -m src.core.chatbot
```

## Estructura del Proyecto
El proyecto está organizado en los siguientes módulos:

- **src/core/chatbot.py**: Contiene la lógica principal del chatbot, incluyendo la integración con OpenAI y YouTube.
- **src/utils/translator.py**: Proporciona una API para traducir texto y elementos de la interfaz.
- **src/utils/content_exporter.py**: Permite exportar resúmenes de interacción a PDF.
- **src/api/youtube.py**: Maneja las consultas y validaciones con la API de YouTube.

## Solución a Problemas Comunes
- **Error de conexión con YouTube API**:
  Verifica que la clave de API es válida y que tienes permiso para acceder a la API.

- **Traducciones no funcionan**:
  Asegúrate de que la biblioteca `deep-translator` esté instalada correctamente.

- **Exportación a PDF falla**:
  Confirma que tienes permisos de escritura en el directorio de salida y que la biblioteca `fpdf` está instalada.

## Futuras Mejoras
1. Incorporar modelos más avanzados para mejorar la generación de respuestas.
2. Añadir compatibilidad con más idiomas en las traducciones.
3. Optimizar la búsqueda de videos relacionados.

### Créditos
El desarrollo de este proyecto es parte del ejercicio final de un bootcamp de inteligencia artificial. Fue diseñado e implementado íntegramente por **Israel Jiménez Hernández**, quien posee todos los derechos de autor sobre la idea y la implementación del mismo.

### Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor fork el repositorio y envía un pull request, o abre un issue con los detalles de lo que te gustaría cambiar.

### Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

