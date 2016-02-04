#!/usr/bin/env python
#
#  Copyright (c) 2013, 2015, Corey Goldberg
#
#  License: GPLv3


import argparse
import os
import pyglet

# Define global variables
window = pyglet.window.Window(fullscreen=True)
sprite = None
current_idx = 0


def update_image(dt):
    global window
    global sprite
    global current_idx
    if sprite is not None:
        old_img = sprite.image
        sprite.delete()
    else:
        old_img = pyglet.image.load(os.environ['HOME'] + "/Softwares/PySlideshow/not_found.jpg")

    new_imgs = set(get_image_paths(args.dir))
    if image_paths != new_imgs :
        image_paths.clear()
        image_paths.update(new_imgs)

    if current_idx >= len(image_paths):
        current_idx = 0

    next_img = list(image_paths)[current_idx]
    img_feat = os.path.splitext(next_img)
    try:
        if img_feat[1] == ".gif":
            img = pyglet.image.load_animation(next_img)
        else:
            img = pyglet.image.load(next_img)
    except:
        img = old_img
        print("Error while loading the image")
    sprite = pyglet.sprite.Sprite(img)
    sprite.image = img
    sprite.scale = get_scale(window, img)
    pos_x = window.width / 2.0 - sprite.width / 2.0
    pos_y = window.height / 2.0 - sprite.height / 2.0
    sprite.x = pos_x
    sprite.y = pos_y
    window.clear()
    current_idx += 1


def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths


def get_scale(win, image):
    ratio = win.width / float(win.height)
    if isinstance(image, pyglet.image.Animation):
        if image.get_max_width() > ratio * image.get_max_height():
            scale = float(win.width) / image.get_max_width()
        else:
            scale = float(win.height) / image.get_max_height()
    else:
        if image.width > ratio * image.height:
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

    image_paths = set(get_image_paths(args.dir))
    update_image(0)

    pyglet.clock.schedule_interval(update_image, args.wait_time)

    pyglet.app.run()
