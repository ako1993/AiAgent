import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help = "the user prompt/question")
    parser.add_argument("--verbose", action = 'store_true', help = 'Enables verbose output')
    args = parser.parse_args()


    messages = [types.Content(role = "user", parts=[types.Part(text = args.prompt)])]
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents= messages)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(response.text)
    if args.verbose:
        print(f'User prompt: {args.prompt}')
        print(f'Prompt tokens: {prompt_tokens}')
        print(f'Response tokens: {response_tokens}')     
    

if __name__ == "__main__":
    main()
