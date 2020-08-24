from django.urls import include, path
from . import views

urlpatterns = [
  path('getbooks/', views.GetBook.as_view()),
  path('addbook/', views.CreateBook.as_view()),
  path('updatebook/<int:book_id>/', views.UpdateBook.as_view()),
  path('deletebook/', views.DeleteBook.as_view()),
  path('getauthor/', views.GetAuthor.as_view()),
  path('addauthor/', views.AuthorList.as_view()),
  path('updateauthor/<int:author_id>/', views.UpdateAuthor.as_view()),
   path('deleteauthor/', views.DeleteAuthor.as_view())
]


