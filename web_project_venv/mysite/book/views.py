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
from django.db.models import Q
from django.db.models import Count
from django.template.loader import render_to_string

import json
from django.views.generic import ListView
from .models import Post_information
from itertools import chain
from .models import User_information, Comment, Comment_Reply,Like,UserProfile
from .models import bookT
from .models import bookW
# Create your views here.
from .form import PersonForm,UserForm,PostForm,CommentForm, CommentReplyForm
 
 
def index(request):
    print("titlelist")
    
    
    category = request.GET.get('category','all')  # 선택된 카테고리 가져오기
    print(category)
    if category == 'all' or category == '': 
        post_list = Post_information.objects.all().annotate(like_count=Count('like_users')).order_by('-created_at')#좋아요도 표시
    else:
        post_list = Post_information.objects.filter(category=category).annotate(like_count=Count('like_users')).order_by('-created_at')#좋아요도 표시
    # print(post_list)
    paginator = Paginator(post_list, 10)  # 페이지당 20개의 게시물을 표시합니다
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    user_id = request.session.get('user_id')
        
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        
        user_profile = None  # 프로필이 없으면 None으로 설정
        
    context = {
        'page_obj': page_obj,
        'user_profile': user_profile,
    }
    print(context)
    print(request)
    return render(request,'book/index.html',context)
    # return HttpResponse(template.render(context,request))
    
def comment_profile_image(request):
    if request.method == 'POST':
        print("comment_profile_image 호출됨")  # 호출 확인용 로그
        user_id = request.session.get('user_id')

        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            user_profile = None  # 프로필이 없으면 None으로 설정

        context = {
            "user_profile": user_profile,
        }
        print("user_profile:", context)  # 디버깅용 로그
        return render(request, "book/post_detail.html", context)
    else:
        print("POST 요청이 아닙니다.")  # POST가 아닐 경우 로그 확인
def get_all_replies(comment):
    """재귀적으로 모든 대댓글과 대대댓글을 가져오는 함수"""
    all_replies = []
    direct_replies = comment.replies.all()

    
    for reply in direct_replies:
        all_replies.append(reply)   
        all_replies.extend(get_all_replies(reply))
    print(all_replies,'alll')
    return all_replies

def ranking_update(request):
    ranking = Post_information.objects.order_by('-views')[:5]
    like_ranking = Post_information.objects.all().annotate(like_count=Count('like_users')).order_by('-like_count')[:5]
    
    return render(request, 'book/ranking_list.html', {'rank': ranking,'like_rank':like_ranking})

def post_detail(request, pk):
    post = get_object_or_404(Post_information, pk=pk)
    
    comments = post.comments.all()  # 해당 게시물에 대한 댓글 가져오기
  
    usernames = User_information.objects.values_list('username', flat=True)
    
    #comments = Comment.objects.filter(post=post)  # 댓글 모델을 사용하여 해당 게시물에 대한 댓글 가져오기
    other_posts = Post_information.objects.exclude(pk=pk)  # 현재 게시물을 제외한 다른 게시물 가져오기
    post.views += 1
    user_info = User_information.objects.filter(username=request.session.get('username')).first()
    print(type(user_info))
    print(type(usernames))
    like_count = post.like_users.count()
    
    
    post.save() 
    comments_anno = post.comments.annotate(like_count=Count('comment_like_users'))
    comment_replies = []
    for comment in comments_anno:
        replies = get_all_replies(comment)
        for reply in replies:
            # 각 대댓글에 대해 좋아요 수를 추가
            reply.like_count = reply.commentR_like_users.count()
            comment_replies.append(reply)
    comments_anno = [comment for comment in comments_anno if comment.comment_like_users.count() > 0]
    comment_replies = [reply for reply in comment_replies if reply.commentR_like_users.count() > 0]
    comment_replies.sort(key=lambda x: x.commentR_like_users.count(), reverse=True)
    print(comment_replies,'commentreply')
    # 댓글과 대댓글을 합쳐서 상위 3개의 항목을 선택
    combined = list(chain(comments_anno, comment_replies))
    combined.sort(key=lambda x: x.like_count, reverse=True)
    best_combined = combined[:3]

    #best_comments = comments.annotate(like_count=Count('comment_like_users')).filter(like_count__gt=0).order_by('-like_count')[:3]
    
    for comment in comments:
        comment.like_count = comment.comment_like_users.count()
        # 대댓글에 대해서도 좋아요 수 추가
        for reply in comment.replies.all():
            reply.like_count = reply.commentR_like_users.count()
    rank = Post_information.objects.all()
    ranking = rank.order_by('-views')[:5]
    
    user_id = request.session.get('user_id')

    try:
        user_profile = UserProfile.objects.all()#get(user_id=user_id)
    except UserProfile.DoesNotExist:
        user_profile = None  # 프로필이 없으면 None으로 설정

    context = {
        'post': post,
        'user':user_info,
        'comment_user':request.session.get('username'),
        'user_check':usernames, # 유저 정보 데이터 베이스에서 유저 아이디 값을 가져와서 현재 들어와있는 유저가 usercheck안에 존재 하면 댓글 작성 가능하게 
        'other_posts': other_posts,
        'like_count':like_count, #좋아요 카운팅
        'rank':ranking,
        'comments': comments,  # 댓글 목록 추가
        'reply':comment_replies,
        'best_comments': best_combined,
        'comment_form': CommentForm(),  # 댓글 폼 추가
        'reply_form': CommentReplyForm(),  # 대댓글 폼 추가
        'user_profile':user_profile,
    }
    # print('comme/nt',context)
    print(context['user_profile'],type(post.author))
    print(comments)
    
    return render(request, 'book/post_detail.html', context) 

