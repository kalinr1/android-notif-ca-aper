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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# @app.on_event("startup")
# async def startup():
#     await client.connect()
#
#     if not await client.is_user_authorized():
#         await client.send_code_request(PHONE_NUMBER)
#         print("Code requested for authorization. Send a post request to authorize your account.")
#
#         await client.sign_in(PHONE_NUMBER, input('Enter the code: '))
#
#     print("TelegramClient started successfully!")


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

    scan_post_for_ca(message)


def scan_post_for_ca(message: str):
    ca_pattern = r'\b[a-zA-Z0-9]{32,44}\b'
    ca_matches = re.finditer(ca_pattern, message)

    for match in ca_matches:
        ca_value = match.group()
        print("found a ca " + ca_value)
        await send_ca_to_trojan(ca_value)

# tg_api_id = 123
# tg_api_hash = '123'
#
# tg_client = TelegramClient('session1', tg_api_id, tg_api_hash)
#
# tg_client.connect()
#
#
# async def trojan_ape(ca_value):
#     await tg_client.send_message("@handle", ca_value)
#     print("tg message")


# def parse_url_encoded_data(data):
#     decoded_data = {}
#     for key, value in parse_qs(data.decode()).items():
#         decoded_data[key] = unquote(value[0])
#     return decoded_data
#
#
# @app.get('/test1')
# async def receive_notification(data: bytes = Form(...)):
#     form_data = parse_url_encoded_data(data)
#     name = form_data.get('name')
#     title = form_data.get('title')
#     text = form_data.get('text')
#
#     print("Name:", name)
#     print("Title:", title)
#     print("Text:", text)
#
#     return 'Received notification successfully!'
#
#
# @app.post("/tg_notif")
# async def tg_notif(request: Request):
#     request_header = request.headers
#     url = request.url
#     request_body = await request.body()
#     request_body_str = request_body.decode("utf-8")
#     print("Received request:")
#     print("Headers:", request_header)
#     print("url:", url)
#     print("Request body:", request_body)
#
#     return {"message": "Notification received"}
#
#
# @app.get("/test2")
# async def tg_notif(name: str = Query(...),
#                    pkg: str = Query(...),
#                    title: str = Query(...),
#                    text: str = Query(...),
#                    subtext: str = Query(...),
#                    bigtext: str = Query(...),
#                    infotext: str = Query(...)):
#     # Do something with the extracted data
#     print("Name:", name)
#     print("Package:", pkg)
#     print("Title:", title)
#     print("Text:", text)
#     print("Subtext:", subtext)
#     print("Bigtext:", bigtext)
#     print("Infotext:", infotext)
#
#     return {"message": "Notification received"}
