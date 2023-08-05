#importing module 
import logging 
  
class Logger:
    __instance = None # singleton
    __logger = None #use log() to access it 

    @staticmethod
    def getInstance():
        if Logger.__instance == None: # do only once
            Logger() # call class __init__ method
        
        #print("point_3 check: %s" % Logger.__instance)
        return Logger.__instance
    
    
    def __init__(self,file_path="newfile.log"):
        if Logger.__instance == None:
            #print("point_1 , check,Logger.__instance : {}".format(Logger.__instance))
            #print(file_path)
            #Create and configure logger 
            logging.basicConfig(filename=file_path, 
                            format='%(asctime)s %(message)s', 
                            filemode='w') 
            #Creating an object 
            self.__logger = logging.getLogger() 
            #print("point_2 , check, self.__logger {}".format(self.__logger))
            # if (self.logger.hasHandlers()):
            #     self.logger.handlers.clear()
        
            console = logging.StreamHandler()
            self.__logger.addHandler(console)



            
            #Setting the threshold of logger to DEBUG 
            self.__logger.setLevel(logging.DEBUG) 
            Logger.__instance = self
        else:
            print("*****************A singleton already exist******************")
            #print("Logger.__instance: {}".format(Logger.__instance))
            #return Logger.__instance
            raise RuntimeError('A singleton already exist')
    
    def log(cls,message): 
        cls.__logger.info(message)

    #turn logger on(True) or off(False)  
    
    def on(cls,state: bool):
        if(state == False): #off
            cls.__logger.disabled = True #disable logger
        else:# state == True
            cls.__logger.disabled = False # enable logger


if __name__ == "__main__":
    #logger = Logger()

    logger = Logger.getInstance()
    #exit()
    #logger = Logger()
    #print(logger)
    _list = "this is a list of string".split(" ")
    _dict = {k:len(k) for k in _list }

    #logger.on(False)
    logger.log("hey there!")
    logger = Logger.getInstance()
    logger = Logger.getInstance()

    #logger = Logger()
    #logger = Logger()
    #logger = Logger()

    logger.log("_list1: %s" % _list)
    #exit()
    

    logger.log("_dict1: %s" % _dict)

    logger.on(False)
    #wont log
    logger.log("_list2: %s" % _list)
    logger.log("_dict2: %s" % _dict)

    logger.on(True)
    #will log 
    logger.log("_list3: %s" % _list)
    logger.log("_dict3: %s" % _dict)
