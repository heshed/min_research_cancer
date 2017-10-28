min_research_cancer

---

# 다운로드

- 통짜 파일을 보려면 [결과-통짜/all-in-one.txt](결과-통짜/all-in-one.txt?raw=true)
- 이 모든걸 다운받으려면 [archive/v1.0.zip](https://github.com/heshed/min_research_cancer/archive/v1.0.zip)
- archived [archive/v1.0.zip](https://github.com/heshed/min_research_cancer/archive/v1.0.zip)

## 집에서도 쉽게 사용할 수 있어요!

- python 설치(생략)

- pip 설치
  - https://packaging.python.org/tutorials/installing-packages/
  ```bash
  # On Linux or macOS:
  $ pip install -U pip setuptools
  
  # On Windows:
  $ python -m pip install -U pip setuptools
  ```

- python 라이브러리 설치
  ```bash
  # 필요한 python
  $ pip install -r requirements.txt
  ```

- 뉴스 수집
  ```
  $ python crawl-kinds.py
  ```
  - output.log 에 수집과정이 기록됩니다.
  - 결과-상세 디렉토리 아래 데이터가 생성됩니다.

- 모은 데이터를 하나의 파일로 모으기
  ```
  $ python merge_all.py
  --- [뉴스 통짜 파일 제작 시작]
     결과-상세/경향신문
     결과-상세/국민일보
     결과-상세/내일신문
     결과-상세/문화일보
     결과-상세/서울신문
     결과-상세/세계일보
     결과-상세/한겨레
     결과-상세/한국일보
  --- [뉴스 통짜 파일 제작 끝]
  --- 결과-통짜/all-in-one.txt
  ```

## crawl-kinds 가 중간에 멈추면 어떻게 되나요?
  - 중간에 프로세스를 재시작하면 중단된 상태부터 수집을 재개합니다.
    - 수집한 상태는 `index.pickle` 에 저장됩니다.
    
## 처음부터 다시 수집하고 싶어요.
    - `index.pickle` 파일을 제거 후 프로세스를 구동합니다.

## 다른 뉴스 데이터를 모으고 싶다면?

- 카인즈 뉴스 검색에서 제공하는 엑셀파일을 가져옵니다.
- 엑셀파일을 csv 파일로 내보냅니다.

### `index.pickle` 파일을 지웁니다(필수)

  ```
  # 상세 데이터 생성
  crawl-kinds.py -i [csv 파일] -o [상세결과 디렉토리]

  # 통짜 데이터 생성
  crawl-kinds.py -i [상세결과 디렉토리] -o [내보낼 파일]
  ```

## 디렉토리 구조

```
├── 상세-결과 : 2014-2016 상세 뉴스 데이터
├── 상세-통짜 : 2014-2016 통짜 뉴스 데이터
└── source : 카인즈에서 다운받은 뉴스 데이터 디렉토리
    ├── NewsResult_20140101-20161231.csv
    ├── NewsResult_20140101-20161231.numbers
    └── NewsResult_20140101-20161231.xlsx
```
