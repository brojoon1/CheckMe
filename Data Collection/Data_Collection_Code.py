import requests
import json
import time
import pandas as pd
from bs4 import BeautifulSoup

'''
[ 장르 변경 URL에 CID 번호만 변경하면 됨 ]
소설 CID = 112011
에세이 CID = 55889
자기계발 CID = 336
'''

def monthly_best_books(year, month, page):
    # 소설 URL 예시
    url = f'https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=MonthlyBest&BranchType=1&CID=112011&Year={year}&Month={month}&Week=1&page={page}&cnt=1000&SortOrder=1'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.select('.ss_book_list li a.bo3 b')

    books_list = []

    for book in books:
        books_list.append(book.text)

    return books_list

monthly_bests = []

for year in range(1999,2024):
    if year < 2023:
        for month in range(1,13):
            for page in range(1, 21):
                books = monthly_best_books(year, month, page)
                monthly_bests.extend(books)
    else:
        # 2023년은 6월까지만 존재하기 때문
        for month in range(1,7):
            for page in range(1, 21):
                books = monthly_best_books(year, month, page)
                monthly_bests.extend(books)

# 제목 중복 제거
monthly_bests = set(monthly_bests)


key = '자신의 API KEY'

# 소설 도서 제목으로 상품 검색
def novel_title_search(title):

    url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={key}"
    query = f"&Query={title}"

    option = f"&CategoryId=112011&QueryType=Keyword&MaxResults=200&start=1&SearchTarget=Book&output=js&Version=20131101"

    url_query = url + query + option

    #request 보내기
    response = requests.get(url_query)

    #받은 response를 json 타입으로 바뀌주기
    response_json = json.loads(response.text)

    df = pd.DataFrame(response_json["item"])

    return df

book_data = pd.DataFrame()

for title in monthly_bests:
    # 알라딘 API 지속적인 요청 시 오류 발생 방지
    time.sleep(0.5)
    # 책 제목으로 상품 검색 시 맨 위 도서 정보만 담음
    df = novel_title_search(title).head(1)
    book_data = pd.concat([book_data, df], ignore_index=True)

# 소설이 아닌 장르 거르기
# ex) '어린왕자' 검색 시, 어린왕자 책이 검색이 되겠지만, 예를 들어 같은 책 제목인 자기계발의 '어린왕자' 이 검색되었을 수도 있음.
''' 
알라딘 상품 카테고리 ID 문서를 참조하여 작성
상품 카테고리 ID 문서 참조 링크
https://image.aladin.co.kr/img/files/aladin_Category_CID_20210927.xls
'''
novel_id = [1, 50930, 89481, 89482, 50922, 52650, 50935, 51126, 51125, 50932, 50925, 51055, 51036, 51032, 52652, 51044, 51023, 51040, 50920, 50933, 50929, 50919, 50918, 50996, 50998, 50923, 50926, 51067, 51062, 51058, 51065, 51245, 51242, 51239, 51120, 51122, 50921, 50917, 50994, 50993, 50931, 112011, 97456, 103696, 103697, 103700, 105277, 105280,105276, 105278, 105279, 105281, 105282, 105283, 105284, 103701, 103702, 103703, 103704, 103705, 103706, 105285, 105286, 105287, 105288, 105289, 105290, 105291, 105292,105293, 105294, 105295, 105296, 105297, 105298, 105299, 105300, 105301, 105302, 103707, 103708, 103709, 103710, 103711, 105303, 105304, 105305, 105306, 105307, 105308, 105309, 105310, 105311, 103712, 103713, 103714, 103715, 103716, 103717, 103718, 103719, 103720, 103721, 107190, 107191, 107182, 107183, 107184, 107185, 107186, 107187, 107188, 103736, 103737, 103722, 103723, 103724, 103725, 103726, 103727, 103728, 103729, 103730, 103731, 103732, 103733, 103734, 103735, 103738, 105317, 105318, 105312, 105313, 105314, 105315, 105316, 108992, 103739, 103740, 103741, 103742, 103743, 103744, 103745, 103746, 103747, 103748, 103749, 105319, 105320, 105321, 105322, 105323, 105324, 105325, 105326, 105327, 105328, 103750, 103751, 78464, 78467, 35597, 78472, 78473, 78475, 104768]

