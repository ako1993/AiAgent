import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt, available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help = "the user prompt/question")
    parser.add_argument("--verbose", action = 'store_true', help = 'Enables verbose output')
    args = parser.parse_args()


    messages = [types.Content(role = "user", parts=[types.Part(text = args.prompt)])]
    response = client.models.generate_content(model='gemini-2.0-flash-001',
                                               contents= messages,
                                               config=types.GenerateContentConfig(
                                                   tools=[available_functions], system_instruction=system_prompt))

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function {function_call.name}{function_call.args}")
    print(response.text)
    if args.verbose:
        print(f'User prompt: {args.prompt}')
        print(f'Prompt tokens: {prompt_tokens}')
        print(f'Response tokens: {response_tokens}')     
    

if __name__ == "__main__":
    main()
