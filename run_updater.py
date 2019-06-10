'''
    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)

'''
import argparse
import logging
import os
import json
from lkmltools.updater.lookml_modifier import LookMlModifier

def parse_arguments():
    """Parse command line arguments

    Returns: argument objects with flags as attributes

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        help='Location of the configuration file',
                        required=True)
    parser.add_argument('--infile',
                        help='Filepath of input LookML file',
                        required=True)
    parser.add_argument('--outfile',
                        help='Filepath of output LookML file',
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

    modifier = LookMlModifier(config)
    modifier.modify(args.infile, args.outfile)

if __name__ == '__main__':
    main()
