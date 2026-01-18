from bs4 import BeautifulSoup
import csv
import pathlib as pl

RAW_DATA_PATH = pl.Path("../data/raw_data/web_data.html")
NEWS_CSV = pl.Path("../data/processed_data/news_data.csv")
MARKET_CSV = pl.Path("../data/processed_data/market_data.csv")

raw_data = RAW_DATA_PATH.read_text(encoding="utf-8")
soup = BeautifulSoup(raw_data, "html.parser")

news = []
for line in soup.select("ul.LatestNews-list > li.LatestNews-item"):
    a = line.select_one("a.LatestNews-headline")
    t = line.select_one("time.LatestNews-timestamp")
    link = (a.get("href") or "").strip()
    news.append([t.get_text(strip=True), a.get_text(strip=True), link])

market = []
for card in soup.select("a.MarketCard-container"):
    symbol = card.select_one("span.MarketCard-symbol")
    position = card.select_one("span.MarketCard-stockPosition")
    market.append([symbol.get_text(strip=True), position.get_text(strip=True)])

NEWS_CSV.parent.mkdir(parents=True, exist_ok=True)

with NEWS_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "title", "link"])
    writer.writerows(news)

with MARKET_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["symbol", "stock_position"])
    writer.writerows(market)

print(f"Saved {len(news)} news items to {NEWS_CSV}")
print(f"Saved {len(market)} market items to {MARKET_CSV}")

