from test import Test
from helpers import Helper

if __name__ == "__main__":


    Test.print_hello()
    l_str  = "abcd"
    _str = "qwert asdf zxcb"
    _str_list = _str.split(" ")
    print("_str_list: ",_str_list)
    print("_str_list type: ",type(_str_list))
    list2d = list(map(list,_str_list))

    print("type of list2d: ",type(list2d))
    print("list2d: ",list2d)
    
    #l = list(l_str)
    #perms = Helper.permutations(l_str)
    #print("permutation of %s: " % l_str)
    #print(perms)
    
    flat_perms = Helper.permutations_on_2dlist(list2d)
    print("flat_perms: ",flat_perms)

    list_str = list(map("".join,flat_perms))
    print("list_str: ",list_str)
