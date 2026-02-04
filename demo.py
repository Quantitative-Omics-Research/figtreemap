import matplotlib.pyplot as plt
import figtreemap

import requests
from io import StringIO
import pandas as pd
response = requests.get("https://gist.githubusercontent.com/DAWells/95fcd46057c66aaf33dd9ca7c294c4b2/raw/c670dce7063c6aaf65085eeead5823d9cd497b0f/gestation_mass.csv")
mammal_size = pd.read_csv(StringIO(response.text))

# mammal_size = pd.DataFrame(
#     [
#         ["Dog", "Canis familiaris", 62, 30,],
#         ["Cat", "Felis catus", 65, 4,],
#         ["Horse", "Equus ferus", 335, 450,],
#         ["African Elephant", "Loxodonta africana", 660, 4800,],
#         ["Cow", "Bos taurus", 280, 700,],
#         ["Lion", "Panthera leo", 108, 190,],
#     ],
#     columns = [ "species", "latin", "gestation_days", "adult_mass_kg",]
# )

sizes = mammal_size.adult_mass_kg
names = mammal_size.latin

# Download
# svgs = [figtreemap.phylopics.get_svg(name) for name in names]

# Load local
svgs = []
from lxml import etree
for name in names:
    tree = etree.parse(f"phylopics/{name}.svg")
    svgs.append(tree)

hexcolours = figtreemap.image_prep.size_colours(sizes)
imgs = [figtreemap.image_prep.prep_svg(svg, fill=colour, stroke="black", stroke_width="300") for svg,colour in zip(svgs, hexcolours)]

figtreemap.squarify_images.figtreemap(
    sizes,
    imgs,
    facecolor=hexcolours,
    alpha = 0.2,
    edgecolor=hexcolours
)
plt.show()
