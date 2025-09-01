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

system_instructions = "Answer should not be more than 325 words."


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
    markdown_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    html = markdown2.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(True):
        tag["class"] = "text"
    html_output = soup.prettify()
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
                "parts": [{"text": f"Generate a very short title (max 5 words) for this conversation"}]
            })
    data = {"contents": accumulated_chat}
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    print(response)
    return response["candidates"][0]["content"]["parts"][0]["text"]
    