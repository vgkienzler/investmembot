from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PodSpec


def create_pinecone_index(index_name: str, dimension: int) -> bool:
    """Create the pinecone index if index_name does not exist."""
    pinecone_client = Pinecone()

    if index_name not in pinecone_client.list_indexes().names():
        pinecone_client.create_index(
            name=index_name.lower(),
            dimension=dimension,
            metric="cosine",
            spec=PodSpec(
                environment="gcp-starter"
            )
        )

        print(f"Index '{index_name}' created successfully.")

        return True

    else:
        print(f"Using existing '{index_name}'.")

        return False


def delete_pinecone_index(index_name: str):
    """Delete pinecone index."""
    pinecone_client = Pinecone()

    if index_name in pinecone_client.list_indexes().names():
        pinecone_client.delete_index(index_name)
        print(f"Index '{index_name}' deleted successfully.")
    else:
        print(f"Index '{index_name}' does not exist.")


def add_documents_to_pinecone(chunks, embedding_model, pine_cone_index_name):
    """Add chunks to pinecone storage."""
    vector_store = PineconeVectorStore.from_documents(
        chunks,
        embedding_model,
        index_name=pine_cone_index_name,
    )
    print(len(chunks))
    return vector_store
