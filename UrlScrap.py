# imports

import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI
from Website import *

# If you get an error running this cell, then please head over to the troubleshooting notebook!

# Load environment variables in a file called .env


# Constants

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"
# Check the key

#if not api_key:
#    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
#elif not api_key.startswith("sk-proj-"):
#   print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
#elif api_key.strip() != api_key:
#    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
#else:
#    print("API key found and looks good so far!")
#

# To give you a preview -- calling OpenAI with these messages is this easy. Any problems, head over to the Troubleshooting notebook.

#message = "Hello, GPT! This is my first ever message to you! Hi!"
#response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":message}])
#print(response.choices[0].message.content)

# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

# A function that writes a User Prompt that asks for summaries of websites:

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


# See how this function creates exactly the format above

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]


# And now: call the OpenAI API. You will get very familiar with this!

def summarize(url):
    website = Website(url)

    payload = {
        "model": MODEL,
        "messages": messages_for(website),
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
    print(response.json()['message']['content'])

def display_summary(url):
    summary = summarize(url)
    print(summary)
    #display(Markdown(summary))

display_summary("https://cnn.com")