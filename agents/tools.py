from typing import Type

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from langgraph.prebuilt import ToolExecutor

from doc_generation.content_generator import generate_content
from main import investment_memo, llm_model
from main import retriever
from rag.rag import get_chain
from doc_generation.docx_generator import generate_docx


################################
# Tools that the agent can use
class DocxGenerator(BaseTool):
    name = "docx_generator"
    description = "Useful when the user asks you to generate the investment memo or report."

    def _run(self, *args, **kwargs) -> str:
        # print(args, kwargs)
        content = generate_content(investment_memo)
        generate_docx(content)
        # print("Investment memo generated.")
        return "Investment memo generated, you can access it in the output repository."

    def _arun(self):
        raise NotImplementedError("docx_generator does not support async.")


class SearchInput(BaseModel):
    query: str = Field(description="The search query as the user typed it.")


class RetrieveAndAnswer(BaseTool):
    name = "retrieve_and_answer"
    description = (
        "A tool to retrieve private information from the document library and answer the user question. "
        "Useful to answer any question that the user asks, specifically when the question is vague and imprecise."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str, *args, **kwargs) -> str:
        # print(query, args, kwargs)
        rag_chain = get_chain(retriever, llm_model)
        response = rag_chain.invoke(query)
        # response = "Here is my answer to the user's question."

        return response

    def _arun(self):
        raise NotImplementedError("retrieve_and_answer does not support async.")


internet_search_tool = TavilySearchResults(
    description=(
        "A search engine optimized for finding information online. "
        "Useful when the user asks general questions, when the user explicitly "
        "asks for online information from the internet, or when the other tools do not return good answers."
    )
)

all_tools = [
    RetrieveAndAnswer(),
    DocxGenerator(),
    internet_search_tool,
]

all_tools_executor = ToolExecutor(all_tools)

rag_or_print_llm_model = llm_model.bind_functions([
    convert_to_openai_function(t) for t in [RetrieveAndAnswer(), DocxGenerator(),]
])

all_tools_model = llm_model.bind_functions([
    convert_to_openai_function(t) for t in all_tools
])

internet_search_llm_model = llm_model.bind_functions([
    convert_to_openai_function(t) for t in [internet_search_tool]
])
