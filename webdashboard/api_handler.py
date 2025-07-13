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