novel_df = book_data[book_data['categoryId'].isin(novel_id)]

# adult = true 삭제 (성인용 소설 제거)
novel_df = novel_df[novel_df['adult'] != True]

# 소설 isbn컬럼만 추출
novel_isbn = list(novel_df['isbn13'])



def premium_search(isbn13):

    key = '자신의 API KEY'
    BASE_URL   = f"http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey={key}"
    ITEM_ID = f"&ItemId={isbn13}"
    OUTPUT = "&output=js"
    VERSION = "&Version=20131101"
    OPT_RESULT = "&OptResult=ratingInfo,bestSellerRank,previewImgList,authors,fulldescription,fulldescription2,Toc,Story,categoryIdList,mdrecommend,phraseList"

    URL = BASE_URL + ITEM_ID + OUTPUT + VERSION + OPT_RESULT

    response = requests.get(URL)
    response = json.loads(response.text)

    df = pd.DataFrame(response['item'])

    # subInfo 요소들 컬럼으로 만들어 저장
    df['bestSellerRank'] = df['subInfo'].apply(lambda x: x.get('bestSellerRank', ''))
    df['previewImgList'] = df['subInfo'].apply(lambda x: x.get('previewImgList', []))
    df['authors'] = df['subInfo'].apply(lambda x: x.get('authors', []))
    df['toc'] = df['subInfo'].apply(lambda x: x.get('toc', ''))
    df['story'] = df['subInfo'].apply(lambda x: x.get('story', ''))
    df['phraseList'] = df['subInfo'].apply(lambda x: x.get('phraseList', []))
    df['ratingInfo'] = df['subInfo'].apply(lambda x: x.get('ratingInfo', []))
    df['packing'] = df['subInfo'].apply(lambda x: x.get('packing', []))


    df = df.drop('subInfo', axis=1)

    # categoryIdList 컬럼화
    df['categoryId'] = df['categoryIdList'].apply(lambda x: [item['categoryId'] for item in x] if len(x) > 0 else [])
    df['categoryName'] = df['categoryIdList'].apply(lambda x: [item['categoryName'] for item in x] if len(x) > 0 else [])

    # authors 컬럼화
    df['authorId'] = df['authors'].apply(lambda x: str(x[0]['authorId']) if len(x) > 0 else '')
    df['authorName'] = df['authors'].apply(lambda x: str(x[0]['authorName']) if len(x) > 0 else '')
    df['authorInfo'] = df['authors'].apply(lambda x: str(x[0]['authorInfo']) if len(x) > 0 else '')

    # ratingInfo 컬럼화
    df['ratingScore'] = df['ratingInfo'].apply(lambda x: x['ratingScore'] if 'ratingScore' in x else '')
    df['ratingCount'] = df['ratingInfo'].apply(lambda x: x['ratingCount'] if 'ratingCount' in x else '')

    # packing 컬럼화
    df['book_weight'] = df['packing'].apply(lambda x: x['weight'] if 'weight' in x else '')
    df['book_height'] = df['packing'].apply(lambda x: x['sizeHeight'] if 'sizeHeight' in x else '')
    df['book_width'] = df['packing'].apply(lambda x: x['sizeWidth'] if 'sizeWidth' in x else '')

    # authors 컬럼화
    df['phrase'] = df['phraseList'].apply(lambda x: [item['phrase'] for item in x] if len(x) > 0 else [])

    # 컬럼화 후 해당 컬럼 삭제
    df = df.drop('categoryIdList', axis=1)
    df = df.drop('authors', axis=1)
    df = df.drop('ratingInfo', axis=1)
    df = df.drop('packing', axis=1)
    df = df.drop('phraseList', axis=1)

    # 불필요한 컬럼 삭제
    df = df.drop(['author','pubDate','isbn','itemId','mallType','stockStatus','mileage','salesPoint','fixedPrice','customerReviewRank','bestSellerRank','previewImgList'], axis=1)

    return df

data = pd.DataFrame()

for i in novel_isbn:
    time.sleep(0.5)
    df = premium_search(i)
    data = pd.concat([data, df], ignore_index = True)