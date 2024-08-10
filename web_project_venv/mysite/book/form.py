#입력을 받은 폼값을 디비로 옮기는 곳인가?
from django import forms
from .models import Person,User_information

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name','age']

class  UserForm(forms.ModelForm):
     class Meta:
        model = User_information
        fields = ['username', 'password', 'nickname', 'birthdate']