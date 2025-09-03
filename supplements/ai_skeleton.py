import os
from dotenv import load_dotenv
import markdown2
from bs4 import BeautifulSoup
import requests
import json
from supplements.entities import db, AiChat


load_dotenv()

gemini_key = os.environ.get("GEMINI_API_KEY")

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": gemini_key
}

system_instructions = "Answer should not be more than 325 words, if any of your response requires any at HTML content at any part of the response, wrap each tag in the HTML content around with <xmp> opening and </xmp> closing tags."

# in the HTML content around  # <xmp> opening and </xmp> closing tags

#  as your response will be rendered on an html page and we don't want your response messing with the HTML content

# replace < with &lt; and > with &gt; in the html content, let there be a <br> between every parent and child in the HTML content, that means, a <br> both between their opening and closing tags and wrap all elements in your response around with the <code> opening and </code> closing tags

# , if you are also explaining the function of an HTML tag in your HTML content, instead of using &lt;b&gt; turns the text bold, use <pre>&lt;b&gt;</pre> turns the text bold


def to_html(markdown_text):
    html = markdown2.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")
    # for tag in soup.find_all(True):
    #     tag["class"] = "text assistant-message"
    for tag in soup.find_all("a"):
        tag["class"] = "text"
    return soup.prettify()


def chat_ai(mes_sage):
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": system_instructions
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": mes_sage
                    }
                ]
            },
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_response = response.json()
    print(json_response)
    if "error" in json_response:
        markdown_text = "Service unavailable, please try again in 15 minutes."
        html_output = "<p>Service unavailable, please try again in 15 minutes.</p>"
    else:
        markdown_text = json_response["candidates"][0]["content"]["parts"][0]["text"]
        html_output = to_html(markdown_text)
    return {"raw_output": markdown_text, "html_output": html_output}


def accumulate_chat(i__d):
    chat = db.session.execute(db.select(AiChat).where(AiChat.id == i__d)).scalar()
    messages = chat.messages
    contents = []
    for message in messages:
        contents.append({"role": message.role, "parts": [{"text": message.message}]})
    return contents


def identify_chat(i_d):
    accumulated_chat = accumulate_chat(i_d)
    accumulated_chat.append({
                "role": "user",
                "parts": [{"text": f"Generate a very short title (max 5 words or max 50 characters total) for this conversation, I am creating an application and using you as the API, I am setting your response as the title of this chat on the side bar, i don't want the title on the sidebar to be more than one line, don't give me title options, just give me one, I want to copy your response and render it as the title directly and it must not be more than 5 words, just respond with the title, all messages that will come from my end next will be messages from a new chat which your title will be used to tag"}]
            })
    data = {"contents": accumulated_chat}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_response = response.json()
    print(json_response)
    if "error" in json_response:
        return "Service unavailable."
    else:
        return json_response["candidates"][0]["content"]["parts"][0]["text"]
    

def message_ai(contents, new_message):
    initial_contents = contents
    initial_contents.append({"role": "user", "parts": [{"text": new_message}]})
    data = {"contents": [initial_contents]}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_response = response.json()
    if "error" in json_response:
        markdown_text = "Service unavailable, please try again in 15 minutes."
        html_output = "<p>Service unavailable, please try again in 15 minutes.</p>"
    else:
        markdown_text = json_response["candidates"][0]["content"]["parts"][0]["text"]
        html_output = to_html(markdown_text)
    return {"raw_output": markdown_text, "html_output": html_output}


print("error" in {'error': {'code': 503, 'message': 'The model is overloaded. Please try again later.', 'status': 'UNAVAILABLE'}})