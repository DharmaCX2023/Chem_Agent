import requests
from bs4 import BeautifulSoup

def search_google_patents(query, api_key, max_results=10):
    response = requests.get(
        url="https://serpapi.com/search",
        params={
            "engine": "google_patents",
            "q": query,
            "api_key": api_key,
            "num": max_results
        }
    )

    if response.status_code != 200:
        return []

    results = []
    for p in response.json().get("organic_results", [])[:max_results]:
        link = p.get("patent_link")
        title, status = "", ""

        try:
            detail_response = requests.get(link, timeout=10)
            if detail_response.status_code == 200:
                soup = BeautifulSoup(detail_response.text, "html.parser")

                title_tag = soup.find("meta", attrs={"name": "DC.title"})
                if title_tag:
                    title = title_tag.get("content", "").strip()

        except Exception as e:
            print(f"Failed to fetch details for {link}: {e}")

        results.append({
            "number": p.get("publication_number"),
            "link": link,
            "title": title or p.get("title", ""),
            "inventors": p.get("inventor"),
            "status": p.get("country_status", "")
        })

    return results