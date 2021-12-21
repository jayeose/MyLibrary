from django.db import models
from django.http.response import Http404
import uuid   # https://officeguide.cc/python-generate-uuid-tutorial-examples/

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='請輸入書本類別(例如：科學書刊。)')
    
    def __str__(self):
        return self.name

from django.urls import reverse #Used to gengerate URLs by reversing the URL patterns

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='請輸入書本摘要')
    isbn = models.CharField('ISBN', max_length=13, help_text='請輸入13碼<a href="https://www.isbn-international.org/content/what-isbn">ISBN號碼</a>')
    genre = models.ManyToManyField(Genre, help_text='請選擇本書類型')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='請輸入一個UUID(獨特ID)來代表書：')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', '維護中'),
        ('o', '借出中'),
        ('a', '可借用'),
        ('r', '已預約'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    
    class Meta:
        ordering = ['due_back']
        
    def __str__(self):
        return f'{self.id} {{self.book.title}}'
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    name = models.CharField(max_length=200, help_text='請輸入語言(例如英語、法語、德語...')
    
    def __str__(self):
        return self.name
    