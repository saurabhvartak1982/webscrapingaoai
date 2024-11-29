import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, urls):
        self.urls = urls
        self.all_scraped_data = {}
        self.scrape_data()

    def scrape_data(self):
        for url in self.urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.body
            ordered_text = []
            # Extract text from span, li, p, td tags. This needs to be updated basis the webpages which are getting scraped.
            for element in body.descendants:
                if element.name in ['span', 'li', 'p', 'td', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    ordered_text.append(element.text.strip())
                if element.name == 'div' and element.get('class') == ['card-body']:
                    child_divs = element.find_all('div')
                    for child_div in child_divs:
                        ordered_text.append(child_div.text.strip())
            self.all_scraped_data[url] = ordered_text

    def get_scraped_data(self):
        return self.all_scraped_data


