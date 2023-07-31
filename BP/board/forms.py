from django import forms
from board.models import Posts, Comment, BookReports, BookComment
class PostsForm(forms.ModelForm) :
    class Meta :
        model = Posts
        fields = ['title', 'content','img_src'] # 나중에 user_id, img_src, 추천 수 등등 필요함
        labels = {
            'title' : '제목',
            'content' : '내용',
            'img_src' : '이미지'
        }

class CommentForm(forms.ModelForm) :
    class Meta :
        model = Comment
        fields = ['content'] # 나중에 user_id, 등등 필요함
        labels = {
            'content' : '답변 내용',
        }
        
class BookReportForm(forms.ModelForm) :
    class Meta :
        model = BookReports
        fields = ['title', 'content', 'img_src']
        labels = {
            'title' : '제목',
            'content' : '내용',
            'img_src' : '이미지'
        }
        
class BookCommentForm(forms.ModelForm) :
    class Meta :
        model = BookComment
        fields = ['content']
        labels = {
            'content' : '댓글 내용'
        }