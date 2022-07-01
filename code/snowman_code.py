# SPDX-FileCopyrightText: 2021, 2022 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# snowman_code.py
# 2022-07-01 v1.2

"""A two-layer snowstorm animation with a snowman bitmap image. STORM_INTENSITY
controls the maximum number of foreground and background snowflakes; 0 for
no storm, 3 for a hot-chocolate-inducing blizzard. A setting of 1 is relaxing."""

import displayio
import gc
import random as rn
import time
import vectorio
from adafruit_matrixportal.matrix import Matrix
from cedargrove_palettefader import PaletteFader

# fmt: off
DISP_BRIGHTNESS = 0.5  # float: 0.1 to 1.0
STORM_INTENSITY = 1    # int: 0 to 3
STORM_INTENSITY = int(max(0, min(STORM_INTENSITY, 3)))

max_foreground_flakes = STORM_INTENSITY * 30
max_background_flakes = STORM_INTENSITY * 10

# Set up a few lists to store animation parameters for each snowflake.
foreground_flake_time  = []
background_flake_time  = []
foreground_flake_displ = []
background_flake_displ = []

display          = Matrix(bit_depth=6).display
display.rotation = 180  # Portrait orientation; MatrixPortal USB connect on bottom

center_group      = displayio.Group()  # The primary display group
foreground_flakes = displayio.Group()
background_flakes = displayio.Group()

# Define the snowman and snowflake color palettes.
snowman_palette_source    = displayio.Palette(5)
snowman_palette_source[0] = 0x000000  # Background: BLACK
snowman_palette_source[1] = 0xFF0000  # Nose and hat trim: RED
snowman_palette_source[2] = 0x0000FF  # Hat and scarf: BLUE
snowman_palette_source[3] = 0x000000  # Eyes, mouth, and buttons (made of coal): BLACK
snowman_palette_source[4] = 0xA0A0A0  # Body and head: GRAY
snowman_palette_source.make_transparent(0)  # Make background transparent

fg_flake_palette_source    = displayio.Palette(1)
fg_flake_palette_source[0] = 0xFFFFFF  # WHITE
bk_flake_palette_source    = displayio.Palette(1)
bk_flake_palette_source[0] = 0x8080C0  # BLUE-GRAY
# fmt: on

snowman_faded = PaletteFader(snowman_palette_source, max(DISP_BRIGHTNESS * 0.7, 0.1))
fg_flake_faded = PaletteFader(fg_flake_palette_source, max(DISP_BRIGHTNESS, 0.1))
bk_flake_faded = PaletteFader(bk_flake_palette_source, max(DISP_BRIGHTNESS * 0.6, 0.1))

# Build the foreground and background snowflake layers.
if STORM_INTENSITY != 0:
    for i in range(0, max_foreground_flakes):
        snowflake = vectorio.Circle(
            pixel_shader=fg_flake_faded.palette,
            x=rn.randrange(0, 63),
            y=1 + (int(32 * (i / max_background_flakes)) % 32),
            radius=1,
        )
        foreground_flakes.append(snowflake)
        foreground_flake_time.append(rn.random() / max_foreground_flakes)
        foreground_flake_displ.append(rn.randrange(1, 3))

    for i in range(0, max_background_flakes):
        snowflake = vectorio.Circle(
            pixel_shader=bk_flake_faded.palette,
            x=rn.randrange(3, 63),
            y=1 + (int(32 * (i / max_background_flakes)) % 32),
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
    snowman = displayio.TileGrid(snowman, pixel_shader=snowman_faded.palette, x=-6)
    center_group.append(snowman)

    # Add and display the foreground snowflake layer.
    # If STORM_INTENSITY is zero, display the snowman forever.
    if STORM_INTENSITY != 0:
        center_group.append(foreground_flakes)
    else:
        while True:
            pass

    gc.collect()
    print(f"free memory = {gc.mem_free()/1000:6.3f} kB")

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
