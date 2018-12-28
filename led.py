from __future__ import print_function
from __future__ import division

import platform
import numpy as np
import socket
import atexit
import config

_api = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""Lightpack Server API connection"""

# Connect to api server
_api.connect((config.LIGHTPACK_HOST, int(config.LIGHTPACK_PORT)))

# Send Auth key if set
if config.LIGHTPACK_APIKEY != '':
    _api.send('apikey:' + config.LIGHTPACK_APIKEY + '\n')


# lock prismatik
_api.send('lock' + '\n')


_gamma = np.load(config.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""

_prev_pixels = np.tile(253, (3, config.N_PIXELS))
"""Pixel values that were most recently displayed on the LED strip"""

pixels = np.tile(1, (3, config.N_PIXELS))
"""Pixel values for the LED strip"""

_is_python_2 = int(platform.python_version_tuple()[0]) == 2


def handle_close():
    # unlock prismatik
    _api.send('unlock' + '\n')
    _api.close()

atexit.register(handle_close)


def update():
    """Update the LED values"""
    global pixels, _prev_pixels

    # Truncate values and cast to integer
    pixels = np.clip(pixels, 0, 255).astype(int)

    # Optional gamma correction
    p = _gamma[pixels] if config.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)

    # Update the pixels
    update_msg = 'setcolor:'

    for i in range(config.N_PIXELS):
        # Ignore pixels if they haven't changed (saves bandwidth)
        #if np.array_equal(p[:, i], _prev_pixels[:, i]):
        #    continue

        color_i = i

        if config.CENTER_OFFSET != 0:
            color_i += config.CENTER_OFFSET

            if color_i < 0:
                color_i = config.N_PIXELS - color_i

            if color_i > (config.N_PIXELS - 1):
                color_i = color_i - (config.N_PIXELS - 1)

        r = p[0][color_i]
        g = p[1][color_i]
        b = p[2][color_i]

        # append led data
        update_msg += str(i + 1) + '-' + str(r) + ',' + str(g) + ',' + str(b) + ';'

    # update px history
    _prev_pixels = np.copy(p)

    if config.N_PIXELS != config.NUM_LEDS:
        update_msg += str(config.NUM_LEDS) + '-0,0,0;'

    # send data
    _api.send(update_msg + '\n')
    

# Execute this file to run a LED strand test
# If everything is working, you should see a red, green, and blue pixel scroll
# across the LED strip continously
if __name__ == '__main__':
    import time

    # Turn all pixels off
    pixels *= 0
    pixels[0, 0] = 255  # Set 1st pixel red
    pixels[1, 1] = 255  # Set 2nd pixel green
    pixels[2, 2] = 255  # Set 3rd pixel blue

    print('Starting LED strand test')

    while True:
        pixels = np.roll(pixels, 1, axis=1)
        update()
        time.sleep(.1)
