from django.contrib import admin

from .models import Book, Exchange

# Register your models here.
admin.site.register(Book)
admin.site.register(Exchange)