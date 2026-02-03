import os
from langchain_openai import OpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

key = os.environ["api_key"]

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_gpt(dom_chunks, parse_description):
    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(api_key=key, model="gpt-4.1-nano-2025-04-14")
    chain = prompt | llm

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        parsed_results.append(response.content)

    return "\n".join(parsed_results)
