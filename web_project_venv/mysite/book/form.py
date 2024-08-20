#입력을 받은 폼값을 디비로 옮기는 곳인가?
from django import forms
from .models import Person,User_information,Post_information, Comment, Comment_Reply
from django.contrib.auth.hashers import make_password

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name','age']

class UserForm(forms.ModelForm):
    class Meta:
        model = User_information
        fields = ['username', 'password', 'nickname', 'birthdate']
        
    # def save(self, commit=True): 
    #     user = super(UserForm, self).save(commit=False)
    #     # 비밀번호 해시화
    #     user.password = make_password(self.cleaned_data['password'])
    #     print(user.password)
    #     if commit:
    #         user.save()
    #     return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post_information
        fields = ['title', 'content', 'category', 'status','tags']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment_Reply
        fields = ['content']    