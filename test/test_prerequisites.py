import pytest
import json
import subprocess
from lkmltools.updater.lookml_modifier import LookMlModifier

'''
    this code intimately relies on a node utility lookml-parser to parse LookML files to JSON

    if that is not installed, the rest of the code cannot work correctly

'''

def test():
    with open("test/config.json", 'r') as f:
        config = json.load(f)
    
    filename = "doesnotexist.lkml"
    cmd = [config['parser'], "--input=%s" % filename]
    process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    assert output == b'{"files":[],"file":{"model":{},"view":{},"explore":{}},"models":[],"model":{}}\n'
    assert error == b'Warning: No input files were matched. (Use argument --input=... )\n'
