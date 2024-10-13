from langchain_community.document_loaders import PyPDFLoader

class PDFReader:
    def __init__(self):
        pass

    def read_pdf(self, pdf_path):
        """
        This method loads the content of a PDF file and returns the text content of all pages.

        :param pdf_path: The path or URL to the PDF file
        :return: List of page contents from the PDF
        """
        try:
            # Load the PDF using PyPDFLoader
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            # Extract the content from each page
            content = {}
            content[pdf_path] = [document.page_content for document in documents]
            
            return content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


