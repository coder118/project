from django.urls import path
from django.views.generic import TemplateView
from . import views # 현 디렉의 views.py파일을 임포트함 

urlpatterns = [
    path('', views.index, name='index'),
    path('',views.book_writer,name='book_writer'),
    path('login/', views.login_view, name='login'),
    path('signup/',views.signup_view,name='signup'),
    
    path('name/', views.get_name, name='get_name'),
    path('success/', TemplateView.as_view(template_name='book/success.html'), name='success'),
]