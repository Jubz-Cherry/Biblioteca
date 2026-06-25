import os
from dotenv import load_dotenv
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

load_dotenv()

API_KEY = os.getenv("GOOGLE_KEY")
#print(f"API_KEY: {API_KEY}")  

#sempre ativar para ver se está correta a ligração


class BooksSearchView(APIView):
    def get(self, request):

        CATEGORY_MAP = {
        "ficcao": "fiction",
        "romance": "romance",
        "terror": "horror",
        "fantasia": "fantasy",
        "historia": "history",
        "administracao": "business",
        "culinaria": "cooking",
        "ingles": "english language",
        "autoajuda": "self-help",
    }
       
        user_category = request.query_params.get("category", "ficcao")

        category = CATEGORY_MAP.get(user_category, "fiction")

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q=subject:{category}&maxResults=20"
            f"&key={API_KEY}"
        )

        response = requests.get(url)
        data = response.json()
        
        books = []

        for item in data.get("items", []):
            volume = item.get("volumeInfo", {})

            books.append({
                "title": volume.get("title"),
                "authors": volume.get("authors", []),
                "description": volume.get("description"),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail"),
                "categories": volume.get("categories", [])
            })

        return Response(books)