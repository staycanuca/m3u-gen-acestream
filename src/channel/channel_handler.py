#!/usr/bin/python3
# -*- coding: utf-8 -*-


from codecs import StreamReaderWriter, open
from contextlib import closing
from datetime import timedelta
from json import loads
from os import makedirs
from os.path import dirname
from sys import stderr
from time import sleep
from typing import List
from urllib.error import URLError
from urllib.request import urlopen

from channel.channel import Channel, ChannelsDecoder
from config.config import Config
from config.data_set import DataSet
from filter.filter_handler import FilterHandler
from utils import Utils


class ChannelHandler:

    @staticmethod
    def write_playlist(data_set: DataSet) -> None:
        out_file_name: str = data_set.out_file_name
        out_file_encoding: str = data_set.out_file_encoding
        out_file_first_line: str = data_set.out_file_first_line

        makedirs(dirname(out_file_name), exist_ok=True)

        with closing(open(out_file_name, 'w', out_file_encoding)) as out_file:
            out_file.write(out_file_first_line)

            total_channel_count: int = 0
            allowed_channel_count: int = 0

            channels: List[Channel] = ChannelHandler._fetch_channels(data_set)
            channels = FilterHandler.replace_categories(channels, data_set)
            channels.sort(key=lambda x: x.name)
            channels.sort(key=lambda x: x.category)

            if data_set.clean_filter:
                FilterHandler.clean_filter(channels, data_set)

            for channel in channels:
                total_channel_count += 1

                if FilterHandler.is_channel_allowed(channel, data_set):
                    ChannelHandler._write_entry(channel, data_set, out_file)
                    allowed_channel_count += 1

        print('Playlist', data_set.out_file_name, 'successfully generated.')
        print('Channels processed in total:', total_channel_count)
        print('Channels allowed:', allowed_channel_count)
        print('Channels denied:', total_channel_count - allowed_channel_count)

    @staticmethod
    def _fetch_channels(data_set: DataSet) -> List[Channel]:
        json_url: str = data_set.json_url
        resp_encoding: str = data_set.resp_encoding

        for attempt_number in range(1, Config.JSON_SRC_MAX_ATTEMPTS):
            print('Retrieving JSON file, attempt', attempt_number, 'of', Config.JSON_SRC_MAX_ATTEMPTS, end='\n\n')

            if attempt_number > 1:
                Utils.wait_for_internet()

            try:
                with closing(urlopen(json_url, timeout=Config.CONN_TIMEOUT)) as response_raw:
                    response: str = response_raw.read().decode(resp_encoding)

                channels: List[Channel] = loads(response, cls=ChannelsDecoder)

                return channels
            except URLError as url_error:
                print('Can not retrieve JSON file.', file=stderr)
                print('Error:', url_error, file=stderr)

                if attempt_number < Config.JSON_SRC_MAX_ATTEMPTS:
                    print('Sleeping for', timedelta(seconds=Config.JSON_SRC_REQ_DELAY), 'before trying again.',
                          end='\n\n',
                          file=stderr)
                    sleep(Config.JSON_SRC_REQ_DELAY)
                else:
                    print('Raising an exception.', end='\n\n', file=stderr)
                    raise

        return [Channel('', '', '')]

    @staticmethod
    def _write_entry(channel: Channel, data_set: DataSet, out_file: StreamReaderWriter) -> None:
        out_file_format: str = data_set.out_file_format

        entry: str = out_file_format \
            .replace('{CATEGORY}', channel.category) \
            .replace('{NAME}', channel.name) \
            .replace('{CONTENT_ID}', channel.content_id)

        out_file.write(entry)
