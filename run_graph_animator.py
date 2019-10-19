'''generate an animated GIF of the state of a LookML repo over time
It uses the Grapher tool to ceate one image per commit

Authors:
    Carl Anderson (carl.anderson@weightwatchers.com)

'''
import os
import json
import argparse
import logging
from lkmltools.grapher.graph_animator import GraphAnimator

def parse_arguments():
    """Parse command line arguments

    Returns: 
        argument objects with flags as attributes

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        help='Location of the configuration file',
                        required=True)
    parser.add_argument('--path_to_repo',
                        help='Path to repo',
                        required=True)
    parser.add_argument('--branch',
                        help='Git repo branch',
                        required=False)
    parser.add_argument('--image_directory',
                        help='Directory to save images to. Will be created if does not exist',
                        required=True)
    parser.add_argument('--gif_filename',
                        help='filepath of output GIF',
                        required=True)
    known_args, pipeline_args = parser.parse_known_args()
    return known_args, pipeline_args

def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(filename)s %(funcName)s: %(message)s', level=logging.INFO)

    args, _ = parse_arguments()

    # Example input config file
    # {
    #     "infile_globs": [
    #         "../somerepo/*.lkml"
    #     ],
    #
    #     "options": {
    #         "node_size": 400,
    #         "label_font_size": 10,
    #         "text_angle": 30,
    #         "image_width": 12,
    #         "image_height" : 8
    #     }
    # }
    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        raise Exception('config file at: {} not found'.format(args.config))

    branch = args.branch if args.branch else 'master'

    if not os.path.exists(args.image_directory):
        os.makedirs(args.image_directory)

    animator = GraphAnimator(config)
    animator.create_gif(args.path_to_repo, branch, args.image_directory, args.gif_filename)

if __name__ == '__main__':
    main()