"""Get most specific phylopic svg url based on open tree taxonomy name and lineage
"""
import requests
from opentree import OT

API_BASE = "https://api.phylopic.org"
HEADERS = {"Accept": "application/vnd.phylopic.v2+json"}

def get_lineage_ott_ids(ott_id:int|str)->list[int]:
    record = OT.taxon_info(ott_id, include_lineage=True)
    lineage = record.response_dict.get('lineage')
    lineage_ott_ids = [ancestor.get('ott_id') for ancestor in lineage]
    return lineage_ott_ids

def get_phylopics_build_number():
    """Get the current PhyloPic build number (required for subsequent queries)."""
    resp = requests.get(API_BASE, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return data.get("build")

build = get_phylopics_build_number()

def get_phylopic_svg_url_from_ott_ids(ott_ids:list[int])->str:
    ott_ids_string = ",".join([str(id) for id in ott_ids])
    response = requests.get(
        API_BASE + 
        f"/resolve/opentreeoflife.org/taxonomy" + 
        f"?objectIDs={ott_ids_string}&" + 
        f"build={build}"
    )
    response.raise_for_status()
    href = response.json().get('_links').get('primaryImage').get('href')
    image_response = requests.get(API_BASE + href)
    image_response.raise_for_status()
    svg_url = image_response.json().get("_links").get("vectorFile").get("href")
    return svg_url

