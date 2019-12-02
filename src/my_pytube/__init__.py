# -*- coding: utf-8 -*-
# flake8: noqa
# noreorder
"""
Pytube: a very serious Python library for downloading YouTube Videos.
"""
__title__ = 'my_pytube'
__version__ = '9.5.2'
__author__ = 'Nick Ficano'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2019 Nick Ficano'

#import logging
#import query
#import streams
#import captions
#import contrib
#import __main__


from my_pytube.logging import create_logger
from my_pytube.query import CaptionQuery
from my_pytube.query import StreamQuery
from my_pytube.streams import Stream
from my_pytube.captions import Caption
from my_pytube.contrib.playlist import Playlist
from my_pytube.__main__ import YouTube


logger = create_logger()
logger.info('%s v%s', __title__, __version__)
