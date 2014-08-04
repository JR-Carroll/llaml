#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<J. R. Carroll>
  Purpose: Settings controller.
  Created: 12/09/2013

  Utility functions that could prove to be useful between
  multiple modules.
"""

def explode_dictKeys(dictionary):
    """
    Returns a list of all the keys nested in a dictionary.

    This is useful if you need to do a 'deep equality' check
    between multiple dictionaries.

    Recursively crawls through a dictionary returning its keys.

    Note:  order matters in lists -- you cannot compae two lists with the
    same contents but in a different order!

    Args:
        dictionary:  the dict you want to deep-introspect.
    Returns:
        keyList: a list of all the keys nested within the dictionary.
    """

    allKeys = dictionary.keys()

    for value in dictionary.values():
        if isinstance(value, dict):
            allKeys.extend(explode_dictKeys(value))
    return sorted(allKeys)

if __name__ == '__main__':
    # Try some of the helper functions out.
    # TODO:  Convert into doctests.
    myDict = {"test":1,
              "test2": {"testsub2": 1,
                        "testsub22": {"testsubsub2":1,
                                      "testsubsub22": {"testsub3": 2,
                                                       "testsub33": 2}
                                      }
                        }
              }

    v = explode_dictKeys(myDict)
    print v