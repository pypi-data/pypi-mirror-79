import pyspeedx.pyspeedx.logger.Logger 

logger = L.Logger.getInstance()
class Pronunciation:
  #sound = None; 
  def __init__(self,sound):
    self.sound = sound;

  def __str__(self):
    return str(self.sound)
  def __eq__(self,other):
    return self.sound == other.sound
  def __hash__(self):
    _hash = tuple(self.sound)
    #logger.log("_hash: %s" %str(_hash))
    return hash(str(self.sound))
    
    #return hash(tuple(self.sound))


if __name__ == "__main__":
        
    hs = Pronunciation(g2p("home"))
    hs2 = Pronunciation(g2p("room")) 
    logger.log("1)hs: %s" % hs)
    logger.log("1_2)hs2: %s" % hs2)

    _dict = {}
    _dict[hs] = 53
    _dict[hs2] = 25
    logger.log("2)_dict: %s" % _dict)

    logger.log("3)_dict[hs]: %s" % _dict[hs])
    logger.log("4)_dict[hs2]: %s" % _dict[hs2])


    #logger.log("3)_dict[hs.sound]: %s" % _dict[hs.sound])

