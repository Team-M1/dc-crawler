# DC Crawler
한국 최대의 익명 커뮤니티 디시인사이드의 글, 댓글 크롤링을 도와주는 python 라이브러리입니다.

## 요구사항
`tqdm`  
`selenium`

## 사용방법
예) `python main.py dcbest 18500 18510`  
해당 경로에서 `python main.py "갤러리 영어이름" "시작 글 번호" "끝 글 번호"`
명령으로 실행하면 됩니다.

data폴더가 없으면 만들고, 그 안에 파일이름 `날짜-시간.csv` 파일로 결과를 저장합니다.  
csv파일은 헤더가 content, label로 설정되어 있고, content에는 수집한 댓글, label은 0이 입력됩니다.  

## 세부사항
[원본 저장소](https://github.com/seunghyukcho/dc-crawler)  
크롤링이 저작권을 침해하는 지 주의바랍니다. https://www.dcinside.com/robots.txt
