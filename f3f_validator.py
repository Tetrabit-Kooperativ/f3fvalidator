import requests
from concurrent.futures import ThreadPoolExecutor
import json

API_URL = "https://old.fagbladet3f.dk/articles_api"
LIMIT = 50
OFFSET = 0
MAX_OFFSET = 36082  # hardcoded for now, update manually
CONCURRENCY = 40

def fetch_data(offset):
    """ returns a list of articles on the current page """
    params = {'limit': LIMIT, 'offset': offset}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return []

def check_url(id_url):
    """ checks individual article, writes to file if not 200 """
    id, url = id_url
    url = url.replace('fagbladet3f.dk', 'old.fagbladet3f.dk')
    response = requests.get(url)
    if response.status_code != 200:
        with open("failed_requests.txt", "a") as file:
            file.write(f"{id}: {response.status_code}\n")

def main():
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        for offset in range(OFFSET, MAX_OFFSET + 1, LIMIT):
            articles = fetch_data(offset)
            if not articles:
                break
            id_url_pairs = [(article['id'], article['url']) for article in articles]
            executor.map(check_url, id_url_pairs)
            print(f"Progress: {offset/MAX_OFFSET*100:.2f}%", end="\r")

if __name__ == "__main__":
    main()