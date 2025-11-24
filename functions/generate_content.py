from google.genai import types
from config import system_prompt, available_functions

def generate_content(client, prompt: str, verbose: bool) -> None:
    messages = [types.Content(role = "user", parts=[types.Part(text = prompt)])]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents= messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt,
        )
    )
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}{function_call.args}")
    else:
        print(response.text)
    if verbose and response.usage_metadata:
        print(f'Prompt tokens: {usage_metadata.prompt_token_count}')
        print(f'Response tokens: {usage_metadata.candidates_token_count}')    
