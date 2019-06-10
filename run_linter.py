'''
    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)

'''
import argparse
import logging
import os
import json
from lkmltools.linter.lookml_linter import LookMlLinter

def parse_arguments():
    """Parse command line arguments

    Returns: argument objects with flags as attributes

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        help='Location of the configuration file',
                        required=True)
    known_args, pipeline_args = parser.parse_known_args()
    return known_args, pipeline_args

def main():
    """

    """
    logging.basicConfig(format='%(asctime)s %(levelname)s %(filename)s %(funcName)s: %(message)s', level=logging.INFO)

    args, _ = parse_arguments()

    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        raise Exception('config file at: {} not found'.format(args.config))

    LookMlLinter(config).run()

if __name__ == '__main__':
    main()
