import requests
from lxml import etree
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import cairosvg
import io
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt

def size_colours(sizes, colormap="viridis"):
    if isinstance(colormap, str):
        colormap = plt.get_cmap(colormap)
    norm = matplotlib.colors.Normalize()
    colours = colormap(norm(sizes))
    hexcolours = [matplotlib.colors.to_hex(c) for c in colours]
    return hexcolours


def edit_svg_tree(tree, **kwargs):
    root = tree.getroot()
    for elem in root.iter():
        if "fill" in elem.attrib:
            elem.attrib["fill"] = colour
    return tree


def svg2png(tree):
    svg_bytes = etree.tostring(tree.getroot())
    png_bytes = cairosvg.svg2png(bytestring=svg_bytes)
    png = Image.open(io.BytesIO(png_bytes))
    return png

# tree:etree._ElementTree, colour=None:str
def prep_svg(tree:etree._ElementTree, colour:str=None):
    if colour:
        tree = fill_svg_tree(tree, colour)
    png = svg2png(tree)
    return png