def post_sort(request):
    print("sort")
    sort_option = request.GET.get('sort')
    category = request.GET.get('category')
    # 기본 정렬: 최신순
     # 기본적으로 모든 게시글을 가져오되, 카테고리가 선택된 경우 필터링
    print(category,'========================================')
    if category:
        print('its working?')
        posts = Post_information.objects.filter(category=category)
    else:
        posts = Post_information.objects.all()
    print(posts)
    if sort_option == 'views_desc':
            print('-view')
            posts = posts.annotate(like_count=Count('like_users')).order_by('-views')
    elif sort_option == 'views_asc':
            print("view")
            posts = posts.annotate(like_count=Count('like_users')).order_by('views')
    elif sort_option == 'likes_desc':
            print("-likes")
            # 좋아요 수를 기반으로 내림차순 정렬
            posts = posts.annotate(like_count=Count('like_users')).order_by('-like_count')
    elif sort_option == 'likes_asc':
            print("likes")
            # 좋아요 수를 기반으로 오름차순 정렬
            posts = posts.annotate(like_count=Count('like_users')).order_by('like_count')
    else:
            posts = posts.order_by('-created_at')
    
    # 페이지네이션 추가
    paginator = Paginator(posts, 10)  # 페이지 당 10개의 게시글
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    print(context)
    return render(request, 'book/index.html', context)


def save_comment(request, pk):  # 댓글 저장
    post = get_object_or_404(Post_information, pk=pk)
    user_id = request.session.get('username')

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            # 일반 댓글 처리
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.author = User_information.objects.get(username=user_id)
                new_comment.post = post
                new_comment.save()
                return redirect('post_detail', pk=pk)
            else:
                print(comment_form.errors)

        elif 'reply_submit' in request.POST:
            # 대댓글 처리
            print("대댓글")
            reply_form = CommentReplyForm(request.POST)
            if reply_form.is_valid():
                new_reply = reply_form.save(commit=False)
                new_reply.author = User_information.objects.get(username=user_id)
                print(request.POST)
                print(request)
                # 부모 댓글 또는 대댓글 ID 가져오기
                parent_comment_id = request.POST.get('parent_id')
                print(f"Received comment_id: {parent_comment_id}")
#                 너무 큰 허점이 있다.
# count 값이 곧 comment 디비의 값들의 개수이다. 
# 난 지금 parent_id하고 parent_reply_id를 똑같이 받아오는 중이다.

# 들어온 id값이 count보다 작거나 같다면 댓글 아래 대댓글을 달 수 있다. 하지만 
# 값이 커진다면 대댓글의 대댓글을 달수가 있는 것이다. 

