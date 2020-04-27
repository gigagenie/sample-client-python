# Copyright 2020 KT AI Lab.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import subprocess
import wave
import platform
import time

#logger = logging.getLogger('player')

def sample_width_to_string(sample_width):
    """Convert sample width (bytes) to ALSA format string."""
    return {1: 's8', 2: 's16', 4: 's32'}.get(sample_width, None)

class WavePlayer(object):
    """Plays short audio clips from a buffer or file."""

    def __init__(self, output_device='default'):
        self._output_device = output_device
        
        self._loaded_bytes = None
        self._loaded_samplerate = None
        self._loaded_samplewidth = None

    def play_bytes(self, audio_bytes, sample_rate=16000, sample_width=2):
        """Play audio from the given bytes-like object.

        Args:
          audio_bytes: audio data (mono)
          sample_rate: sample rate in Hertz (16 kHz by default)
          sample_width: sample width in bytes (eg 2 for 16-bit audio)
        """
        cmd = [
            'aplay',
            '-q',
            '-t', 'raw',
            '-D', self._output_device,
            '-c', '1',
            '-f', sample_width_to_string(sample_width),
            '-r', str(sample_rate),
        ]

        aplay = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        aplay.stdin.write(audio_bytes)
        aplay.stdin.close()
        retcode = aplay.wait()

        if retcode:
            logging.error('aplay failed with %d', retcode)

    def play_file(self, fname):
        if platform.system() == 'Darwin':
            cmd_play = 'afplay'
        else:
            cmd_play = 'aplay'
        retcode = subprocess.call([cmd_play, fname])

        if retcode:
            logging.error('%s failed with %d', cmd_play, retcode)
        wav = wave.open(fname, 'r')
        duration = wav.getnframes() / float(wav.getframerate())
        duration = int(round(duration,3)*1000)
        wav.close()
        
        return duration
    
    def play_wav(self, wav_path):
        """Play audio from the given WAV file.

        The file should be mono and small enough to load into memory.
        Args:
          wav_path: path to the wav file
        """
        wav = wave.open(wav_path, 'r')
        if wav.getnchannels() != 1:
            raise ValueError(wav_path + ' is not a mono file')

        frames = wav.readframes(wav.getnframes())
        self.play_bytes(frames, wav.getframerate(), wav.getsampwidth())
        duration = wav.getnframes() / float(wav.getframerate())
        duration = int(round(duration,3)*1000)
        wav.close()
        
        return duration

    def play(self, wav_path):
        if platform.system() == 'Darwin':
            duration = self.play_file(wav_path)
        else:
            duration = self.play_wav(wav_path)
        return duration
    
    def load_audio(self, wav_path):
        wav = wave.open(wav_path, 'r')
        if wav.getnchannels() != 1:
            raise ValueError(wav_path + ' is not a mono file')

        self._loaded_bytes = wav.readframes(wav.getnframes())
        self._loaded_samplerate = wav.getframerate()
        self._loaded_samplewidth = wav.getsampwidth()
        wav.close()

    def play_audio(self):
        if self._loaded_bytes is None:
            raise ValueError('No loaded audio file. load_audio() first.')
        self.play_bytes(self._loaded_bytes,
                        self._loaded_samplerate, self._loaded_samplewidth)

import threading
import vlc

class VlcMediaPlayer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.player = None
        self.is_player_active = False
        self.state = None
        self.channel = 1
        self.metajson = None
        """
            0: State.NothingSpecial
            1: State.Opening
            2: State.Buffering
            3: State.Playing
            4: State.Paused
            5: State.Stopped
            6: State.Ended
            7: State.Error
        """
        self.currentmedia = None
        self.media = None
        self.event_manager = None

    def run(self):
        self.vlcInstance = vlc.Instance('--no-xlib')
        self.player = self.vlcInstance.media_player_new()
        self.is_player_active = True
        self.state = self.player.get_state()
        
        #self.event_manager = self.player.event_manager()

    def set_end_callback(self, callback):
        if self.event_manager != None:
            self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, callback)

    def set_parsed_callback(self, callback):
        if self.event_manager != None:
            self.event_manager.event_attach(vlc.EventType.MediaParsedChanged, callback)

    def get_channel(self):
        return self.channel

    def play(self, media_url = None, channel = None, metajson = None):
        if media_url is not None:
            #self.player.set_mrl(media_url)
            self.media = self.vlcInstance.media_new(media_url)
            self.player.set_media(self.media)
            self.media.parse_with_options(1,0)
            self.currentmedia = media_url
            self.event_manager = self.player.event_manager()
        if self.currentmedia is not None:
            self.player.play()
        self.state = self.player.get_state()
        if channel is not None:
            self.channel = channel
        if metajson is not None:
            self.metajson = metajson
    
    def pause(self):
        s1 = self.player.is_playing()
        self.player.pause()
        self.state = self.player.get_state()
        time.sleep(0.5)
        s2 = self.player.is_playing()
        if s1 == s2 and s2 == 1:
            self.player.stop()
        elif s1 == s2 and s2 == 0:
            self.player.play()

    def stop(self):
        self.player.stop()
        self.currentmedia = None
        self.metajson = None
        self.state = self.player.get_state()

    def get_state(self):
        self.state = self.player.get_state()
        return self.state

    def get_time(self):
        t = self.player.get_time()
        return t

    def get_duration(self):
        while True:
            if str(self.media.get_parsed_status()) == 'MediaParsedStatus.done':
                break
        return self.media.get_duration()

    def terminate(self):
        self.player = None
        self.is_player_active = False

    def get_mediaurl(self):
        return self.currentmedia

    def is_playing(self):
        return self.player.is_playing()

    def set_user_agent(self, name, http):
        self.vlcInstance.set_user_agent(name, http)

    def get_metainfo(self):
        """
            media_type:     mandatory, music/radio/podcast
            title:          mandatory
            description:    optional
            artist:         optional
            imageurl:       optional
            media_name:     optional
            media_playtime: optional
            media_size:     optional
            category:       optional
            album_name:     optional
        """
        return self.metajson
# end of VlcMediaPlayer

