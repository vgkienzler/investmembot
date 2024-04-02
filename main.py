import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from templates.investment_memo_templates import im_template
from rag.prepare_doc import parse_to_markdown, split_documents
from rag.rag import get_chain, retrieve_and_answer
from utils.list_files import list_files_in_folder
from utils.download_nvidia_financials import download_nvidia_financials
from rag.vector_store import create_pinecone_index, add_documents_to_pinecone


load_dotenv()
INPUT_FOLDER_PATH = os.getenv('INPUT_FOLDER_PATH')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')


def initialisation():
    print(download_nvidia_financials(INPUT_FOLDER_PATH))

    # Create pinecone index if it does not yet exist.
    index_creation = create_pinecone_index(PINECONE_INDEX_NAME, 1536)
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    # If index_creation is True, index has just been created, and documents must be added to it.
    if index_creation:
        documents = list_files_in_folder(INPUT_FOLDER_PATH)
        print(documents)

        parsed_documents = parse_to_markdown(documents)

        add_documents_to_pinecone(
            split_documents(parsed_documents),
            embedding_model,
            PINECONE_INDEX_NAME,
        )

    vectorstore = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embedding_model,
    )

    return vectorstore.as_retriever()


retriever = initialisation()

# Define the model
llm_model = ChatOpenAI(
    # model_name="gpt-4",
    temperature=0,
)

chain = get_chain(retriever, llm_model)
investment_memo = im_template


if __name__ == '__main__':
    # Testing the retriever
    response = retriever.invoke(
        "what is the gross carrying amount of Total Amortizable Intangible Assets for Jan 29, 2023?"
    )
    print("Retriever response: ", response)

    # Define test questions
    question_1 = "Who is the E-VP, Operations - and how old are they?"
    question_2 = "what is the gross carrying amount of Total Amortizable Intangible Assets for Jan 29, 2023?"
    questions = [question_1, question_2]

    print("Answers to test questions:")
    for answer in retrieve_and_answer(questions, chain):
        # print(answer['response'].content)
        print(answer)
