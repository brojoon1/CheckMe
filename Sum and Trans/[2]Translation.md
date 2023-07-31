<br>

---

# 📃 목차
- [📚 번역](#📚-번역)
    - [📌 번역 모델의 필요성](#📌-번역-모델의-필요성)
    - [📌 번역 모델 선정 배경](#📌-번역-모델-선정-배경)
    - [📌 번역 모델 사용 코드](#📌-번역-모델-사용-코드)

<br>

- [📃 참고자료](#📃-참고자료)

<br>
<br>
<br>

---
# 📚 번역

## 📌 번역 모델의 필요성
- Stable Diffusion의 입력 프롬프트에 한국어 입력 미지원

- 번역 API의 제한 사항

    - 비용 발생

    - 일일 사용량 제한
    
    - 위 제한 사항의 이유로 번역 API의 의존도를 낮추고자 번역 모델을 사용하고자 함.

<br>
<br>

## 📌 번역 모델 선정 배경

- Huggingface의 transformers pipeline을 이용하여 아래 2가지 pre-trained 한국어 모델 사용

    1. `Helsinki-NLP/opus-mt-ko-en`<sup>[[2-1]](#footnote_2-1)</sup> 
    
        - Huggingface에서 검색한 ko-en모델 중 2023년 5월에 다운로드 166k로 최대 6k인 사용량 2위 이하 모델에 비해 압도적 

        - ko-en 외에도 1400개 이상의 번역 언어를 구축한 안정적인 모델<sup>[[2-2]](#footnote_2-2)</sup>

    2. `circulus/kobart-trans-ko-en-v2`<sup>[[3]](#footnote_3)</sup> 
    
        - KoBART는 인코더-디코더로 구성되어 자연어의 이해와 생성 모두에 강점이 있으므로<sup>[[4]](#footnote_4)</sup> 번역에도 탁월할 것으로 예상

        - ko-en모델 중 사용량 전체 3위, KoBART 기반 모델 중 1위이지만 2023년 5월 사용량 1위 모델이 사용량 166k인 것에 비해 현저히 낮은 2.3k이며 모델 성능 점수에 대한 언급이 없어 안정성 우려

        - 도서의 description의 요약 텍스트 길이가 50~150자인 것에 비해 Default값이 max_length=20로 설정된 것을 보아 안정성 우려

        - 번역 결과 누락되는 부분 다수 존재

&emsp;&emsp;✅ **`Helsinki-NLP/opus-mt-ko-en` 채택**

<br>
<br> 

## 📌 번역 모델 사용 코드
<br>

- **코드 작성 환경: 구글 colab CPU**

- 구글 colab의 하드웨어 가속기 GPU T4 사용 시 소요 시간 대략 20~30% 단축

<br>
<br>

- 필요 라이브러리 및 모델 불러오기
<small>

```python
# 번역 모델 불러오기

# 불러오는 시간 측정
%%time

!pip install transformers
!pip install transformers[sentencepiece]

import torch
import pandas as pd

from transformers import pipeline

# 요약과 같은 파일이라면 이 부분만 실행
!pip install sacremoses

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-ko-en")
```
</small>
<br>

- 요약된 데이터 불러오기
    - 요약과 같은 파일에서 실행한다면 생략
<small>

```python
# 도서 데이터가 csv 파일인 경우
comp = pd.read_csv('파일경로 및 파일명') 

# 도서 데이터가 pickle 파일인 경우
comp = pd.read_pickle('파일경로 및 파일명')

# 불러온 데이터프레임 확인
comp
```
</small>
<br>

- 번역하기
    - len 칼럼은 한국어 요약문의 길이
<small>

```python
# 실행 시간 측정
%%time

comp['len'] = comp['sum_txt'].apply(len)
comp['en_txt'] = comp['sum_txt'].apply(lambda sum_txt: translator(sum_txt)[0]['translation_text'])
comp = comp[['title', 'sum_txt', 'len', 'en_txt']] # 칼럼 재배열
comp
```
</small>
<br>

- 결과 데이터 저장
<small>

```python
# csv 파일로 저장하는 경우
comp = pd.read_csv('파일경로 및 파일명') 
comp.to_csv('파일경로 및 파일명',index=False)

# pickle 파일로 저장하는 경우
import pickle

comp.to_pickle('파일경로 및 파일명')
```
</small>
<br>

- 저장 결과 확인
<small>

```python
# pickle 파일로 저장한 경우
df = pd.read_pickle('파일경로 및 파일명')

# csv 파일로 저장한 경우
df = pd.read_csv('파일경로 및 파일명') 

# 저장 결과 출력
df
```
</small>

<br>
<br>
<br> 

---
# 📃 참고자료
<b id="footnote_1">[[1]](#📌-번역-모델-선정-배경)</b> <https://jehyunlee.github.io/2023/02/20/Python-DS-128-transqual/>

<b id="footnote_2-1">[[2-1]](#📌-번역-모델-선정-배경)</b> <https://huggingface.co/Helsinki-NLP/opus-mt-ko-en>

<b id="footnote_2-2">[[2-2]](#📌-번역-모델-선정-배경)</b> <https://huggingface.co/Helsinki-NLP>

<b id="footnote_3">[[3]](#📌-번역-모델-선정-배경)</b> <https://huggingface.co/circulus/kobart-trans-ko-en-v2>

<b id="footnote_4">[[4]](#📌-번역-모델-선정-배경)</b> <https://dspace.ewha.ac.kr/handle/2015.oak/262132>


<br>
<br>

&emsp;⏫ [목차로 올라가기](#📃-목차)
