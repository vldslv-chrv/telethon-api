from fastapi import FastAPI, Query
from telethon import TelegramClient
import os

app = FastAPI()

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")

client = TelegramClient("session", api_id, api_hash)

@app.on_event("startup")
async def start():
    await client.start()

@app.get("/channel-posts")
async def get_posts(channel: str = Query(..., alias="channel")):
    try:
        entity = await client.get_entity(channel)
        messages = client.iter_messages(entity, limit=20)
        posts = []
        async for msg in messages:
            if msg.message:
                posts.append({
                    "id": msg.id,
                    "text": msg.message,
                    "views": msg.views,
                    "date": str(msg.date),
                    "link": f"https://t.me/{channel.replace('@','')}/{msg.id}"
                })
        return posts
    except Exception as e:
        return {"error": str(e)}