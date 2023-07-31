import sys
from book.models import Books
import random
# setting path
sys.path.append('../static')

from static.python.render_support import *

# Create your views here.
def index(request):

    return n_render(request,'quiz/index.html')

def get_books():
    #random_nums 안 range(start_index, end_index) : Books table의 시작, 끝 인덱스 연결
    random_nums = random.sample(range(1, 50259), 4)
    random_books = []

    for i in random_nums:
        book = Books.objects.get(id=i)
        book_info = {
            'title' : book.title,
            'cover' : book.cover,
            'id'    : book.pk,
            'isbn'    : book.isbn13,
            'author_name' : book.author_name,
            'description' : book.description,
        }
        random_books.append(book_info)
    return random_books

def prog(request):
    quests = []
    for i in range(6):
        gets = get_books()
        answer = random.choice(range(0, 4))
        quest_img = "/static/gen_imgs/img_" + gets[answer]['isbn'] + ".png"
        hint_img = gets[answer]['cover']
        ans = [
            {"name":gets[0]['title'],
            "author":gets[0]['author_name'],
            "point":0},
            {"name":gets[1]['title'],
            "author":gets[1]['author_name'],
            "point":0},        
            {"name":gets[2]['title'],
            "author":gets[2]['author_name'],
            "point":0},
            {"name":gets[3]['title'],
            "author":gets[3]['author_name'],
            "point":0},
        ]
        ans[answer]["point"] = 1
        quest = {
            "quest_img":quest_img,
            "hint_img":hint_img,
            "anss":ans,
        }
        quests.append(quest)
    
    data = {
        "quests" : quests,
    }
    return n_render(request,'quiz/prog.html', data)


def end(request):
    data = {
        "seq":request.POST['win_total'],
        "score":request.POST['win_point'],
    }
    return n_render(request,'quiz/end.html', data)