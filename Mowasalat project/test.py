#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sys
import os
import pandas as pd
from openai import AzureOpenAI

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key="9453961433ad47bf9117f3b290928327",
    api_version="2023-05-15",
    azure_endpoint="https://moopenai.openai.azure.com/"
)


# In[ ]:


def is_in_doha(location):
    # Implement your logic to check if the location is within Doha, Qatar
    # For simplicity, let's assume all locations are within Doha for this example
    return True

def get_route(conversation):
    # Check if both origin and destination are within Doha, Qatar
    if is_in_doha(conversation[0]["content"]) and is_in_doha(conversation[1]["content"]):
        # Use chat completion to get the route directions
        response = client.chat.completions.create(
            model="OpenAiMo",
            messages=conversation
        )
        
        # Extract and return the route directions
        return response.choices[0].message.content.strip()
    else:
        return "Sorry, the origin or destination is not within Doha, Qatar."

def add_system_response(conversation, response):
    conversation.append({"role": "system", "content": response})

# Initialize conversation with a greeting
conversation = [{"role": "system", "content": "Hi! How can I help you today?"}]

first_message = True

while True:
    # Prompt the user to enter their message
    if first_message:
        user_message = input(conversation[0]["content"])
        first_message = False
    else:
        user_message = input()

    if user_message.lower() == ['exit', 'bye']:
        break

    # Add user's message to the conversation
    conversation.append({"role": "user", "content": user_message})

    # Call the get_route function with the conversation
    route = get_route(conversation)

    # Add the chatbot's response to the conversation
    conversation.append({"role": "system", "content": route})

    # Display chatbot's response
    print("Chatbot:", route)


# In[ ]:


