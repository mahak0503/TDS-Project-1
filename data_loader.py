import os
import requests
from bs4 import BeautifulSoup

def fetch_tds_portal():
    """Fetches text content from https://tds.s-anand.net/#/2025-01/ using requests (fallback since JS won't render)."""
    print("Fetching TDS portal content...")
    url = "https://tds.s-anand.net/#/2025-01/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator="\n").strip()

def fetch_discourse_forum():
    """Fetches latest forum posts from the IITM TDS discourse category."""
    print("Fetching IITM Discourse forum posts...")
    url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34.json"
    resp = requests.get(url)
    topics = resp.json()["topic_list"]["topics"]

    posts = []
    for topic in topics[:10]:  # Limit to 10 topics
        topic_id = topic["id"]
        t_url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_id}.json"
        t_resp = requests.get(t_url)
        if t_resp.status_code == 200:
            data = t_resp.json()
            for post in data["post_stream"]["posts"]:
                soup = BeautifulSoup(post["cooked"], "html.parser")
                text = soup.get_text()
                posts.append(text)

    return "\n\n".join(posts)

def generate_combined_file():
    print("Generating combined.txt...")
    portal = fetch_tds_portal()
    forum = fetch_discourse_forum()

    os.makedirs("data", exist_ok=True)
    with open("data/combined.txt", "w", encoding="utf-8") as f:
        f.write("TDS Portal Content:\n" + portal + "\n\n")
        f.write("Forum Content:\n" + forum)

    print("✅ combined.txt created with portal + forum content.")
