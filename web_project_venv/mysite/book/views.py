from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader

from .models import bookT
from .models import bookW
# Create your views here.
from .form import PersonForm
 
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

#
def get_name(request):
    print("suc")
    if request.method == 'POST':
        
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()  # 모델에 데이터 저장
            return redirect('success')  # 성공 시 리디렉션
    else:
        
        form = PersonForm()
    
    return render(request, 'book/index.html', {'form': form})


# def success(request):
#     return render(request,'book/success.html')



