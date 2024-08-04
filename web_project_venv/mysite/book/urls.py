from django.urls import path

from . import views # 현 디렉의 views.py파일을 임포트함 

urlpatterns = [
    path('', views.index, name='index'),
    path('',views.book_writer,name='book_writer'),
    path('login/', views.login_view, name='login'),
    path('signup/',views.signup_view,name='signup')
]