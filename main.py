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


@app.get("/test1")
async def tg_notif(name: str = Query(...),
                               pkg: str = Query(...),
                               title: str = Query(...),
                               text: str = Query(...),
                               subtext: str = Query(...),
                               bigtext: str = Query(...),
                               infotext: str = Query(...)):

    # Do something with the extracted data
    print("Name:", name)
    print("Package:", pkg)
    print("Title:", title)
    print("Text:", text)
    print("Subtext:", subtext)
    print("Bigtext:", bigtext)
    print("Infotext:", infotext)

    return {"message": "Notification received"}






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

