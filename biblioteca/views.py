import os
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

class BooksGetView(APIView):
    def get(self, request):
        category = request.query_params.get("category", "fiction")

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