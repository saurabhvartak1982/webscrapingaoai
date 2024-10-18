import os
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from dotenv import load_dotenv
from customDocument import CustomDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

class Indexer:
    def __init__(self, all_scraped_data):
        self.all_scraped_data = all_scraped_data
        self.index_data()

    def index_data(self):
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

        embedding_function = embeddings.embed_query

        fields = [
            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
                filterable=True,
            ),
            SearchableField(
                name="content",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=len(embedding_function("Text")),
                vector_search_profile_name="myHnswProfile",
            ),
            SearchableField(
                name="metadata",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            # Additional field to store the title
            SearchableField(
                name="title",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            # Additional field for filtering on document source
            SimpleField(
                name="source",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
        ]

        # Specify additional properties for the Azure client
        index_name: str = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
        vector_store: AzureSearch = AzureSearch(
            azure_search_endpoint=vector_store_address,
            azure_search_key=vector_store_password,
            index_name=index_name,
            embedding_function=embeddings.embed_query,
            fields=fields,
            additional_search_client_options={"retry_total": 4},
        )

        documents_to_add = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)

        for url, content in self.all_scraped_data.items():
            content_text = ' '.join(content)

            # Split content into chunks
            chunks = text_splitter.split_text(content_text)

            # Create a dictionary for metadata, where you can add additional info if required
            metadata_dict = {
                "url": url  # Using the URL as part of the metadata
            }

            # Create unique doc_ids for each chunk
            for i, chunk in enumerate(chunks):
                doc_id = f"{url}_chunk_{i}"

                # Use the custom Document class
                document = CustomDocument(
                    doc_id=doc_id, 
                    content=chunk, 
                    title=url, 
                    source=url, 
                    metadata=metadata_dict
                )

                documents_to_add.append(document)

        # Now, add the structured documents to the vector store
        print("Printing all docs to add")
        for doc in documents_to_add:
            print(doc.id, doc.page_content)

        try:
            vector_store.add_documents(documents=documents_to_add)
        finally:
            vector_store.__del__()  # Explicitly clean up the object
