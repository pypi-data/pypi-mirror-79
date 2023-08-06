Platform-independent beep function, easily installable with pip.

Provides a `simplebeep.beep(pitch, duration)` function and a `simplebeep.play_ndarray(array, sample_rate)` function.

For Linux, it uses gstreamer, which is usually already installed. On Windows / Mac the package depends on simpleaudio, which is automatically installed as a dependency when installing with `pip install simplebeep`.
