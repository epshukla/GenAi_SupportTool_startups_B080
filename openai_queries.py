from openai import OpenAI
from api import API_KEY

'''def construct_messages(system_prompt: str, user_prompt: str):
    """
    Constructs a list of messages for OpenAI's chat completion API.
    :param system_prompt: The system's role description.
    :param user_prompt: The user's request.
    :return: List of message dictionaries.
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def get_openai_response(model: str, messages: list):
    """
    Sends a request to OpenAI's API and returns the response.
    :param model: The OpenAI model to use (e.g., "gpt-4o").
    :param messages: A list of message dictionaries.
    :return: The response message from the API.
    """
    client = OpenAI(api_key = API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message.content  # Extracting content only

def get_openai_response_startup_investments(startup_industry: str):
    """
    Provides insights on startup investments for a given industry.
    :param startup_industry: The specific industry of the startup.
    :return: The response message from the API.
    """
    system_prompt = "You are an expert advisor on startup investments."
    user_prompt = f"I have a startup, I want to find the competitors and investors, and how much the investment is. Giving names of competitors and their investments is extremely important. I want you to give me all the results without markup and in plain text acompanied with a list of hyperlinks in plain text. Industry: {startup_industry}"    
    messages = construct_messages(system_prompt, user_prompt)
    return get_openai_response(model="gpt-4o", messages=messages)

# Example usage
response = get_openai_response_startup_investments("AI and Machine Learning")
print(response)'''

def construct_messages(system_prompt: str, user_prompt: str):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def get_openai_response(model: str, messages: list):
    client = OpenAI(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message.content  # Extracting content only

def get_openai_response_startup_investments(startup_industry: str):
    system_prompt = "You are an expert advisor on startup investments. Provide well-structured insights, ensuring competitors and investors are in plain text without Markdown. "
    user_prompt = f"I have a startup in {startup_industry}. I want to find competitors and investors, and how much the investment is. Giving names of competitors and their investment is extremely important. Provide results in plain text with a list of hyperlinks."    
    messages = construct_messages(system_prompt, user_prompt)
    
    return get_openai_response(model="gpt-4o", messages=messages)
