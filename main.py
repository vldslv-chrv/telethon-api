from fastapi import FastAPI, Query
from telethon.sync import TelegramClient
import os

app = FastAPI()

# Получение переменных из окружения
api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")

@app.get("/channel-posts")
def get_posts(channel: str = Query(..., alias="channel")):
    with TelegramClient("session", api_id, api_hash) as client:
        try:
            entity = client.get_entity(channel)
            messages = client.iter_messages(entity, limit=20)
            posts = []
            for msg in messages:
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
