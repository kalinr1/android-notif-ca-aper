import re
import urllib
import os

from fastapi import FastAPI, Request, Query, Form
from urllib.parse import unquote, parse_qs

from telethon import TelegramClient

app = FastAPI()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

client = TelegramClient('session_name', API_ID, API_HASH)


@app.on_event("startup")
async def startup():
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(PHONE_NUMBER)
        print(
            "Code requested for authorization. Send a post request to '/tg_authorize' with a form to authorize your "
            "account.")


@app.post("/tg_authorize")
async def authorize(code: str = Form(...)):
    await client.sign_in(PHONE_NUMBER, code)
    print("TelegramClient started successfully!")
    return {"message": "TelegramClient started successfully!"}


async def send_ca_to_trojan(message: str):
    entity = '@odysseus_trojanbot'

    await client.send_message(entity=entity, message=message)
    print("Message sent successfully!")


@app.post("/send_message")
async def test_send_message_api(message: str = Form(...)):
    print(message)
    await send_ca_to_trojan(message)


@app.post("/notifications")
async def handle_notifications_from_android(request: Request):
    request_body = await request.body()
    request_body = request_body.decode('utf-8')
    parsed_body = parse_qs(request_body)

    chat_and_sender = unquote(parsed_body['title'][0])
    message = unquote(parsed_body['text'][0])

    print(chat_and_sender + " " + message)

    await scan_post_for_ca(message)


async def scan_post_for_ca(message: str):
    ca_pattern = r'\b[a-zA-Z0-9]{32,44}\b'
    ca_matches = re.finditer(ca_pattern, message)

    for match in ca_matches:
        ca_value = match.group()
        print("found a ca " + ca_value)
        await send_ca_to_trojan(ca_value)

async def scan_post_for_dexscreener_link(message: str):
    ca_pattern = r'https:\/\/dexscreener.com\/solana\/\w+'
    ca_matches = re.finditer(ca_pattern, message)

    for match in ca_matches:
        ca_value = match.group()
        print("found a ca " + ca_value)
        await send_ca_to_trojan(ca_value)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
