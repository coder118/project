from django.urls import path
from django.views.generic import TemplateView
from . import views # 현 디렉의 views.py파일을 임포트함 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    # path('book_writer/',views.book_writer,name='book_writer'),
    path('login/', views.login_view, name='login'),
    path('signup/',views.signup_view,name='signup'),
    
    
    path('get_name/', views.get_name, name='get_name'),
    path('success/', TemplateView.as_view(template_name='book/success.html'), name='success'),
    
    path('signup/check-duplicate/', views.check_duplicate, name='check_duplicate'),
    path('signup/successful_user/',views.successful_user,name='successful_user'),
    
    path('login/trying_to_login/',views.trying_to_login,name="trying_to_login"),
    path('logout/', views.logout_view, name='logout'),
    
    path('upload_profile_pic/', views.upload_profile_pic, name='upload_profile_pic'),#마찬가지 이미지 업로드 url임

    path('ranking_update/', views.ranking_update, name='ranking_update'),

    path('post_create/',views.post_view,name='post_view'),
    path('post_create/post_save/',views.post_save,name='post_save'),
    path('<int:pk>/post_like/',views.post_like, name = "post_like"),
    path('book/',views.post_sort,name="post_sort"),
    
    path('<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    
    path('<int:pk>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('<int:pk>/delete_comment/', views.delete_comment, name='delete_comment'),
    
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/comment/', views.save_comment, name='save_comment'),
    path('<int:pk>/comment_like/',views.comment_like, name = "comment_like"),
    # path('<int:pk>/comment_profile_image/',views.comment_profile_image,name="comment_profile_image"),
    path('post_upload_image/', views.post_upload_image, name='post_upload_image'),
    path('search_post', views.search_posts, name='search_posts'),


    path('my_post/',views.my_post_view, name='my_post_view'),
    # path('my_post_upload_profile_pic/', views.my_post_upload_profile_pic, name='my_post_upload_profile_pic'),#마찬가지 이미지 업로드 url임
    path('my_post_sort/',views.my_post_sort, name='my_post_sort'),
]
# 미디어 파일 제공을 위한 설정
if settings.DEBUG:  # DEBUG 모드에서만 미디어 파일을 제공
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)