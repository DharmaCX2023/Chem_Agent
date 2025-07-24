import openai
import requests
import time
from bs4 import BeautifulSoup

def simple_web_search(query: str, api_key: str) -> str:
    enhanced_query = f"{query} chemical research"
    url = f"https://lite.duckduckgo.com/lite/?q={enhanced_query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=5)

    soup = BeautifulSoup(res.text, 'html.parser')
    snippets = []
    for link in soup.select('a.result-link'):
        text = link.get_text(strip=True)
        href = link.get('href')
        if text:
            snippets.append(f"{text} - {href}")
        if len(snippets) >= 15:
            break

    if not snippets:
        return "Sorry, no relevant information found."

    prompt = f"""You are a chemistry assistant. Based on the following web search snippets, answer the question: "{query}"

Snippets:
{chr(10).join(snippets)}

Answer:"""

    openai.api_key = api_key
    for i in range(3):
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return chat["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[Retry {i+1}] OpenAI error: {e}")
            if hasattr(e, "response"):
                print("Status:", e.response.status_code)
                print("Body:", e.response.text)
            time.sleep(2)
    return "OpenAI error after 3 retries."