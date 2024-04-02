import os
from pathlib import Path

import chainlit as cl
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

from agents.agents import get_imbot

template = ChatPromptTemplate.from_messages([
    ("user", "{content}"),
])

imbot = get_imbot()
modified_imbot = template | imbot


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("runnable", imbot)


@cl.on_message
async def on_message(message: cl.Message):
    output = os.getenv('OUTPUT_FOLDER_PATH', 'output')

    response = imbot.invoke(
        {"messages": [HumanMessage(content=message.content)]},
    )

    print("Response message: ", response["messages"])

    elements = []

    if response["messages"][-2].name == "docx_generator":
        elements = [
            cl.File(
                name="demo.docx",
                path=str(Path(output) / 'demo.docx'),
                display="inline",
            ),
        ]

    await cl.Message(
        content=response["messages"][-1].content, elements=elements
    ).send()

