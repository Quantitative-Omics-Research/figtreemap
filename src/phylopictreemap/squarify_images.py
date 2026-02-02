import squarify
import matplotlib.patches as patches


def letterbox_extent(extent, img):
    """
    Compute an extent for imshow that preserves the image's aspect ratio
    while fitting entirely inside the given rectangle.

    Parameters
    ----------
    xmin, xmax, ymin, ymax : float
        Rectangle bounds in data coordinates.
    img : array-like
        Image array (H x W x C).

    Returns
    -------
    extent : list [xmin2, xmax2, ymin2, ymax2]
        The adjusted extent that preserves aspect ratio.
    """

    # image aspect ratio (width / height)
    w, h = img.size
    img_aspect = w / h

    # rectangle aspect ratio
    xmin, xmax, ymin, ymax = extent
    rect_width = xmax - xmin
    rect_height = ymax - ymin
    rect_aspect = rect_width / rect_height

    # letterbox horizontally or vertically
    if img_aspect > rect_aspect:
        # image is wider → match width, shrink height
        new_height = rect_width / img_aspect
        y_center = (ymin + ymax) / 2
        ymin2 = y_center - new_height / 2
        ymax2 = y_center + new_height / 2
        return [xmin, xmax, ymin2, ymax2]

    else:
        # image is taller → match height, shrink width
        new_width = rect_height * img_aspect
        x_center = (xmin + xmax) / 2
        xmin2 = x_center - new_width / 2
        xmax2 = x_center + new_width / 2
        return [xmin2, xmax2, ymin, ymax]


def squarify_images(squares, images, ax, letterbox=True, aspect="auto"):
    for square, image in zip(squares, images):
        x0 = square.get_x()
        y0 = square.get_y()
        width = square.get_width()
        height = square.get_height()
        extent = (x0, x0 + width, y0, y0 + height)
        if letterbox:
            extent = letterbox_extent(extent, image)
        ax.imshow(image, extent=extent, aspect=aspect, zorder=square.get_zorder() + 1)


def pictreemap(sizes, pics, **kwargs):
    squarify_plot = squarify.plot(sizes, **kwargs)
    # Get the rectangle artists we need
    # Assumes the first n Rectangles are the squares, where n is the number of sizes
    rect_artists = [
        rect
        for rect in squarify_plot.get_children()
        if isinstance(rect, patches.Rectangle)
    ]
    rect_artists = rect_artists[: len(sizes)]
    squarify_images(rect_artists, pics, ax=squarify_plot, letterbox=True)
