from django.contrib import admin

from .models import bookT,Person,User_information,Post_information,Tag

class BookT_Admin(admin.ModelAdmin):
    search_fields = ['book title']

admin.site.register(bookT,BookT_Admin)
admin.site.register(Person)
admin.site.register(User_information)
# Register your models here.
admin.site.register(Post_information)
admin.site.register(Tag)