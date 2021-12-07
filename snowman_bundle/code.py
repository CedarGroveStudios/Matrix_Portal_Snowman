# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# matrix_portal_snowman.py
# 2021-12-07 v1.0

import board
import displayio
import time
import random as rn
from   adafruit_matrixportal.matrix import Matrix
from   adafruit_display_shapes.circle import Circle

STORM_INTENSITY = 1  # 0 to 3
STORM_INTENSITY = int(max(0, min(STORM_INTENSITY, 3)))

max_flakes = STORM_INTENSITY * 32
flake_time = []
flake_displ = []

matrix = Matrix()
display = matrix.display

splash = displayio.Group()
flakes = displayio.Group()
display.show(splash)

with open("/snowman_32_64.bmp", "rb") as f:
    background = displayio.OnDiskBitmap(f)
    background = displayio.TileGrid(background, pixel_shader=displayio.ColorConverter(), x=-6)
    splash.append(background)

    if max_flakes == 0:
        while True:
            pass

    for i in range(0, max_flakes):
        snowflake = Circle(rn.randrange(0, 68), i % 32, 1, fill=0x8080ff)
        flakes.append(snowflake)
        flake_time.append(rn.random() / max_flakes)
        flake_displ.append(rn.randrange(1,3))
    splash.append(flakes)

    # Snowstorm loop
    while True:
        flake = rn.randrange(0, max_flakes)
        flakes[flake].x = flakes[flake].x - flake_displ[i]
        if flakes[flake].x < -2:
            flakes[flake].x = 68
            flake_time[flake] = rn.random() / max_flakes
            flake_displ[flake] = rn.randrange(1,3)
        time.sleep(flake_time[flake])
