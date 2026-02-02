
import requests
import phylopictreemap.phylopics as phylopics
from opentree import OT
import phylopictreemap.image_prep as image_prep
import requests
from lxml import etree
import numpy as np
from io import BytesIO
import cairosvg
import io
from PIL import Image
from phylopictreemap.squarify_images import pictreemap
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

mammal_size = pd.DataFrame(
    [
        ["African Elephant", "Loxodonta africana", 660, 4800,],
        ["Dog", "Canis familiaris", 62, 30,],
        ["Cat", "Felis catus", 65, 4,],
        ["Horse", "Equus ferus", 335, 450,],
        ["Cow", "Bos taurus", 280, 700,],
        ["Lion", "Panthera leo", 108, 190,],
    ],
    columns = [ "species", "latin", "gestation_days", "adult_mass_kg",]
)

# would map be faster?
sizes = mammal_size.adult_mass_kg
names = mammal_size.latin

svgs = [phylopics.get_svg(name) for name in names]
hexcolours = image_prep.size_colours(sizes)
imgs = [image_prep.prep_svg(svg, fill=colour, stroke="black", stroke_width="300") for svg,colour in zip(svgs, hexcolours)]

pictreemap(
    sizes,
    imgs,
    facecolor="white",
    edgecolor=hexcolours
)
plt.show()

root = svgs[0].getroot()
for elem in root.iter():
    elem


elems = root.iter()

elem=next(elems)
elem
elem.attrib

name = "Panthera leo"
svg = phylopics.get_svg(name)
img = image_prep.prep_svg(svg, "red")

x = [13,22,35,5]
pictreemap(
    x,
    [img]*len(x)
)

plt.show()

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

tree.write( "vector.svg", pretty_print=True, xml_declaration=True, encoding="UTF-8" )

# Get svg from file
tree = etree.parse("vector.svg")
tree = image_prep.edit_svg_tree(tree, fill="blue",stroke="black", stroke_width=15)
root = tree.getroot()
for elem in root.iter():
    elem


elems = root.iter()

elem=next(elems)
elem
elem.attrib

# colour and convert svg
img = image_prep.prep_svg(tree, fill="#ff00ff")

img = image_prep.prep_svg(tree)

x = [13,22,35,5]
pictreemap(
    x,
    [img]*len(x)
)

plt.show()
