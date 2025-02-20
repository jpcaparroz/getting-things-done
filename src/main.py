import sys
sys.path.append("src")

from notion_integration import Notion


async def clear() -> None:
    notion = Notion()
    
    query = {
        "and": [
            {"property": "Checkbox", "checkbox": {"equals": False}},
            {"property": "Clean", "checkbox": {"equals": True}}
        ]
    }

    await notion.delete_pages(query)
