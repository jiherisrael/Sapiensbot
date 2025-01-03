from googleapiclient.discovery import build  # Importamos el módulo necesario para la API de YouTube

class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def search_video(self, query):
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=1,
                videoEmbeddable="true"  # Solo videos que se pueden incrustar
            )
            response = request.execute()
            if "items" in response and len(response["items"]) > 0:
                video_id = response["items"][0]["id"]["videoId"]
                return f"https://www.youtube.com/watch?v={video_id}"
            else:
                return "No se encontró ningún video relacionado."
        except Exception as e:
            return f"Ocurrió un error al buscar el video: {str(e)}"

    def search_related_video(self, query):
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=f"{query} related",  # Modificamos la búsqueda con "related"
                type="video",
                maxResults=1
            )
            response = request.execute()
            if "items" in response and len(response["items"]) > 0:
                video_id = response["items"][0]["id"]["videoId"]
                return f"https://www.youtube.com/watch?v={video_id}"
            else:
                return "No se encontró ningún video relacionado."
        except Exception as e:
            return f"Ocurrió un error al buscar el video: {str(e)}"
        
    def search_video_with_validation(self, query):
        """Busca un video y valida que esté disponible."""
        for _ in range(3):  # Intentar hasta 3 veces
            video_link = self.search_video(query)
            if video_link and "youtube.com/watch" in video_link:
                return video_link
        return "No se encontró un video válido."
