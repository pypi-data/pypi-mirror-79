#importing module 
import logging 
  
class Logger:

    logger = None

    def __init__(self,file_path="newfile.log"):
        #print(file_path)
        #Create and configure logger 
        logging.basicConfig(filename=file_path, 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 
        #Creating an object 
        self.logger = logging.getLogger() 
    
        # if (self.logger.hasHandlers()):
        #     self.logger.handlers.clear()
       
        console = logging.StreamHandler()
        self.logger.addHandler(console)



        
        #Setting the threshold of logger to DEBUG 
        self.logger.setLevel(logging.DEBUG) 
        
    def log(self,message): 
        self.logger.info(message)

    #turn logger on(True) or off(False)  
    def on(self,_state: bool):
        if(_state == False):
            self.logger.disabled = True #disable logger
        else:# _state == True
            self.logger.disabled = False # enable logger


if __name__ == "__main__":
    logger = Logger()
    _list = "this is a list of string".split(" ")
    _dict = {k:len(k) for k in _list }

    logger.on(False)
    logger.log("hey there!")

    logger.log("_list1: %s" % _list)
    logger.log("_dict1: %s" % _dict)

    #logger.on(False)
    #wont log
    logger.log("_list2: %s" % _list)
    logger.log("_dict2: %s" % _dict)

    #logger.on(True)
    #will log 
    logger.log("_list3: %s" % _list)
    logger.log("_dict3: %s" % _dict)
