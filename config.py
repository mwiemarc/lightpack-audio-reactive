"""Settings for audio reactive LED strip"""
from __future__ import print_function
from __future__ import division
import os


LIGHTPACK_HOST = '127.0.0.1'
"""Lightpack server host"""

LIGHTPACK_PORT = 3636
"""Lightpack server port"""

LIGHTPACK_APIKEY = ''
"""API Key for authentication"""


NUM_LEDS = 45
"""Number of leds"""

CENTER_OFFSET = 16
"""LED Strip center offset"""


USE_GUI = True
"""Whether or not to display a PyQtGraph GUI plot of visualization"""

DISPLAY_FPS = False
"""Whether to display the FPS when running (can reduce performance)"""

MIC_RATE = 44100
"""Sampling frequency of the microphone in Hz"""

SOFTWARE_GAMMA_CORRECTION = False
"""True for no hardware dithering available"""

GAMMA_TABLE_PATH = os.path.join(os.path.dirname(__file__), 'gamma_table.npy')
"""Location of the gamma correction table"""

FPS = 60
"""Desired refresh rate of the visualization (frames per second)

FPS indicates the desired refresh rate, or frames-per-second, of the audio
visualization. The actual refresh rate may be lower if the computer cannot keep
up with desired FPS value.

Higher framerates improve "responsiveness" and reduce the latency of the
visualization but are more computationally expensive.

Low framerates are less computationally expensive, but the visualization may
appear "sluggish" or out of sync with the audio being played if it is too low.

The FPS should not exceed the maximum refresh rate of the LED strip, which
depends on how long the LED strip is.
"""

N_PIXELS = NUM_LEDS if NUM_LEDS % 2 == 0 else NUM_LEDS - 1

_max_led_FPS = int(((N_PIXELS * 30e-6) + 50e-6)**-1.0)
assert FPS <= _max_led_FPS, 'FPS must be <= {}'.format(_max_led_FPS)

MIN_FREQUENCY = 500
#MIN_FREQUENCY = 200
"""Frequencies below this value will be removed during audio processing"""

MAX_FREQUENCY = 8000
#MAX_FREQUENCY = 12000
"""Frequencies above this value will be removed during audio processing"""

N_FFT_BINS = 24
"""Number of frequency bins to use when transforming audio to frequency domain

Fast Fourier transforms are used to transform time-domain audio data to the
frequency domain. The frequencies present in the audio signal are assigned
to their respective frequency bins. This value indicates the number of
frequency bins to use.

A small number of bins reduces the frequency resolution of the visualization
but improves amplitude resolution. The opposite is true when using a large
number of bins. More bins is not always better!

There is no point using more bins than there are pixels on the LED strip.
"""

N_ROLLING_HISTORY = 2
"""Number of past audio frames to include in the rolling window"""

MIN_VOLUME_THRESHOLD = 1e-7
"""No music visualization displayed if recorded audio volume below threshold"""
