import pip
import os

try:
    import openai
except ImportError as e:
    pip.main(['install', 'openai'])
    import openai

from typing import List, Dict

openai.organization = "org-plLq512k1ocxDkVHLYDsmQXz"
# openai.api_key = os.getenv("OPENAI-API-KEY")
openai.api_key = "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"


def ai_request(request_text,
               system_role="You are a helpful assistant",
               training_messages=None,
               model="gpt-4-0613",
               tokens=1000) -> str:
    """
    Sends a request to the OpenAI API for a chat model and returns the AI's response.

    Parameters
    ---------
    request_text : str
        The text of the instruction/intent/query that will be sent to the AI.

    system_role : str, optional
        The system role's message or goal, by default "You are a helpful assistant".

    training_messages : list or dict, optional
        The list or dictionary of additional training messages that will be appended to the message sent to the AI.

    model : str, optional
        The ID of the OpenAI model being used, by default 'gpt-4-0613'.

    tokens : int, optional
        The maximum number of tokens in the response, by default 1000.

    Returns
    -------
    str
        The content of the AI's first response message.
    """
    messages = [{"role": "system", "content": system_role}]
    if training_messages and type(training_messages) == list:
        messages += training_messages
    elif training_messages and type(training_messages) == dict:
        messages.append(training_messages)
    messages.append({"role": "user", "content": f"{request_text}"})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=tokens
    )
    first_choice = 0
    text = response["choices"][first_choice]["message"]["content"]
    return text