import pytest
import sys
import os
from lkmltools.updater.file_modifier import FileModifier

def test_init():
    modifier = FileModifier("test/minimal.lkml")
    assert len(modifier.lines) == 13

def test_init2():
    with pytest.raises(Exception) as e:
        modifier = FileModifier("test/doesnotexist")
    assert 'Filename does not exist: test/doesnotexist' in str(e.value)

def test_is_header():
    modifier = FileModifier("test/minimal.lkml")
    assert modifier.is_header("dimension: myname {", "dimension", "myname")

def test_is_header2():
    modifier = FileModifier("test/minimal.lkml")
    assert not modifier.is_header("dimension: somethingelse {", "dimension", "myname")

def test_handle_addition():
    modifier = FileModifier("test/minimal.lkml")
    assert len(modifier.lines) == 13

    # add a description to city_code
    modifier.handle_description_addition("dimension", "city_code", "a description")
    assert len(modifier.lines) == 14
    assert modifier.lines[4] == "    description: \"a description\"	# programmatically added by LookML modifier\n"

def test_handle_subscription_substitution():
    modifier = FileModifier("test/minimal_multiline.view.lkml")
    assert len(modifier.lines) == 19
    modifier.handle_desription_substitution(6, "dimension", "city_code", "a description")
    assert len(modifier.lines) == 14
    assert modifier.lines[5] == "    description: \"a description\"	# programmatically added by LookML modifier\n"

def test_write():
    modifier = FileModifier("test/minimal.lkml")
    filename = "test/test_write.lkml"
    if os.path.exists(filename):
        os.remove(filename)
    
    modifier.write(filename)
    assert os.path.exists(filename)

    original =  open("test/minimal.lkml", 'r').readlines()
    written =  open(filename, 'r').readlines()

    assert original == written

    if os.path.exists(filename):
        os.remove(filename)

def test_modify1():
    modifier = FileModifier("test/minimal.lkml")
    assert len(modifier.lines) == 13

    # add a description to city_code
    modifier.modify(1, "dimension", "city_code", "a description", False)
    assert len(modifier.lines) == 14
    assert modifier.lines[4] == "    description: \"a description\"	# programmatically added by LookML modifier\n"

def test_modify2():
    modifier = FileModifier("test/minimal_multiline.view.lkml")
    assert len(modifier.lines) == 19
    modifier.modify(6, "dimension", "city_code", "a description", True)
    assert len(modifier.lines) == 14
    assert modifier.lines[5] == "    description: \"a description\"	# programmatically added by LookML modifier\n"
