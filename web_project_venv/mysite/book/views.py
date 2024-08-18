from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages #메세지 기능인듯?
from django.contrib.auth import authenticate, login # 로그인할떄 사용함
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import json
from django.views.generic import ListView
from .models import Post_information

from .models import User_information
from .models import bookT
from .models import bookW
# Create your views here.
from .form import PersonForm,UserForm,PostForm
 
 
def index(request):
    print("titlelist")
    
    # book_title_list=bookT.objects.all()
    # template = loader.get_template('book/index.html')
    # context={
    #     'book_title_list' : book_title_list,
    # }
    # if request.method == 'POST':# 이게 핵심이었어 form.as_p를 실행하면 안됐어 근데 내가 강제로 input을 만들어주니까 이곳으로 넘어가면서 get_name을 호출함 
    #     print('stop')
    #     return get_name(request)
    post_list = Post_information.objects.all()
    print(post_list)
    paginator = Paginator(post_list, 10)  # 페이지당 20개의 게시물을 표시합니다
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    print(context)
    return render(request,'book/index.html',context)
    # return HttpResponse(template.render(context,request))
 

def post_detail(request, pk):
    post = get_object_or_404(Post_information, pk=pk)
    print(post)
    usernames = User_information.objects.values_list('username', flat=True)
    
    #comments = Comment.objects.filter(post=post)  # 댓글 모델을 사용하여 해당 게시물에 대한 댓글 가져오기
    other_posts = Post_information.objects.exclude(pk=pk)  # 현재 게시물을 제외한 다른 게시물 가져오기
    post.views += 1
    post.save() 
    context = {
        'post': post,
        'user':request.session.get('username'),
        'user_check':usernames, # 유저 정보 데이터 베이스에서 유저 아이디 값을 가져와서 현재 들어와있는 유저가 usercheck안에 존재 하면 댓글 작성 가능하게 
        'other_posts': other_posts,
    }
    print(context)
    return render(request, 'book/post_detail.html', context) 

# 내가 만들어서 적어본것     
#def book_writer(request):
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


###회원 가입과 로그인 기능 중복확인함수까지
@csrf_exempt
def check_duplicate(request): #회원가입시 중복을 확인하는 함수 
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

def successful_user(request): #회원가입 한 후 디비에 저장하는 함수 
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

from django.contrib.auth.hashers import check_password
# 로그인 처리하는 함수 문제가 좀 있음 
# 비밀번호 해쉬화 저장해야 함 폼 파이 가면 해쉬화기능 킬 수가 있음 
#로그인을 했을떄 그 사람의 계정으로 들어가서 각자의 데이터베이스가 만들어져야 함
# 아주 기본적인 기능만 구현하는데 성공함 
def trying_to_login(request): 
    # if request.method == 'POST':
    #     user_id = request.POST.get('username')
    #     pw = request.POST.get('password')
    #     print(user_id,pw)
    #     # 빈칸이 있는지 확인
    #     if not user_id or not pw:
    #         messages.error(request, '아이디와 비밀번호를 모두 입력해주세요.')
    #         return render(request, 'book/login.html')

    #     # 아이디 존재 여부 확인
    #     try:
    #         user = User_information.objects.get(username=user_id)
            
    #     except User_information.DoesNotExist:
    #         # 아이디가 존재하지 않으면 메시지와 회원가입 링크 제공
    #         messages.error(request, '없는 아이디입니다. 회원가입을 해주세요.')
    #         return render(request, 'book/login.html')

    #     # 사용자 인증
    #     # user = authenticate(request, username=user_id, password=pw)
    #     # print(f"Authenticated User: {user}")
    #     # print(login(request,user))
    #     # if user is not None:
    #     #     login(request, user)
    #     #     messages.success(request, '로그인 성공했습니다.')
    #     #     return redirect('book/index.html')  # 로그인 성공 후 리디렉션
    #     # else:
    #     #     messages.error(request, '로그인 실패: 아이디나 비밀번호가 잘못되었습니다.')
    #     #     return render(request, 'book/login.html')
    #     if user.password == pw:  # 해시가 아닌 평문 비밀번호 비교
    #         # 비밀번호가 맞을 경우 로그인 처리
    #         messages.success(request, '로그인 성공했습니다.')
    #         print("login success")
    #         return redirect('index')  # 로그인 성공 후 리디렉션
    #     else:
    #         messages.error(request, '로그인 실패: 아이디나 비밀번호가 잘못되었습니다.')
    #         return render(request, 'book/login.html')
    # else:
    #     return render(request, 'book/login.html')
    if request.method == 'POST':
        
        user_id = request.POST.get('username')
        pw = request.POST.get('password')
        print(user_id,pw)
        # 빈칸이 있는지 확인
        if not user_id or not pw:
            return JsonResponse({'error': '아이디와 비밀번호를 모두 입력해주세요.'})

        # 아이디 존재 여부 확인
        try:
            user = User_information.objects.get(username=user_id)
        except User_information.DoesNotExist:
            return JsonResponse({'error': '없는 아이디입니다. 회원가입을 해주세요.'})

        # 비밀번호 확인
        if user.password == pw:  # 해시가 아닌 평문 비밀번호 비교
            request.session['username'] = user_id
            return JsonResponse({'success': '로그인 성공했습니다!', 'redirect_url': '/book/'})  # 로그인 성공 후 리디렉션할 URL
        else:
            return JsonResponse({'error': '로그인 실패: 아이디나 비밀번호가 잘못되었습니다.'})

    return render(request, 'book/login.html')
    