# comment디비의 count값이 적으면 괜찮을 수도 있지만 값이 커지면 커지고 comment_reply를 달려고 할 경우에는 댓글이 이상한 곳에 달릴 경우가 생긴다.
                # post_comment=Comment.objects.filter(post_id=pk) # 현 게시판의 댓글 목록 반환+ 부모 댓글의 값들만 
                # count=Comment.objects.all().count()
                # print(count)
                # print(post_comment)
                # 결국엔 comment 내부에 값이 존재하지 않을때 reply값이 실행이 되어야 했던 거니까 try-except문을 사용함으로 해결

                try:
                    parent_comment = Comment.objects.get( id=parent_comment_id) 
                    new_reply.comment = parent_comment
                except Comment.DoesNotExist:
                    parent_reply_id = request.POST.get('parent_reply_id')
                    print(f"Received parent_reply_id: {parent_reply_id}")
                    if parent_reply_id:
                        parent_reply = get_object_or_404(Comment_Reply, id=parent_reply_id)
                        new_reply.parent = parent_reply
                
                # if parent_comment_id :# pk를 잘이용하면 될 것 같다. 해당 게시물내에 있는 댓글이어야 한다. 
                #     parent_comment = get_object_or_404(Comment, id=parent_comment_id)
                #     print(parent_comment)
                #     if parent_comment in post_comment:
                #         print("success")
                #         new_reply.comment = parent_comment
                #     else:
                #         # 대댓글의 대댓글 처리
                #         parent_reply_id = request.POST.get('parent_reply_id')
                #         print(f"Received parent_reply_id: {parent_reply_id}")
                #         if parent_reply_id:
                #             parent_reply = get_object_or_404(Comment_Reply, id=parent_reply_id)
                #             new_reply.parent = parent_reply
                            # while parent_reply.parent:  # 최상위 부모 댓글 찾기
                            #     parent_reply = parent_reply.parent
                            # new_reply.comment = parent_reply.comment  # 최상위 부모 댓글 설정
                
                new_reply.save()
                return redirect('post_detail', pk=pk)

    return redirect('post_detail', pk=pk)


def edit_comment(request,pk):
    try:
        print("parent")
        parent_comment = Comment.objects.get( id=pk) 
        print(parent_comment)
        if request.method == 'POST':
            #comment_form = CommentForm(request.POST)
            new_content = request.POST.get('content')
            print(new_content)
            parent_comment.content = new_content
            parent_comment.save()
            return redirect('post_detail', pk=parent_comment.post.id)
    except Comment.DoesNotExist:
        print("reply")
        parent_reply = Comment_Reply.objects.get( id=pk) 
        print(parent_reply)
        if request.method == 'POST':
           
            new_reply_content = request.POST.get('content')
            print(new_reply_content)
            parent_reply.content = new_reply_content
            parent_reply.save()
            
            try:
                # 우선 comment 필드에서 게시글 ID를 가져옴
                post_id = parent_reply.comment.post.id
            except AttributeError:
                # 만약 comment 필드가 None이면 parent 필드를 통해 게시글 ID를 가져옴
                post_id = parent_reply.parent.comment.post.id
            
            return redirect('post_detail',pk=post_id)
               #return render(request, 'book/comment_template.html', {'comment_r': parent_reply })
       
def delete_comment(request,pk):
    try:
        parent_comment = Comment.objects.get( id=pk) 
        if request.method == 'POST':
            parent_comment.delete()
            return redirect('post_detail',pk=parent_comment.post.id)
    except Comment.DoesNotExist:
        parent_reply = Comment_Reply.objects.get( id=pk) 
        if request.method == 'POST':
            parent_reply.delete()
            try:
                # 우선 comment 필드에서 게시글 ID를 가져옴
                post_id = parent_reply.comment.post.id
            except AttributeError:
                # 만약 comment 필드가 None이면 parent 필드를 통해 게시글 ID를 가져옴
                post_id = parent_reply.parent.comment.post.id
            return redirect('post_detail',pk=post_id)

def search_posts(request):
    print('searchpost')
    # query = request.GET.get('q')  # 검색어를 GET 요청에서 가져오기
    existing_query = request.session.get('search_query', None)
    new_query = request.POST.get('search-post') or request.GET.get('search-post')
    print("first query",existing_query,new_query)
    # 새로운 쿼리가 들어오면 세션에 저장
    if new_query and new_query != existing_query:
        request.session['search_query'] = new_query
        query = new_query
    else:
        query = existing_query
    
    # query = request.POST.get('search-post') or request.GET.get('search-post')
    results = []

    if query:
        # 제목 또는 내용에 검색어가 포함된 게시글 검색
        results = Post_information.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    print('searchbar',results)
    paginator = Paginator(results, 2)  # 페이지당 20개의 게시물을 표시합니다
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'results':1,
        'query': query,
    }
    print(context)
    print('checking',existing_query,new_query)
    return render(request, 'book/index.html', context)
