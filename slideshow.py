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
sprite = None


def update_image(dt):
    global img_cyc
    global window
    global sprite
    if sprite is not None:
        sprite.delete()
    if img_cyc is None:
        img_cyc = cycle(image_paths)
    next_img = img_cyc.next()
    img_feat = os.path.splitext(next_img)
    if img_feat[1] == ".gif":
        img = pyglet.image.load_animation(next_img)
    else:
        img = pyglet.image.load(next_img)
    sprite = pyglet.sprite.Sprite(img)
    sprite.image = img
    sprite.scale = get_scale(window, img)
    pos_x = window.width / 2.0 - sprite.width / 2.0
    pos_y = window.height / 2.0 - sprite.height / 2.0
    sprite.x = pos_x
    sprite.y = pos_y
    window.clear()


def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths


def get_scale(win, image):
    if isinstance(image, pyglet.image.Animation):
        if image.get_max_width() > image.get_max_height():
            scale = float(win.width) / image.get_max_width()
        else:
            scale = float(win.height) / image.get_max_height()
    else:
        if image.width > image.height:
            scale = float(win.width) / image.width
        else:
            scale = float(win.height) / image.height
    return scale


@window.event
def on_draw():
    sprite.draw()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images', nargs='?', default=os.getcwd())
    parser.add_argument('-w', '--wait', help='Waiting time between each image update', type=float, dest='wait_time', default=3.0)
    args = parser.parse_args()

    image_paths = get_image_paths(args.dir)
    update_image(0)

    pyglet.clock.schedule_interval(update_image, args.wait_time)

    pyglet.app.run()
