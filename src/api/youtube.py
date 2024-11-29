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
