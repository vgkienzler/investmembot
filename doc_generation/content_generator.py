from copy import deepcopy
from pprint import pprint

from langchain_core.messages import HumanMessage

from templates.investment_memo_templates import im_template
import agents.agents as ag


def generate_content(template: dict) -> dict:
    """Generates content for the investment memo based on the prompts in the
    template."""
    local_template = deepcopy(template)
    sections = local_template['sections']

    imbot = ag.get_imbot()

    summarized_sections = ""

    message_history = []

    for section in sections:
        aggregated_section_information = ""
        if section['type'] == 'text' and len(section['prompts']) > 0:
            for prompt in section['prompts']:
                input_message = HumanMessage(content=prompt)
                results = imbot.invoke({
                    "messages": [*message_history, input_message],
                })
                # Append the first message (prompt)
                message_history.append(input_message)
                # Append the last message (response to the prompt)
                message_history.append(results['messages'][-1])

                aggregated_section_information += results['messages'][-1].content + "\n"
                print(aggregated_section_information)
                print("Message history: ")
                pprint(message_history)

            section['content'] = aggregated_section_information

            # Summarize the section and store the summary for reference by
            # the next sections
            summarized_section = ag.section_summarizer_agent.invoke({
                "messages": [
                    HumanMessage(content=section['content']),
                ],
            })
            section['summary'] = summarized_section.content
            print("Summarized section: ", summarized_section)
            summarized_sections += summarized_section.content + "\n"

    pprint(sections)

    return local_template


if __name__ == '__main__':
    print(generate_content(im_template))
