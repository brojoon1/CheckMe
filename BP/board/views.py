from static.python.render_support import *
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from .models import Posts, BookReports, Comment, BookComment
from django.utils import timezone
from .forms import PostsForm, CommentForm, BookReportForm, BookCommentForm
from django.core.paginator import Paginator
from .models import Books
from .models import User

app_name = 'board'

def posts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login') + "?alert=로그인 이후에 이용하실 수 있습니다.")    
    '''목록 출력'''
    # 
    page = request.GET.get('page','1') # 페이지
    
    # 조회
    posts_list = Posts.objects.order_by('-id')
    
    # 페이징 처리
    paginator = Paginator(posts_list, 20)
    page_obj = paginator.get_page(page)
    
    posts_list = Posts.objects.order_by('-id')
    
    context = {'posts_list' : page_obj}
    
    return n_render(request, 'board/list.html', context)
    
def detail(request, posts_id) :
    '''내용 출력'''
    post = get_object_or_404(Posts, id = posts_id)
    
    # 연관된 다른 posts 예제
    relative = []
    for i in range(5):
        relative.append([post.title +' 와 관련있는 다른 글' + str(i) , 'test_id'])
    
    context = {
        'post' : post,
        'relative': relative,
        
    }
    return n_render(request, 'board/detail.html', context)

def comment_create(request, posts_id) :
    '''답변 등록'''
    post = get_object_or_404(Posts, id = posts_id)
    
    if request.method == "POST" : # 전송방식 "POST"
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.create_date = timezone.now()
            comment.post = post
            comment.comment_id = posts_id
            comment.user_nickname = request.user.nickname
            comment.save()
            return redirect('board:detail', posts_id=post.id)
    else :
        form = CommentForm()
    context = {'post' : post, 'form' : form}
    return n_render(request, 'board/detail.html', context)

def post_create(request) :
    '''게시글 등록'''
    if request.method == 'POST' : # 전송방식 "POST"
        form = PostsForm(request.POST, request.FILES) # 전송방식 "POST"
        if form.is_valid():
            posts = form.save(commit = False)
            posts.create_date = timezone.now()
            posts.user_nickname = request.user.nickname
            posts.save()
            return redirect('board:posts')
    else :
        form = PostsForm()
    context = {'form' : form}
    return n_render(request, 'board/form.html', context)

def search(request):
    query = request.GET.get('query','')

    # 검색 쿼리 실행
    if query : 
        results = Books.objects.filter(title__icontains=query).values_list('title', flat=True)
    else :
        results = []
    return JsonResponse({'results': list(results)})


def search_results(request):
    keyword = request.GET.get('keyword', '')

    # 검색 쿼리 실행
    books = Books.objects.filter(title__icontains=keyword)

    return render(request, 'board/bookreport/search_results.html', {'books': books})

def bookreport_create(request) :
    '''독후감 등록'''
    if request.method == 'POST' : # 전송방식 "POST"
        form = BookReportForm(request.POST, request.FILES) # 전송방식 "POST"
        
        if form.is_valid():
            bookreport = form.save(commit = False)
            book_title = request.POST.get('book')
            book = Books.objects.get(title=book_title)
            book_id = book.id
            book_t = book.title
            bookreport.book_id = book_id
            bookreport.book_title=book_t
            bookreport.create_date = timezone.now()
            bookreport.user_nickname = request.user.nickname
            bookreport.save()
            return redirect('board:bookreports')
    else :
        form = BookReportForm()
    context = {'form' : form}
    return n_render(request, 'board/bookreport/form.html', context)

