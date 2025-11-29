import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import available_functions, system_prompt
from functions.call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help = "the user prompt/question")
    parser.add_argument("--verbose", action = 'store_true', help = 'Enables verbose output')
    args = parser.parse_args()

    messages = [types.Content(role = "user", parts=[types.Part(text = args.prompt)])]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents= messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt,
        )
    )

    tool_parts = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=args.verbose)

        if not function_call_result.parts:
            raise RuntimeError("Function Returned no parts")
        
        part = function_call_result.parts[0]
        
        if not part.function_response or not part.function_response.response:
            raise RuntimeError("Function response missing")
        tool_parts.append(part)

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
 

if __name__ == "__main__":
    main()
