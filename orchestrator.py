# from scraper import Scraper
# from scraperimg import Scraper
# from recursive_scraper import RecursiveScraper
from pdftextextractor import PDFTextExtractor
# from indexer import Indexer
# from retriever import Retriever
# from llmchatbot import Chatbot

def main():
    #--Invocation code for Scraper begins here--

    # List of URLs to scrape
    # urls = [
    #     'https://www.ibm.com/topics/neural-networks',
    #     # '<url2>',
    #     # '<url3>',
    #     # '<url4>',
    #     # '<url5>',
    #     # '<url6>'
        
    # ]

    # objScraper = Scraper(urls)
    # all_scraped_data = objScraper.get_scraped_data()
    # print(all_scraped_data)
    #--Invocation code for Scraper ends here--

    #--Invocation code for RecursiveScraper begins here--
    # start_url = 'https://example.com'
    # scraper = RecursiveScraper(max_depth=2)
    # scraper.crawl(start_url)
    # scraped_content = scraper.get_scraped_data()
    # print(scraped_content)
    #--Invocation code for RecursiveScraper ends here--

    ##--Invocation code for pdftextextractor begins here--
    url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    # Create an instance of the class
    pdf_extractor = PDFTextExtractor(url)
    
    # Get the extracted text
    extracted_text = pdf_extractor.get_pdf_text()
    print(extracted_text)

    ##--Invocation code for pdftextextractor ends here--

    # #--Invocation code for Indexer begins here--
    # objIndexer = Indexer(all_scraped_data)
    # #--Invocation code for Indexer ends here--


    # # #--Invocation code for Retriever begins here--
    # objRetriever = Retriever("Tell me 10 things about Mumbai")
    # context = objRetriever.fetch_data()
    # print("Context: ", context)
    # # #--Invocation code for Retriever ends here--


    # #--Invocation code for Chatbot begins here--
    # chatbot = Chatbot()
    
    # user_query = "Tell me 10 things about Mumbai"
    
    # # Synchronously call get_response and handle streaming
    # for response_chunk in chatbot.get_response(user_query):
    #     print(response_chunk, end="", flush=True)  # Print each streamed chunk
    # #--Invocation code for Chatbot ends here--

if __name__ == "__main__":
    main()


