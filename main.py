import os
import argparse

from dotenv import load_dotenv
from google import genai

from functions.generate_content import generate_content


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help = "the user prompt/question")
    parser.add_argument("--verbose", action = 'store_true', help = 'Enables verbose output')
    args = parser.parse_args()
 
    if args.verbose:
        print(f'User prompt: {args.prompt}')

    generate_content(client, args.prompt, args.verbose)

if __name__ == "__main__":
    main()
