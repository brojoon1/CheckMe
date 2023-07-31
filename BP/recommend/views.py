import sys
import random

# setting path
sys.path.append('../static')

from static.python.render_support import *
from static.python.book_recommend import *
from .models import Genre

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login') + "?alert=로그인 이후에 이용하실 수 있습니다.")
    return n_render(request,'recommend/index.html')


def prog(request): # 52 genre 
    genres = ['한국소설','일본소설','영미소설','스페인/중남미소설',
'프랑스소설','독일소설','중국소설','러시아소설','세계의 소설',
'추리/미스터리소설','판타지/환상문학','역사소설','과학소설(SF)',
'호러.공포소설','무협소설','액션/스릴러소설','로맨스소설','한국에세이',
'외국에세이','동물에세이','명상에세이','심리치유 에세이','사진/그림 에세이',
'음식에세이','여행에세이','독서에세이','예술에세이','종교에세이',
'사랑/연애 에세이','노년을 위한 에세이','자연에세이','명언/잠언록',
'일기/편지','유머/풍자/우화','포켓에세이','작은 이야기 모음',
'명사에세이','성공','리더십','행복론','인간관계','힐링',
'정리/심플라이프','협상/설득/화술','프레젠테이션/회의','기획/보고',
'시간관리/정보관리','창의적사고/두뇌계발','취업/진로/유망직업',
'20대의 자기계발','여성의 자기계발','중년의 자기계발']
    book_selection = {}
    gen = []
    all_books = Genre.objects.all()
    available_books = list(all_books)

    for genre in genres:
        # 해당 장르를 포함하는 책들을 가져옴
        books_in_genre = all_books.filter(categories__icontains=genre)
        
        if books_in_genre.exists():
  
            # 사용 가능한 책들 중에서 임의의 책 선택
            selected_book = random.choice(books_in_genre)
            
            # 선택된 책의 필드 값을 가져와서 저장
            book_selection[genre] = {
                'name': genre,
                'keyword': 'keyword',
                'url': selected_book.cover,
                'isbn': selected_book.isbn13,
            }
            
            # 선택된 책을 사용 가능한 책들 리스트에서 제거
            available_books.remove(selected_book)
        else:
            book_selection[genre] = None

        gen.append(book_selection[genre])
    random.shuffle(gen)
    data = {
        'genres': gen,
    }

    return n_render(request,'recommend/prog.html', data)


def end(request):
    # 결과 페이지
    name = request.POST['name']
    isbn = request.POST['isbn']

    img = Genre.objects.filter(isbn13__icontains=isbn).values('cover')
    img = img[0]['cover']
    title = Genre.objects.filter(isbn13__icontains=isbn).values('title')
    title = title[0]['title']
    
    genre_name = name

    rg = recommend_genre(isbn)

    ra = recommend_author(isbn)

    kr = keyword_recommend(isbn)

    data = {
        "isbn" : isbn,
        "name": genre_name,
        "img" : img,
        "title" : title,
        "rg" : rg,
        "ra" : ra,
        "kr" : kr,
    }

    return n_render(request,'recommend/end.html', data)


def loading(request): # 로딩 페이지
    return n_render(request, 'recommend/loading.html')

