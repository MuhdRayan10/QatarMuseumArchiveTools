import os, json, urllib.parse, requests

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
    Calculate the total number of assets from the fetched data.
    """
    total_count = assets["search_result_resource"]["search_result"]["total_hit_count"]
    assets = assets["search_result_resource"]["search_result"]["assetL_list"]
    
    month_template = {"videos": 0, "images": 0, "audio": 0, "documents": 0}
    data = {
        "all_data": {month:month_template for month in ["January", "February", "March", "April", "May", "June", 
                                            "July", "August", "September", "October", "November", "December"]}
    }

