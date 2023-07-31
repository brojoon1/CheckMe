from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    # 게시판 기능
    path('', views.posts, name = 'posts'),
    path('<int:posts_id>/', views.detail, name = 'detail'),
    path('<int:posts_id>/comment_create', views.comment_create, name = 'comment_create'),
    path('posts/create/', views.post_create, name = 'post_create'),
    
    path('posts/delete/<int:posts_id>', views.del_post, name = 'del_post'),
    
    path('posts/fix/<int:posts_id>', views.post_fix, name = 'post_fix'), 
    path('posts/delcom/<int:comment_id>', views.del_post_comment, name = 'del_post_comment'),
    # 독후감 기능
    path('bookreport/create', views.bookreport_create, name = 'bookreport_create'),
    path('bookreport/', views.bookreports, name = 'bookreports'),
    path('bookreport/<int:bookreports_id>/', views.bookreport_detail, name = 'bookreport_detail'),
    path('bookreport/<int:bookreports_id>/comment_create', views.bookreport_comment_create, name = 'bookreport_comment_create'),
    
    path('bookreport/search/', views.search, name='search'),

    path('bookreport/fix/<int:bookreports_id>', views.bookreport_fix, name = 'bookreport_fix'), 
    path('bookreport/fix/search/', views.search, name='fix_search'),

    path('bookreport/delete/<int:bookreports_id>', views.del_bookreport, name = 'del_bookreport'),
    path('bookreport/delcom/<int:BookComment_id>', views.del_bookreport_comment, name = 'del_bookreport_comment'), 
]
