import test_path
import pyspeedx.helpers

def test_subsets(_list:list=['a','b','c']):
	 assert pyspeedx.helpers.Helper.permutations(_list) == [['a'],['a','b'],['a','b','c'],['b'],['b','c'],['c']]

	