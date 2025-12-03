import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from app.db import db
from app.services.crud import insert_document, find_documents

SCHEMES_COLLECTION = db["gov_schemes"]

async def fetch_schemes_from_portal():
    """
    Fetch scheme data from government portal (example: Data.gov.in agriculture schemes).
    NOTE: This is a scraper, you may need to adjust CSS selectors if site changes.
    """
    url = "https://www.myscheme.gov.in/schemes?sectors=agriculture"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=30)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")


    scheme_cards = soup.find_all("div", class_="MuiCard-root")
    schemes = []

    for card in scheme_cards:
        title_tag = card.find("h2")
        desc_tag = card.find("p")
        link_tag = card.find("a", href=True)

        if not title_tag:
            continue

        schemes.append({
            "title": title_tag.get_text(strip=True),
            "description": desc_tag.get_text(strip=True) if desc_tag else "",
            "source_url": link_tag["href"] if link_tag else url,
            "last_synced": datetime.utcnow(),
            "active": True
        })

    return schemes

async def sync_schemes():
    """
    Pull schemes from govt portal and insert into DB if new.
    """
    new_schemes = await fetch_schemes_from_portal()
    existing = await find_documents(SCHEMES_COLLECTION, {}, limit=1000)
    existing_titles = {s.get("title") for s in existing}

    added = []
    for scheme in new_schemes:
        if scheme["title"] not in existing_titles:
            scheme_id = await insert_document(SCHEMES_COLLECTION, scheme)
            added.append(scheme_id)

    return {"new_schemes_added": len(added), "ids": added}
