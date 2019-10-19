import os
import git
import logging
import imageio
from datetime import datetime
from lkmltools.grapher.lookml_grapher import LookMlGrapher

class GraphAnimator():

    def __init__(self, config):
        '''
            {
                "infile_globs": [
                    "../somerepo/*.lkml"
                ],

                "options": {
                    "node_size": 400,
                    "label_font_size": 10,
                    "text_angle": 30,
                    "image_width": 12,
                    "image_height" : 8
                }
            }
        '''
        self.config = config

    def create_gif(self, path_to_repo, branch, directory, gif_filename):
        '''create an animated GIF given path to a repo

        Args:
            path_to_repo (str): path to the git repo
            branch (str): the brnch name, e.g. 'master'
            directory (str): directory to save the image files to
            gif_filename (str): filepath of final GIF file

        Returns:
            nothing. Side effect is to save a GIF file at gif_filename

        '''
        repo, commits = self.get_commits(path_to_repo, branch)
        image_filenames = self.generate_images(repo, commits, directory)
        self.generate_gif(image_filenames, gif_filename)

    def get_commits(self, path_to_repo, branch='master'):
        '''get the list of commits from a repo

        Args:
            path_to_repo (str): path to the git repo
            branch (str): the brnch name, e.g. 'master'

        Returns:
            repo (Repo): git Repo
            commits (list): list of commits in going forward in time (oldest -> newest)

        '''
        repo = git.Repo(path_to_repo)
        commits = list(repo.iter_commits(branch))
        #reverse as we want oldest first so that gif goes forward in time
        commits.reverse()
        return repo, commits

    def generate_images(self, repo, commits, directory):
        '''given a set of commits, run the LookML grapher to produce one image per commit

        Args:
            commits (list): list of commits in going forward in time (oldest -> newest)
            directory (str): directory to save the image files to

        Returns:
            nothing. Side effect is to create a set of images in a directory

        '''
        filenames = []
        for i, commit in enumerate(commits):

            commit_id = str(commit)

            ts = int(commit.committed_date)

            dt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            logging.info("Processing %d %s %s" % (i, commit.message, dt))

            repo.git.checkout(commit_id)

            # add some metadata to the config...
            config = self.config
            filename = directory + os.path.sep + "img" + str(i) + ".png"
            config['output'] = filename
            config['options']['title'] = dt

            filenames.append(filename)

            try:
                grapher = LookMlGrapher(config).run()
            except Exception as e:
                print("issue with " + str(i) + "," + commit_id)
                #raise e
            
        return filenames

    def generate_gif(self, filenames, gif_filename):
        '''create an animated GIF given a list of images

        Args:
            filenames (list): list of image filenames, ordered in required sequence
            gif_filename (str): filepath of final GIF file

        Returns:
            nothing. Side effect is to save a GIF file at gif_filename

        '''
        images = []
        for filename in filenames:
            if os.path.exists(filename):
                logging.info("Adding to gif: image " + filename)
                images.append(imageio.imread(filename))

        logging.info("Creating GIF. This can take some time...")

        imageio.mimsave(gif_filename, images)

        logging.info("Gif generated at " + gif_filename)
