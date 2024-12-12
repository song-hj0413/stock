from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import yfinance as yf

app = Flask(__name__)

# 주식 데이터 가져오기 (1년치 데이터 포함)
def fetch_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1y")  # 최근 1년 데이터
        return [
            {"date": str(date.date()), "open": round(row["Open"], 2), "close": round(row["Close"], 2)}
            for date, row in hist.iterrows()
        ]
    except Exception as e:
        print(f"Error fetching stock data for {symbol}: {e}")
        return []


# 네이버 뉴스 크롤링 함수
def fetch_news(keyword):
    try:
        url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_jum"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch news. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # 뉴스 제목과 링크 가져오기
        articles = soup.select(".news_tit")
        news_data = [
            {"title": article.get_text(strip=True), "url": article["href"]}
            for article in articles
        ]
        return news_data
    except Exception as e:
        print(f"Error fetching news for {keyword}: {e}")
        return []



# Yahoo Finance에서 영어 회사 이름 가져오기
def get_company_name_from_yahoo(symbol):
    try:
        ticker = yf.Ticker(symbol)
        company_name = ticker.info.get("shortName", symbol)  # 회사 이름 가져오기
        return company_name
    except Exception as e:
        print(f"Error fetching company name for {symbol}: {e}")
        return symbol  # 에러 시 Symbol 반환

# 네이버에서 한국어 회사 이름 가져오기
def get_korean_company_name_from_naver(symbol):
    try:
        # 네이버 검색 페이지 URL
        url = f"https://search.naver.com/search.naver?where=nexearch&query={symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch data from Naver Search. Status code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        
        # 검색 결과에서 회사명 추출
        company_name_tag = soup.select_one(".stk_nm")  # 클래스명이 `stk_nm`인 태그
        if company_name_tag:
            return company_name_tag.get_text(strip=True)
        else:
            print(f"Korean company name not found for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching Korean company name from Naver Search for {symbol}: {e}")
        return None



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stock", methods=["GET", "POST"])
def stock():
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()  # 종목 코드를 대문자로 변환
        stock_data = fetch_stock_data(symbol)  # 주가 데이터 가져오기
        korean_name = get_korean_company_name_from_naver(symbol)  # 한국어 회사명 가져오기
        
        # 관련 뉴스 검색 (한국어 회사 이름으로만 검색)
        related_news = fetch_news(korean_name) if korean_name else []

        print(f"Korean name: {korean_name}")  # 디버깅용 출력

        return render_template(
            "stock.html",
            stock_data=stock_data,
            related_news=related_news,  # 중복 제거 로직 제거
            symbol=symbol,
            english_name=symbol,  # 심볼을 영어 이름 대신 사용
            korean_name=korean_name,
        )
    return render_template("stock.html", stock_data=[], related_news=[], symbol="", english_name="", korean_name="")

if __name__ == "__main__":
    app.run(debug=True)
