import os, json, urllib.parse, requests
from datetime import datetime
from database import add_asset, get_asset_id_list

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
    
def update_data(assets):
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
    
    saved_assets = get_asset_id_list()
    assets = assets["search_result_resource"]["asset_list"]
    for asset in assets:

        # if asset already exists, skip it
        if asset["asset_id"] in saved_assets:
            continue

        # extract date
        date_str = asset.get("date_imported")
        if not date_str:
            continue                      # skip if no date

        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        month = dt.strftime("%B")           # get month name
        d = dt.day
        week = (
            1 if d <= 7 else         # get week number
            2 if d <= 14 else
            3 if d <= 21 else
            4
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

        # get user 
        user = asset.get("content_state_user_name", "unknown")

        add_asset(asset["asset_id"], user, month, week, type_)

