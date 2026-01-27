import requests
import phylopictreemap.phylopics as phylopics
from opentree import OT
import phylopictreemap.image_prep as image_prep
import requests
from lxml import etree
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import cairosvg
import io
from PIL import Image
from phylopictreemap.squarify_images import pictreemap

name = "Panthera leo"   # example: the lion
# Get open tree taxonomy id for name
ott_id = OT.get_ottid_from_name(name)
# Get lineage ids in case species not available
lineage_ott_ids = phylopics.get_lineage_ott_ids(ott_id)
ott_ids = [str(ott_id)] + lineage_ott_ids
# Get most specific svg url
svgurl = phylopics.get_phylopic_svg_url_from_ott_ids(ott_ids)


# Get svg from url
response = requests.get(svgurl)
response.raise_for_status()
tree = etree.parse(BytesIO(response.content))

# Get svg from file
tree = etree.parse("vector.svg")

# colour and convert svg
img = image_prep.prep_svg(tree, "#ff00ff")

img = image_prep.prep_svg(tree)

x = [13,22,35,5]
pictreemap(
    x,
    [img]*len(x)
)

plt.show()
