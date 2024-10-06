import requests
from bs4 import BeautifulSoup
from imagedescriber import describe_image

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

            # Extract text from span, li, p, td tags
            for element in body.descendants:
                if element.name in ['span', 'li', 'p', 'td']:
                    ordered_text.append(element.text.strip())
                if element.name == 'div' and element.get('class') == ['card-body']:
                    child_divs = element.find_all('div')
                    for child_div in child_divs:
                        ordered_text.append(child_div.text.strip())
                
                # Detect image elements and call describe_image
                if element.name == 'img' and element.get('src'):
                    image_url = element.get('src')
                    # If the image URL is relative, convert it to an absolute URL
                    image_url = self.get_absolute_url(url, image_url)
                    image_description = describe_image(image_url)
                    ordered_text.append(f"Image: {image_description}")
            
            self.all_scraped_data[url] = ordered_text

    def get_absolute_url(self, base_url, image_url):
        # Convert relative URL to absolute URL if necessary
        if image_url.startswith('http'):
            return image_url
        else:
            from urllib.parse import urljoin
            return urljoin(base_url, image_url)
   
    def get_scraped_data(self):
        return self.all_scraped_data
