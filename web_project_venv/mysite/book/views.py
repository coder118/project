from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User_information
from .models import bookT
from .models import bookW
# Create your views here.
from .form import PersonForm,UserForm
 
 
def index(request):
    print("titlelist")
    
    book_title_list=bookT.objects.all()
    # template = loader.get_template('book/index.html')
    context={
        'book_title_list' : book_title_list,
    }
    # if request.method == 'POST':# 이게 핵심이었어 form.as_p를 실행하면 안됐어 근데 내가 강제로 input을 만들어주니까 이곳으로 넘어가면서 get_name을 호출함 
    #     print('stop')
    #     return get_name(request)
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
    print("suc")#걍 실행확인용
    book_title_list = bookT.objects.all()
    print(book_title_list) 
 
    if request.method == 'POST':
        
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()  # 모델에 데이터 저장
            return redirect('success')  # 성공 시 리디렉션
    else:
        
        form = PersonForm() 
    return render(request, 'book/index.html', {'form': form})



@csrf_exempt
def check_duplicate(request):
    print('dupli')
    if request.method == 'POST':
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')
        
        if field == 'username':
            exists = User_information.objects.filter(username=value).exists()
        elif field == 'nickname':
            exists = User_information.objects.filter(nickname=value).exists()
        else:
            return JsonResponse({'exists': False})

        return JsonResponse({'exists': exists})
    
    # return JsonResponse({'error': 'Invalid request method'}, status=400)

def successful_user(request):
    print('user save')
    if request.method == 'POST':
        print('POST request received') 
        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()  # 모델에 데이터 저장
            return redirect('success')  # 성공 시 리디렉션
        else:
            print(form.errors)
            
    else:
        
        form = UserForm() 
    return render(request, 'book/index.html', {'form': form})

# 데이터 저장후에  book/signup/successful_user 경로로 넘어감
# 그리고 데이터에 저장에 성공하고 원래 기본 화면창으로 넘어가는 기능이 필요함 


