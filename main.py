import re

from fastapi import FastAPI, Request
from pydantic import BaseModel
from telethon import TelegramClient

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# @app.post("/tg_notif")
# async def tg_notif(request: Request):
#     request_body = await request.body()
#     request_body_str = request_body.decode("utf-8")
#     print("Received request:")
#     print(request_body_str)
# 
#     return {"message": "Notification received"}


@app.post("/tg_notif")
async def listen_for_post_tg_notif(request: Request):
    try:
        data = await request.form()
        name = data.get("name")
        pkg = data.get("pkg")
        title = data.get("title")
        text = data.get("text")
        subtext = data.get("subtext")
        bigtext = data.get("bigtext")
        infotext = data.get("infotext")
        print("received a message " + text)
        scan_post_for_ca(text)
    except Exception as e:
        return {"message": str(e)}


def scan_post_for_ca(post_content: str):
    ca_pattern = r'\b[a-zA-Z0-9]{32,44}\b'
    ca_matches = re.finditer(ca_pattern, post_content)

    for match in ca_matches:
        ca_value = match.group()
        print("found a ca " + ca_value)
        # trojan_ape(ca_value)


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
