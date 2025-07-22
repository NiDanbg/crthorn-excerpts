import json, datetime, requests, os
TOKEN = os.getenv("MEDIUM_TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
me = requests.get("https://api.medium.com/v1/me", headers=headers).json()['data']['id']

with open('articles_s1b1.json', encoding='utf-8') as f:
    arts = json.load(f)

today = datetime.datetime.utcnow().weekday()  # 0=Mon, 1=Tue ...
for art in arts:
    if art['publish_day_offset'] == today:
        payload = {
            "title": art['title'],
            "contentFormat": "markdown",
            "content": art['content'] + f"\n\n[👉 Купи книгата]({art['amazon_link']})",
            "tags": art['tags'],
            "publishStatus": "public",
            "canonicalUrl": f"https://crthorn.com/excerpt/{art['series']}b{art['book_no']}-{art['lang_code']}"
        }
        r = requests.post(f"https://api.medium.com/v1/users/{me}/posts",
                          headers=headers, json=payload)
        print(r.status_code, r.json().get('data', {}).get('url'))
