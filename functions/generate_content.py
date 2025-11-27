from google.genai import types
from config import system_prompt, available_functions
from functions.call_function import call_function

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

    my_list = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)
        if len(function_call_result.parts) == 0:
            raise Exception
        my_list.append(function_call_result.parts[0])
    
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
           
