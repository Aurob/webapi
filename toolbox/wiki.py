import requests
import os

def default():
    return "wiki"

def listpages(public_only=True):
    
    url = "https://api.notion.com/v1/search"
    headers = {
        'Authorization': f'Bearer {os.getenv("NOTION_TOKEN")}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }
    data = {
        "filter": {
            "value": "page",
            "property": "object"
        },
        "page_size": 100
    }
    
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
        pages = []
        for result in data["results"]:
            page_data = {}
            # if public_only:
            #     if result["public_url"] == None:
            #         continue

            page_data["title"] = result["properties"]["title"]["title"][0]["plain_text"]
            page_data["id"] = result["id"]
            page_data["url"] = result["public_url"]
            
            pages.append(page_data)
        return pages
    
    return False