def bookreports(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login') + "?alert=로그인 이후에 이용하실 수 있습니다.")    
    '''독후감 목록 출력'''
    # 
    page = request.GET.get('page','1') # 페이지

    # 조회
    bookreports_list = BookReports.objects.order_by('-id')
    
    # 페이징 처리
    paginator = Paginator(bookreports_list, 20)
    page_obj = paginator.get_page(page)
    
    bookreports_list = BookReports.objects.order_by('-id')
    
    context = {'bookreports_list' : page_obj}
    
    return n_render(request, 'board/bookreport/list.html', context)

def bookreport_detail(request, bookreports_id) :
    '''독후감 내용 출력'''
    bookreport = get_object_or_404(BookReports, id = bookreports_id)
    
    # 연관된 다른 독후감 예제
    relative = []
    for i in range(5) :
        relative.append([bookreport.title +' 와 관련있는 다른 글' + str(i), 'test_id'])
        
    context = {
        'bookreport' : bookreport,
        'relative' : relative, 
    }
    return n_render(request, 'board/bookreport/detail.html', context)
    
def bookreport_comment_create(request, bookreports_id) :
    '''독후감 댓글 등록'''
    bookreport = get_object_or_404(BookReports, id = bookreports_id)
    
    if request.method == "POST" : # 전송방식 "POST"
        form = BookCommentForm(request.POST)
        if form.is_valid():
            bookcomment = form.save(commit = False)
            bookcomment.create_date = timezone.now()
            bookcomment.bookreport = bookreport
            bookcomment.comment_id = bookreports_id
            bookcomment.user_nickname = request.user.nickname
            bookcomment.save()
            return redirect('board:bookreport_detail', bookreports_id=bookreport.id)
    else :
        form = BookCommentForm()
    context = {'bookreport' : bookreport, 'form' : form}
    return n_render(request, 'board/bookreport/detail.html', context)

def post_fix(request, posts_id) :
    # 게시글 수정
    posts = get_object_or_404(Posts, id = posts_id)
    
    try : 
        post = Posts.objects.get(id = posts_id)
    except Posts.DoesNotExist : 
        return HttpResponseNotFound("게시물을 찾을 수 없습니다.")
    
    if posts.user_nickname == request.user.nickname : 
        if request.method == "POST" :
            form = PostsForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit = False)
                post.id = posts_id
                post.create_date = timezone.now()
                post.user_nickname = request.user.nickname
                post.save()
                return redirect('board:posts')
        else :
            form = PostsForm(initial={'title': post.title,
            'content': post.content,
            'img_src': post.img_src})
    
        context = {'form' : form}
        return n_render(request, 'board/form.html', context)
    else :
        return HttpResponseForbidden("글 수정 권한이 없습니다.")

def bookreport_fix(request, bookreports_id) :
    # 독후감 수정
    bookreports = get_object_or_404(BookReports, id = bookreports_id)
    
    try : 
        bookreport = BookReports.objects.get(id = bookreports_id)
    except BookReports.DoesNotExist : 
        return HttpResponseNotFound("독후감을 찾을 수 없습니다.")
    
    if bookreports.user_nickname == request.user.nickname : 
        if request.method == "POST" :
            form = BookReportForm(request.POST, request.FILES, instance=bookreport)
            if form.is_valid():
                bookreport = form.save(commit = False)
                bookreport.id = bookreports_id
                book_title = request.POST.get('book')
                book = Books.objects.get(title=book_title)
                book_id = book.id
                book_t = book.title
                bookreport.book_id = book_id
                bookreport.book_title=book_t
                bookreport.create_date = timezone.now()
                bookreport.user_nickname = request.user.nickname
                bookreport.save()
                return redirect('board:bookreports')
        else :
            form = BookReportForm(initial={'title': bookreport.title,
            'content': bookreport.content,
            'book_title' : bookreport.book_title,
            })
    
        context = {'form' : form}
        return n_render(request, 'board/bookreport/form.html', context)
    else :
        return HttpResponseForbidden("글 수정 권한이 없습니다.")
    
def del_post(request, posts_id) :
    # 게시판 삭제기능
    posts = get_object_or_404(Posts, id = posts_id)
    
    try : 
        post = Posts.objects.get(id = posts_id)
    except Posts.DoesNotExist : 
        return HttpResponseNotFound("게시물을 찾을 수 없습니다.")
    
    if posts.user_nickname == request.user.nickname : 
        post.delete()
        return redirect('board:posts')
    else : 
        #return n_render(request, 'board:list.html', {'error':'삭제할 수 없습니다.'})
        return HttpResponse("삭제할 수 없습니다.")
    
def del_bookreport(request, bookreports_id) : 
    # 독후감 삭제기능
    bookreports = get_object_or_404(BookReports, id = bookreports_id)
    
    try : 
        bookreport = BookReports.objects.get(id = bookreports_id)
    except BookReports.DoesNotExist : 
        return HttpResponseNotFound("게시물을 찾을 수 없습니다.")
    
    if bookreports.user_nickname == request.user.nickname : 
        bookreport.delete()
        return redirect('board:bookreports')
    else : 
        return HttpResponse("삭제할 수 없습니다.")
    
def del_post_comment(request, comment_id) :
    # 게시판 댓글 삭제기능
    comments = get_object_or_404(Comment, id = comment_id)
    try : 
        comment = Comment.objects.get(id = comment_id)
    except Comment.DoesNotExist : 
        return HttpResponseNotFound("댓글을 찾을 수 없습니다.")
    
    if comments.user_nickname == request.user.nickname : 
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else : 
        return HttpResponse("삭제할 수 없습니다.")
    
def del_bookreport_comment(request, BookComment_id) :
    # 독후감 댓글 삭제기능
    BookComments = get_object_or_404(BookComment, id = BookComment_id)
    
    try : 
        comment = BookComment.objects.get(id = BookComment_id)
    except BookComment.DoesNotExist : 
        return HttpResponseNotFound("댓글을 찾을 수 없습니다.")
    
    if BookComments.user_nickname == request.user.nickname : 
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else : 
        return HttpResponse("삭제할 수 없습니다.")