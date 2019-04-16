#!/usr/bin/python3
# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from os import chdir
from socket import gethostname, gethostbyname
from sys import stderr, path
from time import sleep
from traceback import print_exc, format_exc

from channel.channel_handler import ChannelHandler
from config.config import Config
from utils import Utils


class M3UGenAceStream:

    @staticmethod
    def main() -> None:
        channel_handler: ChannelHandler = ChannelHandler()

        while True:
            print('Started at', datetime.now().strftime('%b %d %H:%M:%S'), end='\n\n')

            Utils.wait_for_internet()

            data_set_number: int = 0

            for data_set in Config.DATA_SETS:
                data_set_number += 1
                print('Processing data set', data_set_number, 'of', len(Config.DATA_SETS))

                channel_handler.data_set = data_set
                channel_handler.write_playlist()

                if data_set_number < len(Config.DATA_SETS):  # TODO: Do not wait if using cached response.
                    print('Sleeping for', timedelta(seconds=Config.DATA_SET_DELAY),
                          'before processing next data set...')
                    sleep(Config.DATA_SET_DELAY)

                print('')

            print('Finished at', datetime.now().strftime('%b %d %H:%M:%S'))
            print('Sleeping for', timedelta(seconds=Config.UPDATE_DELAY), 'before the new update...')
            print('-' * 45, end='\n\n\n')
            sleep(Config.UPDATE_DELAY)


# Main start point.
if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        chdir(path[0])

        M3UGenAceStream.main()
    except Exception:
        print_exc()

        if Config.MAIL_ON_CRASH:
            print('Sending notification.', file=stderr)

            subject: str = 'm3u-gen-acestream has crashed on ' + gethostname() + '@' + gethostbyname(gethostname())
            Utils.send_email(subject, format_exc())

        if Config.PAUSE_ON_CRASH:
            input('Press <Enter> to exit...\n')

        exit(1)
