import pandas as pd

class Helper:
    def permutations(alphabets):
        perms : list = [] #  list of all permutations

        n = len(alphabets)# number of elements 
        #arr = []
        for i in range(0,n):# i is save point 

            for j in range(i,n):# j is the steps away from the save point 
                perms.append(alphabets[i:j+1])

        return perms
#the name dictionary does refer to a language dictionary as an analogy,
#and not to python's dict data type 
#dictionary is list of words
#word is list of alphabets/characters
    def permutations_on_2dlist(dictionary):
        flat_perms: list = [] # flat means all elements have been appended to one 1D list
        
        for word in dictionary:#
            flat_perms.extend(Helper.permutations(word))
        return flat_perms

#get the input to DataFrame
    # import itertools
    # def data_frame_input(keys: tuple,values: tuple):
    #     for k,v in zip((keys,values)):
    #         print("k: %s,v: %s" % (k,v))


    def data_frame_input(keys: list,values: list):
    #def data_frame_input(keys_values: tuple):
    
        _dict = {}
        #keys = keys_values[0]
        #values = keys_values[1]
        for k,v in zip(keys,values):
            
            _dict[k] = v

        print("_dict: ", _dict)
        return _dict
    #df_input : data frame input
    #df : data frame
    def create_data_frame(keys: list, values: list):
        #data frame input
        df_input = Helper.data_frame_input(keys,values)
        df = pd.DataFrame(df_input)
        
        return df

    def save_data_frame_to_csv(file_path,data_frame):
        data_frame.to_csv(file_path)

    def convert_list_to_dict(_list: list,init_value):
        _dict = {k: init_value for k in _list}
        
        return _dict
    def score_permutation_by_word(permutations_score: dict,word,word_score):
        word_permutations: list = Helper.permutations(word)
        
        for perm in word_permutations:
            print(perm,end=' ')
            print(word)
            permutations_score[perm] = permutations_score.get(perm,0) + word_score    
        return permutations_score
    
    # def _map_score_permutation_by_word(_dict: dict):
    #     return Helper.score_permutation_by_word(_dict['permutations_score'],
    #                                     _dict['word'],
    #                                     _dict['word_score'])
    


    def score_permutations_by_words(permutations_score: dict,words,words_score):
    #def score_permutations_words(_dict: dict):
        #map(Helper._map_score_permutation_by_word,zip(_dict))
        for word,word_score in zip(words,words_score):
            Helper.score_permutation_by_word(permutations_score, word, word_score)
        return permutations_score  

    #dict_keys =  dict.keys()
    #condition is a user defined function that be used as a filtering criteria  
    def get_alphabet_from_dictionary(condition ,dict_keys: list):
        alphabet: list = list (filter(condition,dict_keys))
        
        return alphabet

if __name__ == "__main__":
    import pandas as pd
    keys = [1,2,3,4]
    values = ['a','b','c','d']
    
    
    _dict = Helper.convert_list_to_dict(keys,0)
    print(_dict)
    
    _dict = Helper.convert_list_to_dict(values,'z')
    print(_dict)
    #df = pd.DataFrame(data_frame_input)
    

    df = Helper.create_data_frame(['Keys','Names'],[keys,values])
    print("df: \n",df)
    Helper.save_data_frame_to_csv("data_1.csv",df)
    
    #words = ["time"]
    #freqs = [1000]
    words: list = "time to do this rrrignt abdullah".split(" ")
    freqs: list = [100] * 6
    perms_score_dict = {}
    #Helper.score_permutation_by_word(perms_score_dict,words[4],freqs[4])
    #print(perms_score_dict)
    #Helper.score_permutations_words({'permutations_score': perms_score_dict, 'word': words,'word_score': freqs })
    Helper.score_permutations_by_words(perms_score_dict, words,freqs)
    
    print(perms_score_dict)

    dict_keys = perms_score_dict.keys()
    print("dict_keys: \n", dict_keys)
    is_alphabet = lambda k: len(k) == 1 
    alphabet = Helper.get_alphabet_from_dictionary(is_alphabet, dict_keys)
    print("alphabet: \n",alphabet)