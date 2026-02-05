import io
from unittest.mock import patch, MagicMock

import numpy as np
import pytest
from lxml import etree
from PIL import Image

import figtreemap.image_prep as mod


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def simple_svg_tree():
    """Small in-memory SVG for tests."""
    root = etree.Element("svg")
    etree.SubElement(root, "rect")
    etree.SubElement(root, "circle")
    return etree.ElementTree(root)


# ---------------------------------------------------------------------
# size_colours
# ---------------------------------------------------------------------


def test_size_colours_returns_hex_strings():
    sizes = [0, 5, 10]

    colours = mod.size_colours(sizes)

    assert len(colours) == 3
    assert all(isinstance(c, str) for c in colours)
    assert all(c.startswith("#") for c in colours)


def test_size_colours_accepts_colormap_object():
    import matplotlib.pyplot as plt

    cmap = plt.get_cmap("plasma")

    colours = mod.size_colours([1, 2, 3], colormap=cmap)

    assert len(colours) == 3


def test_size_colours_same_input_same_output():
    sizes = [1, 1, 1]
    colours = mod.size_colours(sizes)

    # identical sizes should map to identical colours
    assert len(set(colours)) == 1


# ---------------------------------------------------------------------
# edit_svg_tree
# ---------------------------------------------------------------------


def test_edit_svg_tree_sets_attributes_on_all_elements():
    tree = simple_svg_tree()

    out = mod.edit_svg_tree(tree, fill="red", stroke_width="2")

    root = out.getroot()

    for elem in root.iter():
        assert elem.get("fill") == "red"
        # underscore converted to dash
        assert elem.get("stroke-width") == "2"


def test_edit_svg_tree_returns_same_tree_instance():
    tree = simple_svg_tree()
    result = mod.edit_svg_tree(tree, fill="blue")

    assert result is tree


# ---------------------------------------------------------------------
# svg2png
# ---------------------------------------------------------------------


def test_svg2png_calls_cairosvg_and_returns_pil_image():
    tree = simple_svg_tree()

    fake_png_bytes = b"fakepng"

    fake_image = Image.new("RGB", (10, 10))

    with (
        patch.object(
            mod.cairosvg, "svg2png", return_value=fake_png_bytes
        ) as svg2png_mock,
        patch.object(mod.Image, "open", return_value=fake_image) as open_mock,
    ):
        img = mod.svg2png(tree)

    svg2png_mock.assert_called_once()
    open_mock.assert_called_once()
    assert img is fake_image


def test_svg2png_passes_svg_bytes_to_cairosvg():
    tree = simple_svg_tree()

    with (
        patch.object(mod.cairosvg, "svg2png", return_value=b"x") as mock_svg2png,
        patch.object(mod.Image, "open", return_value=MagicMock()),
    ):
        mod.svg2png(tree)

    args, kwargs = mock_svg2png.call_args
    assert "bytestring" in kwargs
    assert isinstance(kwargs["bytestring"], (bytes, bytearray))


# ---------------------------------------------------------------------
# prep_svg (integration)
# ---------------------------------------------------------------------


def test_prep_svg_calls_edit_and_svg2png_in_order():
    tree = simple_svg_tree()

    fake_img = Image.new("RGB", (5, 5))

    with (
        patch.object(mod, "edit_svg_tree", return_value=tree) as edit_mock,
        patch.object(mod, "svg2png", return_value=fake_img) as svg2png_mock,
    ):
        result = mod.prep_svg(tree, fill="green")

    edit_mock.assert_called_once_with(tree, fill="green")
    svg2png_mock.assert_called_once_with(tree)
    assert result is fake_img


def test_prep_svg_real_edit_then_mock_png():
    """Slightly higher level test combining real edit + mocked render."""
    tree = simple_svg_tree()

    fake_img = Image.new("RGB", (5, 5))

    with patch.object(mod, "svg2png", return_value=fake_img):
        img = mod.prep_svg(tree, fill="purple")

    # ensure edit happened
    for elem in tree.getroot().iter():
        assert elem.get("fill") == "purple"

    assert img is fake_img
