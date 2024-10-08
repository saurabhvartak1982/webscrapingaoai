import requests
import pdfplumber
from io import BytesIO

class PDFTextExtractor:
    """Class to fetch and extract text from a PDF given its URL."""

    def __init__(self, url):
        self.url = url

    def fetch_pdf(self):
        """Fetch PDF from the provided URL."""
        response = requests.get(self.url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            raise Exception(f"Failed to fetch PDF. Status code: {response.status_code}")

    def extract_text(self, pdf_data):
        """Extract text from the fetched PDF data."""
        text = ""
        with pdfplumber.open(pdf_data) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    def get_pdf_text(self):
        """Main method to fetch and extract text from the PDF."""
        try:
            pdf_data = self.fetch_pdf()
            text = self.extract_text(pdf_data)
            return text
        except Exception as e:
            return f"Error: {e}"
