# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_palettefader`
================================================================================

PaletteFader is a CircuitPython driver class for brightness-adjusting color
lists and displayio palettes. Normalization is optionally applied to the palette
prior to brightness and gamma adjustments. Transparency index values are
preserved and associated with the adjusted palette. Creates an adjusted
displayio color palette object (displayio.Palette) that can also be read as a
color list.

For adjusting a single color value, create a list containing a single color or
use cedargrove_palettefader.set_single_color_brightness().

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------

The ulab-based reference palette creation code was adapted from the Adafruit
Ocean Epoxy Lightbox project's Reshader class; Copyright 2020 J Epler and L Fried.
<https://learn.adafruit.com/ocean-epoxy-resin-lightbox-with-rgb-led-matrix-image-scroller>

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  <https://circuitpython.org/downloads>

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Palette_Fader.git"

from ulab import numpy
import displayio


class PaletteFader:
    """Displayio palette fader with normalization, brightness (fading), and
    gamma control. Returns an adjusted displayio palette object."""

    def __init__(self, source_palette, brightness=1.0, gamma=1.0, normalize=False):
        """Instantiate the palette fader. Creates a reference numpy array
        containing RGB values derived from the source palette. During
        initialization, the maximum RGB component value for normalization is
        determined.

        :param union(list, displayio.Palette) source_palette: The color list or
          displayio palette object. No default.
        :param float brightness: The brightness value for palette adjustment.
          Value range is 0.0 to 1.0. Default is 1.0 (maximum brightness).
        :param float gamma: The gamma value for palette adjustment. Value range
          is 0.0 to 2.0. Default is 1.0 (no gamma adjustment).
        :param bool normalize: The boolean normalization state. True to normalize;
          False to skip normalization. Default is False (no normalization)."""

        self._src_palette = source_palette
        self._brightness = brightness
        self._gamma = gamma
        self._normalize = normalize

        self._list_transparency = []  # List of transparent items in a color list

        # Create the ulab array reference palette with source palette RGB values
        self._ref_palette = numpy.zeros((len(self._src_palette), 3), dtype=numpy.uint8)
        for index, color in enumerate(self._src_palette):
            rgb = self._src_palette[index]
            if rgb is not None:
                self._ref_palette[index, 2] = rgb & 0x0000FF
                self._ref_palette[index, 1] = (rgb & 0x00FF00) >> 8
                self._ref_palette[index, 0] = (rgb & 0xFF0000) >> 16
            else:
                # Store black in reference palette and note the index of the None value
                self._ref_palette[index] = [0, 0, 0]
                self._list_transparency.append(index)

        # Find the brightest RGB component; used for the normalization process
        if self._normalize:
            self._ref_palette_max = numpy.max(self._ref_palette)
        else:
            # If normalization is not selected, set the value to maximum (8-bit)
            self._ref_palette_max = 0xFF
        self.fade_normalize()


    @property
    def brightness(self):
        """The palette's overall brightness level, 0.0 to 1.0."""
        return self._brightness

    @brightness.setter
    def brightness(self, new_brightness):
        if self._brightness != new_brightness:
            self._brightness = new_brightness
            self.fade_normalize()

    @property
    def gamma(self):
        """The adjusted palette's gamma value, typically from 0.0 to 2.0. The
        gamma adjustment is applied after the palette is normalized and
        brightness-adjusted."""
        return self._gamma

    @property
    def normalize(self):
        """The palette's normalization mode state; True for normalization
        applied; False for no normalization."""
        return self._normalize

    @property
    def palette(self):
        """The adjusted displayio palette."""
        return self._new_palette

    def fade_normalize(self):
        """Create an adjusted displayio palette from the reference palette. Use
        the current brightness, gamma, and normalize parameters to build the
        adjusted palette. The reference palette is first adjusted for
        brightness and normalization (if enabled), followed by the gamma
        adjustment. Transparency index values are preserved."""

        # Determine the normalization factor to apply to the palette
        self._norm_factor = round((0xFF / self._ref_palette_max) * self._brightness, 3)

        self._new_palette = self._src_palette  # Preserves transparency association
        # Adjust for normalization and brightness
        norm_palette = numpy.array(
            self._ref_palette * self._norm_factor, dtype=numpy.uint8
        )
        # Adjust result for gamma
        norm_palette = numpy.array(norm_palette**self._gamma, dtype=numpy.uint8)

        # Build new_palette with the newly normalized changes
        for i, color in enumerate(norm_palette):
            if i in self._list_transparency:
                self._new_palette[i] = None
            else:
                self._new_palette[i] = (
                    (norm_palette[i, 0] << 16)
                    + (norm_palette[i, 1] << 8)
                    + norm_palette[i, 2]
                )


def set_single_color_brightness(self, source_color=None, brightness=1.0, gamma=1.0):
    """Scale a 24-bit RGB source color value in proportion to the brightness
    setting (0 to 1.0). Returns an adjusted 24-bit RGB color value or None if
    the source color is None (transparent). The adjusted color's gamma value is
    typically from 0.0 to 2.0 with a default of 1.0 for no gamma adjustment.

    :param int source_color: The color value to be adjusted. Default is None.
    :param float brightness: The brightness value for color value adjustment.
      Value range is 0.0 to 1.0. Default is 1.0 (maximum brightness).
    :param float gamma: The gamma value for color value adjustment. Value range
      is 0.0 to 2.0. Default is 1.0 (no gamma adjustment).

    :return int: The adjusted color value."""

    if source_color is None:
        return

    # Extract primary colors and scale to brightness
    r = min(int(brightness * ((source_color & 0xFF0000) >> 16)), 0xFF)
    g = min(int(brightness * ((source_color & 0x00FF00) >> 8)), 0xFF)
    b = min(int(brightness * ((source_color & 0x0000FF) >> 0)), 0xFF)

    # Adjust result for gamma
    r = min(int(round((r**gamma), 0)), 0xFF)
    g = min(int(round((g**gamma), 0)), 0xFF)
    b = min(int(round((b**gamma), 0)), 0xFF)

    return (r << 16) + (g << 8) + b
