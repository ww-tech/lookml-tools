import pytest
from lkmltools.grapher.graph_animator import GraphAnimator
import git

def test_get_commits():
    config = {
                "infile_globs": [
                    "test/grapher/*.lkml"
                ],

                "options": {
                    "node_size": 400,
                    "label_font_size": 10,
                    "text_angle": 30,
                    "image_width": 12,
                    "image_height" : 8
                }
            }
    animator = GraphAnimator(config)
    repo, commits = animator.get_commits("./", branch='master')
    assert isinstance(repo, git.Repo)
    assert len(commits) > 1
    assert isinstance(commits[0], git.Commit)