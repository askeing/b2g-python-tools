#!/usr/bin/env python

import sys
import csv
import json
import logging
import argparse


logger = logging.getLogger(__name__)


class BugSubimtter(object):

    def __init__(self, connection_options=None):
        self.input_json = None

    def cli(self):
        """
        This method will parse the argument for CLI.
        """
        # argument parser
        parser = argparse.ArgumentParser(prog='CSV to JSON Parser',
                                         description='The simple parser for gip to gij csv file.')
        parser.add_argument('--input', action='store', dest='input', required=True,
                            help='The input JSON file.')
        parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False,
                            help='Turn on verbose output, with all the debug logger.')

        # parser the argv
        options = parser.parse_args(sys.argv[1:])
        # setup the logging config
        if options.verbose is True:
            verbose_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            logging.basicConfig(level=logging.DEBUG, format=verbose_formatter)
        else:
            formatter = '%(levelname)s: %(message)s'
            logging.basicConfig(level=logging.INFO, format=formatter)
        # assign the variable
        self.input_json = options.input
        return self

    def run(self):
        """
        Run.
        """
        # TODO
        print('Not Implemented.')
        pass

def main():
    try:
        BugSubimtter().cli().run()
    except Exception as e:
        logger.error(e)
        if e.__dict__:
            logger.error(e.__dict__)
        exit(1)


if __name__ == '__main__':
    main()
