import sys
 
# setting path
sys.path.append('../static')

from static.python.render_support import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Books
from static.python.book_recommend import *

# Create your views here.
def list(request):
    '''검색 기능'''
    search_query = ''
    try:
        search_query = request.GET['search_query']
    except:
        search_query = ''
    
    data = {
        "search_query" : search_query,
    }
        
    return n_render(request,'book/list.html', data)

def list_child(request): # 순차적 검색기능
    count = int(request.GET['count'])
    search_query = request.GET['search_query']
    
    books = Books.objects.filter(
        Q(title__icontains=search_query) |
        Q(author_name__icontains=search_query) |
        Q(category_name__icontains=search_query)
    )[count:count+12]
    
    for book in books :
        cover_url = book.cover
        cover_url = cover_url
        book.cover = cover_url
    
    message = ''
    if len(books) == 0:
        # 검색결과가 없는경우
        message = '찾으시는 결과가 없습니다.'
        
    elif search_query == "바보":
        # 이 외 예외상황
        message = '유효하지 않은 결과입니다.'
        
    data = {
        "books" : books,
        "message" : message,
        "count" : count,
    }
    
    return n_render(request,'book/list_child.html', data)

def detail(request, isbn): # 상세 페이지
    
    #-------------------------------book query------------------------
    book_info = get_object_or_404(Books, isbn13 = isbn)
    categories = book_info.category_name.replace("[", "").replace("]", "").replace("'", "")  # [ ] ' 제거
    new_categories = []
    
    def remove_partial_elements(lst):
        result = []
        for i in range(len(lst)):
            element = lst[i]
            is_partial = False
            for j in range(len(lst)):
                if i != j and element in lst[j]:
                    is_partial = True
                    break
            if not is_partial:
                result.append(element)
        return result
    
    new_categories = remove_partial_elements(categories.split(','))


    #-------------------------AI recommend part-------------------------------
    
    rg = recommend_genre(isbn)
    ra = recommend_author(isbn)
    kr = keyword_recommend(isbn)

    #------------------------------data-------------------------
    data = {
        'book_data' : book_info,
        'categories': new_categories,
        "rg" : rg,
        "ra" : ra,
        "kr" : kr,
    }
    return n_render(request,'book/detail.html', data)