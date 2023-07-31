'''
Content Based Filtering
'''


'''
[ 설치 라이브러리 ]
pip install krwordrank
'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from django.conf import settings
book_data = settings.BOOK_DATA


'''
####### 장르 추천 #######
'''
def recommend_genre(isbn13, top=10):
    # book_data = data_load()
    
    counter_vector = CountVectorizer(ngram_range=(1,1))
    c_vector_genre = counter_vector.fit_transform(book_data['categoryId'])

    isbn13 = str(isbn13)
    target_cate = list( book_data.loc[ book_data["isbn13"] == isbn13 ]["categoryId"] )
    target_vector = counter_vector.transform(target_cate)

    similarity = cosine_similarity(c_vector_genre, target_vector)
    book_data["similarity"] = similarity

    title = book_data.loc[ book_data["isbn13"] == isbn13].iloc[0]["title"]
    remove_word = title.split(' ')[0]

    result = book_data.loc[ ~book_data["title"].str.contains(remove_word) ]

    result = result.sort_values(by=['similarity'], ascending=False).head(20)
    result = result[["title", "authorName", "link", "cover","isbn13"]]
    result = result.sample(4)
    result["cover"] = result["cover"].apply(lambda x : x.replace("coversum", "cover500"))
    result = result.to_dict("records")

    return result


'''
####### 작가가 쓴 다른 책 추천 #######
'''
def recommend_author(isbn13):

    # 특정 도서 인덱스
    target_book_index = book_data[book_data['isbn13'] == f'{isbn13}'].index.values

    # 그 인덱스의 authorId 추출
    author_id = book_data.loc[target_book_index, 'authorId']

    # 해당 authorId의 모든 책 추출
    result = book_data[book_data['authorId'] == author_id.values[0]]
    result = result[["title", "authorName", "link", "cover","isbn13"]]
    result["cover"] = result["cover"].apply(lambda x : x.replace("coversum", "cover500"))

    if len(result) > 3 :
        result = result.sample(4)

    result = result.to_dict("records")

    return result


'''
####### 비슷한 줄거리 책 추천 #######
'''
def keyword_recommend(isbn13):
    idx = int(book_data[book_data['isbn13']== f'{isbn13}'].index.values[0])

    # TF-IDF 벡터화 객체 생성
    tfidf_vectorizer = TfidfVectorizer()

    # 키워드 컬럼의 데이터를 TF-IDF 벡터로 변환
    tfidf_matrix = tfidf_vectorizer.fit_transform(book_data['keyword'])

    isbn13 = str(isbn13)
    target_keyword = list( book_data.loc[ book_data["isbn13"] == isbn13 ]["keyword"] )

    target_vector = tfidf_vectorizer.transform(target_keyword)
    similarity = cosine_similarity(tfidf_matrix, target_vector)
    book_data["similarity"] = similarity

    title = book_data.loc[ book_data["isbn13"] == isbn13].iloc[0]["title"]
    remove_word = title.split(' ')[0]
    result = book_data.loc[ ~book_data["title"].str.contains(remove_word) ]
    
    result = result.sort_values(by=['similarity'], ascending=False).head(20)

    result = result[["title", "authorName", "link", "cover","isbn13"]]
    result = result.sample(4)
    result["cover"] = result["cover"].apply(lambda x : x.replace("coversum", "cover500"))
    result = result.to_dict("records")

    return result