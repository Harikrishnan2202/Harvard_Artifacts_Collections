import requests
import time
import sqlite3
from tqdm import tqdm

DB_PATH = "harvard_artifacts.db"
API_BASE = "https://api.harvardartmuseums.org"


def fetch_objects(classification, api_key, limit=1000):
    objects = []
    page = 1

    while len(objects) < limit:
        res = requests.get(f"{API_BASE}/object", params={
            "apikey": api_key,
            "classification": classification,
            "size": 100,
            "page": page,
            "hasimage": 1
        })

        data = res.json()

        if "records" not in data:
            break

        objects.extend(data["records"])

        if "next" not in data.get("info", {}):
            break

        page += 1
        time.sleep(0.2)

    return objects[:limit]


def transform(obj):
    metadata = {
        "id": obj.get("id"),
        "title": obj.get("title"),
        "culture": obj.get("culture"),
        "period": obj.get("period"),
        "century": obj.get("century"),
        "medium": obj.get("medium"),
        "dimensions": obj.get("dimensions"),
        "description": obj.get("description"),
        "department": obj.get("division"),
        "classification": obj.get("classification"),
        "accessionyear": obj.get("accessionyear"),
        "accessionmethod": obj.get("accessionmethod"),
    }

    images = obj.get("images") or []
    colors_raw = obj.get("colors") or []

    if not colors_raw:
        for img in images:
            colors_raw.extend(img.get("colors", []))

    media = {
        "objectid": obj.get("id"),
        "imagecount": len(images),
        "mediacount": len(images),
        "colorcount": len(colors_raw),
        "rank": obj.get("rank"),
        "datebegin": obj.get("datebegin"),
        "dateend": obj.get("dateend")
    }

    colors = []
    for c in colors_raw:
        colors.append({
            "objectid": obj["id"],
            "color": c.get("color"),
            "spectrum": c.get("spectrum"),
            "hue": c.get("hue"),
            "percent": c.get("percentage"),
            "css3": c.get("css3")
        })

    return metadata, media, colors


def insert_to_db(metadata_list, media_list, color_list):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executemany("""
        INSERT OR REPLACE INTO artifact_metadata
        (id,title,culture,period,century,medium,dimensions,description,department,classification,accessionyear,accessionmethod)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, [
        (m["id"], m["title"], m["culture"], m["period"], m["century"], m["medium"],
         m["dimensions"], m["description"], m["department"], m["classification"],
         m["accessionyear"], m["accessionmethod"])
        for m in metadata_list
    ])

    cur.executemany("""
        INSERT OR REPLACE INTO artifact_media
        (objectid,imagecount,mediacount,colorcount,rank,datebegin,dateend)
        VALUES (?,?,?,?,?,?,?)
    """, [
        (m["objectid"], m["imagecount"], m["mediacount"], m["colorcount"],
         m["rank"], m["datebegin"], m["dateend"])
        for m in media_list
    ])

    cur.executemany("""
        INSERT INTO artifact_colors (objectid,color,spectrum,hue,percent,css3)
        VALUES (?,?,?,?,?,?)
    """, [
        (c["objectid"], c["color"], c["spectrum"], c["hue"], c["percent"], c["css3"])
        for c in color_list
    ])

    conn.commit()
    conn.close()


def run_etl(classification, api_key, limit=500):
    print("Fetching objects...")
    objects = fetch_objects(classification, api_key, limit)

    metadata_rows, media_rows, color_rows = [], [], []

    for obj in tqdm(objects):
        m, mm, cc = transform(obj)
        metadata_rows.append(m)
        media_rows.append(mm)
        color_rows.extend(cc)

    print("Inserting into DB...")
    insert_to_db(metadata_rows, media_rows, color_rows)
    print("ETL Completed!")


if __name__ == "__main__":
    API_KEY = "1a7ae53e-a8d5-4ca8-8cbf-e12a843ceec9"
    run_etl("Paintings", API_KEY, limit=300)
