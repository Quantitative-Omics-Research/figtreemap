import pandas as pd
import matplotlib.pyplot as plt
import figtreemap

mammal_size = pd.DataFrame(
    [
        ["Dog", "Canis familiaris", 62, 30,],
        ["Cat", "Felis catus", 65, 4,],
        ["Horse", "Equus ferus", 335, 450,],
        ["African Elephant", "Loxodonta africana", 660, 4800,],
        ["Cow", "Bos taurus", 280, 700,],
        ["Lion", "Panthera leo", 108, 190,],
    ],
    columns = [ "species", "latin", "gestation_days", "adult_mass_kg",]
)

# would map be faster?
sizes = mammal_size.adult_mass_kg
names = mammal_size.latin


svgs = [figtreemap.phylopics.get_svg(name) for name in names]
hexcolours = figtreemap.image_prep.size_colours(sizes)
imgs = [figtreemap.image_prep.prep_svg(svg, fill=colour, stroke="black", stroke_width="300") for svg,colour in zip(svgs, hexcolours)]

figtreemap.squarify_images.figtreemap(
    sizes,
    imgs,
    facecolor="white",
    edgecolor=hexcolours
)
plt.show()
