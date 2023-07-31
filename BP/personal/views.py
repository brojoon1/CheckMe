import sys
import random
import pandas as pd 
import pickle
import os 
import logging

# setting path
sys.path.append('../static')

from static.python.render_support import *
from book.models import Books
from django.db.models import Q
from django.shortcuts import redirect
from user.models import user_favor
# Create your views here.

def genre_load() :
    # 서버용 위치
    # file_path = '/home/ubuntu/one-one-project/BP/static/pkl_file/52genre.pkl'
    file_path = 'C:\\Users\\User\\Documents\\GitHub\\one-one-project\\BP\\static\\pkl_file\\52genre.pkl'

    with open(file_path, "rb") as file:
            genre_data = pickle.load(file)

    data_dict = genre_data.set_index("장르번호").to_dict()["장르"]

    return data_dict


def get_books(genre, count):
    genre_books = Books.objects.filter(category_id__icontains=genre).order_by('?')[:count]
    books = []
    for book in genre_books :
        cover_url = book.cover
        cover_url = cover_url
        book_info = {
            'title' : book.title,
            'cover' : cover_url,
            'id'    : book.pk,
            'author_name' : book.author_name,
            'description' : book.description,
            'isbn13' : book.isbn13,
        }
        books.append(book_info)

    return books

def index(request) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login') + "?alert=로그인 이후에 이용하실 수 있습니다.")
    
    try:
        username=str(request.user)
        p_genres = user_favor.objects.get(username=username)
    except user_favor.DoesNotExist:
        return HttpResponseRedirect(reverse('user:select') + "?alert=좋아하시는 장르를 선택 하신 후에 추천해 드릴게요.")
    
    data_dict = genre_load()
    gen1 = int(p_genres.favor1)
    gen2 = int(p_genres.favor2)
    gen3 = int(p_genres.favor3)
    gen4 = int(p_genres.favor4)
    genres = [
        {'name': data_dict[gen1], 'category_name': data_dict[gen1], 'books': get_books(gen1, 4)},
        {'name': data_dict[gen2], 'category_name': data_dict[gen2], 'books': get_books(gen2, 4)},
        {'name': data_dict[gen3], 'category_name': data_dict[gen3], 'books': get_books(gen3, 4)},
        {'name': data_dict[gen4], 'category_name': data_dict[gen4], 'books': get_books(gen4, 4)},
    ]
    
    # random.shuffle(genres)

    context = {'ganres': genres}
    return n_render(request, 'personal/index.html', context)

def loading(request):
    return n_render(request, 'personal/loading.html')