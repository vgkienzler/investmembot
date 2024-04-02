import json
import operator
from pprint import pprint
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage, FunctionMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolInvocation

import agents.tools as tl
from main import llm_model, retriever
from rag.rag import get_chain


def create_agent(llm_chat_model, system_message: str):
    """Create an agent."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    return prompt | llm_chat_model


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    company_name: str


def force_query_if_rag(response, messages):
    """If the response is a RAG tool, force the query parameters to be the
    content of the previous message (the human query)."""
    if response.additional_kwargs.get('function_call'):
        function_call = response.additional_kwargs['function_call']
        if function_call['name'] == "retrieve_and_answer":
            function_call['arguments'] = '{"query":"' + messages[-1].content + '"}'
    return response


def call_model(state):
    """Invokes the model to generate a response based on the current state.
    Given the question, it will decide to use a tool or not.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """

    if not state['company_name']:
        rag_chain = get_chain(retriever, llm_model)
        response = rag_chain.invoke("What is the company name?")
        state['company_name'] = response

    messages = state["messages"]
    print("Messages sent to model for generation: ")
    pprint(messages)
    response = tl.rag_or_print_llm_model.invoke(messages)

    # Needed to prevent the LLM to simplify the user's query and lose information.
    response = force_query_if_rag(response, messages)

    return {"messages": [response], "company_name": state["company_name"]}


def call_tools(state):
    """Call the tools, depending on the decision from the model."""
    last_message = state["messages"][-1]

    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(
            last_message.additional_kwargs["function_call"]["arguments"]
        )
    )

    response = tl.all_tools_executor.invoke(action)
    function_message = FunctionMessage(content=str(response), name=action.tool)

    return {"messages": [function_message]}


def call_internet_search_tool(state):
    """Force call the internet search tool (Tavily) to search for the query."""

    search_query = state["messages"][-2].additional_kwargs["function_call"]["arguments"]

    tool_input = json.loads(search_query)

    # Update the query so that the 'company name' is known, since the model too often
    # fails at retrieving it from past messages.
    query = tool_input["query"]
    query = "Company name: " + state["company_name"] + " - " + query
    query = "{" + '"query": "' + query + '"' + "}"
    # print(query)

    action = ToolInvocation(
        tool='tavily_search_results_json',
        tool_input=json.loads(query)
    )

    response = tl.all_tools_executor.invoke(action)
    function_message = FunctionMessage(content=str(response), name=action.tool)

    return {"messages": [function_message]}


def should_search_internet(state):
    """Decide whether to search the internet or go back to the agent."""
    last_message = state["messages"][-1]

    # Letting the model decide whether to search the internet or not is not
    # reliable, so web search is decided deterministically if the model cannot answer.
    if "cannot answer" in last_message.content:
        return "go_to_internet_search"

    return "go_to_agent"


def should_continue(state):
    last_message = state["messages"][-1]

    if "function_call" not in last_message.additional_kwargs:
        return "end"

    return "continue"


content_generation_agent = create_agent(
    llm_chat_model=llm_model,
    system_message=(
        "You are a writer assistant. You are tasked with writing "
        "sections of a larger report. To write a section, you will be "
        "provided with different pieces of information. "
        "The section you write must be structured in paragraphs, without a title, "
        "and contain all the pieces of information you have been provided with."
        "Do not add any title, just provide the content of the section."
    )
)


section_summarizer_agent = create_agent(
    llm_chat_model=llm_model,
    system_message=(
        "You are a section summarizer. You are tasked with summarizing "
        "sections of a larger report. To summarize a section, you will be "
        "provided with a section of a report. Your task is to summarize the "
        "section in a maximum of two sentences."
    )
)


def get_imbot():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("rag_or_print", call_tools)
    workflow.add_node("internet_search", call_internet_search_tool)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "rag_or_print",
            "end": END
        }
    )
    workflow.add_conditional_edges(
        "rag_or_print",
        should_search_internet,
        {
            "go_to_internet_search": "internet_search",
            "go_to_agent": "agent"
        }
    )
    workflow.add_edge("internet_search", "agent")
    imbot = workflow.compile()
    return imbot


if __name__ == "__main__":
    questions = [
        # 'What is the company name?',
        # 'What is the company industry?',
        'Generate the report for me',
        # 'Provide an overview of the management team and key personnel.',
        # 'Add any other relevant information about the company, relevant for this overview.',
    ]

    # bot = get_print_or_answer_bot()

    bot = get_imbot()

    for question in questions:
        print('Question: ', question)
        inputs = {"messages": [HumanMessage(question)]}
        pprint(bot.invoke(inputs))
