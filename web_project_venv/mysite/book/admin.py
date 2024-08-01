from django.contrib import admin

from .models import bookT

class BookT_Admin(admin.ModelAdmin):
    search_fields = ['book title']

admin.site.register(bookT,BookT_Admin)
# Register your models here.
