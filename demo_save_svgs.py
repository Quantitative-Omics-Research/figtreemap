from lxml import etree
import matplotlib.pyplot as plt
import figtreemap

import requests
from io import StringIO
import pandas as pd
response = requests.get("https://gist.githubusercontent.com/DAWells/95fcd46057c66aaf33dd9ca7c294c4b2/raw/c670dce7063c6aaf65085eeead5823d9cd497b0f/gestation_mass.csv")
mammal_size = pd.read_csv(StringIO(response.text))

sizes = mammal_size.adult_mass_kg
names = mammal_size.latin

svgs = [figtreemap.phylopics.get_svg(name) for name in names]

for name,svg in zip(names, svgs):
    svg.write(
        f"phylopics/{name}.svg",
        encoding="utf-8",
        xml_declaration=True,
        pretty_print=True
    )
