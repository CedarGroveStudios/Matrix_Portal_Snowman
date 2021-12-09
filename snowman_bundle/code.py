# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# matrix_portal_snowman.py
# 2021-12-08 v1.1

"""A two-layer snowstorm animation with a snowman bitmap image. STORM_INTENSITY
controls the maximum number of foreground and background snowflakes; 0 for
no storm, 3 for a hot-chocolate-inducing blizzard. A setting of 1 is relaxing."""

import board
import displayio
import gc
import random as rn
import time
import vectorio

from adafruit_matrixportal.matrix import Matrix

STORM_INTENSITY = 1  # 0 to 3
STORM_INTENSITY = int(max(0, min(STORM_INTENSITY, 3)))

max_foreground_flakes = STORM_INTENSITY * 30
max_background_flakes = STORM_INTENSITY * 10

# Set up a few lists to store animation parameters for each snowflake.
foreground_flake_time = []
background_flake_time = []
foreground_flake_displ = []
background_flake_displ = []

matrix = Matrix(bit_depth=6)
display = matrix.display

center_group = displayio.Group()  # The primary display group
foreground_flakes = displayio.Group()
background_flakes = displayio.Group()

# Define the snowman and snowflake color palettes.
snowman_palette = displayio.Palette(5)
snowman_palette[0] = 0x000000  # Background: BLACK
snowman_palette[1] = 0x600000  # Nose and hat trim: RED
snowman_palette[2] = 0x000070  # Hat and scarf: BLUE
snowman_palette[3] = 0x000000  # Eyes, mouth, and buttons (made of coal): BLACK
snowman_palette[4] = 0x606060  # Body and head: GRAY
snowman_palette.make_transparent(0)  # Make background transparent

foreground_snowflake_palette = displayio.Palette(1)
foreground_snowflake_palette[0] = 0xfcfcfc  # WHITE
background_snowflake_palette = displayio.Palette(1)
background_snowflake_palette[0] = 0x10101c  # GRAY

# Build the foreground and background snowflake layers.
if STORM_INTENSITY != 0:
    for i in range(0, max_foreground_flakes):
        snowflake = vectorio.Circle(
            pixel_shader=foreground_snowflake_palette,
            x = rn.randrange(0, 63),
            y = 1 + (int(32 * (i / max_background_flakes)) % 32),
            radius=1,
        )
        foreground_flakes.append(snowflake)
        foreground_flake_time.append(rn.random() / max_foreground_flakes)
        foreground_flake_displ.append(rn.randrange(1, 3))

    for i in range(0, max_background_flakes):
        snowflake = vectorio.Circle(
            pixel_shader=background_snowflake_palette,
            x = rn.randrange(3, 63),
            y = 1 + (int(32 * (i / max_background_flakes)) % 32),
            radius=1,
        )
        background_flakes.append(snowflake)
        background_flake_time.append(rn.random() / max_foreground_flakes)
        background_flake_displ.append(rn.randrange(1, 3))

display.show(center_group)

with open("/snowman_32_64.bmp", "rb") as f:

    # Add and display the background snowflake layer.
    if STORM_INTENSITY != 0:
        center_group.append(background_flakes)

    # Retrieve and display the snowman bitmap graphic file.
    snowman = displayio.OnDiskBitmap(f)
    snowman = displayio.TileGrid(snowman, pixel_shader=snowman_palette, x=-6)
    center_group.append(snowman)

    # Add and display the foreground snowflake layer.
    # If STORM_INTENSITY is zero, display the snowman forever.
    if STORM_INTENSITY != 0:
        center_group.append(foreground_flakes)
    else:
        while True:
            pass

    gc.collect()
    print(f'free memory = {gc.mem_free()/1000:6.3f} kB')

    # Animate the background and foreground snowflakes forever.
    while True:
        flake = rn.randrange(0, max_foreground_flakes)
        foreground_flakes[flake].x = (
            foreground_flakes[flake].x - foreground_flake_displ[i]
        )
        if foreground_flakes[flake].x < -2:
            foreground_flakes[flake].x = 66
            foreground_flake_time[flake] = rn.random() / max_foreground_flakes
            foreground_flake_displ[flake] = rn.randrange(1, 3)
        time.sleep(foreground_flake_time[flake])

        flake = rn.randrange(0, max_background_flakes)
        background_flakes[flake].x = (
            background_flakes[flake].x - background_flake_displ[i]
        )
        if background_flakes[flake].x < 4:
            background_flakes[flake].x = 66
            background_flake_time[flake] = rn.random() / max_background_flakes
            background_flake_displ[flake] = rn.randrange(1, 3)
        time.sleep(background_flake_time[flake])
