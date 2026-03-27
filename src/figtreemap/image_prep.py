"""Prepare images for treemap, simple SVG image editing and convertion to PNG"""

import requests
from lxml import etree
import numpy as np
from io import BytesIO
import cairosvg
import io
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt


def size_colours(sizes, colormap="viridis", normalise=True):
    """Convert a list of sizes to colour hex codes

    Converts `sizes` to colours using a matplotlib colour map,
    and returns the colours as hex codes. Optionally normalises
    the given `sizes` to 0-1 first.

    Args:
        sizes (list[float]): An iterable of numbers to convert to colours
        colormap (str, optional): Name of a matplotlib colour map, or a colormap that accepts numbers 0-1. Defaults to "viridis".
        normalise (bool, optional): Should `sizes` be normalised before converting to colours?

    Returns:
        (list[str]): List of colour hex codes
    """
    if isinstance(colormap, str):
        colormap = plt.get_cmap(colormap)
    if normalise:
        norm = matplotlib.colors.Normalize()
        colours = colormap(norm(sizes))
    else:
        norm = matplotlib.colors.Normalize()
        colours = colormap(sizes)
    hexcolours = [matplotlib.colors.to_hex(c) for c in colours]
    return hexcolours


def edit_svg_tree(tree, **kwargs):
    """Set attributes of an SVG element tree

    Args:
        tree (lxml.etree._ElementTree): An SVG element tree
        **kwargs: Any additional keyword arguments are used to update SVG attributes of all elements.
            E.g. `fill`, `stroke`, `stroke_width`. Note that _ are internally converted to -, e.g. `stroke_width` becomes `stroke-width`.

    Returns:
        (lxml.etree._ElementTree): An updated tree
    """
    root = tree.getroot()
    for key, value in kwargs.items():
        for elem in root.iter():
            svg_attr = key.replace("_", "-")
            elem.set(svg_attr, value)
    return tree


def svg2png(tree):
    """Converts an SVG element tree to a PNG

    Args:
        tree (lxml.etree._ElementTree): An SVG element tree

    Returns:
        (PIL.PngImagePlugin.PngImageFile): PNG image
    """
    svg_bytes = etree.tostring(tree.getroot())
    png_bytes = cairosvg.svg2png(bytestring=svg_bytes)
    png = Image.open(io.BytesIO(png_bytes))
    return png


def prep_svg(tree: etree._ElementTree, **kwargs):
    """Edits an SVG element tree and converts it to a PNG

    Args:
        tree (lxml.etree._ElementTree): An SVG element tree
        **kwargs: Any additional keyword arguments are used to update SVG attributes of all elements.
            E.g. `fill`, `stroke`, `stroke_width`. Note that _ are internally converted to -, e.g. `stroke_width` becomes `stroke-width`.

    Returns:
        (PIL.PngImagePlugin.PngImageFile): PNG image
    """
    tree = edit_svg_tree(tree, **kwargs)
    png = svg2png(tree)
    return png
