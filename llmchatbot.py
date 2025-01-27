import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from retriever_async import Retriever
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

        # History storage for multiple sessions
        self.session_histories = {}

        # Initialize the retriever
        self.retriever = Retriever()

        # Prompt template
        # 2. Identify the specific text or snippet used from the context that directly supports your answer. Include this as a “Reference Text” section, and expand it without fail to include the sentence or two immediately before and after the relevant snippet, to provide better continuity for the reader.
        self.template = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI bot that provides information with clear sources. For each response:
                1. Generate a clear and concise answer based on the provided context.
                2. If any sources or reference materials were used, include the URL as a “Reference Link” at the end of your response. Each reference link should point directly to the source to enable verification.
                3. The reference data provided is in multiple chunks. There is some overlapping text between the chunks. You will need to first stitch the relevant chunks together and then formulate the answer.
                4. The questions asked would be from multiple functional areas like Credit Cards, Loans, etc. You need to provide the answer strictly specific to the functional area on which the question is asked. For e.g., if the question is on Credit Cards, the answer should be strictly specific to Credit Cards.

                Only use information from the provided context: {context}."""),  # Context placeholder
            MessagesPlaceholder("history", optional=True),
            ("human", "{user_input}"),
        ])

    def format_docs(self, docs):
        """Helper function to format documents retrieved by the retriever."""
        return "\n\n".join(f"SourceURL: {doc.metadata['url']}\nContent: {doc.page_content}" for doc in docs)

    async def get_response(self, user_query, session_id, user_token):
        # Retrieve or initialize history for the session
        if session_id not in self.session_histories:
            self.session_histories[session_id] = []

        # Retrieve context from the retriever
        retrieved_docs = await self.retriever.fetch_data(user_query)
        formatted_context = self.format_docs(retrieved_docs)

        # print("***Reference docs for context***")
        # print(formatted_context)
        # print("***Context ends***")

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
            for item in self.session_histories[session_id]
        ]

        response_chunks = await chain.ainvoke({
            "history": message_history,
            "context": formatted_context,
            "user_input": user_query
        })

        # Append the response chunks to the conversation history
        appended_chunks = ""
        for response_chunk in response_chunks:
            appended_chunks += response_chunk
            yield response_chunk

        # Update the conversation history after streaming is complete
        self.session_histories[session_id].append(("human", user_query))
        self.session_histories[session_id].append(("ai", appended_chunks))
