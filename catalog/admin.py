from django.contrib import admin
from django.db import models

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Language)