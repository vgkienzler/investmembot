from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, \
    RunnableSerializable


def get_chain(retriever, llm_model) -> RunnableSerializable[Any, str]:
    """Get the chain for the RAG model.
    :arg retriever: The retriever object to use in the chain.
    :arg llm_model: The language model to use in the chain.
    :return: The LCEL runnable.
    """
    # Define the retrieval prompt.
    retrieval_prompt_template = """Answer the question based only on the following context. If you cannot answer the question with the context, please respond with 'I cannot answer the question with the context provided.':
    Context: {context}

    Question:
    {question}
    """
    prompt = ChatPromptTemplate.from_template(retrieval_prompt_template)

    return (
            RunnableParallel(context=retriever, question=RunnablePassthrough())
            | prompt
            | llm_model
            | StrOutputParser()
    )


def retrieve_and_answer(questions: list, chain) -> list:
    answers = []

    for question in questions:
        answer = chain.invoke(question)
        answers.append(answer)
    return answers
