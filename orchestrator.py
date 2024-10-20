# from scraper import Scraper
from pdfreader import PDFReader
# from scraperimg import Scraper
# from recursive_scraper import RecursiveScraper
from indexer_chunking import Indexer
# from retriever import Retriever
# from llmbot import LLMBot
# from llmchatbot import Chatbot
# import imagedescriber

def main():
    #--Invocation code for Scraper begins here--

    # List of URLs to scrape
    # urls = [
        # '<url1>',
        # '<url2>',
        # '<url3>',
        # '<url4>',
        # '<url5>',
        # '<url6>'
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

    #--Invocation code for PDFReader begins here--
    pdf_reader = PDFReader()
    all_scraped_data = pdf_reader.read_pdf("https://mywebsite/myfile.pdf")

    # #--Invocation code for Indexer begins here--
    objIndexer = Indexer(all_scraped_data)
    # #--Invocation code for Indexer ends here--


    # # #--Invocation code for Retriever begins here--
    # question = "Tell me 10 things about Mumbai"
    # objRetriever = Retriever(question)
    # context = objRetriever.fetch_data()
    # # #--Invocation code for Retriever ends here--

    # #--Invocation code for LLMBot begins here--
    # client = LLMBot()
    # response = client.get_response(context, question)
    # print(response)

    # #--Invocation code for LLMBot ends here--

    # #--Invocation code for Chatbot begins here--
    # chatbot = Chatbot()
    
    # user_query = "Tell me 10 things about Mumbai"
    
    # # Synchronously call get_response and handle streaming
    # for response_chunk in chatbot.get_response(user_query):
    #     print(response_chunk, end="", flush=True)  # Print each streamed chunk
    # #--Invocation code for Chatbot ends here--

    #--Invocation code for ImageDescriber begins here--
    # image_path = "https://cdn.gyftr.com/promotionwallet/brand/indusindwelcomegift/11715079989-_0018_Hamleys.png"
    # response = imagedescriber.describe_image(image_path)
    # print(response)
    #--Invocation code for ImageDescriber ends here--

if __name__ == "__main__":
    main()


