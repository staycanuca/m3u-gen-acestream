#!/usr/bin/python3
# -*- coding: utf-8 -*-


from codecs import StreamReaderWriter, open
from contextlib import closing
from datetime import timedelta
from json import loads, load
from os import makedirs
from os.path import dirname
from sys import stderr
from time import sleep
from typing import List
from urllib.error import URLError
from urllib.request import urlopen

from channel.channel import Channel, ChannelsDecoder, InjectionDecoder
from config.config import Config
from config.data_set import DataSet
from filter.filter_handler import FilterHandler
from utils import Utils


class ChannelHandler:

    def __init__(self) -> None:
        self._data_set: DataSet = None
        self._filter_handler: FilterHandler = FilterHandler()

    @property
    def data_set(self) -> DataSet:
        return self._data_set

    @data_set.setter
    def data_set(self, data_set: DataSet) -> None:
        self._data_set = data_set
        self._filter_handler.data_set = data_set

    def write_playlist(self) -> None:
        channels: List[Channel] = self._fetch_channels()

        self._inject_channels(channels)

        self._filter_handler.replace_categories(channels)

        channels.sort(key=lambda x: x.name)
        channels.sort(key=lambda x: x.category)

        if self.data_set.clean_filter:
            self._filter_handler.clean_filter(channels)

        out_file_name: str = self.data_set.out_file_name
        out_file_encoding: str = self.data_set.out_file_encoding
        out_file_first_line: str = self.data_set.out_file_first_line

        makedirs(dirname(out_file_name), exist_ok=True)

        with closing(open(out_file_name, 'w', out_file_encoding)) as out_file:
            out_file.write(out_file_first_line)

            total_channel_count: int = 0
            allowed_channel_count: int = 0

            for channel in channels:
                total_channel_count += 1

                if self._filter_handler.is_channel_allowed(channel):
                    self._write_entry(channel, out_file)
                    allowed_channel_count += 1

        print('Playlist', self.data_set.out_file_name, 'successfully generated.')
        print('Channels processed in total:', total_channel_count)
        print('Channels allowed:', allowed_channel_count)
        print('Channels denied:', total_channel_count - allowed_channel_count)

    def _fetch_channels(self) -> List[Channel]:
        src_channels_url: str = self.data_set.src_channels_url
        src_channels_resp_encoding: str = self.data_set.src_channels_resp_encoding

        for attempt_number in range(1, Config.JSON_SRC_MAX_ATTEMPTS):
            print('Retrieving JSON file, attempt', attempt_number, 'of', Config.JSON_SRC_MAX_ATTEMPTS, end='\n\n')

            if attempt_number > 1:
                Utils.wait_for_internet()

            try:
                with closing(urlopen(src_channels_url, timeout=Config.CONN_TIMEOUT)) as response_raw:
                    response: str = response_raw.read().decode(src_channels_resp_encoding)

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

    def _inject_channels(self, channels: List[Channel]) -> None:
        injection_file_name: str = self.data_set.injection_file_name
        injection_file_encoding: str = self.data_set.injection_file_encoding

        with closing(open(injection_file_name, 'r', injection_file_encoding)) as injection_file:
            injection: List[Channel] = load(injection_file, cls=InjectionDecoder)

        channels.extend(injection)

    def _write_entry(self, channel: Channel, out_file: StreamReaderWriter) -> None:
        out_file_format: str = self.data_set.out_file_format

        entry: str = out_file_format \
            .replace('{CATEGORY}', channel.category) \
            .replace('{NAME}', channel.name) \
            .replace('{CONTENT_ID}', channel.content_id)

        out_file.write(entry)
