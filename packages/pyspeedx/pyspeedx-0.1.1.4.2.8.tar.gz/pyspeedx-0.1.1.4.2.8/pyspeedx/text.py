#from . helpers import Helper
#from . import helpers
#from helpers import *
#import helpers

# import os
# working_dir = os.getcwd()
# print("working dir from text.py:\n" ,working_dir)

# import sys
# sys.path.append('E:\\tools\\python\\pyspeedx')
# print("sys.path from text.py:\n\n:",sys.path)


from pyspeedx.helpers import Helper
# import helpers
from pyspeedx.logger import Logger
logger = Logger.getInstance()

class Text:
    
    def palindromic_partitions(_str:str):
        pass
    def text_to_str_list(_text: str,):
        # convert a text of words into a list of words
        return _text.split(" ")    


class Word:
    # a word is generic container for text  type that has multiple usefull representations 
    # for example  text_rep = "word", list_rep = ['w',o','r','d']
    # so word object will containe all needed representation of a string for specific task 
    ##### Implementation: 
    # take a string "cat" --------store/convert it-------> ['c','a','t']
    def __init__(self,_str:str):
        self._str = _str
        self._list = list(_str)
    def __str__(self):
        return str((self._str,self._list))
from g2p_en import G2p
g2p = G2p()
class Sound(Word):
    def __init__(self,_str):
        # find g2p sound represintation
        # 
        #
        # 
        #  
        #g2p = G2p()
        #super().__init__(_str)
        
        self._str = _str
        self._list = list(_str) 
        self._sound = g2p(_str)
        self._sound_str = "_".join(self._sound)
    def __str__(self):
        # return str((self._str,self._list,self._sound,self._sound_str))
        return str((self._str,self._sound_str))

    def __repr__(self):
        return str((self._str,self._list,self._sound,self._sound_str))

    def __len__(self):
        return len(self._sound)
    def __eq__(self,other):
        return self._sound == other._sound
    def __hash__(self):
        #return self._sound_str
        return hash(self._sound_str)
    def __getitem__(self,items):
        return tuple(self._sound[items])
    
    
def list_to_counted_dict(_list:list):
  _dict ={}
  for k in _list:
    _dict[k] = _dict.get(k,0)  + 1
  return _dict


def similarity_weight(word1,word2):
    # find every subsets of the first word 
    # find every subsets of the second word
    # store all subsets that are in both word1_subsets and word2_subsets with their count .
    ### calculate the count => count = count_in_word1_subsets * count_in_word2_subsets.   
    # return similarity_weight  = the intersected_subsets with their count
    #  
    word1_subsets = Helper.permutations(tuple(word1._sound))
    word2_subsets = Helper.permutations(tuple(word2._sound))
    subsets1_count = list_to_counted_dict(word1_subsets)
    subsets2_count = list_to_counted_dict(word2_subsets)
    
    
    _similarity_weight = {}

    for subset_key in subsets1_count:
        
        _similarity_weight[subset_key] = subsets1_count[subset_key] * subsets2_count.get(subset_key,0)

    is_zero = lambda x : x[1] > 0
    _similarity_weight = dict(filter(is_zero,_similarity_weight.items()))

    return _similarity_weight

def weight_len_product (weight):
    _weight_len_product = {}
    for k,v in weight.items():
        l = len(k) 
        _weight_len_product[k] = (l*l) * v
    return _weight_len_product


def similarity_score_helper(_weight_len_product,subsets_freq):
    score = 0
    for k,v in _weight_len_product.items():
        # print("socre,value,subsets_freq:",score,v,subsets_freq.get(k,0))

        # the weight * freq of subsets added to score
        score = score + v * subsets_freq.get(k,0)

    return score  

def similarity_score(word1,word2,subsets_freq):
    ## the similarity score between two words ##
    # pass
    _similarity_weight = similarity_weight(word1,word2)
    similarity_wlp =  weight_len_product(_similarity_weight)
    # ranked_simi_wlp = Sort.sort_dict_by_value(similarity_wlp)
    score = similarity_score_helper(similarity_wlp,subsets_freq)
    return  score


if __name__ == "__main__":
    # ## test Word class ##
    # _str = "hello"
    # word = Word(_str)
    # print("word: \n", word)
    # #####################


    # ## test Text class ##
    # _str = "hello Text this is a long text"
    # print("text to words: \n",Text.text_to_str_list(_str))
    # Text.palindromic_partitions(_str)
    # #####################

    # ## test Sound class ##
    
    # # make a long text made of words
    # # convert text to list of strings 
    # # from the list of strings create a list of sounds
    # #   
    # sound = Sound("sound")
    # print("sound:\n", sound)

    # str_list = Text.text_to_str_list("time to hear the sounds of these words")
    # sounds_list = list(map(Sound,str_list)) 
    
    # print(*sounds_list,sep='\n')
    
    # ######################

    # ## test similarity_weight() ##
    # from sort import Sort

    # sound1 = Sound('cat hat')
    # sound2 = Sound('fat rat')
    # print("sound1:\n",sound1)
    # print("sound2:\n",sound2)

    # weight = similarity_weight(sound1,sound2)
    # _weight_len_product = weight_len_product(weight)
    # sort_weight_len_product = Sort.sort_dict_by_value(_weight_len_product)

    # print("weight:\n",weight)
    # print("sorted weight:\n",Sort.sort_dict_by_value(weight))
    # print("sorted weight_len_product:\n",sort_weight_len_product)

    # ######################

    # ## Test hashable sound ##
    # import pprint
    # sound1 = Sound('drink')
    # _dict = {}
    # _dict[sound1] = 5
    # _dict[Sound('mat')] = 3
    
    # #print("_dict:\n",_dict)
    # pprint.pprint(_dict)
    
    # ##########################

    ## Test save data to csv ##
    import pandas as pd
    
    data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    # data = {'a':1,'b':2,'c':3}
    # pd.DataFrame(d.items(), columns=['Date', 'DateValue'])
    data_frame = pd.DataFrame(data.items(), columns=['key', 'value'])
    print(data_frame)
    # exit()
    
    sound1 = Sound('drink')
    sound2 = Sound('good')
    
    _dict = {}
    _dict[sound1] = 5
    _dict[Sound('mat')] = 342
    
    #_dict2 = {sound2:1,'b':2,'c':sound1}
    # data_frame = pd.DataFrame(_dict2)
    #data_frame = pd.DataFrame(_dict2.items(),columns=['word','count'])

    data_frame = pd.DataFrame(_dict.items(),columns=['sound','count'])
    # print("type(data_frame['word'][0]:",type(data_frame['word'][0]))
    
    print(data_frame)
    Helper.save_data_frame_to_csv("sound_count_data.csv",data_frame)

    ###########################

    
    
 
