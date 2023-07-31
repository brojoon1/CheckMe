<a name="project-name"></a>

# 프로젝트 소개

## 프로젝트 정보
- 프로젝트명 :  책크미
  - Text2Img를 활용한 도서 추천 시스템   

- 배포 주소 : [나에게 맞는 책을 Check 하다](http://chaekme.com/)

- 개발 기간 : 23.05.30 ~ 23.07.06

- 소속 : AIVLE School 3기 AI 개발자 트랙 1반 1조

</br>

## Convention 규칙 
- 해당 프로제트는 아래 규칙에 따라 관리 되었습니다.
  - [Convention규칙](./.github/convention.md)

</br>
 
<a name="list"></a>

# 목차
- [상세설명](#프로젝트-상세설명)
- [팀구성원](#팀-구성원)
- [담당역할](#담당-역할)
- [세부사항](#세부-사항)

</br>

# 프로젝트 상세설명

### 1. 서비스 제작 및 필요성
- 한국의 성인 1인 독서량은 매년 꾸준히 감소하고 있다.
- 근본적인 문제 해결을 위해 책을 읽지 않는 사람들이 책을 읽을 수 있도록 AI의 생성 이미지를 활용한 도서 추천 서비스를 제공하고자 한다.


### 2. 활용 데이터 및 모델 

- 알라딘 API
  - 크롤링을 통한 베스트 셀러 정보 수집 
    - 1999년 ~ 2023년 6월 셋째주 베스트 셀러 정보 수집
  
  - 알라딘 API를 사용하여 도서에 대한 추가적인 정보 수집 
  - 데이터 수집 과정에 대한 자세한 정보는 수집 과정에 대한 문서 및 코드를 참고해주세요. 
  - [데이터 수집 과정 상세 보기](./Data%20Collection/Data_Collection.md)

   

- Stable Diffusion Image
  - 크롤링 및 알라딘 API를 사용하여 수집한 도서 정보를 토대로 이미지 생성
  - 책 정보에 대한 텍스트 요약 및 번역 작업 수행 
  - 약 5만 개의 책 데이터의 특징을 반영한 이미지 생성
    
    
- 🤗Hugging Face
  - Stable Diffusion 2.1
  - Kobart
  - Transformers


### 3. 개발툴 및 방법

- **Git hub**
  - Issue로 진행해야할 작업들에 대한 관리를 진행
  - Frontend, Backend, AI 별 담당자를 두고, branch를 개별 관리
  - 파트별 PR 과정시 상호 리뷰 및 상대방의 Merge를 통해 독자적인 행동 방지 

- **Figma**
  - 아이디에이션을 위해 사용

- **Google docs**
  - 과제 정의서 및 회의록등 문서 작업에 사용

- **Google Drive**
  - 공유 드라이브를 생성하여 데이터, 모델, 문서등 파일 관리에 사용

- **Google Colab**
  - 이미지 생성을 위한 텍스트의 요약, 번역 과정에 사용
  - Stable Diffusion을 사용한 이미지 생성

- **Micro Teams**
  - 비대면 미팅간에 사용하였습니다.

- **MySql**
  - DB 관리에 사용


</br>

# 팀 구성원

<table>
<tr>
    <td align="center"><a href="https://github.com/Pang-dachu"><img src="https://avatars.githubusercontent.com/u/54354769?v=4" width="100px;" alt="Pang-dachu"/>         <br /><sub><b>Pang-dachu</b><br>
    <td align="center"><a href="https://github.com/sangka9"><img src="https://avatars.githubusercontent.com/u/12123743?v=4" width="100px;" alt="sangka9"/>         <br /><sub><b>sangka9</b><br>
    <td align="center"><a href="https://github.com/geonura"><img src="https://avatars.githubusercontent.com/u/38072049?v=4" width="100px;" alt="geonura"/>         <br /><sub><b>geonura</b><br>
    <td align="center"><a href="https://github.com/ShrimFry"><img src="https://avatars.githubusercontent.com/u/43872943?v=4" width="100px;" alt="ShrimFry"/>         <br /><sub><b>ShrimFry</b><br>
</tr>
<tr>
    <td align="center"><a href="https://github.com/brojoon1"><img src="https://avatars.githubusercontent.com/u/81418195?v=4" width="100px;" alt="brojoon1"/>         <br /><sub><b>brojoon1</b><br>
    <td align="center"><a href="https://github.com/ParkRang"><img src="https://avatars.githubusercontent.com/u/104675938?v=4" width="100px;" alt="ParkRang"/>         <br /><sub><b>ParkRang</b><br>
    <td align="center"><a href="https://github.com/kiimnj"><img src="https://avatars.githubusercontent.com/u/124108719?v=4" width="100px;" alt="kiimnj"/>         <br /><sub><b>kiimnj</b><br>
</tr>


</table>

</br>

# 담당 역할

- Leader
  김인재

- Infra
  오상화

- Frontend
  박세민, 김형준, 박진우

- Backend
  나건우, 오상화, 박진우

- AI
  김인재, 김형준, 김나진


  </br>

  # 기술 스택

:computer: **Infra (  )**

:computer: **Front-End ( HTML / CSS / Java Script )**

:computer: **Back-End ( django / MySQL / AWS )**

:computer: **AI ( Stable Diffusion / krwordrank / Kobart / Transformers / Scikit Learn )**

<br>

<div align=center> 
<img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visual studio code&logoColor=white">
<img src="https://img.shields.io/badge/git hub-181717?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/html5-F7931E?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white">
<br>
<img src="https://img.shields.io/badge/amazon aws-232F3E?style=for-the-badge&logo=amazon aws&logoColor=white">
<img src="https://img.shields.io/badge/scikit learn-E34F26?style=for-the-badge&logo=scikit learn&logoColor=white">
<img src="https://img.shields.io/badge/google colab-F9AB00?style=for-the-badge&logo=google colab&logoColor=white">
<img src="https://img.shields.io/badge/google drive-4285F4?style=for-the-badge&logo=google drive&logoColor=white">
<img src="https://img.shields.io/badge/Stable Diffusion-99CC00?style=for-the-badge&logo=&logoColor=white">
<br>
<img src="https://img.shields.io/badge/KoBart-4A154B?style=for-the-badge&logo=&logoColor=white">
<img src="https://img.shields.io/badge/microsoft teams-6264A7?style=for-the-badge&logo=microsoft teams&logoColor=white">
<img src="https://img.shields.io/badge/Hugging face-FABC0C?style=for-the-badge&&logoColor=white">
<br>
