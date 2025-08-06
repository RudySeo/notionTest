from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

app = FastAPI()


class MeetingRequest(BaseModel):
    title: str
    date: str
    content: list[str]
    summary: list[str]
    keywords: list[str]


@app.post("/create_meeting")
async def create_meeting(req: MeetingRequest):
    children = (
        [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "📝 회의록"}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": f"📅 날짜: {req.date}"}}
                    ]
                },
            },
            {"object": "block", "type": "divider", "divider": {}},
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📌 회의 내용"}}]
                },
            },
        ]
        + [
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": item}}]
                },
            }
            for item in req.content
        ]
        + [
            {"object": "block", "type": "divider", "divider": {}},
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🧠 요약"}}]
                },
            },
        ]
        + [
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": item}}]
                },
            }
            for item in req.summary
        ]
        + [
            {"object": "block", "type": "divider", "divider": {}},
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🔑 키워드"}}]
                },
            },
        ]
        + [
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"`{item}`"}}]
                },
            }
            for item in req.keywords
        ]
    )

    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "properties": {"title": [{"type": "text", "text": {"content": req.title}}]},
        "children": children,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.notion.com/v1/pages", headers=headers, json=payload
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {
        "message": "회의록이 성공적으로 생성되었습니다.",
        "notion_response": response.json(),
    }
