import os
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

class Retriever:
    def __init__(self):
        pass
#        self.user_query = user_query
#        self.fetch_data()

    def fetch_data(self, user_query):
        azure_endpoint = os.getenv("AZURE_AOAI_ENDPOINT")
        azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        azure_deployment = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
        vector_store_address = os.getenv("AZURE_AI_SEARCH_SERVICE_ADDRESS")
        vector_store_password = os.getenv("AZURE_AI_SEARCH_API_KEY")

        embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
            azure_deployment=azure_deployment,
            openai_api_version=azure_openai_api_version,
            azure_endpoint=azure_endpoint,
            api_key=azure_openai_api_key,
        )


        # Specify additional properties for the Azure client such as the following https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/core/azure-core/README.md#configurations
        index_name: str = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
        vector_store: AzureSearch = AzureSearch(
            azure_search_endpoint=vector_store_address,
            azure_search_key=vector_store_password,
            index_name=index_name,
            embedding_function=embeddings.embed_query,
            #fields=fields,
            # Configure max retries for the Azure client
            additional_search_client_options={"retry_total": 4},
        )

        # Perform a similarity search
        docs = vector_store.similarity_search(
            query=user_query,
            k=15,
            search_type="hybrid",
        )


        return docs
