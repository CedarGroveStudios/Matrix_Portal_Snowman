# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# matrix_portal_snowman.py
# 2021-12-09 v1.1

import board
import displayio
import time
import random as rn
from   adafruit_matrixportal.matrix import Matrix
from   adafruit_display_shapes.circle import Circle

STORM_INTENSITY = 1  # 0 to 3
STORM_INTENSITY = int(max(0, min(STORM_INTENSITY, 3)))

max_foreground_flakes = STORM_INTENSITY * 30
max_background_flakes = STORM_INTENSITY * 10
foreground_flake_time = []
background_flake_time = []
foreground_flake_displ = []
background_flake_displ = []

matrix = Matrix()
display = matrix.display

center_group = displayio.Group()
foreground_flakes = displayio.Group()
background_flakes = displayio.Group()

if STORM_INTENSITY != 0:
    for i in range(0, max_foreground_flakes):
        snowflake = Circle(rn.randrange(0, 68), 0 + (i * int(32/max_background_flakes)) % 32, 1, fill=0xffffff)
        foreground_flakes.append(snowflake)
        foreground_flake_time.append(rn.random() / max_foreground_flakes)
        foreground_flake_displ.append(rn.randrange(1,3))

    for i in range(0, max_background_flakes):
        snowflake = Circle(rn.randrange(0, 68), 1 + (i * int(32/max_background_flakes)) % 32, 1, fill=0x404040)
        background_flakes.append(snowflake)
        background_flake_time.append(rn.random() / max_foreground_flakes)
        background_flake_displ.append(rn.randrange(1,3))
        #center_group.append(background_flakes)

display.show(center_group)

with open("/snowman_32_64.bmp", "rb") as f:

    if STORM_INTENSITY != 0:
        center_group.append(background_flakes)

    snowman_palette = displayio.Palette(5)
    snowman_palette[0] = 0x000000
    snowman_palette[1] = 0x600000
    snowman_palette[2] = 0x000060
    snowman_palette[3] = 0x000000
    snowman_palette[4] = 0x606060
    snowman_palette.make_transparent(0)

    snowman = displayio.OnDiskBitmap(f)
    snowman = displayio.TileGrid(snowman, pixel_shader=snowman_palette, x=-6)
    center_group.append(snowman)

    if STORM_INTENSITY != 0:
        center_group.append(foreground_flakes)
    else:
        while True:
            pass

    # Snowstorm loop
    while True:
        flake = rn.randrange(0, max_foreground_flakes)
        foreground_flakes[flake].x = foreground_flakes[flake].x - foreground_flake_displ[i]
        if foreground_flakes[flake].x < -2:
            foreground_flakes[flake].x = 68
            foreground_flake_time[flake] = rn.random() / max_foreground_flakes
            foreground_flake_displ[flake] = rn.randrange(1,3)
        time.sleep(foreground_flake_time[flake])

        flake = rn.randrange(0, max_background_flakes)
        background_flakes[flake].x = background_flakes[flake].x - background_flake_displ[i]
        if background_flakes[flake].x < -2:
            background_flakes[flake].x = 68
            background_flake_time[flake] = rn.random() / max_background_flakes
            background_flake_displ[flake] = rn.randrange(1,3)
        time.sleep(background_flake_time[flake])
