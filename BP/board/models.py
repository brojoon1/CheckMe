from django.db import models
from user.models import User
from book.models import Books

# Create your models here.
class Posts(models.Model) : # 게시글 기능
    title = models.CharField(max_length = 100)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    img_src = models.ImageField(upload_to='images/post/', blank=True, null=True)
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    create_date = models.DateTimeField()
    user_nickname = models.CharField(max_length=16, null=True)

    def __str__(self) : 
        return self.title
    
class Comment(models.Model) : # 댓글 기능
    comment = models.ForeignKey(Posts, on_delete = models.CASCADE)
    content = models.CharField(max_length = 500)
    create_date = models.DateTimeField()
    user_nickname = models.CharField(max_length=16, null=True)

    
class BookReports(models.Model) : # 독후감 기능
    title = models.CharField(max_length = 100)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    img_src = models.ImageField(upload_to='images/bookreport/', blank=True, null=True)
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    create_date = models.DateTimeField()
    user_nickname = models.CharField(max_length = 16, null=True)
    book_title = models.TextField(null=True)
    def __str__(self) : 
        return self.title
    
class BookComment(models.Model) : # 독후감 댓글 기능
    comment = models.ForeignKey(BookReports, on_delete = models.CASCADE)
    content = models.CharField(max_length = 500)
    create_date = models.DateTimeField()
    user_nickname = models.CharField(max_length=16, null=True)
