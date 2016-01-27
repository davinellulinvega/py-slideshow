#!/usr/bin/env python
#
#  Copyright (c) 2013, 2015, Corey Goldberg
#
#  License: GPLv3


import argparse
import os
import pyglet
from itertools import cycle

# Define global variables
img_cyc = None
window = pyglet.window.Window(fullscreen=True)


def update_image(dt):
    global img_cyc
    if img_cyc is None:
        img_cyc = cycle(image_paths)
        print(image_paths)
    img = pyglet.image.load(img_cyc.next())
    sprite.image = img
    sprite.scale = get_scale(window, img)
    sprite.x = 0
    sprite.y = 0
    window.clear()


def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths


def get_scale(window, image):
    if image.width > image.height:
        scale = float(window.width) / image.width
    else:
        scale = float(window.height) / image.height
    return scale


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images', nargs='?', default=os.getcwd())
    parser.add_argument('-w', '--wait', help='Waiting time between each image update', type=float, dest='wait_time', default=3.0)
    args = parser.parse_args()

    image_paths = get_image_paths(args.dir)
    img = pyglet.image.load(image_paths[0])
    sprite = pyglet.sprite.Sprite(img)
    sprite.scale = get_scale(window, img)

    pyglet.clock.schedule_interval(update_image, args.wait_time)

    pyglet.app.run()
