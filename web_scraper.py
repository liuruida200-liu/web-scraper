import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def get_content(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    }
    response = requests.get(url, headers=headers, timeout=20)
    return BeautifulSoup(response.text, "html.parser")


def get_market_data(url):
    opts = Options()
    opts.binary_location = "/usr/bin/chromium-browser"
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=opts)
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MarketCard-row"))
        )
        return BeautifulSoup(driver.page_source, "html.parser")
    finally:
        driver.quit()



def main():
    target_url = "https://www.cnbc.com/world/?region=world"
    raw_data_path = "../data/raw_data/web_data.html"
    news_soup = get_content(target_url)
    latest_news = news_soup.find("ul", class_="LatestNews-list")
    market_soup = get_market_data(target_url)
    market_banner = market_soup.find("div", class_="MarketsBanner-marketData")
    with open(raw_data_path, "w", encoding="utf-8") as file:
        if market_banner:
            file.write(market_banner.prettify())
        if latest_news:
            file.write(latest_news.prettify())
if __name__ == "__main__":
    main()