# {'results': results, 'query': query}
# 내가 만들어서 적어본것     


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
from django.contrib.auth import authenticate, login
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
            request.session['user_id'] = user.id # 숫자값 받기 
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                print(f"UserProfile created for user ID: {user.id}")  # 프로필 생성 확인
            else:
                print(f"UserProfile already exists for user ID: {user.id}")  # 프로필이 이미 존재함
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
    user_id = request.session.get('user_id')
    print(f"User ID from session: {user_id}") 
    if request.method == 'POST' and request.FILES['profile_pic']:
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        uploaded_file_url = fs.url(filename)
        # 파일의 절대 경로 생성
        # 세션에 이미지 URL 저장
        try:
            # 사용자 ID로 UserProfile 가져오기
            user_profile,created = UserProfile.objects.get_or_create(user_id=user_id)
            user_profile.profile_image = uploaded_file_url  # 이미지 URL 저장
            user_profile.save()  # 변경사항 저장
        except UserProfile.DoesNotExist:
            print(f"No UserProfile found for user ID: {user_id}")  # 로그 출력
            # 사용자 프로필이 없는 경우에 대한 처리 추가
            return redirect('index')  # 적절한 리다이렉션
        return redirect('index')  # 적절한 리다이렉션 URL로 변경하세요.

    return redirect('index')  # GET 요청 시에도 리다이렉트  # 적절한 템플릿으로 변경하세요.

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
        form = PostForm(request.POST)
        
        
        post_id = request.POST.get('post_id')  # 숨겨진 필드로 게시물 ID를 받아옴
        print(post_id)
        if post_id:  # 수정 작업인 경우
            print("adujust")
            print(request.POST.get('title'))
            post = Post_information.objects.get(id=post_id)
            post.title = request.POST.get('title')
            post.category = request.POST.get('category')
            post.content = request.POST.get('content')
            post.status = request.POST.get('status')
            post.tag = request.POST.get('tag-input')
            post.author=  User_information.objects.get(username=user_id)
            post.created_at = timezone.now()  # 현재 시간으로 설정
            post.save()
            return redirect('index')
            
            
        
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
        

def edit_post(request, pk):
    #post = get_object_or_404(Post_information, pk=pk)
    post = Post_information.objects.get(id=pk)
    
    if request.method == 'POST':
        post.save()
        return render(request, 'book/edit_post.html', {'post': post})
     
   


def delete_post(request, pk):
    post = get_object_or_404(Post_information, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('index')  # 삭제 후 리디렉션


def post_like(request, pk):
    print('like')
    post = get_object_or_404(Post_information, pk=pk)
    user_id = request.session.get('username')
    print(request.user)
    
    user = User_information.objects.get(username=user_id)
    print(user)
    if post.like_users.filter(pk=user.pk).exists():
        print("cancel like button")
        post.like_users.remove(user)
        return redirect('post_detail', pk=pk)
    else:
        print('add like')
        post.like_users.add(user)
    # 이미 좋아요를 누른 경우
    # if Like.objects.filter(user=user).exists():
    #     print("cancel like button")
    #     # 좋아요 취소
    #     Like.objects.filter(user=user).delete()
    #     return redirect('post_detail', pk=pk)
    # print('press like')
    # # 좋아요 누르기
    # like = Like.objects.create(user=user)
    # like.save()
    return redirect('post_detail', pk=pk)
                
      #  , post=post

def comment_like(request,pk):
    print("commentlike")
    user_id = request.session.get('username')
    user = User_information.objects.get(username=user_id)
    try:
        comment = Comment.objects.get(id=pk)
        print(comment)
        if comment.comment_like_users.filter(pk=user.pk).exists():
            print("comemntcancel like button")
            comment.comment_like_users.remove(user)
           
        else:
            print('commentadd like')
            comment.comment_like_users.add(user)
        
        # comment_like_count = comment.comment_like_users.count()
        # context = {
        #     'comment_like_count': comment_like_count,
            
        # }
        # pk=comment.post.id
        # return render(request, 'book/post_detail.html', context)
        return redirect('post_detail', pk=comment.post.id)
    
    except Comment.DoesNotExist:
        print("commentreply")
        comment_reply = Comment_Reply.objects.get(id=pk) 
        try:
                # 우선 comment 필드에서 게시글 ID를 가
            post_id = comment_reply.comment.post.id
        except AttributeError:
                # 만약 comment 필드가 None이면 parent 필드를 통해 게시글 ID를 가져옴
            post_id = comment_reply.parent.comment.post.id
        print(comment_reply)
        if comment_reply.commentR_like_users.filter(pk=user.pk).exists():
            print("cpmmentReplycancel like button")
            comment_reply.commentR_like_users.remove(user)
        else:
            print('comment reply add like')
            comment_reply.commentR_like_users.add(user)
        
        
        return redirect('post_detail', pk=post_id)
    
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


