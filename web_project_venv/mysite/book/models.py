import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
#model.py라는 파일은 데이터 베이스를 만들어주는 장소라는 듯? 



class bookT(models.Model):
    book_Title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    def __str__(self):
        return self.book_Title
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now()- datetime.timedelta(days =1 )
    
class bookW(models.Model):
    bookt= models.ForeignKey(bookT,on_delete = models.CASCADE)
    book_Writer = models.CharField(max_length=200)
    vote = models.IntegerField(default = 0 )#이건 걍 기능 사용을 해보고 싶어서 
    
    def __str__(self):
        return self.book_Writer
    
 # 템플릿에서 정보를 입력받은 후에 저장할 데이터 베이스 생성   
class Person(models.Model):
    name = models.CharField(max_length=100,null=True)
    age = models.CharField(max_length=3,null=True)
    
    def __str__(self):
        return self.name
    
    