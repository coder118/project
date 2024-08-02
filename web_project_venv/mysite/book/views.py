from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import bookT
# Create your views here.

def index(request):
    book_title_list=bookT.objects.all()
    # template = loader.get_template('book/index.html')
    context={
        'book_title_list' : book_title_list,
    }
    return render(request,'book/index.html',context)
    # return HttpResponse(template.render(context,request))
    
