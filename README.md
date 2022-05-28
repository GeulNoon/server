# :green_book: 글눈 서비스
사용자가 원하는 지문으로 기초 문해력과 어휘력을 함께 학습할 수 있는 문제를 제공하는 서비스<p>
<p align="center"><img width="250" alt="logo" src="https://user-images.githubusercontent.com/68368589/170729953-c726f81e-06d4-4a29-befa-250460b7e5be.png"></p>

## :book: 소개
![main](https://user-images.githubusercontent.com/68368589/170729871-0cbe4874-fe08-4abf-aaac-038949800201.png)

## :file_folder: 레파지토리 소개
* Frontend <img src="https://img.shields.io/badge/React-61DAFB? style=flat&logo=React&logoColor=white"/><p>
* Bacekend <img src="https://img.shields.io/badge/Django-092E20? style=flat&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/Amazon-FF9900? style=flat&logo=Amazon&logoColor=white"/><p>
* Dev <img src="https://img.shields.io/badge/Python-3776AB? style=flat&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Colab-F9AB00? style=flat&logo=Goole Colab&logoColor=white"/> <img src="https://img.shields.io/badge/Numpy-013243? style=flat&logo=Numpy&logoColor=white"/> <img src="https://img.shields.io/badge/Jupyter-F37626? style=flat&logo=Jupyter&logoColor=white"/><p>

## :mag_right: 사용방법
1. 학습하기
  * 원하는 지문 제목 작성하고 입력하기
  * 모르거나 헷갈리는 단어 검색하며 지문 자세히 읽기
  * 읽은 지문을 바탕으로 3문장 또는 1문장으로 요약하기
  * 지문 속 단어문제 풀기
  * 지문 속 핵심단어 빈칸문제 풀기
  * 푼 문제 결과보기
2. 복습하기
  * 다시풀고 싶은 지문 선택하기
  * 선택한 지문 다시 학습하기
3. 학습결과
  * 학습결과 페이지를 통해 다양한 데이터 확인
    + 학습한 지문 수, 평균어휘 정답률, 평균지문 이해도, 학습통계, 학습이력
4. 내정보
  * 회원정보 수정
    + 이메일, 닉네임, 생년월일
  * 회원탈퇴

## :wrench: 시스템 아키텍쳐
![sys](https://user-images.githubusercontent.com/68368589/170730368-ce2bbaf0-17e8-440c-8dec-e10bf790784a.png)

## :pencil2: 포스터
![29팀_글눈_포스터_page-0001](https://user-images.githubusercontent.com/68368589/170729123-2c6637af-ad11-4996-a4e1-3d4450f4f360.jpg)

## :clapper: 시연영상 URL
https://youtu.be/ZMhYZTsl3Aw

## :computer: 사이트 URL
https://geulnoon.github.io/Frontend/

## :clap: 역할
팀원 | 역할 |
---- | ---- | 
전다윤<br>[DAYOON0836](https://github.com/DAYOON0836)| 1. <b>Sentence Transformer</b>를 이용한 직접 요약문과 KoBART/TextRank 생성 요약문 간의 텍스트 유사도 비교<br>2. <b>Sentence Transformer</b>를 이용한 KoBART 생성 요약문과 사용자 요약문 간의 텍스트 유사도 비교<br>3. 요약문제 채점 모델 개발<br>4. 백엔드(서버, DB)
|김소현<br>[zhtmahthgus](https://github.com/zhtmahthgus)| 1. <b>KoBART</b> 학습<br>2. <b>TextRank</b>를 이용한 지문 키워드 추출<br>3. 요약문제 출제 모델 개발<br>4. 프론트엔드
|이서경<br>[skldd](https://github.com/skldd)| 1. <b>kss</b>를 이용한 문장 토큰화<br>2. <b>Kkma</b>, <b>Komoran</b>, <b>Hannanum</b>, <b>Okt</b>, <b>Mecab</b>을 이용한 형태소 분석<br>3. 어휘문제 출제 모델 개발
|한소현<br>[sh329](https://github.com/sh329)| 1. <b>Kkma</b>, <b>Komoran</b>, <b>Hannanum</b>, <b>Okt</b>을 이용한 지문 형태소 분석<br>2. 형태소 분석기 별 <b>불용어</b> 제거, <b>빈출어휘</b> 추출<br>3. 형태소 분석한 파일을 이용한 <b>시각화</b><br> 4. 어휘문제 출제 모델 개발
