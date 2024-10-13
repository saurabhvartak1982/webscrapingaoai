import os

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import AzureAISearchRetriever

from dotenv import load_dotenv

load_dotenv()

class Chatbot:

    def __init__(self):
        # Azure OpenAI setup
        azure_endpoint = os.getenv("AZURE_AOAI_ENDPOINT")
        azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        azure_deployment = os.getenv("AZURE_LLM_DEPLOYMENT")
        azure_aisearch_index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
        
        # Initialize the Azure OpenAI model with streaming enabled
        self.chatbot = AzureChatOpenAI(
            azure_deployment=azure_deployment,
            openai_api_version=azure_openai_api_version,
            azure_endpoint=azure_endpoint,
            api_key=azure_openai_api_key,
            verbose=True,
            streaming=True  # Enable streaming mode
        )

        # Initialize history and prompt template
        self.history = []

        # Initialize the retriever.
        self.retriever = AzureAISearchRetriever(
            content_key="content", top_k=3, index_name=azure_aisearch_index_name
        )

        # Prompt template
        self.template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI bot that helps people find information. Please refer only to the context for answering the questions: {context}"),
            MessagesPlaceholder("history", optional=True),
            ("human", "{user_input}"),
        ])

    def format_docs(self, docs):
        """Helper function to format documents retrieved by the retriever."""
        return "\n\n".join(doc.page_content for doc in docs)

    def get_response(self, user_query):
        # Retrieve context from the retriever
        retrieved_docs = self.retriever.invoke(user_query)
        formatted_context = self.format_docs(retrieved_docs)

        # Create the pipeline chain
        chain = (
            {
                "context": RunnablePassthrough(),
                "user_input": RunnablePassthrough()
            }
            | self.template
            | self.chatbot  # This is now set to stream responses
            | StrOutputParser()
        )

        # Convert history into Langchain message objects
        message_history = [
            HumanMessage(content=item[1]) if item[0] == "human" else AIMessage(content=item[1])
            for item in self.history
        ]

        # Pass the inputs to the chain and handle streaming
        appended_chunks = ""
        for response_chunk in chain.invoke({
            "history": message_history,
            "context": formatted_context,
            "user_input": user_query
        }):
            # Stream the response chunk back to the caller
            appended_chunks += response_chunk
            yield response_chunk

        # Update the conversation history after streaming is complete
        self.history.append(("human", user_query))
        self.history.append(("ai", appended_chunks))
        
