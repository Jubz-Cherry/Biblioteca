from datetime import date, timedelta
import os
from rest_framework import viewsets, status
from dotenv import load_dotenv
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from biblioteca.models import RegisterBooks, Userlogin, Loanbook
from biblioteca.serializers import RegisterBooksSerializer, UserloginSerializer


load_dotenv()

API_KEY = os.getenv("GOOGLE_KEY")
#print(f"API_KEY: {API_KEY}")  
#sempre ativar para ver se está correta a ligração

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


        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code != 200:
            return Response(
                {"erro": "Erro ao consultar a API."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
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


    
class UserloginView(viewsets.ModelViewSet):
    queryset = Userlogin.objects.all()
    serializer_class = UserloginSerializer

class RegisterBooksView(viewsets.ModelViewSet):
    queryset = RegisterBooks.objects.all()
    serializer_class = RegisterBooksSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def borrow(self, request, pk=None):
        livro = self.get_object()

        # Usuário já possui um livro emprestado?
        if Loanbook.objects.filter(
            user=request.user,
            returned_at__isnull=True
        ).exists():
            return Response(
                {"erro": "Você já possui um livro emprestado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Livro já está emprestado?
        if Loanbook.objects.filter(
            book=livro,
            returned_at__isnull=True
        ).exists():
            return Response(
                {"erro": "Este livro já está emprestado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Loanbook.objects.create(
            user=request.user,
            book=livro,
            due_date=date.today() + timedelta(days=30)
        )

        return Response(
            {"mensagem": "Livro emprestado com sucesso."},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        livro = self.get_object()

        try:
            emprestimo = Loanbook.objects.get(
                user=request.user,
                book=livro,
                returned_at__isnull=True
            )

        except Loanbook.DoesNotExist:
            return Response(
                {"erro": "Você não possui este livro emprestado."},
                status=status.HTTP_404_NOT_FOUND
            )

        emprestimo.returned_at = date.today()
        emprestimo.save()

        return Response(
            {"mensagem": "Livro devolvido com sucesso."},
            status=status.HTTP_200_OK
        )

        # ATIVAR QUANDO O CÓDIGO ESTIVER "PRONTO"
        #pois envolve lógia da lista de espera e envio de email/notificações ao usuário

            # Livro já está emprestado?
 #       if Loanbook.objects.filter(
 #           book=livro,
 #           returned_at__isnull=True
 #       ).exists():
 #           return Response(
 #               {"erro": "Este livro já está emprestado."},
 #               status=status.HTTP_400_BAD_REQUEST
 #           )

            
    
