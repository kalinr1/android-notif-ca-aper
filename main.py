import re
import urllib

from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from urllib.parse import unquote, parse_qs

from telethon import TelegramClient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

def parse_url_encoded_data(data):
    decoded_data = {}
    for key, value in parse_qs(data.decode()).items():
        decoded_data[key] = unquote(value[0])
    return decoded_data


@app.post('/test1')
async def receive_notification(data: bytes = Form(...)):
    form_data = parse_url_encoded_data(data)
    name = form_data.get('name')
    title = form_data.get('title')
    text = form_data.get('text')

    print("Name:", name)
    print("Title:", title)
    print("Text:", text)

    return 'Received notification successfully!'



@app.post("/tg_notif")
async def tg_notif(request: Request):
    request_header = request.headers
    url = request.url
    request_body = await request.body()
    request_body_str = request_body.decode("utf-8")
    print("Received request:")
    print("Headers:", request_header)
    print("url:", url)
    print("Request body:", request_body)

    return {"message": "Notification received"}



def scan_post_for_ca(post_content: str):
    ca_pattern = r'\b[a-zA-Z0-9]{32,44}\b'
    ca_matches = re.finditer(ca_pattern, post_content)

    for match in ca_matches:
        ca_value = match.group()
        print("found a ca " + ca_value)
        # trojan_ape(ca_value)

