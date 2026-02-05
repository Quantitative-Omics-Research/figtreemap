import pytest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import matplotlib.patches as patches

import figtreemap.squarify_images as mod


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


class DummyImage:
    """Minimal stand-in for PIL image using only `.size`."""

    def __init__(self, w, h):
        self.size = (w, h)


# ---------------------------------------------------------------------
# letterbox_extent
# ---------------------------------------------------------------------


def test_letterbox_extent_wider_image_matches_width():
    # image wider than rect -> shrink height
    extent = (0, 10, 0, 10)  # square
    img = DummyImage(20, 10)  # aspect 2

    xmin, xmax, ymin2, ymax2 = mod.letterbox_extent(extent, img)

    assert xmin == 0
    assert xmax == 10
    # height becomes 10/2 = 5 centered at 5
    assert pytest.approx(ymin2) == 2.5
    assert pytest.approx(ymax2) == 7.5


def test_letterbox_extent_taller_image_matches_height():
    extent = (0, 10, 0, 10)
    img = DummyImage(10, 20)  # aspect 0.5

    xmin2, xmax2, ymin, ymax = mod.letterbox_extent(extent, img)

    assert ymin == 0
    assert ymax == 10
    # width becomes 10 * 0.5 = 5 centered at 5
    assert pytest.approx(xmin2) == 2.5
    assert pytest.approx(xmax2) == 7.5


def test_letterbox_extent_equal_aspect_returns_original():
    extent = (0, 10, 0, 5)
    img = DummyImage(10, 5)

    assert mod.letterbox_extent(extent, img) == [0, 10, 0, 5]


# ---------------------------------------------------------------------
# squarify_images
# ---------------------------------------------------------------------


def test_squarify_images_calls_imshow_with_letterbox():
    rect = patches.Rectangle((0, 0), 10, 10)
    rect.set_zorder(2)

    img = DummyImage(20, 10)

    ax = MagicMock()

    mod.squarify_images([rect], [img], ax, letterbox=True, aspect="equal")

    ax.imshow.assert_called_once()
    _, kwargs = ax.imshow.call_args

    assert kwargs["aspect"] == "equal"
    assert kwargs["zorder"] == 3
    # height should be letterboxed to 5
    assert pytest.approx(kwargs["extent"][3] - kwargs["extent"][2]) == 5


def test_squarify_images_without_letterbox_uses_full_extent():
    rect = patches.Rectangle((1, 2), 4, 6)
    img = DummyImage(20, 10)

    ax = MagicMock()

    mod.squarify_images([rect], [img], ax, letterbox=False)

    _, kwargs = ax.imshow.call_args
    assert kwargs["extent"] == (1, 5, 2, 8)


# ---------------------------------------------------------------------
# _sort_relative_to_x
# ---------------------------------------------------------------------


def test_sort_relative_to_x_descending():
    x = [1, 3, 2]
    y = ["a", "b", "c"]

    result = mod._sort_relative_to_x(x, y)

    assert result == [(3, "b"), (2, "c"), (1, "a")]


# ---------------------------------------------------------------------
# figtreemap
# ---------------------------------------------------------------------


def make_rect(x):
    return patches.Rectangle((x, 0), 1, 1)


def test_figtreemap_sorts_sizes_and_images_and_passes_to_helpers():
    sizes = [1, 3, 2]
    images = ["img1", "img3", "img2"]

    fake_ax = SimpleNamespace()

    rects = [make_rect(i) for i in range(3)]
    fake_ax.get_children = lambda: rects

    with (
        patch.object(mod.squarify, "plot", return_value=fake_ax) as plot_mock,
        patch.object(mod, "squarify_images") as sq_images_mock,
    ):
        mod.figtreemap(sizes, images, letterbox=True, aspect="auto")

    # sizes sorted descending
    plot_mock.assert_called_once()
    assert plot_mock.call_args.args[0] == [3, 2, 1]

    # images sorted to match sizes
    args, kwargs = sq_images_mock.call_args
    passed_rects, passed_images = args[0], args[1]

    assert passed_images == ["img3", "img2", "img1"]
    assert passed_rects == rects[:3]


def test_figtreemap_no_sort_keeps_order():
    sizes = [1, 3, 2]
    images = ["a", "b", "c"]

    fake_ax = SimpleNamespace()
    rects = [make_rect(i) for i in range(3)]
    fake_ax.get_children = lambda: rects

    with (
        patch.object(mod.squarify, "plot", return_value=fake_ax) as plot_mock,
        patch.object(mod, "squarify_images") as sq_images_mock,
    ):
        mod.figtreemap(sizes, images, sort=False)

    assert plot_mock.call_args.args[0] == sizes

    args, _ = sq_images_mock.call_args
    assert args[1] == images
