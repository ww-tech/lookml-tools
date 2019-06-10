'''
    utility methods

    Authors:
            Carl Anderson (carl.anderson@weightwatchers.com)
'''
from enum import Enum

class FieldCategory(Enum):
    """type of LookML field"""
    DIMENSION = "dimension"
    DIMENSION_GROUP = "dimension_group"
    MEASURE = "measure"
    DESCRIPTION = "description"
