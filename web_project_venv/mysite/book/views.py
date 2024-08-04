from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import bookT
from .models import bookW
# Create your views here.

def index(request):
    book_title_list=bookT.objects.all()
    # template = loader.get_template('book/index.html')
    context={
        'book_title_list' : book_title_list,
    }
    return render(request,'book/index.html',context)
    # return HttpResponse(template.render(context,request))
 
# 내가 만들어서 적어본것     
def book_writer(request):
    book_writer_list = bookW.objects.all()
    context={
        "book_writer_list": book_writer_list
    }
    return render(request,'book/index.html',context)

def login_view(request):
    return render(request,'book/login.html')

def signup_view(request):
    return render(request,'book/signup.html')