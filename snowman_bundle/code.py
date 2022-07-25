# SPDX-FileCopyrightText: 2021, 2022 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# snowman_code.py
# 2022-07-24 v1.2

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
DISP_BRIGHTNESS = 0.1  # float: 0.1 to 1.0
STORM_INTENSITY = 1    # int: 0 to 3
STORM_INTENSITY = int(max(0, min(STORM_INTENSITY, 3)))

max_fg_flake_count = STORM_INTENSITY * 30
max_bg_flake_count = STORM_INTENSITY * 10

# Set up a few lists to store animation parameters for each snowflake.
fg_flake_duration  = []
bg_flake_duration  = []
fg_flake_displacement = []
bg_flake_displacement = []

display          = Matrix(bit_depth=6).display
display.rotation = 180  # Portrait orientation; MatrixPortal USB connect on bottom

center_group      = displayio.Group()  # The primary display group
fg_flakes = displayio.Group()
bg_flakes = displayio.Group()

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
    for i in range(0, max_fg_flake_count):
        snowflake = vectorio.Circle(
            pixel_shader=fg_flake_faded.palette,
            x=rn.randrange(0, 63),
            y=1 + (int(32 * (i / max_bg_flake_count)) % 32),
            radius=1,
        )
        fg_flakes.append(snowflake)
        fg_flake_duration.append(rn.random() / max_fg_flake_count)
        fg_flake_displacement.append(rn.randrange(1, 3))

    for i in range(0, max_bg_flake_count):
        snowflake = vectorio.Circle(
            pixel_shader=bk_flake_faded.palette,
            x=rn.randrange(3, 63),
            y=1 + (int(32 * (i / max_bg_flake_count)) % 32),
            radius=1,
        )
        bg_flakes.append(snowflake)
        bg_flake_duration.append(rn.random() / max_fg_flake_count)
        bg_flake_displacement.append(rn.randrange(1, 3))

display.show(center_group)

# Load landscape snowman bitmap
with open("/snowman_32_64.bmp", "rb") as snowman_bitmap:

    # Add and display the background snowflake layer.
    if STORM_INTENSITY != 0:
        center_group.append(bg_flakes)

    # Display the snowman bitmap graphic file.
    snowman = displayio.OnDiskBitmap(snowman_bitmap)
    snowman = displayio.TileGrid(snowman, pixel_shader=snowman_faded.palette, x=-6)
    center_group.append(snowman)

    # Add and display the foreground snowflake layer.
    # If STORM_INTENSITY is zero, display the snowman forever.
    if STORM_INTENSITY != 0:
        center_group.append(fg_flakes)
    else:
        while True:
            pass

    gc.collect()
    print(f"free memory = {gc.mem_free()/1000:6.3f} kB")

    # Animate the background and foreground snowflakes forever.
    while True:
        flake = rn.randrange(0, max_fg_flake_count)
        fg_flakes[flake].x = (
            fg_flakes[flake].x - fg_flake_displacement[i]
        )
        if fg_flakes[flake].x < -2:
            fg_flakes[flake].x = 66
            fg_flake_duration[flake] = rn.random() / max_fg_flake_count
            fg_flake_displacement[flake] = rn.randrange(1, 3)
        time.sleep(fg_flake_duration[flake])

        flake = rn.randrange(0, max_bg_flake_count)
        bg_flakes[flake].x = (
            bg_flakes[flake].x - bg_flake_displacement[i]
        )
        if bg_flakes[flake].x < 4:
            bg_flakes[flake].x = 66
            bg_flake_duration[flake] = rn.random() / max_bg_flake_count
            bg_flake_displacement[flake] = rn.randrange(1, 3)
        time.sleep(bg_flake_duration[flake])
