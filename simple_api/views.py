from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author
from rest_framework import status
import json
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class GetBook(APIView):

  def get(self,request):
    user = request.user.id
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_200_OK)

# @api_view(["POST"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
class CreateBook(APIView):

  def post(self,request):
    payload = request.data
    
    author = Author.objects.get(id=payload["author_id"])
    book_dict={
      "title" : payload["title"],
      "description" : payload["description"],
      "author": author.name
      }
    serializer = BookSerializer(data=book_dict)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  # payload = request.data
  
  # book = Book.objects.create(
  #   title = payload["title"],
  #   description = payload["description"],
  #   author = author
  # )
  # serializer = BookSerializer(book)
  # return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_201_CREATED)

# @api_view(["PUT"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
class UpdateBook(APIView):

  def put(self, request, book_id):
    payload = request.data

    try:
      book_item = Book.objects.filter(id=book_id)
      # returns 1 or 0
      book_item.update(**payload)
      book = Book.objects.get(id=book_id)
      serializer = BookSerializer(book)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
      return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
      return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteBook(APIView):

  def post(self,request):
    try:
      payload=request.data
      Book.objects.filter(id=payload["book_id"]).delete()
      return Response(status=status.HTTP_200_OK)

    except ObjectDoesNotExist as e:
      return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
      return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAuthor(APIView):

  def get(self,request):
    user = request.user.id
    author = Author.objects.all()
    serializer = AuthorSerializer(author, many=True)
    return JsonResponse({'authors': serializer.data}, safe=False, status=status.HTTP_200_OK)


class AuthorList(APIView):

  def post(self, request, format=None):

    payload = request.data
    author_dict={
      "name" : payload["name"],
    }

    serializer = AuthorSerializer(data=author_dict)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateAuthor(APIView):

  def post(self, request, author_id):
    try:
      payload = request.data
      author = Author.objects.filter(id=author_id)
      # returns 1 or 0
      author.update(**payload)
      specific_author = Author.objects.get(id=author_id)
      serializer = AuthorSerializer(specific_author)
      return Response(serializer.data, status=status.HTTP_200_OK)

    except ObjectDoesNotExist as e:
      return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
      
class DeleteAuthor(APIView):

  def post(self,request):
    try:
      payload=request.data
      Author.objects.filter(id=payload["author_id"]).delete()
      return Response(status=status.HTTP_200_OK)

    except ObjectDoesNotExist as e:
      return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
      return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


