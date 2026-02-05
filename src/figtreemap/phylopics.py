"""Get most specific phylopic svg url based on open tree taxonomy name and lineage"""

import requests
from ratelimit import limits, sleep_and_retry 
from opentree import OT
from io import BytesIO
from lxml import etree

API_BASE = "https://api.phylopic.org"
HEADERS = {"Accept": "application/vnd.phylopic.v2+json"}

def get_phylopics_build_number():
    """Get the current PhyloPic build number (required for subsequent queries)."""
    resp = requests.get(API_BASE, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return data.get("build")


_build = None

def get_build():
    global _build
    if _build is None:
        _build = get_phylopics_build_number()
    return _build


def get_lineage_ott_ids(ott_id: int | str) -> list[int]:
    """Get open tree taxonomy IDs for lineage

    Args:
        ott_id (int | str): An open tree taxonomy ID

    Returns:
        list[int]: List of taxon IDs for given ID, most to least specific
    """
    record = OT.taxon_info(ott_id, include_lineage=True)
    lineage = record.response_dict.get("lineage")
    lineage_ott_ids = [ancestor.get("ott_id") for ancestor in lineage]
    return lineage_ott_ids


def get_phylopic_svg_url_from_ott_ids(ott_ids: list[int]) -> str:
    """Get primary SVG URL for first open tree taxonomy ID with available image

    Args:
        ott_ids (list[int]): List of open tree taxonomy IDs from most to least specific

    Returns:
        str: Most specific available SVG URL
    """
    ott_ids_string = ",".join([str(id) for id in ott_ids])
    build = get_build()
    response = requests.get(
        API_BASE
        + f"/resolve/opentreeoflife.org/taxonomy"
        + f"?objectIDs={ott_ids_string}&"
        + f"build={build}"
    )
    response.raise_for_status()
    href = response.json().get("_links").get("primaryImage").get("href")
    image_response = requests.get(API_BASE + href)
    image_response.raise_for_status()
    svg_url = image_response.json().get("_links").get("vectorFile").get("href")
    return svg_url

@sleep_and_retry 
@limits(calls=5, period=1) # max 5 calls per second
def get_svg(name: str):
    """Get a phylopic SVG based on a scientific name

    If no image is available, an image of the most specific available taxon will be returned

    Args:
        name (str): Scientific name from open tree taxonomy

    Returns:
        lxml.etree._ElementTree: lxml tree of SVG image
    """
    # Get open tree taxonomy id for name
    ott_id = OT.get_ottid_from_name(name)
    # Get lineage ids in case species not available
    lineage_ott_ids = get_lineage_ott_ids(ott_id)
    ott_ids = [str(ott_id)] + lineage_ott_ids
    # Get most specific svg url
    svgurl = get_phylopic_svg_url_from_ott_ids(ott_ids)
    # Get svg from url
    response = requests.get(svgurl)
    response.raise_for_status()
    tree = etree.parse(BytesIO(response.content))
    return tree
