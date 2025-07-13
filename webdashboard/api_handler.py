import os, json, urllib.parse, requests
import datetime, pprint

API  = "https://otmm-qa1.qm.org.qa/otmmapi/v6"
USER = os.getenv("OTMM_USER")
PWD  = os.getenv("OTMM_PASS")


def fetch_data():
    with requests.Session() as s:
        # logging in 
        login = s.post(
            f"{API}/sessions",
            data={"username": USER, "password": PWD},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15
        )
        login.raise_for_status()
        sess_json = login.json()["session_resource"]["session"]
        token     = sess_json["message_digest"]
        session_id= sess_json["id"]

        # base headers
        s.headers.update({
            "Accept": "application/json",
            "otmmauthtoken": token,
            "X-OTMM-Locale": "en_US"
        })

        # POST /search/text 
        search_headers = {
            "X-Requested-By": str(session_id),
            "X-Requested-With": "XMLHttpRequest",
            "Authorization": f"Bearer otmmToken {token}",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        form = {
            "keyword_query": "*",
            "load_type": "metadata",
            "load_multilingual_values": "true",
            "level_of_detail": "slim",
            "after": "0",
            "limit": "25",
            "multilingual_language_code": "en_US",
            "search_config_id": "3",
            "keyword_scope_id": "3",
            "preference_id": "ARTESIA.PREFERENCE.GALLERYVIEW.DISPLAYED_FIELDS",
            "metadata_to_return": "ARTESIA.FIELD.TAG",
        }

        r = s.post(
            f"{API}/search/text",
            headers=search_headers,
            data=urllib.parse.urlencode(form),
            timeout=30
        )
        r.raise_for_status()          # no 400 now
        return r.json()
    
def calculate_asset_count(assets):
    """
    Organises an OTMM asset_list into

        { "all_data": {
              "<Month>": {
                  "Week 1": {"images": n, "videos": n, "audio": n, "documents": n},
                  ...
                  "Week 4": {...}
              },
              ...
        } }

    - Month name is taken from date_imported 
    - Week buckets are 1-7, 8-14, 15-21, 22-end-of-month
    - File type is taken from mime_type / content_type:
        • image/*  or BITMAP/IMAGE  →  images
        • video/*  or VIDEO         →  videos
        • audio/*  or AUDIO         →  audio
        • everything else           →  documents
    """
    buckets = {}

    assets = assets["search_result_resource"]["asset_list"]
    for asset in assets:
        # extract date
        date_str = asset.get("date_imported") or asset.get("date_last_updated")
        if not date_str:
            continue                      # skip if no date

        ts = date_str.split("+")[0].split("-")[0] if "+" in date_str else date_str
        dt = datetime.fromisoformat(ts)
        month = dt.strftime("%B")           # get month name
        d = dt.day
        week = (
            "Week 1" if d <= 7 else         # get week number
            "Week 2" if d <= 14 else
            "Week 3" if d <= 21 else
            "Week 4"
        )

        # get file type
        mime = (asset.get("mime_type") or "").lower()
        ctype = (asset.get("content_type") or "").upper()

        if mime.startswith("image/") or ctype in {"BITMAP", "IMAGE"}:
            type_ = "images"
        elif mime.startswith("video/") or ctype == "VIDEO":
            type_ = "videos"
        elif mime.startswith("audio/") or ctype == "AUDIO":
            type_ = "audio"
        else:
            type_ = "documents"

        # increment the counter
        month_bucket = buckets.setdefault(month, {})
        week_bucket  = month_bucket.setdefault(week, {})
        week_bucket[type_] = week_bucket.get(type_, 0) + 1

    # initialize if key pair does not exist
    classes = ("images", "videos", "audio", "documents")
    for month_bucket in buckets.values():
        for w in ("Week 1", "Week 2", "Week 3", "Week 4"):
            week_bucket = month_bucket.setdefault(w, {})
            for cls in classes:
                week_bucket.setdefault(cls, 0)

    return {"all_data": buckets})


with open ("webdashboard/new_assets.json", "r") as f:
    assets = json.load(f)
    a = calculate_asset_count(assets)
    pprint.pprint(a)

