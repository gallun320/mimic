#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import socket
import subprocess
import tempfile
import threading
import miniproduction as Face

# name of WAV to produce
__output_wav = "audio.wav"
# name of MP4 to process
__input_mp4 = "input.mp4"
# template for storing extracted frames
__frame_template = "frame_%09d.jpg"
# how many frames extract from one second of video
__fps_to_extract = 30
# size of the socket buffer to read into
__sock_buf_size = 4096

__wav_tmp = "./wav_tmp"

__mp4_tmp = "./mp4_tmp"


def generate_temporary_directory():
    """
    Create temporary directory to store JPGs.

    :return: absolute pathname of directory
    """
    #return tempfile.mkdtemp()
    return "./faces"


class WavProcessThread(threading.Thread):
    def __init__(self, tmpdir, mp4_input):
        threading.Thread.__init__(self)
        self.tmpdir = tmpdir
        self.mp4_input = mp4_input

    def run(self):
        ret = extract_wav_from_mp4(self.tmpdir, self.mp4_input)
        if ret != 0:
            print "Error WAV extracting"


class JpgsProcessThread(threading.Thread):
    def __init__(self, tmpdir, mp4_input):
        threading.Thread.__init__(self)
        self.mp4_input = mp4_input
        self.tmpdir = tmpdir

    def run(self):
        ret = extract_jpg_frames_from_mp4(self.tmpdir, self.mp4_input)
        if ret != 0:
            print "Error JPG frames extracting"


def extract_jpg_frames_from_mp4(tmpdir, mp4_input):
    """
    Extract JPG frames from MP4.

    :param tmpdir: absolute filename of temporary directory
    :param mp4_input: absolute filename of MP4 file to extract
        JPG frames from
    :return: 0 - extraction succeeded, otherwise - not succeeded
    """
    saved_umask = os.umask(0077)
    fpath = os.path.join(tmpdir, __frame_template)
    ret = None
    try:
        ret = subprocess.call(["ffmpeg", "-y", "-r", str(__fps_to_extract),
                               "-i", mp4_input, fpath])
    except IOError as e:
        print "IOError occured"
    finally:
        os.umask(saved_umask)
    if ret != 0:
        print "Error extracting frames from MP4"
    return ret


def extract_wav_from_mp4(tmpdir, mp4_input):
    """
    Extract audio from MP4 into WAV using ffmpeg utility.

    :param tmpdir: absolute filenaem of temporary directory
    :param mp4_input: absolute MP4 filename to extract WAV from
    :return: 0 - extraction succeeded, otherwise - not succeeded
    """
    saved_umask = os.umask(0077)
    opath = os.path.join(tmpdir, __output_wav)
    ret = None
    try:
        ret = subprocess.call(["ffmpeg", "-y", "-i", mp4_input, opath])
    except IOError as e:
        print "IOError occured"
    finally:
        os.umask(saved_umask)
    if ret is None:
        print "Error converting file"
    return ret


def main():
    tmp = generate_temporary_directory()
    input_mp4 = os.path.join(__mp4_tmp, __input_mp4)
    print "Filename:", input_mp4
    thr_wav = WavProcessThread(__wav_tmp, input_mp4)
    thr_jpgs = JpgsProcessThread(tmp, input_mp4)
    thr_wav.start()
    thr_jpgs.start()
    thr_wav.join()
    # TODO: perform WAV analysis
    thr_jpgs.join()
    Face.landmarksFunc()
    # os.remove(input_mp4) # Remove MP4 after extracting WAV and JPGs
    # TODO: perform` face, voice , mimics analysis
    # TODO: send results to socket
    # shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
