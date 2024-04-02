"""Module for preparing documents (parsing to markdown + splitting) for storage
 in the vector store."""

import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from llama_parse import LlamaParse


def parse_to_markdown(pdf_docs) -> list[Document]:
    """Parses a pdf file to markdown with LlamaParse. Returns documents as
  langchain Document object."""
    parser = LlamaParse(
        result_type="markdown",
        verbose=True,
        language="en",
        num_workers=3,
    )
    documents = parser.load_data(pdf_docs)
    langchain_docs = []

    for document in documents:
        langchain_docs.append(document.to_langchain_format())

    return langchain_docs


def tiktoken_len(text):
    tokens = tiktoken.encoding_for_model("gpt-3.5-turbo").encode(
        text,
    )
    return len(tokens)


def split_documents(doc_list):
    """Split documents into chunks using recursive character splitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=tiktoken_len,
    )
    chunks = text_splitter.split_documents(doc_list)

    return chunks
