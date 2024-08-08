#입력을 받은 폼값을 디비로 옮기는 곳인가?
from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name']
