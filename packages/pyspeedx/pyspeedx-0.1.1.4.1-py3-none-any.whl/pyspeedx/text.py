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
        return str((self._str,self._list,self._sound,self._sound_str))



if __name__ == "__main__":
    ## test Word class ##
    _str = "hello"
    word = Word(_str)
    print("word: \n", word)
    #####################


    ## test Text class ##
    _str = "hello Text this is a long text"
    print("text to words: \n",Text.text_to_str_list(_str))
    Text.palindromic_partitions(_str)
    #####################

    ## test Sound class ##
    
    # make a long text made of words
    # convert text to list of strings 
    # from the list of strings create a list of sounds
    #   
    sound = Sound("sound")
    print("sound:\n", sound)

    str_list = Text.text_to_str_list("time to hear the sounds of these words")
    sounds_list = list(map(Sound,str_list)) 
    
    print(*sounds_list,sep='\n')
    
    ######################