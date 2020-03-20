from PIL import Image


def main():
    im = Image.open("/media/sf_KTH/KEX/English/Img/GoodImg/Bmp/Sample033/img033-00023.png")
    print(im.format, im.size, im.mode)

    edge_colors = get_edge_colors(im)
    average = get_averages(edge_colors)
    interval = get_majority_interval(average, edge_colors)
    color = get_edge_common_color(average, edge_colors, interval)
    print(average)
    print(interval)
    print(color)

    im.save("/home/l/Documents/test.jpg")


def get_edge_colors(im):
    """
    This function will get the color values of the pixels that are
    located on the edge of an image

    :param im: The image of type (:py:class:`~PIL.Image.Image`), of which the pixel values are extracted.
    :returns: A list of tuples that represent the pixel values.
    """
    result = []
    for x in range(im.size[0]):
        result.append(im.getpixel((x, 0)))
        result.append(im.getpixel((x, im.size[1] - 1)))
    for y in range(1, im.size[1] - 1):
        result.append(im.getpixel((0, y)))
        result.append(im.getpixel((im.size[0] - 1, y)))
    return result


def get_averages(colors):
    """
    This function will calculate the average value of each color component (red, green, blue) in a
    given list of colors

    :param colors: The input list of colors, where each color is a tuple of the format (R, G, B).
    :returns: A tuple of format (R, G, B).
    """
    red = 0
    green = 0
    blue = 0
    for c in colors:
        red += c[0]
        green += c[1]
        blue += c[2]
    return (red / len(colors), green / len(colors), blue / len(colors))


def get_majority_interval(avg, colors):
    """
    The function will check for each color component if the majority of colors are grater than the average or
    less than. If the majority is grater, a value of 1 will be returned otherwise 0

    :param avg: The average value of each color component as a tuple (R,G,B)
    :param colors: The list of colors, where each color is (R,G,B) tuple
    :return: A tuple of 3 items, each item is either 0 or 1
    """
    countR, countG, countB = (0, 0, 0)
    for c in colors:
        if c[0] < avg[0]:
            countR += 1
        if c[1] < avg[1]:
            countG += 1
        if c[2] < avg[2]:
            countB += 1
    r, g, b = (0, 0, 0)
    if countR < (len(colors) / 2):
        r = 1
    if countG < (len(colors) / 2):
        g = 1
    if countB < (len(colors) / 2):
        b = 1
    return (r, g, b)


def get_edge_common_color(avg, colors, interval):
    """
    This funktion will calculate the average common color.

    :param avg: The average value of each color component as a tuple (R,G,B)
    :param colors: The list of colors, where each color is (R,G,B) tuple
    :param interval: The interval in which the common color exists. 0 for interval 0 to ``avg``,
    1 for the interval ``avg`` to 255.
    :return: A color as a (R,G,B) tuple.
    """
    selectedColors = []
    for c in colors:
        if in_interval(interval[0], c[0], avg[0]) \
                and in_interval(interval[1], c[1], avg[1]) \
                and in_interval(interval[2], c[2], avg[2]):
            selectedColors.append(c)
    r, g, b = get_averages(selectedColors)
    return (round(r), round(g), round(b))


def in_interval(interval, sample, avg):
    """
    A function that will check if a given value is within an interval.
    A tolorence of 10 is added to the average value to include colors that are close to the
    avarage but form the other side.
    :param interval: An integer that will specify the interval. If 0 then the interval is
    between 0 and ``avg``; if 1 then the interval is between ``avg`` and 255.
    :param sample: The color sample value, which will be checked if in interval. Type
    integet between 0 and 255.
    :param avg: A decimal value between 0 and 255.
    :return: A boolean value.
    """
    if interval and sample > (avg - 10): return True
    if not interval and sample < (avg + 10): return True
    return False


if __name__ == '__main__':
    main()
