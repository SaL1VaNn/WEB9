import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

# Функція для скрапінгу цитат та авторів
def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    quotes = []
    authors = set()

    # Пройдемося по усіх сторінках сайту з цитатами
    next_page = "/page/1/"
    while next_page:
        response = requests.get(base_url + next_page)
        soup = BeautifulSoup(response.text, "html.parser")

        for quote in soup.select("div.quote"):
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            authors.add(author)
            tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

            quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        next_page = soup.find("li", class_="next")
        if next_page:
            next_page = next_page.find("a")["href"]

    return quotes, list(authors)

# Запис цитат у JSON файл
def save_quotes_to_json(quotes):
    with open("quotes.json", "w", encoding="utf-8") as json_file:
        json.dump(quotes, json_file, ensure_ascii=False, indent=4)

# Запис авторів у JSON файл
def save_authors_to_json(authors):
    with open("authors.json", "w", encoding="utf-8") as json_file:
        json.dump(authors, json_file, ensure_ascii=False, indent=4)

# Основна функція
def main():
    quotes, authors = scrape_quotes()
    save_quotes_to_json(quotes)
    save_authors_to_json(authors)

    # Підключення до MongoDB та завантаження даних
    client = MongoClient("mongodb://localhost:27017/")
    db = client["quotes_db"]

    # Завантаження цитат у колекцію "quotes"
    quotes_collection = db["quotes"]
    quotes_collection.insert_many(quotes)

    # Завантаження авторів у колекцію "authors"
    authors_collection = db["authors"]
    authors_collection.insert_many([{"name": author} for author in authors])

if __name__ == "__main__":
    main()
