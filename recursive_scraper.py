import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class RecursiveScraper:
    def __init__(self, max_depth=2):
        self.visited_links = set()
        self.max_depth = max_depth
        self.scraped_data = []  # To store scraped content

    def crawl(self, url, current_depth=0):
        if current_depth > self.max_depth:
            return

        # Skip URLs that have already been visited
        if url in self.visited_links:
            return

        self.visited_links.add(url)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            return

        # Parse the content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract content from the current page
        title = soup.find('title').get_text() if soup.find('title') else 'No Title'
        self.scraped_data.append({'url': url, 'title': title, 'depth': current_depth})
        print(f"Crawling: {url} | Title: {title} | Depth: {current_depth}")

        # Find all links on the current page
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)

            # Make sure the URL is not external
            if urlparse(full_url).netloc == urlparse(url).netloc:
                self.crawl(full_url, current_depth + 1)

    def get_scraped_data(self):
        return self.scraped_data


