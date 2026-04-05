import os
import argparse
from constants import *
from dotenv import load_dotenv
from google import genai
from google.genai import types



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
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]    
    response = client.models.generate_content(model=model, contents=messages)

    print("\n")
    if args.verbose:
        print(f"{RESET}User prompt:{TEXT_WHITE} {args.user_prompt}")
        print(f"{RESET}Prompt tokens:{TEXT_WHITE} {response.usage_metadata.prompt_token_count}")
        print(f"{RESET}Response tokens:{TEXT_WHITE} {response.usage_metadata.candidates_token_count}")
        print("\n")    
    print(f"{RESET}Response:\n{TEXT_MAGENTA}{response.text}")
    print("\n")
    


if __name__ == "__main__":
    main()