def logout_view(request):
    print(request)
    print(request.session.get('username'))
    logout(request)
    request.session.flush() # 세션 삭제
    return redirect('index')

# 이미지 업로드 코드인데 일단 너무 복잡한 것 같아서 보류함
from django.shortcuts import render, redirect 
from django.core.files.storage import FileSystemStorage
import os

def upload_profile_pic(request):
    if request.method == 'POST' and request.FILES['profile_pic']:
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        uploaded_file_url = fs.url(filename)
        # 파일의 절대 경로 생성
        base_path = "C:\\web_project\\web_project_venv\\mysite"  # 기본 경로
        full_path = os.path.join(base_path, uploaded_file_url.lstrip('/'))  # 앞의 '/' 제거
        # 세션에 이미지 URL 저장
        print('check')
        print(full_path)
        request.session['profile_pic'] = full_path
        print(request.session['profile_pic'])
        return redirect('index')  # 적절한 리다이렉션 URL로 변경하세요.

    return redirect('index')  # 적절한 템플릿으로 변경하세요.

###게시판 


def post_view(request):
    return render(request, 'book/post_create.html')

from django.utils import timezone
def post_save(request):
    print('post upload')
    
    # user_id = request.POST.get('username')
    # print(user_id)
    user_id = request.session.get('username')  # 세션에 저장된 사용자계졍의 값을 가져온다.
    if request.method == 'POST':
        print('POST POST request received') 
        
        print("현재 로그인된 사용자:",user_id )
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)  # 모델 인스턴스를 생성하되 아직 저장하지 않음
            
            post.author=  User_information.objects.get(username=user_id)#바로 세션값을 사용할 수 없어서 인스턴스 값을 사용을 해준다.
            print("저장 전 created_at:", post.created_at)
            print("저장 전 updated_at:", post.updated_at)
            
            post.created_at = timezone.now()  # 현재 시간으로 설정
            post.updated_at = timezone.now()   # 현재 시간으로 설정
            
            post.save()  # 모델에 데이터 저장
            print("저장 후 created_at:", post.created_at)
            print("저장 후 updated_at:", post.updated_at)
            # create= post.created_at
            # update= post.updated_at
            
            # post.created_at = create
            # post.updated_at = update
            # # post.refresh_from_db()
            # # post.created_at=post.created_at
            # # post.updated_at=post.updated_at
            # post.save() 
            return redirect('index')  # 성공 시 리디렉션
        else:
            print(form.errors)
            
    else:
        form = PostForm() 
    return render(request, 'book/index.html', {'form': form})
        


# class PostListView(ListView):
#     print("postlist working")
#     model = Post_information
#     template_name = 'index.html'  # 사용할 템플릿 파일
#     context_object_name = 'posts_information'  # 템플릿에서 사용할 컨텍스트 변수 이름
#     paginate_by = 20  # 페이지당 표시할 게시글 수
#     print("workin done")
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(context['posts_information'])  # 데이터가 제대로 전달되는지 확인
#         return context
# 데이터 저장후에  book/signup/successful_user 경로로 넘어감
# 그리고 데이터에 저장에 성공하고 원래 기본 화면창으로 넘어가는 기능이 필요함 


