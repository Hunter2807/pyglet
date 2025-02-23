# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# Copyright (c) 2008-2021 pyglet contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

from pyglet.util import CodecRegistry, Decoder, Encoder
from .base import *

import pyglet


_debug = pyglet.options['debug_media']

registry = CodecRegistry()
add_decoders = registry.add_decoders
add_encoders = registry.add_encoders
get_decoders = registry.get_decoders
get_encoders = registry.get_encoders


class MediaDecoder(Decoder):

    def decode(self, filename, file, streaming):
        """Read the given file object and return an instance of `Source`
        or `StreamingSource`. 
        Throws DecodeException if there is an error.  `filename`
        can be a file type hint.
        """
        raise NotImplementedError()


class MediaEncoder(Encoder):

    def encode(self, source, filename, file):
        """Encode the given source to the given file.  `filename`
        provides a hint to the file format desired.  options are
        encoder-specific, and unknown options should be ignored or
        issue warnings.
        """
        raise NotImplementedError()


def add_default_codecs():
    # Add all bundled codecs. These should be listed in order of
    # preference.  This is called automatically by pyglet.media.

    try:
        from . import wave
        registry.add_decoders(wave)
        registry.add_encoders(wave)
    except ImportError:
        pass

    if pyglet.compat_platform.startswith('linux'):
        try:
            from . import gstreamer
            registry.add_decoders(gstreamer)
        except ImportError:
            pass

    try:
        if pyglet.compat_platform in ('win32', 'cygwin'):
            from pyglet.libs.win32.constants import WINDOWS_VISTA_OR_GREATER
            if WINDOWS_VISTA_OR_GREATER:  # Supports Vista and above.
                from . import wmf
                registry.add_decoders(wmf)
    except ImportError:
        pass

    try:
        if have_ffmpeg():
            from . import ffmpeg
            registry.add_decoders(ffmpeg)
    except ImportError:
        pass

    try:
        from . import pyogg
        registry.add_decoders(pyogg)
    except ImportError:
        pass


def have_ffmpeg():
    """Check if FFmpeg library is available.

    Returns:
        bool: True if FFmpeg is found.

    .. versionadded:: 1.4
    """
    try:
        from . import ffmpeg_lib
        if _debug:
            print('FFmpeg available, using to load media files. Versions: {}'.format(ffmpeg_lib.compat.versions))
        return True

    except (ImportError, FileNotFoundError, AttributeError):
        if _debug:
            print('FFmpeg not available.')
        return False
