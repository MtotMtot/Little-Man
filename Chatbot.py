
import os
import base64
from pyexpat import model
from pyexpat.errors import messages
from urllib import response
from openai import OpenAI
from pydantic.functional_validators import ModelAfterValidator
import tiktoken
from parse import parse_with_gpt

key = os.environ["api_key"]

client = OpenAI(api_key=key)
MODEL = "gpt-4.1-nano-2025-04-14"
TEMPERATURE = 0.5
MAX_TOKENS = 100
TOKEN_BUDGET = 100
SYSTEM_PROMPT = "You are tasked with extracting specific information from the following text content: {dom_content}. Please follow these instructions carefully: 1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. 2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. 3. **Empty Response:** If no information matches the description, return an empty string (''). 4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
MESSAGES = messages=[{"role": "system", "content": SYSTEM_PROMPT}]

def get_encoding(model):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Waring: Tokenizer for model '{model}' not found. Falling back to 'cl100k_base'.")
        return tiktoken.get_encoding("cl100k_base")

ENCODING = get_encoding(MODEL)

def count_tokens(text):
    return len(ENCODING.encode(text))


def total_tokens_used(messages):
    try:
        return sum(count_tokens(msg["content"]) for msg in messages)
    except Exception as e:
        print(f"[token count error]: {e}")
        return 0


def enforce_token_budget(messages, budget=TOKEN_BUDGET):
    try:
        while total_tokens_used(messages) > budget:
            if len(messages) <= 2:
                break
            messages.pop(1)
    except Exception as e:
        print(f"[token budget error]: {e}")


def chat(dom_chunks, user_input):

    messages.append({"role": "user", "content": user_input})

    response = parse_with_gpt(dom_chunks, user_input)

    messages.append({"role": "assistant", "content": response})

    enforce_token_budget(messages)

    return response

'''def chat_loop(dom_chunks):
    while True:
        user_input = input("Enter Prompt... ")
        if user_input.strip().lower() in {"exit", "quit", ""}:
            break
        answer = chat(dom_chunks, user_input)
        print("Assistant: ", answer)
        print("Current tokens: ", total_tokens_used(messages))'''