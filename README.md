# webscrapingaoai
This repo provides a prototype written in Python. 
The prototype has the code to scrape the contents on a website and to vectorize and store the same in the Azure AI Search Service. 

It also has an API which accepts questions from a user and passes them on to an Azure OpenAI instance to fetch an answer.  The API also passes the relevant chunks from the Azure AI Search as the knowledge-base to help the Azure OpenAI instance answer the questions asked by the user.  


## Code files

### Environment set-up
**sampleenv**: File comprising of all the required environment variables required by the prototype. This file needs to be renamed to **.env**.
**requirements.txt**: File mentioning all the packages to be used to run the prototype.

### Scraping and Vectorizing
**scraper.py**: This Python program scrapes the HTML contents from a bunch of URLs passed to it as parameters. This code is triggered by **orchestrator.py**.
**recursive_scraper.py**: This Python program recursively scrapes the HTML contents from the base URL and all the URLs that are referred in the HTML of the base URL. The **max depth** variable in this program to control the depth of the URL traversing from the base URL. This code is triggered by **orchestrator.py**.
**indexer.py**: This Python program vectorizes and indexes the scraped content. The vectors are stored in Azure AI Search. This code is triggered by **orchestrator.py**.

### Test clients
**retriever.py**: This is a **test code** to check if the Azure AI Search is able to retrieve the relevant content (scraped content).This code is triggered by **orchestrator.py**.  
**orchestrator.py**: This Python file has invocation code snippets for **scraper.py**, **recursive_scraper.py**, **indexer.py**, **retriever.py** and **llmchatbot.py**.   
**apitestharness.py**: An HTTP test client to test the API exposed by **chatapi.py**.

### API
**chatapi.py**: A FastAPI-based API. This API accepts a question from the end user. It makes use of **llmchatbot.py**. 
**llmchatbot.py**: This python module interfaces with Azure AI Search (to fetch the relevant scraped content) and then passes the same to the Azure OpenAI along with the user question.

### Containerization and Kubernetes deployment
**Dockerfile**: Dockerfile to containerize the API exposed by **chatapi.py**.
**k8smanifest.py**: Kubernetes manifest file to deploy and run the containerized API exposed by **chatapi.py**.


## Using the prototype

### Scraping and Indexing
1. Rename the sampleenv file to .env
2. Enter all the necessary parameter values in the .env file.
3. Refer to **orchestrator.py** for referring to the invocation code snippets for **scraper.py**, **recursive_scraper.py**, **indexer.py**.
4. Invoke either **scraper.py** OR **recursive_scraper.py** for scraping the desired web pages and **indexer.py** to create the vectors of the scraped content and store the same in Azure AI Search.

### Containerize and host the chatapi on Kubernetes
1. Rename the sampleenv file to .env
2. Enter all the necessary parameter values in the .env file
3. Build the container image: docker build -t <image_name> .
4. Run the container: docker run -p 8000:8000 <image_name>
5. Push the container to a container registry - like Azure Container Registry
6. Edit **k8smanifest.py** with the container image pushed in point 5.
7. Deploy the application to Kubernetes: kubectl apply -f k8smanifest.py 
7. Test the deployed application using **apitestharness.py**
