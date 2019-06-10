'''git clone a repo, or hub clone a repo (if "use_hub": true is set in config),
    using remote repo URL defined in config and local folder to check out to
    (also defined in config)

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)

'''
import argparse
import logging
import os
import json
import subprocess

def parse_arguments():
    """Parse command line arguments

    Returns: 
        argument objects with flags as attributes

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        help='Location of the configuration file',
                        required=True)
    known_args, pipeline_args = parser.parse_known_args()
    return known_args, pipeline_args

def main():
    """
        do a git clone based on the url and folder in the config
    """
    logging.basicConfig(format='%(asctime)s %(levelname)s %(filename)s %(funcName)s: %(message)s', level=logging.INFO)

    args, _ = parse_arguments()

    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        raise Exception('config file at: {} not found'.format(args.config))

    url = config['git']['url']
    folder = config['git']['folder']

    cmd = ["git", "clone", url, folder]

    if 'use_hub' in config and config['use_hub']:
        logging.info("Using hub instead of git")
        cmd = ["hub", "clone", url, folder]

    logging.info("About to run %s", " ".join(cmd))

    try:
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, shell=False, timeout=3,
            universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        logging.error("%s %s" % (exc.returncode, exc.output))
    else:
        logging.info("Output: %s", output)

if __name__ == '__main__':
    main()
