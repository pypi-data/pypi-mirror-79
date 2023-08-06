import test_path
from pyspeedx.text import * 
from pyspeedx.helpers import *
from pyspeedx.sort import *
if __name__ == "__main__":
    import pprint
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

    # ## Test save data to csv ##
    # import pandas as pd
    
    # data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
    # # data = {'a':1,'b':2,'c':3}
    # # pd.DataFrame(d.items(), columns=['Date', 'DateValue'])
    # data_frame = pd.DataFrame(data.items(), columns=['key', 'value'])
    # print(data_frame)
    # # exit()
    
    # sound1 = Sound('drink')
    # sound2 = Sound('good')
    
    # _dict = {}
    # _dict[sound1] = 5
    # _dict[Sound('mat')] = 342
    
    # #_dict2 = {sound2:1,'b':2,'c':sound1}
    # # data_frame = pd.DataFrame(_dict2)
    # #data_frame = pd.DataFrame(_dict2.items(),columns=['word','count'])

    # data_frame = pd.DataFrame(_dict.items(),columns=['sound','count'])
    # # print("type(data_frame['word'][0]:",type(data_frame['word'][0]))
    
    # print(data_frame)
    # Helper.save_data_frame_to_csv("sound_count_data.csv",data_frame)
    # ###########################

    ## test find  subsets_ranked_by_freq  ##
    data = {'word':['mate','rate','hate','hat','ate','p'],
    'count':[100,100,100,100,100,100]}
    words = data['word']
    counts = data['count']

    sounds = list(map(Sound,words))

    pprint.pprint(sounds)
    subsets_scored = {}
    # Helper.score_permutation_by_word(subsets_scored,sounds[0],counts[0])
    Helper.score_permutations_by_words(subsets_scored,sounds,counts)
    subsets_ranked_by_freq = Sort.sort_dict_by_value(subsets_scored)
    print("subsets_ranked_by_freq:\n",subsets_ranked_by_freq)
    
    ## similarity weight for one to one word
    _similarity_weight = similarity_weight(sounds[0],sounds[5])
    similarity_wlp =  weight_len_product(_similarity_weight)
    ranked_simi_wlp = Sort.sort_dict_by_value(similarity_wlp)
    
    # two_words_simi_score =  
    print("_similarity_weight: ",_similarity_weight)
    print("similarity_wlp: ",similarity_wlp)
    print("ranked_simi_wlp: ",ranked_simi_wlp)

    # score = similarity_score_helper(similarity_wlp,subsets_ranked_by_freq)
    # print("score:",score)
    
    score = 0
    for s in sounds:
        score = similarity_score(sounds[0],s,subsets_ranked_by_freq)
        print("similarity score between: {} & {} = {}".format(sounds[0]._sound,s._sound,score))
    ## similarity weight for one to many words
    

    # exit()
    #sound1 = Sound('fear')
    
    #print("sound1:",sound1)
    # for i in :
    #     print("{}: {}".format(i,sound1[i]))

    # _subsets = Helper.permutations(sound1)
    # print(_subsets)
