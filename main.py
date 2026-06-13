import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environmental variable not set")

    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    verbose: bool = args.verbose
    for i in range(20):
        response, function_responses, final_response = generate_content(client, messages, verbose)
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        messages.append(types.Content(role="user", parts=function_responses))
        if final_response:
            break
        if i == 20:
            print("Maximum number of agent iterations reached.")
            sys.exit(1)


def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed.")

    function_responses = []
    final_response: bool = False

    if verbose:
        print("User prompt:", messages[0].parts[0].text)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    if not response.function_calls:
        print("Response:")
        print(response.text)
        final_response = True
    else:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if not function_call_result.parts:
                raise Exception("function_call_result.parts is malformed")
            if not function_call_result.parts[0].function_response:
                raise Exception("function_call_result.parts[0].function_response is malformed")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("No function result")
            function_responses.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    return response, function_responses, final_response


if __name__ == "__main__":
    main()
