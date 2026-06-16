from django.http import JsonResponse

def livros_biblioteca(request):
    if request.method == 'GET':
        livros = [
        {"id": 1, "titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien"},
        {"id": 2, "titulo": "Harry Potter e a Pedra Filosofal", "autor": "J.K. Rowling"},
        {"id": 3, "titulo": "1984", "autor": "George Orwell"},
        ]
    return JsonResponse(livros, safe=False)