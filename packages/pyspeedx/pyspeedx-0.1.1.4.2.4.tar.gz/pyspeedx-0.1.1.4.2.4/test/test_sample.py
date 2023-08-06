# content of test_sample.py
# from pyspeedx import pyspeedx
import test_path
import os 

import pyspeedx.helpers
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)



def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4