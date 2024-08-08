from django.contrib import admin

from .models import bookT,Person

class BookT_Admin(admin.ModelAdmin):
    search_fields = ['book title']

admin.site.register(bookT,BookT_Admin)
admin.site.register(Person)
# Register your models here.
