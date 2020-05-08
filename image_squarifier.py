from PIL import Image
from pathlib import Path
from os.path import join
from os import path
import os
import sys


def main():
    if len(sys.argv) != 3:
        print("Error, two arguments are required: <size> <directory_location>")
        exit(1)
    directory = sys.argv[2]
    if directory == "/":
        print("Error, root directory cannot be used.")
        exit(1)
    if not path.isdir(directory):
        print("Error, invalid directory path.")
        exit(1)

    size = sys.argv[1]
    if not is_int(size):
        print("Error, invalid size. Size must be a positive integer.")
        exit(1)

    size = int(size)

    files = list(Path(directory).rglob("*.[pP][nN][gG]"))
    print("Resizing", len(files), "files...")
    for file in files:
        im = Image.open(file)
        if im.mode != "RGB":
            continue
        edge_colors = get_edge_colors(im)
        average = get_averages(edge_colors)
        interval = get_majority_interval(average, edge_colors)
        color = get_edge_common_color(average, edge_colors, interval)
        resized_im = resize_im(size, im)
        new_im = Image.new("RGB", (size, size), color)
        result = paste_in_middle(new_im, resized_im)

        new_file_path = Path(join(get_new_path(directory), str(file.absolute())[len(directory):]))
        if not os.path.exists(new_file_path.parent):
            os.makedirs(new_file_path.parent)
        result.save(new_file_path)

    print("Resizing complete")
    exit(0)


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
    A tolorence of 20 is added to the average value to include colors that are close to the
    avarage but form the other side.
    :param interval: An integer that will specify the interval. If 0 then the interval is
    between 0 and ``avg``; if 1 then the interval is between ``avg`` and 255.
    :param sample: The color sample value, which will be checked if in interval. Type
    integet between 0 and 255.
    :param avg: A decimal value between 0 and 255.
    :return: A boolean value.
    """
    if interval and sample > (avg - 20): return True
    if not interval and sample < (avg + 20): return True
    return False


def resize_im(size, image):
    """
    A function that will resize an image so that its longest side is as long as `size`.
    :param size: The target size as a tuple (x,y)
    :param image: The image to resize
    :return: The new resized image
    """
    if image.size[0] > image.size[1]:
        size = (size, round(size * (image.size[1] / image.size[0])))
    else:
        size = (round(size * (image.size[0] / image.size[1])), size)
    return image.resize(size, Image.LANCZOS)


def paste_in_middle(background, foreground):
    """
    The function will past the foreground image on the middle of the background image.
    :param background: The bottom image. Must be larger than the foreground image.
    :param foreground: The top image. Must be smaller than the background image.
    :return: The new merged image.
    """
    x1 = round((background.size[0] - foreground.size[0]) / 2)
    y1 = round((background.size[1] - foreground.size[1]) / 2)
    x2 = x1 + foreground.size[0]
    y2 = y1 + foreground.size[1]
    box = (x1, y1, x2, y2)
    background.paste(foreground, box)
    return background


def get_new_path(input):
    """
    This function will take a path of a directory and return a new path of a new directory in
    the parent directory of the input path. `/home/user/images` will return `/home/user/images_resized`
    :param path: The input path as a string.
    :return: The new path as a string.
    """
    if input[-1] == '/':
        input = input[:-1]
    return input + "_resized"


def is_int(input):
    """
    A function that checks whether a given number is a positive integer
    :param input: The string to check.
    :return: A boolean value.
    """
    if len(input) == 0:
        return False
    try:
        x = int(input)
        if x < 1:
            return False
        else:
            return True
    except:
        return False


if __name__ == '__main__':
    main()
