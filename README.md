# figtreemap
Plot treemaps with figures

Create treemaps with images proportional to the rectangles. This package focuses on getting and colouring [phylopic](https://www.phylopic.org/) SVGs but any PNG will work too.

# 🛠️ Installation

# 🚀 Quick start
```{python}
import matplotlib.pyplot as plt
import figtreemap

sizes = [30,4,450,700,190,1200,2,50,70,450,60]
names = ["Canis familiaris","Felis catus","Equus ferus","Bos taurus","Panthera leo","Giraffa camelopardalis","Oryctolagus cuniculus","Pan troglodytes","Homo sapiens","Ursus maritimus","Orycteropus afer"]

svgs = [figtreemap.phylopics.get_svg(name) for name in names]
imgs = [figtreemap.image_prep.prep_svg(svg) for svg in svgs]
figtreemap.squarify_images.figtreemap(sizes, imgs)
plt.show()
```
# ✨ Features

# 📄 Docs
Docs are hosted [here](https://quantitative-omics-research.github.io/figtreemap/)
with a [step by step guide](https://quantitative-omics-research.github.io/figtreemap/guide.html)
and [API reference](https://quantitative-omics-research.github.io/figtreemap/docs/api_index.html).

# 🐛 Troubleshooting
Please highlight bugs and ask questions as github [issues](https://github.com/Quantitative-Omics-Research/figtreemap/issues).

# 🤝 Contributing
Please make requests and suggestions as github [issues](https://github.com/Quantitative-Omics-Research/figtreemap/issues) and if you would like to make an improvement yourself please submit a pull request.

# ⚖️ Licence
`figtreemap` is distributed under [MIT licence](https://github.com/Quantitative-Omics-Research/figtreemap/blob/main/LICENCE).
