from PIL import Image


def main():
    im = Image.open("/media/sf_KTH/KEX/English/Img/GoodImg/Bmp/Sample033/img033-00023.png")
    print(im.format, im.size, im.mode)

    edge_colors = get_edge_colors(im)
    average = get_averages(edge_colors)
    print(type(edge_colors))
    print(type(im))
    print(type(average))
    print(average)

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
    for y in range(im.size[1]):
        result.append(im.getpixel((0, y)))
        result.append(im.getpixel((im.size[0] - 1, y)))
    assert (im.size[0] + im.size[1]) * 2 == len(result)
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
    return (red/len(colors),green/len(colors),blue/len(colors))


if __name__ == '__main__':
    main()
