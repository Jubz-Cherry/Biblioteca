import os
from dotenv import load_dotenv
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter


load_dotenv()

API_KEY = os.getenv("GOOGLE_KEY")
#print(f"API_KEY: {API_KEY}")  

#sempre ativar para ver se está correta a ligração

#quando alguém abrir a documentação, vai aparecer a lista de categorias que podem ser pesquisadas
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="category",
            location=OpenApiParameter.QUERY,
            type=str,
            enum=[
                "ficcao",
                "romance",
                "fantasia",
                "terror",
                "culinaria",
                "administracao",
                "ingles",
                "autoajuda"
            ]
        )
    ]
)

class BooksSearchView(APIView):
    def get(self, request):

#Lógica para mapear as categorias em inglês, que é o que a API do Google Books espera.
        CATEGORY_MAP = {
        "ficcao": "fiction",
        "romance": "romance",
        "terror": "horror",
        "fantasia": "fantasy",
        "historia": "history",
        "administracao": "business",
        "culinaria": "cooking",
        "ingles": "english",
        "autoajuda": "self-help",
    }
       
        user_category = request.query_params.get("category", "")

        #print para testar se o swagger ta recebendo a categoria correta
        #print("Categoria recebida:", user_category)

        category = CATEGORY_MAP.get(user_category)
        
        #print para testar se o swagger ta pegando a categoria correta
        #print("Categoria Google:", category)

        #query = CATEGORY_MAP.get(user_category, user_category)

## colocar url de cada categoria de livros e achar a api_key
        lang = request.query_params.get("lang", "pt")

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q={category}"
            f"&maxResults=20"
            f"&key={API_KEY}"
            f"&langRestrict={lang}"
        )


        response = requests.get(url)
        data = response.json()
        print(data)
        
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