
import pytest
import os
from lkmltools.lookml import LookML
from conftest import get_lookml_from_raw_lookml


def test_init():
    with pytest.raises(Exception) as e:
        LookML("doesnotexist")
    assert 'Filename does not exist: doesnotexist' in str(e.value)

def test_init2():
    filename = "somefile.xxx"
    if not os.path.exists(filename):
        with open(filename, 'w'): pass

    with pytest.raises(Exception) as e:
        LookML(filename)
    assert 'Unsupported filename somefile.xxx' in str(e.value)

    os.remove(filename)

def test_explores():
    #this will test duplicate model keys
    raw_lookml="""
        connection: "datawarehouse"
        
    include: "*.view.lkml"

    week_start_day: sunday
    week_start_day: monday

    explore: explore1 {
        from: view1
        join: view2 {
            from: view2
        }
    }
    """
    lookml = get_lookml_from_raw_lookml(raw_lookml, "amodel.model")
    explores = lookml.explores()
    assert explores is not None
    assert lookml.has_explores()
    assert lookml.json_data['week_start_day'] == 'monday'

def test_explores2():
    raw_lookml = """
      view: aview {
        dimension: SHOUTYNAME {
          type: string
        }
      }
    """
    lookml = get_lookml_from_raw_lookml(raw_lookml, "aview.view")
    explores = lookml.explores()
    assert explores is None
    assert not lookml.has_explores()
