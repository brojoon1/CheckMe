<br> 

---

# 📃 목차
- [📚 요약](#📚-요약)
    - [📌 요약 모델의 필요성](#📌-요약-모델의-필요성)
    - [📌 요약 모델 선정 배경](#📌-요약-모델-선정-배경)
    - [📌 요약 모델 사용 코드](#📌-요약-모델-사용-코드)
    
<br>

- [📃 참고자료](#📃-참고자료)

<br>
<br>
<br>

---
---
# 📚 요약

## 📌 요약 모델의 필요성 
1. Stable Diffusion의 입력 프롬프트에 텍스트 전달 시 길이 제한

    : 텍스트 기반 이미지 생성(txt2img) 모델 Stable Diffusion 의 Prompt에 간결한 내용을 전달하기 위함

2. 번역 모델 사용 시, 글자 수 제한 

    : Stable Diffusion의 Prompt는 영어 입력만 지원함

    **=>** 번역 모델의 input 값 길이 제한으로 인함

<br>
<br>


## 📌 요약 모델 선정 배경
1. 요약 방식은 크게 추출 요약, 생성 요약 두 가지로 나뉨


    - 추출 요약과 생성 요약의 특징 비교<sup>[[1]](#footnote_1)</sup>

|   |**추출 요약**|**생성 요약**|
|:---:|:---:|:---:|
|입력 문장을 그대로 사용하는가?|O|X|
|정보 누락 정도|많음|적음|
|컴퓨팅 리소스 필요량|적음|많음|
|학습 시간 필요량|적음|많음|


&emsp;&emsp;✅ 정보의 누락을 줄이기 위해 **생성 요약 모델 채택**

<br>
<br>

2. SKTBrain 언어 모델 비교<sup>[[2-1]](#footnote_2-1)</sup>
    
    -  KoGPT2
    
        : 디코더로만 구성되어 자연어 생성에만 강점이 있음

    -  KoBART
    
        : 인코더-디코더로 구성되어 자연어의 이해와 생성 모두에 강점이 있고, 일반적으로 요약에서 가장 강력한 모델로 알려져 있음<sup>[[2-2]](#footnote_2-2)</sup>
    
&emsp;&emsp;✅ **KoBART 채택**

<br>
<br>

3. pre-trained가 추가적으로 더 된 KoBART 모델을 요약에 사용
- Huggingface의 transformers 라이브러리를 이용하여 아래 3가지 모델 사용
    1. `gogamza/kobart-summarization`<sup>[[3]](#footnote_3)</sup>

    2. `gogamza/kobart-base-v1`<sup>[[4]](#footnote_4)</sup>

    3. `ainize/kobart-news`<sup>[[5]](#footnote_5)</sup> 

- 세 가지 모델 중 요약 결과 길이가 특정 모델이 평균적으로 짧다기 보다 각 도서 데이터마다 다름

&emsp;&emsp;✅ **각각의 도서 데이터에서** 요약 전 문장<sup>\**</sup>과 세 가지 모델 사용 결과 중 **가장 짧은 요약 결과를 추출하는 방식 채택**

&emsp;&emsp;&emsp;<small>\** 간혹 요약 모델의 결과보다 요약 전 텍스트가 더 짧은 경우 있음</small>


<br>
<br>

## 📌 요약 모델 사용 코드
<br>

- **코드 작성 환경: 구글 colab CPU**

- 구글 colab의 하드웨어 가속기 GPU T4 사용 시 소요 시간 대략 20~30% 단축


<br>
<br>

### **필요 라이브러리 및 모델 불러오기**
- 네트워크 상태에 따라 다르지만, 대략 1분 20초간 실행
<small>

```python
# 요약 모델 불러오기

# 불러오는 시간 측정
%%time

!pip install transformers
!pip install transformers[sentencepiece]

from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import torch

import pandas as pd

# 요약 모델1 불러오기
tokenizer1 = PreTrainedTokenizerFast.from_pretrained("gogamza/kobart-summarization")
model1 = BartForConditionalGeneration.from_pretrained("gogamza/kobart-summarization")

# 요약 모델2 불러오기
tokenizer2 = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model2 = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

# 요약 모델3 불러오기
tokenizer3 = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
model3 = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")
```
</small>

<br>

### **도서 데이터 불러오기**
- `df` : 불용어 처리 등의 텍스트 전처리까지 마친 도서 데이터
<small>

```python
# 도서 데이터가 csv 파일인 경우
df = pd.read_csv('파일경로 및 파일명') 

# 도서 데이터가 pickle 파일인 경우
df = pd.read_pickle('파일경로 및 파일명')

# 불러온 데이터프레임 확인
df
```
</small>
<br>

- 데이터 레코드와 칼럼 개수 확인
<small>

```python
df.shape
```
</small>
<br>

- 요약에 사용할 칼럼 확인
<small>

```python
list(df)
```
</small>
<br>

- 요약에 사용할 칼럼의 데이터 확인
<small>

```python
df[['description']] # 'description' 칼럼을 사용할 경우의 코드
```
</small>

<br>

### **요약 전 df**
- 간혹 요약 모델의 결과보다 요약 전 텍스트가 더 짧은 경우 있어 비교용 df 생성
<small>

```python
temp = pd.DataFrame(columns=['text','sum_txt','len'])
temp['text'] = df['description']
temp['sum_txt'] = df['description']
temp['len'] = temp['text'].apply(lambda text: len(text))

temp[['sum_txt','len']]
```
</small>
<br>

### **요약**
### **모델1로 요약**
- 네트워크 상태에 따라 다르지만 대략 200자 이내 텍스트 데이터 30개 처리 시 약 3분 이상 소요
<small>

```python
# 실행 시간 측정
%%time

temp1 = pd.DataFrame(columns=['text','sum_txt1','len1'])
temp1['text'] = df['description']

for i, text in enumerate(temp1['text']):

    input_ids = tokenizer1.encode(text)

    input_ids = [tokenizer1.bos_token_id] + input_ids + [tokenizer1.eos_token_id]
    input_ids = torch.tensor([input_ids])


    summary_text_ids = model1.generate(
        input_ids=input_ids,
        bos_token_id=model1.config.bos_token_id,
        eos_token_id=model1.config.eos_token_id,
        length_penalty=1.0, # 길이에 대한 penalty값. 1보다 작은 경우 더 짧은 문장을 생성하도록 유도하며, 1보다 클 경우 길이가 더 긴 문장을 유도
        max_length=128,     # 요약문의 최대 길이 설정
        min_length=32,      # 요약문의 최소 길이 설정
        num_beams=4,        # 문장 생성시 다음 단어를 탐색하는 영역의 개수
    )


    sum_txt = tokenizer1.decode(summary_text_ids[0], skip_special_tokens=True)

    temp1['sum_txt1'][i] = sum_txt
    temp1['len1'][i] = len(sum_txt)

# 요약 결과 확인
temp1[['sum_txt1','len1']]
```
</small>
<br>

### **모델2로 요약**
- 네트워크 상태에 따라 다르지만 대략 200자 이내 텍스트 데이터 30개 처리 시 약 3분 이상 소요
<small>

```python
# 실행 시간 측정
%%time

temp2 = pd.DataFrame(columns=['text','sum_txt2','len2'])
temp2['text'] = df['description']

for i, text in enumerate(temp2['text']):

    raw_input_ids = tokenizer2.encode(text)
    input_ids = [tokenizer2.bos_token_id] + raw_input_ids + [tokenizer2.eos_token_id]

    summary_ids = model2.generate(torch.tensor([input_ids]),
                                 num_beams=4,
                                 max_length=128,
                                 eos_token_id=1)
    sum_txt = tokenizer2.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

    temp2['sum_txt2'][i] = sum_txt
    temp2['len2'][i] = len(sum_txt)

# 요약 결과 확인
temp2[['sum_txt2','len2']]
```
</small>
<br>

### **모델3으로 요약**
- 네트워크 상태에 따라 다르지만 대략 200자 이내 텍스트 데이터 30개 처리 시 약 4분 이내 소요
<small>

```python
# 실행 시간 측정
%%time

temp3 = pd.DataFrame(columns=['text','sum_txt3','len3'])
temp3['text'] = df['description']

for i, text in enumerate(temp3['text']):
    input_ids = tokenizer3.encode(text, return_tensors="pt")

    summary_text_ids = model3.generate(
        input_ids=input_ids,
        bos_token_id=model3.config.bos_token_id,
        eos_token_id=model3.config.eos_token_id,
        length_penalty=1.0, 
        max_length=128,
        min_length=32,
        num_beams=4,
    )

    sum_txt = tokenizer3.decode(summary_text_ids[0], skip_special_tokens=True)

    temp3['sum_txt3'][i] = sum_txt
    temp3['len3'][i] = len(sum_txt)

# 요약 결과 확인
temp3[['sum_txt3','len3']]
```
</small>
<br>

### **가장 짧은 요약문으로 df 생성**
-  모델 1, 2, 3의 실행 결과와 요약 전 문장 길이 네 가지 중 가장 짧은 요약 데이터를 추출하여 df 생성
<small>

```python
# 실행 시간 측정
%%time

comp = temp.copy(deep=True) # warning 뜨지만 이상 없음

# 가장 짧은 데이터 비교 추출
for i in range(len(comp)):
    comp['sum_txt'][i] = min(temp['text'][i], temp1['sum_txt1'][i], temp2['sum_txt2'][i], temp3['sum_txt3'][i], key=len)

# 추출 결과 확인
comp['title'] = df['title']
comp['len'] = comp['sum_txt'].apply(len)
comp[['sum_txt','len']]
```
</small>
<br>

- 번역을 같은 파일에 이어서 진행한다면 여기서 부터 실행 생략
### **결과 데이터 저장**
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
<b id="footnote_1">[[1]](#📌-요약-모델-선정-배경)</b> <https://cocosy.tistory.com/78>

<b id="footnote_2-1">[[2-1]](#📌-요약-모델-선정-배경)</b> <https://dspace.ewha.ac.kr/handle/2015.oak/262132>

<b id="footnote_2-2">[[2-2]](#📌-요약-모델-선정-배경)</b> <https://chloelab.tistory.com/34>

<b id="footnote_3">[[3]](#📌-요약-모델-선정-배경)</b> <https://huggingface.co/gogamza/kobart-summarization>

<b id="footnote_4">[[4]](#📌-요약-모델-선정-배경)</b> <https://huggingface.co/gogamza/kobart-base-v1>

<b id="footnote_5">[[5]](#📌-요약-모델-선정-배경)</b> <https://huggingface.co/ainize/kobart-news>

<br>
<br>

&emsp;⏫ [목차로 올라가기](#📃-목차)
