# -*- coding: utf-8 -*-

from iktomi.cms.stream_app import Streams

streams_tree = [
    'admins',
]

streams = Streams.from_tree(streams_tree, __package__)
