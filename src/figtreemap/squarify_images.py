import squarify
import matplotlib.patches as patches


def letterbox_extent(extent, img):
    """
    Compute an extent for imshow that preserves the image's aspect ratio
    while fitting entirely inside the given rectangle.

    Args:
        extent (tuple[float, float, float, float]): A tuple
            (xmin, xmax, ymin, ymax) defining the rectangle bounds in
            data coordinates.
        img (array-like): Image array shaped (H, W, C).

    Returns:
        list: A list [xmin2, xmax2, ymin2, ymax2] representing the adjusted
        extent that preserves the aspect ratio.
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
    """Add images to fit within rectangles in a plot.
        `squares` and `images` should be iterables of the same length.
        Optionally preserve the image aspect ratio with `letterbox=True`.

    Args:
        squares (list[matplotlib.pathces.Rectangle]): List of rectangle objects in a plot.
        images (list[PIL.PngImagePlugin.PngImageFile]): List of PNG images.
        ax (matplotlib.axes._axes.Axes): A matplotlib axes to add the images to.
        letterbox (bool, optional): Should the image aspect ratio be preserved? Defaults to True.
        aspect (str, optional): `aspect` argument passed to `imshow`. Defaults to "auto".
    """
    for square, image in zip(squares, images):
        x0 = square.get_x()
        y0 = square.get_y()
        width = square.get_width()
        height = square.get_height()
        extent = (x0, x0 + width, y0, y0 + height)
        if letterbox:
            extent = letterbox_extent(extent, image)
        ax.imshow(image, extent=extent, aspect=aspect, zorder=square.get_zorder() + 1)


def _sort_relative_to_x(x, y):
    """Sort y based on the values in x

    Args:
        x (iterable): An iterable to sort by its values.
        y (iterable): An iterable in the same order as x in need of sorting.

    Returns:
        list: A list of the values in y, sorted by the values in x.
    """
    sorted_y = sorted(zip(x, y), key=lambda xy: xy[0], reverse=True)
    return sorted_y


def figtreemap(sizes, images, letterbox=True, aspect="auto", sort=True, **kwargs):
    """Plot treemap with figures in it.

    Uses `squarify.plot()` to create a tree map then adds images to the rectangles
    with `squarify_images`. `sizes` and `images` must be in the same order so the
    first size goes with the first image etc.

    Args:
        sizes (list[float]): An iterable of numbers to convert to colours.
        images (list[PIL.PngImagePlugin.PngImageFile]): List of PNG images.
        letterbox (bool, optional): Should the image aspect ratio be preserved? Defaults to True.
        sort (bool, optional): Should the images (and other attributes) be sorted by sizes? Improves squareness. Defaults to True.
        aspect (str, optional): `aspect` argument passed to `imshow`. Defaults to "auto".
        **kwargs: Any additional keyword arguments are passed to `squarify.plot` e.g. `facecolor` and `edgecolor`.
            can be used to edit the rectangles behind the figures. Or labels can be added with `label`.
    """
    if sort:
        # Sort sizes and images based on sizes
        images = [image for _, image in _sort_relative_to_x(x=sizes, y=images)]
        for key, values in kwargs.items():
            try:
                if len(sizes) == len(values):
                    sorted_values = _sort_relative_to_x(x=sizes, y=values)
                    kwargs[key] = [v for _, v in sorted_values]
            except TypeError:
                pass
                # values for key not sorted relative to sizes
        sizes = sorted(sizes, reverse=True)
    # Get the rectangle artists we need
    squarify_plot = squarify.plot(sizes, **kwargs)
    # Get the rectangle artists we need
    # Assumes the first n Rectangles are the squares, where n is the number of sizes
    rect_artists = [
        rect
        for rect in squarify_plot.get_children()
        if isinstance(rect, patches.Rectangle)
    ]
    rect_artists = rect_artists[: len(sizes)]
    squarify_images(
        rect_artists, images, ax=squarify_plot, letterbox=letterbox, aspect=aspect
    )
