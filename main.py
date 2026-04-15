import argparse
import os
from constants import *
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    try:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")        
    except Exception:
        print(f"\n{TEXT_RED}API Key not found. Check your environment file.\n")
    
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # user_prompt = ""
    # if len(sys.argv) > 1:
    #     user_prompt = sys.argv[1]

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(20): 
        # call the model, handle responses, etc.
        success = generate_content(client, model, messages, args.verbose)
        if not success:
            exit(0)


def generate_content(client, model, messages, verbose):

    function_responses = []

    response = client.models.generate_content(
        model=model, 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    for candidate in response.candidates:
        messages.append(candidate.content)            
        
    if verbose:
        print(f"{RESET}Prompt tokens:{TEXT_WHITE} {response.usage_metadata.prompt_token_count}")
        print(f"{RESET}Response tokens:{TEXT_WHITE} {response.usage_metadata.candidates_token_count}")
        print("\n")   
            
    # call the model, handle responses, etc.
    if response.function_calls:
        for function_call in response.function_calls:            
            # print(f"{RESET}Calling function:\n{TEXT_MAGENTA}{function_call.name}({function_call.args})")
            function_call_result = call_function(function_call)
            
            if function_call_result.parts is None:
                raise Exception("Error: No function name or arguments provided")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Error: function_response should be a FunctionResponse object")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Error: No response")
            
            function_responses.append(function_call_result.parts[0])
            print(f":->{function_call_result.parts[0].function_response.response}")            
    else:
        print(f"{RESET}Response:\n{TEXT_GREEN}{response.text}")
        return False

    messages.append(types.Content(role="user", parts=function_responses))
    return True


if __name__ == "__main__":
    main()
