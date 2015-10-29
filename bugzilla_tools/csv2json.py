#!/usr/bin/env python

import sys
import csv
import json
import logging
import argparse


logger = logging.getLogger(__name__)


class CSV2JSONParser(object):

    def __init__(self, connection_options=None):
        self.input_csv = None
        self.output_json = None

    def cli(self):
        """
        This method will parse the argument for CLI.
        """
        # argument parser
        parser = argparse.ArgumentParser(prog='CSV to JSON Parser',
                                         description='The simple parser for gip to gij csv file.')
        parser.add_argument('--input', action='store', dest='input', required=True,
                            help='The input CSV file.')
        parser.add_argument('--output', action='store', dest='output', required=True,
                            help='The output JSON file.')
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
        self.input_csv = options.input
        self.output_json = options.output
        return self

    def run(self):
        """
        Run.
        """
        result_dict = {}
        issue_list = []
        with open(self.input_csv, 'rb') as csvfile:
            # parse CSV
            logger.info('Start parsing {} ...'.format(self.input_csv))
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                logger.info('processing: {} {}'.format(row['App'], row['Test']))
                obj = {}
                obj['summary'] = 'Implement {} as an integration test in JavaScript'.format(row['Test'])
                obj['product'] = row['Product']
                obj['component'] = row['Component']
                obj['version'] = 'unspecified'
                obj['whiteboard'] = '[gip-to-gij]'
                obj['description'] = '{}.\n{}'.format(obj['summary'], row['Link'])
                issue_list.append(obj)
            result_dict['issues'] = issue_list
            logger.info('Done.')

        with open(self.output_json, 'w') as jsonfile:
            # write to json
            logger.info('Strat writing {} ...'.format(self.output_json))
            json.dump(result_dict, jsonfile, indent=4)
            logger.info('Done.')


def main():
    try:
        CSV2JSONParser().cli().run()
    except Exception as e:
        logger.error(e)
        if e.__dict__:
            logger.error(e.__dict__)
        exit(1)


if __name__ == '__main__':
    main()
