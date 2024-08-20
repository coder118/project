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


class User_information(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False)  # 아이디
    password = models.CharField(max_length=100, null=False)               # 비밀번호
    nickname = models.CharField(max_length=100, unique=True, null=False)  # 닉네임
    birthdate = models.CharField(max_length=8, null=False)                # 생년월일 (YYYYMMDD)

    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 태그 이름

    def __str__(self):
        return self.name
    
class Post_information(models.Model):
    STATUS_CHOICES = [
        ('published', '공개'),
        ('unpublished', '비공개'),
    ]

    title = models.CharField(max_length=255, null=False)                  # 제목
    content = models.TextField(null=False)                                # 내용
    category = models.CharField(max_length=100, blank=True)               # 카테고리
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')  # 상태
    author = models.ForeignKey(User_information, on_delete=models.CASCADE)  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)                  # 작성일
    updated_at = models.DateTimeField(auto_now=True)                      # 수정일
    tags = models.ManyToManyField('Tag', blank=True)  # 태그 추가
    views = models.IntegerField(default=0)  #조회수
    
    def __str__(self):
        return self.title
    
    

class Comment(models.Model):
    post = models.ForeignKey(Post_information, related_name='comments', on_delete=models.CASCADE)  # 게시물과의 관계
    author = models.ForeignKey(User_information, on_delete=models.CASCADE)  # 작성자
    content = models.TextField(null=False)  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    likes = models.IntegerField(default=0)  # 좋아요 수
    
    def __str__(self):
        return f'{self.author.nickname}: {self.content[:20]}'

class Comment_Reply(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)  # 댓글과의 관계
    author = models.ForeignKey(User_information, on_delete=models.CASCADE)  # 작성자
    content = models.TextField(null=False)  # 대댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    likes = models.IntegerField(default=0)  # 좋아요 수

    def __str__(self):
        return f'{self.author.nickname}: {self.content[:20]}'

class Like(models.Model):
    user = models.ForeignKey(User_information, on_delete=models.CASCADE)  # 좋아요한 사용자
    comment = models.ForeignKey(Comment, related_name='comment_likes', null=True, blank=True, on_delete=models.CASCADE)  # 댓글과의 관계
    reply = models.ForeignKey(Comment_Reply, related_name='reply_likes', null=True, blank=True, on_delete=models.CASCADE)  # 대댓글과의 관계
    created_at = models.DateTimeField(auto_now_add=True)  # 좋아요 누른 시간

    def __str__(self):
        if self.comment:
            return f'{self.user.nickname} liked comment: {self.comment.content[:20]}'
        if self.reply:
            return f'{self.user.nickname} liked reply: {self.reply.content[:20]}'